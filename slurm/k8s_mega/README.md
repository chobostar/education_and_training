
```
To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

```
kubeadm join 172.26.108.5:6443 --token szpod2.q5uy6bq4ka37mesv \
    --discovery-token-ca-cert-hash sha256:b6a2d56d90c443f5c3a65cd41b2d8edf5d9c31d737252e15612f1fb57d9d9629 \
    --control-plane --certificate-key 5db3281fc69ac30f6dfdae88c96891ab917bffd5f9f1507ff0dce9457023358a \
    --ignore-preflight-errors=NumCPU

kubeadm join 172.26.108.5:6443 --token szpod2.q5uy6bq4ka37mesv \
     --discovery-token-ca-cert-hash sha256:b6a2d56d90c443f5c3a65cd41b2d8edf5d9c31d737252e15612f1fb57d9d9629
```

--cpu-manager-policy=static
(если указано целочисленное, то под ни с кем не шарит это цпу)

--eviction-hard=memory.available<1Gi
--eviction-minimum-reclaim=memory.availble=2Gi
(что делать если кончается память)

--system-reserved=memory=1.5Gi,cpu=1
--kube-reserved=memory=512Mi,cpu=500m
(резервирование под k8s и system)

Тестирование кластера:
https://github.com/vmware-tanzu/sonobuoy/releases

Аутентификация:
- сертификаты
- файл с токенами
- файл с логинами/паролоями (http basic)
- service account
- authentication proxy (ходить в внешку, например в AD)
- oidc провайдер

OIDC - open id connect (oauth2)

---
Network Policy

У каждого пода должен быть свой уникальный IP адрес.

На каждом узле создается мост, к этому мосту подключается виртуальный ethernet интерфейс. Все поды на узле общаются через мост.
Запускается инфраструктурный контейнер pause с namespace, где и есть виртуальный eth0. На каждый узел свой range IP-адресов, 
откуда подам назначаются адреса. Например:

```
для pod'ов выделена сеть 10.244.0.0/16
На каждый узел выделяется подсеть из сети 10.244.0.0/16, из которой и назначается адрес
```

k8s созданием сети не занимается. Хочешь упросить - добавь абстракций. Для создания сети используется контейнер Network Interface (CNI - стандарт конфигурации сетевых интерфейсов linux-контейнеров).

containter runtime -> CNI -> плагины CNI (loopback, IPvlan, etc)


```
--network-plugin=kubenet
--network-plugin=cni
```
выбирает плагин по алфавиту

calico хранит свои настройки в etcd.
- BGP
- Dynamic IP pool
- Network policies
- IPIP tunnel

```
$ calicoctl get ippool -o yaml
$ calicoctl get nodes -o wide
```
Если ноды находятся в одной сети, то между ними calico не строит туннели.

```
Преимущества Calico
Calico прекрасно подходит для работы в больших кластерах из сотен, или даже тысяч узлов. Использование для маршрутизации протокола BGP и специального кеширующего прокси calico-typha позволяет уверенно обслуживать кластера больших размеров.

Также calico позволяет создать кластер, узлы которого находятся в нескольких локальных сетях.
```

Шифрование трафика - 10-15 раз медленнеее

Как узнать, c помощью каких плагинов была создана сеть в кластере Kubernetes?
- Посмотреть, какие плагины указаны в первом по алфавиту файле в каталоге из ключа --cni-conf-dir kubelet
- Посмотреть значения ключей --network-plugin у kubelet
- Посмотреть, какие Daemonset с частями сетевых плагинов запущены в кластере

Network Policies - запрещено все, что не разрешено

Список из двух элементов, правила выборки будут объединены как логическое ИЛИ:
```
  - from:
      - podSelector:
          matchLabels:
            run: access
      - namespaceSelector:
          matchLabels:
            type: prod
```
(обратить внимание на `-`)

логическое И:
```
  - from:
    - podSelector:
        matchLabels:
          run: access
      namespaceSelector:
        matchLabels:
           type: prod
```

все политики имеют PolicyTypes: Ingress, а если в политике есть разрешения для egress (исходящего) трафика, то в нее добавляется тип Egress

Исправить эту ошибку очень просто, применим манифест, в котором явно укажем его тип.
```
  policyTypes:
    - Egress
