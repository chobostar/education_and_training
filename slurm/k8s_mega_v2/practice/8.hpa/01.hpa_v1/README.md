### HPA v1

---

#### Цели практики
Целью данной практики является знакомство с работой HPA v1 на практике. Первая версия HPA умеет производить scaling только на основании метрик `cpu` и `ram`. В качестве источника данных для scaling будет использоваться `Metric server`. Это нативная система мониторинга для Kubernetes, в частности ее поддержка интегрирована в `kubectl`.  Так как HPA может получать метрики только из kube-api сервера, то в кластер будет установлено расширение kube-api сервера, абстракция `APIService`. Данная абстракция позволяет перенаправлять запросы к kube-api в сторонние приложения.

#### С чем будем работать

* В каталоге `metrics-server` содержатся все манифесты, необходимые для установки его в Kubernetes кластер. 
* Тестовое приложение `hpa-example`. Это специально разработанное приложение для тестирования HPA, в каталоге `deploy` содержатся необходимые для его запуска в кластере манифесты.

#### Где будем выполнять практику

* Данная практика выполняется на сервере `master-1.s<Ваш номер студента>`.
* Практика выполняется под учетной записью `root`.
* Материалы для прохождения практики находятся в каталоге `megakube/8.hpa/01.hpa_v1`.

```
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/8.hpa/01.hpa_v1/
```

#### Практика

**1. Запускаем Metric server**

* Применяем манифесты Metric server

Поскольку Metric server не устанавливается в Kubernetes кластер по умолчанию, первое что необходимо сделать - это установить его. Все необходимые манифесты находятся в каталоге `metric-server` и их можно сразу применить в кластер. Для этого необходимо в консоли выполнить команду:

```bash
kubectl apply -f metrics-server/ -n kube-system
```

* Проверяем работу Metric server

Metric server собирает данные с kubelet c периодичностью 1 раз в минуту. После установки необходимо подождать 1-2 минуты и выполнить команду:

```bash
kubectl top node
```

Данная команда выведет текущую нагрузку на ноды. В результате выполнения команды на экран будут выведены примерно следующие данные:

```bash
NAME                     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
master-1.s000000.slurm.io   122m         12%    1693Mi          44%
master-2.s000000.slurm.io   114m         11%    1489Mi          38%
master-3.s000000.slurm.io   97m          9%     1423Mi          37%
node-1.s000000.slurm.io     59m          5%     1505Mi          39%
node-2.s000000.slurm.io     357m         35%    1389Mi          36%
```

Важной особенностью Metric Server является то, что он не хранит полученные данные, а только отображает последние полученные. По этому расценивать его как полноценную систему мониторинга нельзя. 

**2. Запускаем тестовое приложение**

В качестве тестового приложения будет использоваться специальное приложение, предназначенное для тестирования HPA. Приложение написано на PHP, и при запросах генерирует высокую нагрузку. Для начала применим Deployment в кластер, выполнив команду:

```bash
kubectl apply -f deploy/deployment.yml -n default
```

Для работы HPA обязательным является наличие у Pod выставленных `request`. Обратите внимание на [deployment.yml](deploy/deployment.yml), в нем указано:

```yaml
resources:
  requests:
    cpu: 100m
```

Теперь создадим Service. Для этого мы не будем использовать готовые манифесты, а воспользуемся ключом `expose` для kubectl. Данный ключ позволяет создать Service для Deployment без написания манифеста. В итоге получается следующая команда, которую необходимо выполнить в консоли:

```bash
kubectl expose deployment php-apache --port 80 -n default
```

**3. Устанавливаем HPA**

Для запуска HPA так же воспользуемся возможностями kubectl. Для создания абстракции HPA без манифеста можно использовать ключ `autoscale`. Выполним команду:

```bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=5 -n default
```

В результате выполнения команды будет создан HPA, который отслеживает состояние Deployment с именем `php-apache`. При достижении средней нагрузки на все Pod 50% (для расчетов суммируется процент нагрузки на каждый Pod и делится на их количество) scaling будет производиться в границах от 1-го Pod до 5 Pod.

**4. Проверяем работу**

* Смотрим на текущее количество Pod

```bash
kubectl get pod -n default
```

Должен быть запущен один Pod

```bash
NAME                          READY   STATUS    RESTARTS   AGE
php-apache-566d7644df-z9dtt   1/1     Running   0          15s
```

* Смотрим на HPA

```bash
kubectl get hpa -n default
```

Видим созданный HPA

```bash
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   1%/50%    1         5         1          32s
```

Она будет скейлить Pod, как только их использование cpu начнет составлять 50% от request.

* Создаем нагрузку

Для генерации нагрузки создадим еще один Pod из образа busybox. Внутри Pod в цикле будет запущена утилита wget, которая будет обращаться к тестовому приложению по имени Service. В итоге получается следующая команда, которую необходимо выполнить в консоли:

