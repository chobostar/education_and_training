### Настроим blue/green релизы

> Все работы всё ещё проводим с первого мастера своего кластера, master-1.s<номер вашего логина>

1) Переходим в директорию с практикой.
```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/11.deploy/blue-green
```

2) Открываем файл `ingress.yaml` и в нем правим

```yaml
    - host: nginx.s<номер своего логина>.edu.slurm.io
```

3) Создаем все объекты в директории
```bash
kubectl apply -f .
```

4) В ответ должны увидеть
```bash
configmap/configmap-blue created
deployment.extensions/myapp-blue created
configmap/configmap-green created
deployment.extensions/myapp-green created
ingress.extensions/my-ingress created
service/myapp created
```

5) Смотрим на Pod'ы
```bash
kubectl get pod --show-labels
```
Видим
```bash
NAME                           READY   STATUS    RESTARTS   AGE   LABELS
myapp-blue-78c998b576-6qwfc    1/1     Running   0          22m   app=myapp,deploy=blue
myapp-blue-78c998b576-xfpdn    1/1     Running   0          22m   app=myapp,deploy=blue
myapp-green-57766d7c86-dlv44   1/1     Running   0          22m   app=myapp,deploy=green
myapp-green-57766d7c86-zpdzb   1/1     Running   0          22m   app=myapp,deploy=green
```

6) Смотрим куда сейчас смотрит Service
```bash
kubectl get service -o custom-columns='NAME:.metadata.name, SELECTOR:.spec.selector.deploy'
```
Видим

```bash
NAME         SELECTOR
myapp        green
```

7) Пробуем проверить, что наше приложение доступно через Ingress и оно "зеленой" версии

```bash
curl -i nginx.s<номер своего логина>.edu.slurm.io
```
В ответ получаем
```bash
HTTP/1.1 200 OK
Server: nginx/1.13.12
Date: Sun, 27 Jan 2019 15:09:36 GMT
Content-Type: application/octet-stream
Content-Length: 27
Connection: keep-alive

I am green!
```

8) Пробуем перенаправить трафик на "голубую" версию
```bash
kubectl patch service myapp -p '{"spec":{"selector":{"deploy":"blue"}}}'
```

9) Проверяем Service
```bash
kubectl get service -o custom-columns='NAME:.metadata.name, SELECTOR:.spec.selector.deploy'
```
Видим
```bash
NAME         SELECTOR
myapp        blue
```

10) Проверяем через Ingress:

```bash
curl -i nginx.s<номер своего логина>.edu.slurm.io
```
В ответ получаем
```bash
HTTP/1.1 200 OK
Server: nginx/1.13.12
Date: Sun, 27 Jan 2019 15:09:36 GMT
Content-Type: application/octet-stream
Content-Length: 27
Connection: keep-alive

I am blue!
```

11) Чистим за собой кластер
```bash
kubectl delete -f .
```
