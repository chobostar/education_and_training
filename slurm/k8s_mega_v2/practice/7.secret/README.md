# Устанавливаем HashiCorp Vault с помощью оператора от BanzaiCloud

Сейчас мы установим Vault Operator от BanzaiCloud, потом с его помощью запустим Vault в простой конфигурации с хранением данных на local-storage. Также установим webhook для прописывания секретов из Vault в процесс приложения.

После установки посмотрим на веб-интерфейс Vault, на его консоль, и развернем тестовое приложение с секретами из Vault.

### Переходим в каталог с практикой

```
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/7.secret/
```

### Устанавливаем оператор

1) Откроем все права PSP на ns default

```
kubectl apply -f psp.yaml
```

2) Добавим репо с чартами

```
helm repo add banzaicloud-stable https://kubernetes-charts.banzaicloud.com
```

3) Установим оператор

```
kubectl create namespace vault-infra
kubectl label namespace vault-infra name=vault-infra

helm upgrade --namespace vault-infra --install vault-operator banzaicloud-stable/vault-operator --wait
```

### Устанавливаем Vault

4) Создадим ресурс, который скажет оператору создать нам vault

Сначала поменяем в файле operator/deploy/cr.yaml название хоста s<номер_студента> на ваш реальный номер:

```
  ingress:
    spec:
      rules:
        - host: vault.s<номер_студента>.edu.slurm.io
```

Также убедимся, что в PVC описан сторадж класс local-storage

```
kind: PersistentVolumeClaim
metadata:
  name: vault-file
  spec:
    storageClassName: "local-storage"
```
 
```
kubectl apply -f operator/deploy/rbac.yaml
kubectl apply -f operator/deploy/cr.yaml
```

5) Посмотрели на vault

```
kubectl get pod
```

### Теперь устанавливаем mutating webhook with Helm

6) Добавляем репозиторий и устанавливаем чарт

```
helm upgrade --namespace vault-infra --install vault-secrets-webhook banzaicloud-stable/vault-secrets-webhook --wait --create-namespace
```

В crd указано, что ключи расшифровки и root-token надо положить в секрет kubernetes, для учебного Vault такое допустимо. Примеры для production решений можно посмотреть на github BanzaiCloud (https://github.com/banzaicloud/bank-vaults/tree/master/operator/deploy)

### Получаем root токен администратора vault

> Токен админа root оператор записал нам в секрет куба
>
> Обычный вариант входа в vault - задаем переменные окружения и входим **( для примера! не выполнять )**
>
> ```export VAULT_TOKEN=$(kubectl get secrets vault-unseal-keys -o jsonpath={.data.vault-root} | base64 -d)```<br>
> ```export VAULT_SKIP_VERIFY=true```<br>
> ```export VAULT_ADDR=https://127.0.0.1:8200```<br>
> ```vault```

7) Выполняем команду

```
kubectl get secrets vault-unseal-keys -o jsonpath={.data.vault-root} | base64 -d
```

### Заходим в web UI

> при создании vault мы попросили оператора создать нам ingress и включить UI

8) Заходим браузером по адресу  ```http://vault.s<номер_студента>.edu.slurm.io```

> Для авторизации введем root token, получить его можно командой выше<br>
> Смотрим, видим ключик с данными. Он там появился, потому что в operator/deploy/cr.yaml мы попросили его создать.

### Войдем в vault консолью

9) Создаем под, в котором настроен vault

```
kubectl apply -f console.yaml
```

10) Ждем, пока он поднимется

```
kubectl get pod -w
```

11) Запускаем внутри пода шелл

```
kubectl exec -it vault-console sh
```

12) Выполняем внутри пода команды:

> статус vault

```
vault status
```

> добавление ключа

```
vault kv put secret/accounts/aws AWS_SECRET_ACCESS_KEY=myGreatKey
```

> Этот запрос в vault перезапишет содержимое пути `secret/accounts/aws`, чтобы обновить только содержимое секрета `AWS_SECRET_ACCESS_KEY` можно выполнить следующую команду:

```
vault kv patch secret/accounts/aws AWS_SECRET_ACCESS_KEY=myGreatKey
```

> Выйдем из pod'а с консолью и посмотрим на веб-интерфейс Vault, для входа в него нам понадобится root-token, который лежит в секрете vault-unseal-keys
```
exit
```

### Проверяем в web UI изменение ключа

13) идем в браузер ```http://vault.s<номер_студента>.edu.slurm.io``` посмотреть, что ключ изменился

> кстати, kv версии 2 поддерживает версионирование, так что можно посмотреть предыдущие значения секретов.

