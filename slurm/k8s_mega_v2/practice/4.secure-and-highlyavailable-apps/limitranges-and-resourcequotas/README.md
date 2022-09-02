> **Все работы все еще проводим с первого мастера**

### Создаем LimitRange и ResourceQuota

1) Переходим в директорию с практикой

```bash
cd ~/megakube/4.secure-and-highlyavailable-apps/limitranges-and-resourcequotas
```

2) Создаем Namespace

```bash
kubectl create ns test
```

3) Создаем в нем Limitrange и Resourcequota

```bash
kubectl apply -f limitrange.yaml -f resourcequota.yaml -n test
```

4) Смотрим, что получилось

```bash
kubectl describe ns test
```

5) Запускаем Deployment

```bash
kubectl apply -f deployment.yaml -n test
```

И ещё раз заглядываем в описание ns.

> Видим, что количество доступных ресурсов начало уменьшаться.

**САМОСТОЯТЕЛЬНАЯ РАБОТА:**
- Подправить Deployment таким образом, чтобы в лимитах у него был 1 cpu
- Посмотреть describe последнего Replicaset'а.
- Там должно быть что то типа такого:

```bash
  Warning  FailedCreate  20s (x4 over 38s)  replicaset-controller  (combined from similar events): Error creating: pods "nginx-6579b4dfb7-n7wmd" is forbidden: [maximum cpu usage per Container is 1, but limit is 2., cpu max limit to request ratio per Pod is 2, but provided ratio is 20.000000.]
```

6) Чистим за собой кластер
```bash
kubectl delete ns test
```
