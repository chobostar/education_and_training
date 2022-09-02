# Istio

> :exclamation: Все работы проводим с первого мастера под рутом

### Подготовка

1) Переходим в директорию с практикой.
```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/12.istio/
```

2) Применяем политики PSP, для istio

```bash
kubectl apply -f psp.yaml
```

> :exclamation: НЕ Качаем все нужные манифесты и утилиты, потому что github может нас поблочить.

```bash
###curl -L https://istio.io/downloadIstio | sh -
```

3) Распаковываем, заранее скачанный архив:
```
tar -zxvf istio-1.10.0-linux-amd64.tar.gz
```

4) Ставим в кластер Istio

```bash
./istio-1.10.0/bin/istioctl install --set profile=demo
```

### Тестируем сайдкары

5) Ставим лэйбл на дефолтный нэймспэйс

```bash
kubectl label namespace default istio-injection=enabled
```

6) Запускаем тестовое приложение

```bash
kubectl apply -f ./istio-1.10.0/samples/sleep/sleep.yaml
```

7) Смотрим что получилось

```bash
kubectl get pod

NAME                     READY     STATUS        RESTARTS   AGE
sleep-45kdj8kd83-fd99v   2/2       Running       0          23s
```

8) Чистим за собой кластер

```bash
kubectl delete -f ./istio-1.10.0/samples/sleep/sleep.yaml
```

### Тестируем сетевые абстракции

9) Заменяем nginx-ingress-controller на isio-ingressgateway

```bash
kubectl scale deployment -n ingress-nginx ingress-nginx-controller --replicas=0
```

```bash
kubectl edit deployments.apps -n istio-system istio-ingressgateway
```

Вставляем hostPort

```yaml
- containerPort: 8080
  hostPort: 80      # добавляем вот это
  protocol: TCP
- containerPort: 8443
  hostPort: 443      # и это
  protocol: TCP
```

Создаем дефолтный gateway и проверяем работу ингресс-гейтвея
```
kubectl apply -f gw.yaml

curl -I s<номер студента>.edu.slurm.io

HTTP/1.1 404 Not Found
Date: Wed, 20 May 2020 17:05:28 GMT
Connection: keep-alive
server: istio-envoy
```

10) Деплоим тестовое приложение

```bash
kubectl apply -f ./istio-1.10.0/samples/bookinfo/platform/kube/bookinfo.yaml
```

11) Создаем Gateway и Vitrualservice для тестового приложения

```bash
kubectl apply -f ./istio-1.10.0/samples/bookinfo/networking/bookinfo-gateway.yaml
```

12) Проверяем что все заработало. В браузере, в инкогнито можно открыть. Если не появилось, то ждём до 5-ти минут. 

```bash
http://test.s<Ваш номер логина>.edu.slurm.io/productpage
```

13) Досоздаем Destinationrules

```bash
kubectl apply -f ./istio-1.10.0/samples/bookinfo/networking/destination-rule-all.yaml
```

### Тестим политики роутинга

14) Применяем виртуалсервисы для всех компонентов

```bash
kubectl apply -f ./istio-1.10.0/samples/bookinfo/networking/virtual-service-all-v1.yaml
```

15) Проверяем в браузере, что теперь отзывы отображаются всегда одинаково.

### Пробуем роутинг на основе пользователя

16) Добавляем VirtualService

```bash
kubectl apply -f ./istio-1.10.0/samples/bookinfo/networking/virtual-service-reviews-test-v2.yaml
```

17) В браузере логинимся под пользователем jason (пароль любой) 

видим что отображаются отзывы версии 2. чёрные звездочки. 

### Тестим работу с ошибками

18) Добавляем задержку при обращении к компоненту рейтингов

```bash
kubectl apply -f ./istio-1.10.0/samples/bookinfo/networking/virtual-service-ratings-test-delay.yaml
```
В браузере видим, что сервис ревью упал с ошибкой.
`Sorry, product reviews are currently unavailable for this book.`

19) Правим virtualservice - меняем на возврат 502 ошибки сразу

```bash
kubectl edit virtualservice.networking.istio.io/ratings
```

```
  - fault:
      abort:
        httpStatus: 502
        percentage:
          value: 100
```

Сервис review работает, рейтинг нет

20) Визуализация.

Добавляем kiali - исправляем плейсхолдер в файле `kiali-vs.yaml`

```
  hosts:
    - "kiali.s<номер студента>.edu.slurm.io"
```

```bash
kubectl apply -f ./istio-1.10.0/samples/addons/prometheus.yaml
kubectl apply -f ./istio-1.10.0/samples/addons/kiali.yaml
kubectl apply -f kiali-vs.yaml
```

21) Обновляем много раз окно с сайтом bookinfo

Идем в веб интерфейс `kiali.s<номер студента>.edu.slurm.io`

Удаляем virtual service

```
k delete virtualservices.networking.istio.io reviews
```

Еще раз обновляем сайт bookinfo, смотрим в интерфейс kiali.