Из интересного можно обратить внимание на значение секрета http://vault.s000000.edu.slurm.io/ui/vault/secrets/secret/show/accounts/aws, который мы изменяли. Нажав на History видно, что при изменении секрета он был переписан целиком. Ключ, который был в Version 1 и не было в команде на запись секрета в Version 2 отсутствует.

Так же можно посмотреть на политики доступа и аутентификатор Kubernetes. К сожалению, роли которым разрешен доступ в Vault, через веб-интерфейс не показывает. Роль default можно посмотреть из консоли командой vault read  auth/kubernetes/role/default​​​​​​

### Создадим тестовое приложение, которое должно получить секреты из vault

Теперь мы готовы к запуску тестового приложения. Сначала рассмотрим его манифест в файле test-deployment.yaml, в нем видно, что в pod'е есть два контейнера: init и основной, в каждом из них есть переменная окружения cо специальным значением, в котором указано, из какого секрета и ключа в Vault необходимо подставить данные. И также есть поле command, в котором выводится значение переменной окружения.

14) Запускаем из манифеста

```
kubectl apply -f test-deployment.yaml
```

15) Посмотрели имя пода

```
kubectl get pod | grep hello-secret

hello-secrets-596b4574fd-zbx9b     1/1     Running   0          15s
```

16) Посмотрели в логи основного контейнера

```
kubectl logs hello-secrets-<Tab>

time="2021-10-05T08:56:07Z" level=info msg="received new Vault token" addr= app=vault-env path=kubernetes role=default
time="2021-10-05T08:56:07Z" level=info msg="initial Vault token arrived" app=vault-env
time="2021-10-05T08:56:07Z" level=info msg="spawning process: [sh -c env && echo && echo $AWS_SECRET_ACCESS_KEY && echo going to sleep... && sleep 10000]" app=vault-env
... (вывод команды env сокрашен)
AWS_SECRET_ACCESS_KEY=myGreatKey
...
myGreatKey
going to sleep...
```

17) Посмотрели в логи init-контейнера

```
kubectl logs hello-secrets-<Tab> -c init-ubuntu

time="2021-10-05T08:56:05Z" level=info msg="received new Vault token" addr= app=vault-env path=kubernetes role=default
time="2021-10-05T08:56:05Z" level=info msg="initial Vault token arrived" app=vault-env
time="2021-10-05T08:56:05Z" level=info msg="spawning process: [sh -c echo $AWS_SECRET_ACCESS_KEY && echo initContainers ready]" app=vault-env
myGreatKey
initContainers ready
```

> видим, что нам показывает секрет

### Проверяем манифесты

18) Смотрим в описание деплоймента, видим что в `env:` написана ссылка на vault, и что команда выводит значение переменной окружения

```
cat test-deployment.yaml
```

19) Смотрим в describe пода - видим, что там так же ссылка на vault, а не секретное значение

```
kubectl describe pod hello-secrets-6d46fb96db-tvsvb

  Environment:
    AWS_SECRET_ACCESS_KEY:  vault:secret/data/accounts/aws#AWS_SECRET_ACCESS_KEY
```

20) Заходим в Pod и смотрим переменные окружения 

```
kubectl exec -it hello-secrets-6d46fb96db-tvsvb env | grep AWS
```

> видим также ссылку на vault: ```AWS_SECRET_ACCESS_KEY=vault:secret/data/accounts/aws#AWS_SECRET_ACCESS_KEY```

На первый взгляд все замечательно, секретное значение было передано в процесс приложения прямо из Vault, никто посторонний в процессе передачи его подсмотреть не мог. Но, к сожалению, в Linux значение всех переменных окружения процесса можно легко подсмотреть в файле /proc/1/environ. Так что даже при хранении секретной информации в Vault права на exec в контейнере нельзя выдавать всем подряд.

21) Запускаем продакшен в неймспейсе default

```
kubectl apply -f prod-deployment.yaml
```

Pod войдет в состояние CrashloopBackoff, потому что с токеном от сервис аккаунтов в ns default не разрешен доступ в хранилище prod

22) Запускаем продакшен в неймспейсе producton

```
kubectl create ns production
kubectl -n production apply -f prod-deployment.yaml
```

Под запустится

23) Смотрим логи

```
kubectl -n production logs -l app=hello-secrets
```

24) Удаляем всё

```
kubectl delete pod vault-console
kubectl delete deployment hello-secrets
kubectl delete deployment hello-prod-secrets
kubectl delete deployment hello-prod-secrets -n production
```

Удаляем vault путём удаления CRD

```bash
kubectl delete vault vault
```

Смотрим, что происходит

```
kubectl get pod
```

Добиваем оператора

```
helm delete -n vault-infra vault-operator
helm delete -n vault-infra vault-secrets-webhook

kubectl delete ns vault-infra
```

Удаляем диск с данными vault

```
kubectl delete pvc vault-file
```