```bash
kubectl run load-generator --image=busybox  -n default -- /bin/sh -c "while true; do wget -q -O- http://php-apache; done"
```

* Проверяем текущее потребление cpu Pod

Metric server может отдавать не только нагрузку по Node, но и по Pod. Для вывода информации по нагрузке от Pod выполните команду:

```
kubectl top pod -n default
```

Видим, что нагрузка начинает увеличиваться.

```bash
NAME                          CPU(cores)   MEMORY(bytes)
php-apache-566d7644df-z9dtt   936m         11Mi
```

* Ждем когда начнет работать Autoscaling

У kubectl есть ключ `-w`, который позволяет выводить в режиме реального времени все изменения для нашего текущего запроса. Выполним следующую команду в консоли, чтобы отслеживать изменения количества Pod:

```bash
kubectl get pod -w -n default
```
`--horizontal-pod-autoscaler-downscale-stabilization`

Это флаг у kube-controller-manager используется для задания кулдауна при уменьшении количества реплик с помощью HPA.

Таким образом после снижения нагрузки должно пройти время (5 минут по умолчанию), прежде чем HPA начнет уменьшать количество реплик.

Спустя несколько минут количество Pod должно увеличиться до 5-ти.

```bash
NAME                              READY   STATUS    RESTARTS   AGE
load-generator-6b9cf94758-5qmbx   1/1     Running   0          2m16s
php-apache-566d7644df-4zvv7       1/1     Running   0          108s
php-apache-566d7644df-kv662       1/1     Running   0          93s
php-apache-566d7644df-tg8qw       1/1     Running   0          108s
php-apache-566d7644df-z9dtt       1/1     Running   0          13m
php-apache-566d7644df-zlwd7       1/1     Running   0          108s
```

Отлично, autoscaling сработал!

* Проверяем работу в обратную сторону

Удаляем Pod с тестовой нагрузкой выполнив команду:

```bash
kubectl delete pod load-generator -n default
```

* Проверяем нагрузку на поды

```bash
kubectl top pod -n default
```

Через какое-то время замечаем, что она упала

```bash
NAME                          CPU(cores)   MEMORY(bytes)
php-apache-566d7644df-4zvv7   1m           11Mi
php-apache-566d7644df-kv662   1m           11Mi
php-apache-566d7644df-tg8qw   1m           11Mi
php-apache-566d7644df-z9dtt   1m           11Mi
php-apache-566d7644df-zlwd7   1m           11Mi
```

* Проверяем, как autoscaling отработает в обратную сторону

```bash
kubectl get pod -w -n default
```

Видим, что ненужные поды умирают (в течение 5 минут).  После снижения нагрузки scale down не происходит слишком быстро, чтобы избежать ситуации, когда значения по потреблению находятся в пограничном состоянии.

```bash
NAME                          READY   STATUS        RESTARTS   AGE
php-apache-566d7644df-4zvv7   0/1     Terminating   0          8m59s
php-apache-566d7644df-kv662   0/1     Terminating   0          8m44s
php-apache-566d7644df-tg8qw   0/1     Terminating   0          8m59s
php-apache-566d7644df-z9dtt   1/1     Running       0          20m
php-apache-566d7644df-zlwd7   0/1     Terminating   0          8m59s
```

Autoscaling вернул все к первоначальному варианту с одним Pod.

**5. Чистим за собой кластер**

```bash
kubectl delete all --all -n default
```

**6. Дополнительный вопрос**

Что будет, если в кластере запущен 1 Pod с потреблением 100% от request, а scaling настроен на значение 50%? После увеличения Pod до 2х, нагрузка на каждый Pod составляет 45% от request. Будет ли HPA производить scale down, и если да, то через какое время?


#### Troubleshooting

* Проверяем, что Metric server запущен

```bash
kubectl get po -n kube-system | grep metrics-server
```

Поды должны быть в состоянии `STATUS: Running` и `READY 1/1`. Если Pod отсутствует, начинаем практику с первого пункта. Если состояние не `Running` или `0/1`, то смотрим причины, выполнив команду:

```bash
kubectl describe po -n kube-system metrics-server-<TAB>
```

* Проверяем, что метрики доступны

Для проверки доступности метрик выполним команду:

```bash
kubectl top node
```

Если не выводится потребления по Node, но в прошлом шаге не выявлено ошибок, то пробуем установить еще раз все абстракции, выполнив команду:

```bash
kubectl apply -f ~/slurm/practice/8.hpa/v1/metrics-server -n kube-system
```

#### Полезные ссылки

1. [k8s doc: HPA v1](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)
2. [Metric server](https://github.com/kubernetes-sigs/metrics-server)