```

Сначала указываем тип Ingress и/или Egress, потом в разделах ingress: и/или egress: указывается, кому откуда и/или куда разрешен трафик, а также какой именно трафик разрешен: порт и протокол
```
spec:
  policyTypes:
  - Ingress
  - Egress
  - Ingress,Egress
#- входящие
  ingress: 
    - ports:
       - port: 80
         protocol: TCP или UDP или SCTP
    - from:
       - ipBlock
          cidr: диапазон разрешенных адресов
          except: список вырезанных кусочков
       - namespaceSelector:
           matchLabels:
       - podSelector:
           matchLabels:
# - исходящие
  egress: 
    - ports:
    - to:
```


Как работают сетевые политики:
- Обращаясь к сервису, который отправляет трафик на pod, мы также попадаем под ограничения политики.
- Если в NetworkPolicy выбран pod, то предназначенный для этого pod'а трафик будет ограничиваться. По умолчанию весь трафик запрещен.
- Если для pod'а не определен объект NetworkPolicy, к этому pod'у смогут подключаться все pod'ы из всех пространств имен. То есть, если для конкретного pod'а не определена сетевая политика, по умолчанию неявно подразумевается поведение «разрешить все (allow all)».
- Если трафик к pod'у А ограничен, а pod Б должен к нему подключиться, необходимо создать объект NetworkPolicy. В котором выбран pod А, а также есть ingress-правило, в котором выбран pod Б.


одним pod'ам адреса выдавал flannel, а новым calico, который не знал об адресах, который занял flannel. У старых pod'ов есть liveness probe, которые не проходят, и kubernetes перегружает контейнеры в pod'е. Контейнеры (!), а не под целиком, поэтому ip-адрес, который привязан к sandbox контейнеру, не меняется. В итоге перезагрузка контейнера не помогает.

После добавления контроллера сетевых политик на узлах остались правила iptables, созданные flannel, которые теперь некому удалить. Самый простой способ от них избавиться, зайти на узлы node-1 и node-2 и перезагрузить их.

```
$ kubectl label ns base name=base
```
```
---
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: deny-dev
  namespace: dev
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
       matchLabels:
         run: test
      namespaceSelector:
       matchLabels:
         name: base
