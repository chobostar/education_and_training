### Установка RabbitMQ

> Все работы всё ещё проводим с первого мастера своего кластера, master-1.s<номер вашего логина>

1) Переходим в каталог с практикой

```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/6.stateful/1.rabbitmq
```

2) Смотрим `values.yaml`

```bash
vi rabbitmq/values.yaml
```

3) Правим в 'hostName' значение `rabbit.s<Ваш номер студента>.edu.slurm.io`

```yaml
ingress:
  enabled: true
  hostName: rabbit.s<Ваш номер студента>.edu.slurm.io  # <-- подставляем номер логина
```

4) Создаем Namespace и устанавливаем чарт из локальной папки

```bash
kubectl create ns rabbitmq
helm upgrade --install rabbitmq rabbitmq/ --namespace=rabbitmq
```

5) Смотрим за появлением Pod'а

```bash
kubectl get pod -o wide -w -n rabbitmq
```

6) Открываем в браузере в режиме инкогнито админку по URL `rabbit.s<Ваш номер студента>.edu.slurm.io`

```
http://rabbit.s<Ваш номер студента>.edu.slurm.io
```

> Логин/пароль от админки у нас задан в `rabbitmq/values.yaml` в секции rabbitmq. В рамках практики он у всех одинаков:

```yaml
rabbitmq:
  username: user

  password: rrabit
```

### Потестим устойчивость RabbitMQ 

1) Скейлим наш Rabbitmq до 3

```bash
kubectl scale sts rabbitmq --replicas 3 -n rabbitmq
```

2) Смотрим за появлением Pod'ов в консоли и в браузере

```bash
kubectl get pod -o wide -w -n rabbitmq
```

> В браузере смотрим: cтарый Pod остался, добавились два новых

3) Удаляем один Pod

```bash
kubectl delete pod rabbitmq-0 -n rabbitmq
```

4) Смотрим за удалением Pod'а в консоли и в браузере. Видим как он поднимается обратно

```bash
kubectl get pod -o wide -w -n rabbitmq
```

5) Имитируем обновление кластера с рестартом всего. Правим `rabbitmq/values.yaml`:

```yaml
livenessProbe:
  initialDelaySeconds: 120  # <-- Пишем 122 вместо 120
```

6) Запускаем апгрейд

```bash
helm upgrade --install rabbitmq rabbitmq/ --namespace=rabbitmq
```

7) Cмотрим в консоли и в браузере как узлов снова стало 1. Вопрос: почему так?

```bash
kubectl get pod -o wide -w -n rabbitmq
```

8) Подчищаем за собой

```bash
helm delete rabbitmq --namespace=rabbitmq
kubectl delete ns rabbitmq
```
