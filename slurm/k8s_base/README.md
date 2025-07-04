Принципы k8s:
- immutable (нет проблемы configuration drift)
	- containers
	- nodes
- declarative
	- describe
	- IaC
- self-healing (каждый компонент отвечает за свою часть всей инфраструктуры и постоянн поддерживает ее в актуальном состоянии)
	- more time (меньше времени на поддержку, больше времени на развитие)
	- .. to sleep
- decoupling (каждый компонент инфраструктуры независим от других, и полагается на их SLA)
	- cluster
	- app


Kubernetes workflow
UI or CLI -> API -> Kubernetes Master -> Nodes


When Kubernetes creates a Pod it assigns one of these QoS classes to the Pod:
- Guaranteed (limits == requests)
- Burstable ( limits > requests)
- BestEffort ( no limits + no request)

в первую очередь эвакуируется BestEffort -> Burstable -> Guaranteed

BestEffort - высокий OOMScore - убивается первую очередь
Guaranteed - в последнюю очередь


# удалить все (не удаляет cm, secrets, ingress)
$ kubectl delete all --all


$ kubectl delete -f .


namespace wide:
- pod
- deployment
- pvc
- configmap
- service
- ingress

cluster wide:
- pvc
- StorageClass


---
Controller-manager:
- Набор контроллеров
	- Node controller (аварийная эвакуакция подов с ноды)
	- ReplicaSet controller
	- EndPoints controller
	- etc...
- GarbageCollector - сборщик мусора (н-р: 10 реплика сет, 11-ый рс будет удален gc)


Scheduler:
- Назначает POD-ы на ноды, учитывая:
	- QoS (наиболее важные Guaranteed, OOMKiller убивает в первую очередь BestEffort)
	- Affinity / anti-affinity
	- Requested resources
	- Priority Class (при возникновении аварий, в первую очередь эвакуюриуются те кто PC больше; если не удается запуститься, то будут гасится те поды, у которых PC ниже)


$ kubectl get componentstatuses
$ kubectl get nodes
$ kubectl describe node minikube.s013939.slurm.io


Kubelet:
- работает на каждой ноде
- единственный компонент, работающий не в Docker (systemd приложение)
- отдает команды Docker daemon
- создает POD-ы (так же контролирует их работы, hc, probes)

Kube-proxy:
- смотрит в KubeAPI
- смотрит на всех серверах
- управляет сетевыми правилами на нодах
- фактически реализует Service (ipvs или iptables)

```
-A KUBE-SERVICES
  -d 1.1.1.1/32
  -p tcp
  -m comment --comment "mynamespace/myservice:http cluster IP"
  -m tcp --dport 80
-j KUBE-SVC-UT6A43GJFBEBBO3V


-A KUBE-SVC-UT6A43GJFBEBBO3V
  -m comment --comment "mynamespace/myservice:http"
  -m statistic
    --mode random --probability 0.500000000
-j KUBE-SEP-MMYWB6DZJI4RZ5CQ

-A KUBE-SVC-UT6A43GJFBEBBO3V
  -m comment --comment "mynamespace/myservice:http"
-j KUBE-SEP-J33LX377GA3DLDWM

-A KUBE-SEP-MMYWB6DZJI4RZ5CQ
  -p tcp
  -m comment --comment "mynamespace/myservice:http"
  -m tcp
-j DNAT
  --to-destination 10.102.0.93:80
```

Service:
- static IP
- DNS имя в kube-dns на этот IP (myservice.mynamespace.svc.cluster.local)
- Правила iptables для роутинга
- Service это не прокси!
- Проблемы NAT в Linux (исходящий трафик проходящий через NAT записывает в табличку исходящий порт, бывает что записывается 2 одинаковых порта, соответственно первый пакет, который возращается отрабатывается и удаляется, а второй пакет откидывается)

Network plugin (Flannel, Calico..):
- обеспечивает связь между нодами и подами
- раздает IP-адреса подам
- реализиует шифроивание между нодами
- управляет network policies


Способы установки K8s:
- kubernetes hard way
- rancher
- kubeadm
- kubespray (ansible сценарий)

