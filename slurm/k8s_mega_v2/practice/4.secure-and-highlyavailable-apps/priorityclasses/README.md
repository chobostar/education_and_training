> **Все работы все еще проводим с хоста master-1**

### Создаем новый Priority Class в Kubernetes

1) Переходим в директорию с практикой

```bash
cd ~/megakube/4.secure-and-highlyavailable-apps/priorityclasses
```

2) Смотрим PC в кластере

```bash
kubectl get pc
```

3) Создаем Priority Class'ы и Namespace'ы для наших приложений

```bash
kubectl create -f pc-prod.yaml
kubectl create -f pc-develop.yaml

kubectl create ns production
kubectl create ns development
```

4) Деплоим наши приложения

```bash
kubectl create -f deployment-prod.yaml -n production
kubectl create -f deployment-develop.yaml -n development
```

5) Смотрим, что всё задеплоилось. Смотрим также ресурсы нод

```bash
kubectl get pod -n production
kubectl get pod -n development

kubectl describe node node-1.s<ваш номер логина>.slurm.io
kubectl describe node node-2.s<ваш номер логина>.slurm.io
```

> Видим, что количество доступных ресурсов осталось небольшим.

6) Эвакуируем pod'ы с ноды. Смотрим на Pod'ы production и development окружения. Наш продакшен должен работать

```bash
kubectl drain node-2.s<ваш номер логина>.slurm.io --ignore-daemonsets

kubectl get pod -n production
kubectl get pod -n development
```

> Обратите внимание на Pod'ы Ingress-controller'а. Все ли ОК с ними и насколько это может быть критично?

7) Подчищаем за собой:

```bash
kubectl delete ns production
kubectl delete ns development

kubectl delete pc develop-priority
kubectl delete pc production-priority

kubectl uncordon node-2.s<ваш номер логина>.slurm.io
```
