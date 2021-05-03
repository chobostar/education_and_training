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