```

Безопасность Pod-ов, Pod Security Policy:
- Priveled
- Root user
- Host namespace
- Host path volume
...

PSP позволяет ограничить использование HostPath/HostNetwork, использование флага Privileged на pod'ах и т.д.


```
$ kubectl get po --as=system:serviceaccount:default:user --all-namespaces
```

 количество ресурсов, выданных с помощью resourcequot всем namespace'ам в кластере никак в мозгах Kubernetes'а не коррелирует с общим количеством ресурсов в кластере. То есть в кластере с 10 cpu и 10Gi памяти можно выдать 10 namespace'ам по 10 cpu и 10 Gi памяти. Kubernetes вам ничего об этом не скажет. Поэтому важно мониторить соотношение между всеми resourcequotа'ми и реальным количеством ресурсов в кластере и вовремя предпринимать действия по корректировке размеров кластера.

- Запуск приложений в нескольких реплик
- Контроль доступа и ограничений в кластере
- Использование PDB (позволяет снизить вероятность человеческого фактора на кластер k8s)


### Scheduler
Полный список всех параметров для фильтрации node можно найти тут:
https://github.com/kubernetes/kubernetes/blob/v1.16.3/pkg/scheduler/algorithm/predicates/predicates.go

Полный список всех параметров для scoring'а node тут:
https://github.com/kubernetes/kubernetes/blob/v1.16.3/pkg/scheduler/algorithm/priorities/priorities.go

Задача оператора точно какая-же как и любого Controller manager-a - смотреть в API сервере за своими объектами. Объекты кастомные.

---

StatefulSet

В версии 1.13 включили механизм эвакуации подов на основании тейнтов, с помощью feature gate TaintBasedEvictions и опция controller-manager pod-eviction-timeout перестала действовать. Вместо нее необходимо использовать опции apiserver default-not-ready-toleration-seconds и default-unreachable-toleration-seconds

Почему deployment не подхолдит для запуска stateful приложения:
- RS назначает подам имена со случайными суффиксами
- Доступ только через сервис к случайному поду из пула
- Поды создаются в произвольном порядке
- Нельзя задать отдельный том для каждого пода
- Одинаковый конфиг у всех подов


Проблемы при запуске stateful приложений в k8s:
- хранение данных
- переключение при аварии, фенсинг
  - service labels - медленно
  - защиту от split brain
- стабильность docker
  - резервировать ресурсы под докер демона
  - проблемы с количеством контейнеров
- настройка и управление
  - init-container
  - entrypoint скрипты (костыли)


## Секреты

kubectl create secret generic название_секрета \
# ключ - название файла, значение ключа - содержимое файла
--from-file=file.txt \ 
# ключ - keyname, значение ключа - содержимое файла
--from-file=keyname=file.txt \ 
# ключ - keyname, значение ключа - value
--from-literal=keyname=value
# несколько ключей и значений ( key=val ) из содержимого файла (как в docker .env файле)
--from-env-file=.env

Типы секретов:
- docker-registry

kubectl create secret docker-registry NAME \
  --docker-username=user \
  --docker-password=password \
  --docker-email=email \
 [--docker-server=string]

Использование: добавить в манифест поле imagePullSecrets

apiVersion: v1
kind: Pod
metadata:
  name: foo
spec:
  containers:
    - name: foo
      image: janedoe/awesomeapp:v1
  imagePullSecrets:
    - name: myregistrykey

- tls:
kubectl create secret tls NAME --cert=path/to/cert/file --key=path/to/key/file
Использование: ingress ссылаются на секреты типа tls при указании, где брать сертификат для SSL/TLS.


Kubernetes периодически проверяет, не изменился ли secret, и если он был изменен, то он будет перемонтирован во всех контейнерах, где используется. Таким образом при обновлении secret обновится и информация в файлах внутри контейнеров, куда был смонтирован этот secret.

Не работает с subPath.

Файл монтируется в /tmpfs

---
HPA + metrics-server:
https://raw.githubusercontent.com/kubernetes/community/master/contributors/design-proposals/instrumentation/monitoring_architecture.png

kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=5

kubectl run load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://php-apache; done"

---
Что бэкапить:
- манифесты
- секреты
- сертификаты и настройки узлов (ansible, chef)
- образы контейнеров
- содержимое постоянных томов (хранение истории изменения, защита от логических аварий)
- базы данных


Методы и способы:
- IaC - проще создать новый, чем старый восстановить
- etcd (snapshot save), одним махом
- heptio valero - придирчиво выбираем

Очень много объектов kubernetes зависят от корневого сертификата и сертификатов компонентов control plane, от названий и ip-адресов узлов. Поэтому, восстановив из snapshot'а только базу данных etcd без восстановления сертификатов и структуры, получим нерабочий кластер, в котором надо будет пересоздавать token'ы сервис аккаунтов, удалять отсутствующие узлы, вручную удалять pod'ы statefulset. Очень много ручной работы, требующей хорошего знания внутреннего устройства kubernetes. Одной командой snapshot restore не обойтись.


Heptio valero -> s3, azure, gcs

---
Kubeadm кладет сертификаты в каталог /etc/kubernetes/pki. Он создает несколько самоподписанных корневых сертификатов, которыми подписывает все остальные группы сертификатов.

корневые - 10 год
остальные - 1 год

серты kubelet-а на node могут продляться в автоматическом режиме

kubelet bootstrapping: https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/

kubeadm token create --print-join-command

Список сертификатов, сроки их действия отличаются в зависимости от метода установки кластера, но если брать kubeadm как стандарт, то надо помнить, что раз в 11 месяцев необходимо продлять сертификаты для etcd, api, controller manager, scheduler и kubelet'ов на мастер узлах.
---

Версия kubeadm	Команда	Что делает
1.12	
kubeadm alpha phase certs renew all

продлевает все сертификаты в каталоге /etc/kubernetes/pki
1.13  и 1.14	
kubeadm alpha certs renew  all

продлевает все сертификаты в каталоге /etc/kubernetes/pki
1.15 и выше	
kubeadm alpha certs renew all

продлевает все сертификаты в каталоге /etc/kubernetes/pki, а также сертификаты в файлах конфигурации 
controller-manager.conf
scheduler.conf
admin.conf
















