### Подготовим себе постоянные тома для работы 

1) Переходим в каталог с практикой

```bash
cd ~/megakube/6.stateful/2.cockroachdb
```

2) Сначала создаем локальные постоянные тома. Заходим в каталог pv и правим во всех файлах `pv` название узла в разделе nodeAffinity

```bash
cd pv
sed -i 's/s000000/sXXXXXX/g' pv* # Где sXXXXXX - ваш номер студента
cd ..
```

3) Применяем
```bash
kubectl apply -f pv
```

4) Проверяем, должен быть список из 5 PV со статусом `available`

```bash
kubectl get pv
```

5) Тестируем подключение, для этого задеплоим тестовое приложение

```bash
kubectl apply -f test
```

6) Проверяем, что PVC захватил себе PV

```bash
kubectl get pv
```

7) Pod не поднимается, смотрим его describe

```bash
kubectl get pod
kubectl describe pod local-pv-test-<имя пода>
```

8) Видим что надо создать пути на node-1 и node-2

```bash
ssh node-1.s<Ваш номер студента>
mkdir -p /local/pv{1..3}

ssh node-2.s<Ваш номер студента>
mkdir -p /local/pv{4..6}
```

9) После этого Pod поднялся, можно в него зайти и создать что нибудь в каталоге /data, после этого проверить что это появилось в каталоге на узле.

10) Похулиганим. Заскейлим Pod в 3

```bash
kubectl scale deployment.apps/local-pv-test --replicas 3
```

> Все поды поднялись на одном узле, смотрим в новый Pod, видим тот же каталог внутри Pod'а.

11) Смотрим на PVC

```bash
kubectl get pvc pvc1 -o yaml
```

12) Удаляем приложение, смотрим что с PV

```bash
kubectl delete -f test
kubectl get pv
```

> Статус pv - Released, использовать повторно нельзя. Надо удалять руками или ставить Provisioner

### Устанавливаем CockroachDB 

1) Переходим к установке Cockroachdb. Смотрим какие values есть у чарта с Cockroachdb

> Обратите внимание, в `cockroachdb/values.yaml` поле `StorageClass` стоит конкретное значение - "local-storage" . Это тот SC который мы создали на предыдущих шагах вместе с PV

```bash
less cockroachdb/values.yaml
```

2) Создаем Namespace для Cockroachdb

```bash
kubectl create ns cockroachdb
```

3) Устанавливаем чарт из локальной папки

```bash
helm upgrade --install cockroachdb cockroachdb/ --namespace=cockroachdb
```

4) Дожидаемся пока создадутся CSR в количестве 4 штук:

```bash
kubectl get csr
```

5) Аппрувим данные CSR, чтобы кластер продолжил собираться. Без выполнения этих команд pod'ы так и будут висеть в Pending

```bash
kubectl certificate approve cockroachdb.client.root
kubectl certificate approve cockroachdb.node.cockroachdb-0
kubectl certificate approve cockroachdb.node.cockroachdb-1
kubectl certificate approve cockroachdb.node.cockroachdb-2
```

6) Смотрим что наши CSR теперь в статусе "Approved,Issued":

```bash
kubectl get csr
```

7) Ожидаем пока соберется кластер, проверяем PV/PVC и запуск подов:

```bash
kubectl get po -n cockroachdb
kubectl get pv
kubectl get pvc -n cockroachdb
```

### Запускаем SQL-клиент для Cockroachdb и подключаемся им в Service

1) Сперва создаем Pod с клиентом

```bash
kubectl create -f client-secure.yaml -n cockroachdb
```

2) Затем подключаемся через этот Pod клиента к CockroachDB:

```bash
kubectl exec -it cockroachdb-client-secure -n cockroachdb -- ./cockroach sql --certs-dir=/cockroach-certs --host=cockroachdb-public
```

3) Создадим базу данных и таблицу там

```bash
CREATE DATABASE bank;

CREATE TABLE bank.accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      balance DECIMAL
  );

INSERT INTO bank.accounts (balance)
  VALUES
      (1000.50), (20000), (380), (500), (55000);

SELECT * FROM bank.accounts;

quit
```

4) Проверим, действительно ли наши транзакции применились на других нодах. А также сразу проверим возможность писать в разные ноды. Подключимся к какой-нибудь конкретной ноде Cockroachdb:

```bash
kubectl exec -it cockroachdb-client-secure -n cockroachdb -- ./cockroach sql --certs-dir=/cockroach-certs --host=cockroachdb-0.cockroachdb
```

