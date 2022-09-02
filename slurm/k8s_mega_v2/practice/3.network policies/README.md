# Эксперименты с Network Policy

### Переходим в каталог с практикой

Заходим на master-1 в репозиторий с материалами практик, переходим в каталог `3.network policies`.

```
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/3.network\ policies/
```

Подготовим тестовую площадку, на которой будем тестировать NetworkPolicy. Площадка состоит из трех namespace, в которых запущены поды base, prod и test. Они будут имитировать базу данных, к которой обращаются прод- и тест-площадки приложения. Также на ns prod ставится метка. Для запуска pod'ов используется образ, в котором есть утилиты ping и curl. Ещё запускает sshd.

Площадка создается запуском скрипта `./prepare.sh` 
```
./prepare.sh
namespace/base created
namespace/prod created 
namespace/dev created 
namespace/prod labeled 

pod/base created 
pod/test created 
pod/access created 

service/bd2 exposed 

pod/test created 
pod/access created 

pod/test created 
pod/access created
```
Пока в кластере нет ни одной сетевой политики, разрешено все. Чтобы проверить, можно запросить ping из одного pod'а в другой. Для этого запомним ip-адреса pod'ов, зайдем в pod `access` и запросим ping в pod `base`
```
kubectl -n base get pod -o wide
```
```
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE                   NOMINATED NODE   READINESS GATES
access   1/1     Running   0          25s   10.244.4.3   node-2.m000.slurm.io   <none>           <none>
base     1/1     Running   0          25s   10.244.4.2   node-2.m000.slurm.io   <none>           <none>
test     1/1     Running   0          25s   10.244.3.2   node-1.m000.slurm.io   <none>           <none>
```
```
kubectl -n base exec -it access sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes
64 bytes from 10.244.4.2: seq=0 ttl=63 time=0.079 ms
64 bytes from 10.244.4.2: seq=1 ttl=63 time=0.067 ms
```

Применим политику, в которой нет ни одного разрешающего правила. Только селектор выбора, под который попадают все pod'ы в namespace. Network policy создается в namespace и применяется к pod'ам, подходящим под выборку podSelector, только в этом namespace:

Манифест лежит в файле:`1.deny_all.yml`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: default-deny
  namespace: base
spec:
  podSelector:
    matchLabels: {}
```

Применяем:
```
kubectl apply -f 1.deny_all.yml
```

Заходим в под, пробуем запросить ping — ping не проходит 
```
kubectl -n base exec -it access sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes
```

Удаляем сетевую политику
```
kubectl delete networkpolicy default-deny --namespace base
```

Чтобы открыть входящие соединения, надо указать селектор, указывающий, к кому применять политику и правила, разрешающие пропуск трафика. На основании этой информации в firewall'е создадутся правила блокировки. 

Создаем политику, разрешающую доступ к поду base из pod'а access

Манифест в файле:`2.allow_pod.yml`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-bd
  namespace: base
spec:
  podSelector:
    matchLabels:
      run: base
  ingress:
  - from:
      - podSelector:
          matchLabels:
            run: access
```

`podSelector:` — применяем политику к pod'ам с меткой run=base 

`ingress:` — описываем список правил для входящего в поды трафика

`- from:` — разрешаем трафик от подов с меткой run=access
```
kubectl apply -f 2.allow_pod.yml
```

Пробуем запросить ping из различных контейнеров и различных namespace.
```
kubectl -n base exec -it access sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes
64 bytes from 10.244.4.2: seq=0 ttl=63 time=0.071 ms
64 bytes from 10.244.4.2: seq=1 ttl=63 time=0.073 ms

kubectl -n base exec -it test sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes

kubectl -n prod exec -it access sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes

/ # ping 10.244.4.3
PING 10.244.4.3 (10.244.4.3): 56 data bytes
64 bytes from 10.244.4.3: seq=0 ttl=63 time=0.074 ms
64 bytes from 10.244.4.3: seq=1 ttl=63 time=0.071 ms
```