Kubespray, некоторые проблемы при переходе на установку через kubeadm:
- нет возможности апгрейда кластера, установленного классическим способом
- сертификаты выписаны на 1 год, обновлять надо вручную
- если установка остановилась по ошибке, потвороный запуск не всегда может помочь

Подготовка серверов:
- Master 2vcpu, 4Gb RAM, 10Gb disk
- Ingress 1vcpu, 2GB RAM, 10Gb disk
- Node 2-4vcpu, 4-8GB RAM
- Kernel 4.x
- Disable firewalld
- local network between servers
- Disable swap
- ssh доступ по ключам


```
$ git clone https://github.com/southbridgeio/kubespray
$ cd kubespray
$ pip install -r requirements.txt
...
```

Проблемы при обновлении:
- Устаревшие версии манифестов (deprecated: extensions/v1beta1)
- Устаревшие ключи запуска (deprecated: --experimental-bootstrap-kubeconfig --bootstrap-kubeconfig)
- Изменённые опции (kubeadm alpha phase)
- Исправленные ошибки:
	- в 1.14.1 - валидация манифестов стала строже
	- cephfs-provisioner перестал ставится из-за ошибки
	- cniVersion: - стало обязательным полем
- обновление docker

Порядок обновления:
- Изучаем change log
- Устанавливаем тестовый кластер
- Обновляем тестовый кластер
- Деплоим приложения, проверяем работу
- Планируем время обновления
- Делаем бэкапы
- Обновляем прод по одной ноде
- После каждой ноды проверяем работоспособность

Что обновляем:
- etcd database
- Control plane: API, controller-manager, scheduler + kubelet
- kubelet on worker node
- kube-proxy
- kube-flannel
- coredns, nodelocaldns
- ingress-nginx-controller
- certificate

https://kubernetes.io/docs/setup/release/version-skew-policy/


Задача мониторинга
- на каждой ноде автоматически запускается агент
- управляются агенты из одной точки
- конфигурируются так же из одной точки

- static pod (лежат на узлах кластера, в /etc/kubernetes/manifests/, kubelet проверяет при запуске, после этого пробует соед и api server)
- pod anti-affinity
- daemon set

StatefulSet
- Позволяет запускать группу подов (как Deployment)
	- Гарантирует их уникальность
	- Гарантирует их последовательность
- PVC template
	- при удалении не удаляет PVC
- Используется для запуска приложений с сохранением состояния
	- rabbit
	- DBs
	- Redis
	- Kafka
	- ...

!!! k8s не переносить поды SS из упавших узлов

Headless Service
- .spec.clusterIP: None
- Резолвится в IP всех эндпоинтов
- Создает записи с именами всех эндоинтов


Job
- создает под для выполнения задачи
- перезапускает поды до успешного выполнения задачи
	- или исчетчечния таймаутов
		- activeDeadLineSeconds
		- backoffLimit
		- ttlSecondsAfterFinished


ttlSecondsAfterFinished - нужен обязательно. Т.к. остановленные контейнеры не учитываются в pod limit-ах, может пострадать docker daemon.


CronJob
- создает Job по расписанию
- важные параметры
	- startingDeadlineSeconds
	- concurrencyPolicy
	- successfulJobsHistoryLimit
	- failedJobsHistoryLimit


https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#cron-job-limitations
```
A cron job creates a job object about once per execution time of its schedule. We say "about" because there are certain circumstances where two jobs might be created, or no job might be created. We attempt to make these rare, but do not completely prevent them. Therefore, jobs should be idempotent.
```

RBAC
- Role
- RoleBinding
- ClusterRole
- ClusterRoleBinding
- ServiceAccount

rbac не защищает от docker exec в контейнер из узла.
Роль - список правил объединенных в одну абстракцию. Никаких прав никому не выдает.

$ kubectl get clusterrole
$ kubectl get role

$ kubectl get service --as=system:serviceaccount:default:user


Service ClusterIP

Способы публикации:
- Service: L3 OSI, NAT, kube-proxy
	- ClusterIP
	- NodePort
	- LoadBalancer
- Ingress: L7 OSI, HTTP и HTTPS, nginx, envoy, traefik, haproxy

если сервис в одной NS, а под в другом - они друг друга не найдут.



ExternalName