5) Смотрим записи в табличке

```bash
SELECT * FROM bank.accounts;
```

6) Добавляем еще одну запись в табличку

```bash
INSERT INTO bank.accounts (balance) VALUES (77777);

SELECT * FROM bank.accounts;

quit
```

7) Теперь подключимся к другой ноде Cockroachdb:

```bash
kubectl exec -it cockroachdb-client-secure -n cockroachdb -- ./cockroach sql --certs-dir=/cockroach-certs --host=cockroachdb-1.cockroachdb
```

8) Смотрим что ранее созданные данные там есть и добавляем еще одну строчку для проверки возможности записи

```bash
SELECT * FROM bank.accounts;

INSERT INTO bank.accounts (balance) VALUES (99999);

quit
```

### Теперь потестим восстановление Cockroachdb

1) Для этого удалим Pod Statefulset'а и затем проверим данные на нем

```bash
kubectl delete po -n cockroachdb cockroachdb-2
```

2) Ждем поднятия Pod'а

```bash
kubectl get po -n cockroachdb -w
```

3) После поднятия заходим клиентом на эту ноду и проверяем данные

```bash
kubectl exec -it cockroachdb-client-secure -n cockroachdb -- ./cockroach sql --certs-dir=/cockroach-certs --host=cockroachdb-2.cockroachdb

SELECT * FROM bank.accounts;

quit
```

### Disaster Recovery. Попробуем теперь уничтожить реплики CockroachDB совсем и посмотрим какую недоступность это вызывает

1) Сохраняем Statefulset в файл и удаляем его, оставляя Pod'ы работать:

```bash
kubectl get statefulset -n cockroachdb cockroachdb -o yaml > sts.yaml

kubectl delete sts -n cockroachdb cockroachdb --cascade=orphan
```

2) Запускаем наше демо-приложение, которое будет каждую секунду обращаться в базу. Смотрим его логи

```bash
kubectl create -f demo-disaster.yaml -n cockroachdb

kubectl logs -n cockroachdb cockroachdb-client-disaster -f
```

3) Далее будет удобнее работать, открыв вторую консоль. В одной у нас будут показываться логи демо-приложения, а во второй будем производить действия. Удаляем один Pod и смотрим что происходит в логах приложения параллельно: 

```bash
kubectl delete po -n cockroachdb cockroachdb-0

# Смотрим во второй консоли логи демо-приложения
```

4) Делаем по хардкору. Удаляем еще один Pod и параллельно смотрим логи демо-приложения:

```bash
kubectl delete po -n cockroachdb cockroachdb-1

# Смотрим во второй консоли логи демо-приложения
```

> Видим, что демо-приложение перестало выдавать инфу о cockroachdb, а последний оставшийся Pod висит в 0/1. Мы уперлись в фактор репликации.
 
5) Пробуем вернуть все как было, возвращаем Statefulset, смотрим на поднятие реплик, целостность данных и логи демо-приложения:

```bash
kubectl apply -f sts.yaml -n cockroachdb

# Смотрим во второй консоли логи демо-приложения
```

> После поднятия хотя бы одного пода демо-приложение снова заработало, данные стали писаться/читаться. 

6) Проверим нашу ранее созданную табличку:

```bash
kubectl exec -it cockroachdb-client-secure -n cockroachdb -- ./cockroach sql --certs-dir=/cockroach-certs --host=cockroachdb-public

SELECT * FROM bank.accounts;

quit
```
  
**ДОМАШНЯЯ РАБОТА:** 
- Познакомиться с админкой Cockroachdb. Для этого нужно подправить `values.yaml` чарта и включить Ingress в нем, не забыв указать правильное доменное имя. Либо написать свой Ingress и отправить его в CockroachDB.
- Создать пользователя для админки:

```
kubectl exec -it cockroachdb-client-secure -n cockroachdb -- ./cockroach sql --certs-dir=/cockroach-certs --host=cockroachdb-public

CREATE USER slurm WITH PASSWORD 'slurmpass';

quit
```

- Заходим в режиме инкогнито через браузер по адресу вашего Ingress'а (в браузере "Соглашаемся с риском", возможно несколько раз придется согласится пока админка откроется). 
- Используем ранее созданного юзера для авторизации

### Подчищаем за собой

```
helm delete cockroachdb --namespace=cockroachdb
kubectl delete pvc -n cockroachdb --all
kubectl delete ns cockroachdb
kubectl delete csr --all
```