ping проходит только из pod'а access в namespace base. Из pod'а test не проходит ping. Также не проходит ping из pod'а access в namespace prod. Причем из pod'а access в namespace prod прекрасно проходит ping pod access в namespace base, потому что сетевая политика применяется только к pod'ам с меткой run=base.

Ужесточим правило: разрешим доступ только по протоколу tcp на порт 22

Манифест в файле:`3.allow_port_pod.yml`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-bd
  namespace: base
spec:
  podSelector:
    matchLabels:
      run: base
  ingress:
  - ports:
     - port: 22
       protocol: TCP
    from:
      - podSelector:
          matchLabels:
            run: access
```

В правило, разрешающее трафик от pod'ов с меткой `run=access`, добавляется раздел ports: в котором указывается протокол и на какие порты разрешен трафик.
```
kubectl apply -f 3.allow_port_pod.yml
```

Пробуем опять ping и доступ на порт 22/tcp
```
kubectl -n base exec -it access sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes
^C
--- 10.244.4.2 ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
/ # curl 10.244.3.2:22
curl: (1) Received HTTP/0.9 when not allowed

/ # curl bd2:22
curl: (1) Received HTTP/0.9 when not allowed
```

Не проходит ping, работает только curl на 22 порт, точно так же ограничивается трафик, если обращаться не напрямую в pod, а к сервису, который направляет трафик в этот pod.

А теперь откроем доступ из другого namespace по протоколу tcp на порт 22. Выборка объектов в сетевых политиках идет по меткам и, если на pod'ах, созданных командой run метка `run` с именем pod'а создается по умолчанию, то в namespace метку надо добавлять командой `kubectl label namespace prod type=prod`, которая была выполнена в скрипте `prepare.sh`

Манифест в файле `4.allow_port_ns_pod.yml`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-bd-prod
  namespace: base
spec:
  podSelector:
    matchLabels:
      run: base
  ingress:
  - ports:
      - port: 22
        protocol: TCP
    from:
      - podSelector:
          matchLabels:
            run: access
        namespaceSelector:
          matchLabels:
            type: prod
```

Создается новая политика, с другим именем, в которой в разделе `from:` добавляем селектор для namespace.
```
kubectl apply -f 4.allow_port_ns_pod.yml
```
В namespace base теперь два network policy. Одна политика разрешает доступ из pod'а access в том же namespace, а вторая из pod'а access, который находится в namespaces с меткой prod.
```
kubectl -n prod exec -it access sh

/ # ping 10.244.4.2
PING 10.244.4.2 (10.244.4.2): 56 data bytes
^C
--- 10.244.4.2 ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss

/ # curl 10.244.3.2:22
curl: (1) Received HTTP/0.9 when not allowed
```

ping не проходит, но curl на порт 22/tcp работает.
Если удалить политику access-bd, то будет потерян доступ из pod'а access в namespace base, а из pod'а access в namespace prod останется.

Внимание ! Обратите внимание на синтаксис yaml'а:
Если мы укажем вот так:
```
  - from:
      - podSelector:
          matchLabels:
            run: access
      - namespaceSelector:
          matchLabels:
            type: prod
```

То это будет список из двух элементов, правила выборки будут объединены как логическое ИЛИ. Доступ будет разрешен из pod'ов с меткой `run=access` в том же namespace, а также для ВСЕХ pod'ов из namespace с меткой `prod`.

А вот такой манифест, отличающийся только одним минусом:
```
  - from:
    - podSelector:
        matchLabels:
          run: access
      namespaceSelector:
        matchLabels:
           type: prod
```

Представляет собой один элемент списка, и будут выбраны объекты, которые удовлетворяют всем селекторам, то есть pod'ы с меткой `access` из namespace с меткой `prod`.