отсылка на внешний сервис


DNS
- выполняет роль service discovery


ClientPod -> dns запрос -> local dns cache (169.254.25.10) (либо сразу в CoreDNS) -> если в кэше нету записи -> CoreDNS -> резолвит отправляет ответ

local dns cache общается с coredns через CoreDNS ClusterIP (iptables) (caveats - NAT if iptables), Upgrade to TCP.

"pods verify k8s authpath coredns"

headless сервис позволяет обратится к поду, например для StatefulSet-ов.


---
Темплэйтирование
- Sed / Envsubst
- Ansible
- Kubectl based (если возникает ошибка, undo работает наботает только на deployment-ах, она не будет откатывать изменения в servicах, configmapах и т.д.

)
- Helm (cжимает, base64 и хранит манифесты в секретах)


Время, которое дается deployment'у на успешное завершение обновления контролируется с помощью параметра  progressDeadlineSecond в описании deployment'а и по умолчанию = 600 секундам.

$ kubectl rollout status deployment test || kubectl rollout undo deployment test

Почему Helm?
- "пакетный менеджер" (по другому работает с зависимостями - все равно ставит)
- CNCF
- декларативный
- Состоит из Helm + Tiller (в v2)
- есть важные фичи для построения CD
	- watch
	- rollback
- система плагинов (например переезд с v2 в v3, или helm-монитор - контролировать 500-ки)

Пакет (chart-ы) (.tgz)
- набор template manifest
- файл с values
- мета

используется go template

$ helm ls --all-namespaces

$ helm repo add stable https://charts.helm.sh/stable
$ helm inspect values stable/kube-ops-view > values.yaml
$ helm install kube-ops-view stable/kube-ops-view --namespace kube-system -f values.yaml

$ helm create test-chart

Тестирование релиза:
1. создаем папку templates/tests/
2. кладем туда манифесты объектов k8s которые будут тестить релиз
3. манифесты должны содержать аннотакцию helm,.sh/hook: test
4. запускаем в CI helm test <release name>


Подключение хранение данных
- Storage class: хранит параметры подключения
- PersistanceVolumeClaim описывает требования к тому
- PersistanceVolume хранит параметры и статус тома
- Provisioner параметры SC, плагин создания томов

Container Storage Interface - унифицированный интерфейс хранилищ

node plugin - запущен на каждом узле
controller plugin - взаимодействие с хранилищем

Ceph CSI
- dymanically provision RWO and RWX mode
- snapshot
- resize
- quota
- metrics
- topology aware

---
$ echo "172.26.108.6:6789:/ /mnt/cephfs ceph name=admin,secretfile=/etc/ceph/secret.key,noatime,_netdev 0 2">>/etc/fstab


$ getfattr -n ceph.quota.max_bytes /mnt/cephfs/volumes/csi/csi-vol-17f86edb-ae3a-11eb-97e1-da9c18118f93/0fa4ea05-1508-4fb6-a2b1-1ddba2aebb64/
---

Cert-manager
- начинался каак способ получить сертификат от LetsEncrypt
- автоматизирует получение SSL/TLS-сертификатов от различных удостоверяющих центров (LetsEncrypt, selfhosted, selfsigned)
- интегрируется с ингресс-контроллеров
- автоматизирует продление сертификатов
- CRD: Issuer, ClusterIssuer, Certificate, Order, Challenge
- RBAC: certmanager.k8s.io

---
Этапы CI/CD
- build
- test
- clean up
- push
- deploy


$ kubectl create secret docker-registry xpaste-gitlab-registry --docker-server registry.slurm.io --docker-email 'student@slurm.io' --docker-username 'gitlab+deploy-token-1859' --docker-password '_RGgBmcR4tExztXJEs2f' --namespace s013939-xpaste-production

$ helm install postgresql ~/slurm/practice/9.ci-cd/9.5.deploy/5.1.prepare_cluster/postgresql --namespace s013939-xpaste-production --atomic --timeout 120s

$ kubectl create secret generic slurm-xpaste --from-literal secret-key-base=xxxxxxxxxxxxxxxxxxxxxxxxx --from-literal db-user=postgres --from-literal db-password=postgres --namespace s013939-xpaste-production