C правилами для входящего трафика разобрались, теперь давайте посмотрим, каким образом можно регулировать исходящий трафик. Для начала применим манифест, который запрещает доступ в интернет ко всем адресам, кроме 8.8.8.8 и 1.1.1.1.

При первоначальном изучении сетевых политик в этом месте обычно совершают типовую ошибку. Давайте придерживаться традиций и так же совершим ее. Для этого применим манифест из файла:`5.egress_deny.yml.bad`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: deny-prod
  namespace: prod
spec:
  podSelector:
    matchLabels: {}
  egress:
  - to:
    - podSelector:
       matchLabels: {}
      namespaceSelector:
       matchLabels: {}
    - ipBlock:
       cidr: 8.8.8.8/32
    - ipBlock:
       cidr: 1.1.1.1/32
```

Создается политика deny-prod, которая ограничивает исходящий трафик
```
kubectl apply -f 5.egress_deny.yml.bad
```
На первый взгляд вроде бы все хорошо, в манифесте указали раздел `egress:`, `to:` и в нем список объектов, в которые разрешен исходящий трафик — все pod'ы во всех namespace и два ip-адреса. Исходящий трафик работает как надо и вроде бы все хорошо.
```
kubectl -n prod exec -it access sh
/ # curl 10.244.3.2:22
curl: (1) Received HTTP/0.9 when not allowed

/ # ping ya.ru
PING ya.ru (87.250.250.242): 56 data bytes
^C
--- ya.ru ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
/ # ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: seq=0 ttl=45 time=4.691 ms
64 bytes from 8.8.8.8: seq=1 ttl=45 time=4.294 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 4.294/4.492/4.691 ms
/ # ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=59 time=10.850 ms
64 bytes from 1.1.1.1: seq=1 ttl=59 time=10.863 ms
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 10.850/10.856/10.863 ms
```

Но если проверить входящий трафик в pod'ы из namespace prod, то окажется, что он заблокирован.
```
kubectl get pod -n prod -o wide

NAME     READY   STATUS    RESTARTS   AGE   IP           NODE                   NOMINATED NODE   READINESS GATES
access   1/1     Running   0          18m   10.244.4.4   node-2.m000.slurm.io   <none>           <none>
test     1/1     Running   0          18m   10.244.3.3   node-1.m000.slurm.io   <none>           <none>

kubectl -n base exec -it access sh

/ # ping 10.244.3.3
PING 10.244.3.3 (10.244.3.3): 56 data bytes
^C
--- 10.244.3.3 ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
/ # ping 10.244.4.4
PING 10.244.4.4 (10.244.4.4): 56 data bytes
^C
--- 10.244.4.4 ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
/ #
```

Произошло это из-за того, что мы явно не указали, какой тип сетевой политики мы создали: для входящего или для исходящего трафика. И kubernetes сделал это за нас. По его правилам все политики имеют `PolicyTypes: Ingress`, а если в политике есть разрешения для `egress` (исходящего) трафика, то в нее добавляется тип `Egress`. Убедиться в этом можно, посмотрев содержимое сетевой политики:
```
Flag --export has been deprecated, This flag is deprecated and will be removed in future.
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"networking.k8s.io/v1","kind":"NetworkPolicy","metadata":{"annotations":{},"name":"deny-prod","namespace":"prod"},"spec":{"egress":[{"to":[{"namespaceSelector":{"matchLabels":{}},"podSelector":{"matchLabels":{}}},{"ipBlock":{"cidr":"8.8.8.8/32"}},{"ipBlock":{"cidr":"1.1.1.1/32"}}]}],"podSelector":{"matchLabels":{}}}}
  creationTimestamp: null
  generation: 1
  managedFields:
  - apiVersion: networking.k8s.io/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .: {}
          f:kubectl.kubernetes.io/last-applied-configuration: {}
      f:spec:
        f:egress: {}
        f:policyTypes: {}
    manager: kubectl
    operation: Update
    time: "2020-09-30T19:25:11Z"
  name: deny-prod
  selfLink: /apis/networking.k8s.io/v1/namespaces/prod/networkpolicies/deny-prod
spec:
  egress:
  - to:
    - namespaceSelector: {}
      podSelector: {}
    - ipBlock:
        cidr: 8.8.8.8/32
    - ipBlock:
        cidr: 1.1.1.1/32
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

И согласно правилу «Запрещено все, что не разрешено», сетевая политика deny-prod с типом `Ingress` запретила весь входящий трафик, так как в ней нет ни одного разрешающего правила. Исправить эту ошибку очень просто, применим манифест, в котором явно укажем его тип.

Манифест из файла:`5.egress_deny.yml`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: deny-prod
  namespace: prod
spec:
  policyTypes:
    - Egress
  podSelector:
    matchLabels: {}
  egress:
  - to:
    - podSelector:
       matchLabels: {}
      namespaceSelector:
       matchLabels: {}
    - ipBlock:
       cidr: 8.8.8.8/32
    - ipBlock:
       cidr: 1.1.1.1/32
```

Теперь входящий трафик в pod'ы остался разрешенным.
```
kubectl apply -f 5.egress_deny.yml

kubectl -n base exec -it access sh

/ # ping 10.244.3.3
PING 10.244.3.3 (10.244.3.3): 56 data bytes
64 bytes from 10.244.3.3: seq=0 ttl=62 time=4.230 ms
64 bytes from 10.244.3.3: seq=1 ttl=62 time=5.517 ms
^C
--- 10.244.3.3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 4.230/4.873/5.517 ms
/ # ping 10.244.4.4
PING 10.244.4.4 (10.244.4.4): 56 data bytes
64 bytes from 10.244.4.4: seq=0 ttl=63 time=0.072 ms
64 bytes from 10.244.4.4: seq=1 ttl=63 time=0.081 ms
^C
--- 10.244.4.4 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.072/0.076/0.081 ms
```

Если мы хотим разрешить доступ ко всем pod'ам кластера и доступ только на порт 53/udp к адресам 8.8.8.8 и 1.1.1.1, то нам потребуется манифест из файла `6.egress_deny_53.yml`
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: deny-prod
  namespace: prod
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
       matchLabels: {}
      namespaceSelector:
       matchLabels: {}
  - to:
    - ipBlock:
       cidr: 8.8.8.8/32
    - ipBlock:
       cidr: 1.1.1.1/32
    ports:
      - port: 53
        protocol: UDP
```

В этом манифесте уже два элемента в списке правил `egress:` один разрешает доступ ко всем портам всех pod'ов в кластере, а второй только к порту 53/udp на адреса 8.8.8.8 и 1.1.1.1
```
kubectl apply -f 6.egress_deny_53.yml
```
Адрес 1.1.1.1 не проходит ping, но dig прекрасно отсылает dns запросы по 53/udp на этот адрес 
```
kubectl -n prod exec -it access sh

/ # ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1): 56 data bytes
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
/ # dig @1.1.1.1 ya.ru

; <<>> DiG 9.10.8-P1 <<>> @1.1.1.1 ya.ru
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 59022
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
;; QUESTION SECTION:
;ya.ru.                         IN      A

;; ANSWER SECTION:
ya.ru.                  290     IN      A       87.250.250.242

;; Query time: 10 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Sun Jul 14 19:56:58 UTC 2019
;; MSG SIZE  rcvd: 50
```

Рассмотрим, каким образом указываются разрешенные соединения в спецификациях `Network Policy:`

Сначала указываем тип `Ingress` и/или `Egress`, потом в разделах `ingress:` и/или `egress:` указывается, кому откуда и/или куда разрешен трафик, а также какой именно трафик разрешен: порт и протокол.
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
Если в элементе списка указан только `ports:` — значит, трафик на этот порт разрешен всем.

