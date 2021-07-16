Promo code - DEVOPS15 - while registering for the CKA or CKAD exams at Linux Foundation to get a 15% discount.
Use the code - KUBERNETES15

Exam Tips: http://training.linuxfoundation.org/go//Important-Tips-CKA-CKAD
export do="--dry-run=client -o yaml"

kubectl exec etcd-master -n kube-system etcdctl get / --prefix -key-only

export ETCDCTL_API=3
etcdctl snapshot save 
etcdctl endpoint health
etcdctl get
etcdctl put

kubectl exec etcd-master -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /etc/kubernetes/pki/etcd/ca.crt --cert /etc/kubernetes/pki/etcd/server.crt  --key /etc/kubernetes/pki/etcd/server.key" 

---

#kube-apiserver

$ cat /etc/kubernetes/manifests/kube-apiserver.yaml
$ cat /etc/systemd/system/kube-apiserver.service
$ ps -aux | grep kube-api-server


Tips:

Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)
$ kubectl run nginx --image=nginx --dry-run=client -o yaml

Create a deployment
$ kubectl create deployment --image=nginx nginx

Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)
$ kubectl create deployment --image=nginx nginx --dry-run=client -o yaml

Generate Deployment YAML file (-o yaml). Don't create it(--dry-run) with 4 Replicas (--replicas=4)
$ kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml

Save it to a file, make necessary changes to the file (for example, adding more replicas) and then create the deployment.

$ kubectl create deployment nginx --image=nginx --replicas=4

$ kubectl scale deployment nginx --replicas=4


Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379
$ kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml


$ kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml

(This will not use the pods labels as selectors, instead it will assume selectors as app=redis. You cannot pass in selectors as an option. So it does not work very well if your pod has a different label set. So generate the file and modify the selectors before creating the service

$ kubectl expose pod nginx --port=80 --name nginx-service --type=NodePort --dry-run=client -o yaml
(This will automatically use the pod's labels as selectors, but you cannot specify the node port. You have to generate a definition file and then add the node port in manually before creating the service with the pod.)

---
manual scheduling:

nodeName: <node>
---

Edit a POD
Remember, you CANNOT edit specifications of an existing POD other than the below.
- spec.containers[*].image
- spec.initContainers[*].image
- spec.activeDeadlineSeconds
- spec.tolerations

Edit Deployments
With Deployments you can easily edit any field/property of the POD template. Since the pod template is a child of the deployment specification,  with every change the deployment will automatically delete and create a new pod with the new changes. So if you are asked to edit a property of a POD part of a deployment you may do that simply by running the command

$ kubectl edit deployment my-deployment

---
static pods:

kubelet ... --pod-manifest-path=/etc/kubenetes/manifests

...
--config=kubeconfig.yaml
staticPodPath: /etc/kuberentes/manifests

static pods and ds are ignored by kube-scheduler.

static pods has suffix with node name
---

custom scheduler

--scheduler-name=my-custom-scheduler
...
--lock-object-name=my-custom-scheduler

pod definition
schedulerName: my-custom-scheduler


$ kubectl get events
$ kubectl logs my-custom-scheduler

---
metrics-server (in-memory only)
$ kubectl top node
$ kubectl top pod
---
$ kubectl -f logs <pod> -c <container>
---

$ kubectl create -f deployment.yaml
$ kubectl get deployments
$ kubectl apply -f deployment-definition.yaml
$ kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1
$ kubectl rollout status deployment/myapp-deployment
$ kubectl rollout history deployment/myapp-deployment
$ kubectl rollout undo deployment/myapp-deployment
---
image:
from ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]

$ docker run ubuntu-sleeper
5 seconds
$ docker run ubuntu-sleeper 10
10 seconds
$ docker run --entrypoint sleep2.0 ubuntu-sleeper 10
sleep2.0 10
---

$ kubectl create configmap \
    app-config --from-literal=APP_COLOR=blue

$ kubectl create configmap \ 
    app-config --from-file=app_config.properties


$ kubectl get configmaps


envFrom:
  - configMapRef:
      name: app-config

env:
  - name: APP_COLOR
    valueFrom:
      configMapKeyRef:
         name: app-config
         key: APP_COLOR

volumes:
- name: app-config-volume
  configMap:
    name: app-config
---

$ kubectl create secret generic \
   app-secret --from-literal=DB_host=mysql

$ kubectl create secret generic \
   app-secret --from-file=app_config.properties
---
$ kubectl get secrets

envFrom:
  - secretRef:
      name: app-config

env:
  - name: DB_Password
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: DB_Password

volumes:
- name: app-secret-volume
  secret:
    secretName: app-secret

inside container:
$ cat /opt/app-secret-volumes/DB_Password
passwrd_value


Also the way kubernetes handles secrets. Such as:
- A secret is only sent to a node if a pod on that node requires it.
- Kubelet stores the secret into a tmpfs so that the secret is not written to disk storage.
- Once the Pod that depends on the secret is deleted, kubelet will delete its local copy of the secret data as well.
---

initContainers:
```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'git clone <some-repository-that-will-be-used-by-application> ; done;']
```

---

wait for died:
kube-controller --pod-eviction-timeout=5m ...

$ kubectl drain node-1
$ kubectl uncordon node-1

# (prevents scheduling new pods)
$ kubectl cordon node-2
---

see the version:
$ k get nodes 

version number
1.11.3
major minor patch

all components with the same version (except etcd cluster and coredns).

https://kubernetes.io/releases/version-skew-policy/#supported-version-skew


- kube-apiserver     X (minor version)
- controller-manager X-1
- kube-scheduler     X-1
- kubelet            X-2
- kubeproxy          X-2
- kubectl            X+1 > X-1

k8s supports only 3 last minor releases

upgrade only 1 minor version at one time

kubeadm upgrade plan
kubeadm upgrade apply

1. upgrade master 
2. upgrade nodes


$ apt-get upgrade -y kubeadm=1.12.0-00
$ kubeadm upgrade apply v1.12.0

$ kubectl get nodes - shows kubelet versions, not kube-api version

$ apt-get upgrade -y kubelet=1.12.0-00
$ systemctl restart kubelet

then working nodes:
$ kubectl drain node-1
$ apt-get upgrade -y kubeadm=1.12.0-00
$ apt-get upgrade -y kubelet=1.12.0-00
$ kubeadm upgrade node config --kubelet-version v1.12.0
$ systemctl restart kubelet
$ kubectl uncordon node-1

---

kubeadm token list

---
backup and restore
- resource config (github, kubectl get all -A -o yaml > all-deploy-services.yaml (velero) )
- etcd cluster (ETCDCTL_API=3 etcdctl snapshot save sp.db)
  restore process:
    - systemctl stop kube-apiserver
    - etcdctl snapshot restore sp.db --data-dir /var/lib/etcd-from-backup
    - systemctl restart etcd
    - systemctl start kube-apiserver
- pv
---
Security

password based auth disabled
only ssh based on nodes

kube-apiserver
Authentication - who can access?
- username and passwords (not recommended, deprecated 1.19)
- username and tokens (not recommended, deprecated 1.19)
- certificates
- external providers - LDAP
- service accounts

Authorization - what can they do:
- RBAC authorization
- ABAC Auth
- Node
- Web hook

Create a file with user details locally at /tmp/users/user-details.csv
# User File Contents
password123,user1,u0001
password123,user2,u0002
password123,user3,u0003
password123,user4,u0004
password123,user5,u0005

/etc/kubernetes/manifests/kube-apiserver.yaml

  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
      <content-hidden>
    - --basic-auth-file=/tmp/users/user-details.csv
...
    volumeMounts:
    - mountPath: /tmp/users
      name: usr-details
      readOnly: true
  volumes:
  - hostPath:
      path: /tmp/users
      type: DirectoryOrCreate
    name: usr-details

---
ssl/tls

asymmetric encryption - ssh
ssh-keygen - private/public key

$ openssl genrsa -out my-bank.key 1024
my-bank.key
$ openssl rsa -in my-bank.key -pubout > mybank.pem
my-bank.key myback.pem


kube-api: apiserver.crt apiserver.key
etcd server: etcdserver.crt etcdserver.key
kubelet: kubelet.crt kubelet.key

clinet certs: admin.crt admin.key
scheduler: scheduler.crt scheduler.key
kube-controller manager: c-m.crt c-om.key
kube-proxy: kube-proxy.crt kube-proxy.key

ca => admin => scheduler => controller- manager => kube-proxy,
KUBERNETES-CA => kube-admin/O=system:masters,

#generate keys
$ openssl genrsa -out ca.key 2048
ca.key

$ cert signing request
$ openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -out ca.csr
ca.csr

sign certificates:
$ openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
ca.crt

$ openssl req -new -key apiserver.key -subj "\CN=kube-apiserver" -out apiserver.csr -config openssl.cnf
openssl.cnf
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.96.0.1
IP.2 = 172.17.0.87

$ cat /etc/kubernetes/manifests/kube-apiserver.yaml
- --client-ca-file=/etc/kubernetes/pki/ca.crt
...
- --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
- --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
- --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
...
- --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
- --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
...
- --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
- --tls-private-key-file=/etc/kubernetes/pki/apiserver.key

$ openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

https://github.com/mmumshad/kubernetes-the-hard-way/tree/master/tools

---
$ kubectl get csr
$ kubectl certificate approve jane

$ cat /etc/kubernetes/manifests/kube-controller-manager.yaml
- --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
- --cluster-signing-key-file=/etc/kubernetes/pki/ca.key

---
$HOME/.kube/config

$ kubectl config view
$ kubectl config use-context prod-user@production
$ kubectl config -h 
---
API Groups
$ curl http://localhost:6443 -k
$ curl http://localhost:6443/apis -k | grep "name"
--key admin.key
--cert admin.crt
--cacert ca.crt
---
Authorization

kube-apiserver
--authorization-mode=AlwaysAllow (Node,RBAC,Webhook)
---
RBAC
$ kubectl get roles
$ kubectl get rolebinding
$ kubectl auth can-i create deployments
$ kubectl auth can-i delete nodes
$ kubectl auth can-i create deployments --as dev-user
$ kubectl auth can-i create pods --as dev-user
---
$ kubectl api-resources --namespaced==false
$ kubectl get clusterroles
$ kubectl get clusterrolebindings
---
$ docker login private-registry.io
$ docker run private-registry.io/apps/internal-app

$ kubectl create secret docker-registry regcred \
   --docker-server= \
   --docker-username= \
   --docker-password= \
   --docker-email=

imagePullSecrets:
 - name : regcred
---
Security context

securityContext:
  runAsUser: 1000
  capabilites:
    add: ["MAC_ADMIN"]
---
Network Security

default: All Allow

labels:
  role: db
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLables:
          name: api-pod
    ports:
    - protocol: TCP
      port: 3306
```
Flannel doesn't support NP

https://kubernetes.io/docs/concepts/services-networking/network-policies/
---
Docker Storage
- storage drivers
- volume drivers

Container Layer: Read Write (copy-on-write)
Image Layer: Read Only
 
$ docker volume create date_volume
# /var/lib/docker/volumes/data_volume

$ docker run -v data_volume:/var/lib/mysql mysql (volume mount)
$ docker run -v /data/mysql:/var/lib/mysql mysql (volume bind)

storage drives:
- aufs
- zfs
- btrfs
- device mapper
- overlay
- overlay2

volume drivers:
- local
- azure file sotrage
- glusterfs
- netapp
- ...

$ docker run -it --name mysql --volume-driver rexray/ebs --mount src=ebs-vol,target=/var/lib/mysql mysql

CSI - portworx, amazon ebs, dell emv, glusterfs
CRI - rtk, docker, cri-o
CNI - weaveworks, flannel, cilium

CSI RPC:
- CreateVolume
- DeleteVolume
- ControllerPublicVolume

volumes:
- name: data-volume
  hostPath:
    path: /data
    type: Directory

$ kubectl get pv

$ kubectl get pvc

apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim

---
Networking

$ ip link
$ ip addr
$ ip addr add 192.168.1.10/24 dev eth0

/etc/network/interfaces

$ ip route
$ ip route add 192.168.1.0/24 via 192.168.2.1

$ cat /proc/sys/net/ipv4/ip_forward
1

Dns Linux
$ cat /etc/hosts
192.168.1.11 db


^ name resolution

DNS Server - centralized name resolution

$ cat /etc/resolv.conf
nameserver 192.168.1.100

default priority:
1) local /etc/hosts
2) remote dns server

$ cat /etc/nsswitch.conf


Forward All to 8.8.8.8

Root: .
Top Level Domain Name: .com
google

Subdomain: mail drive www maps apps

$ cat /etc/resolv.conf
nameserver
search mycompany.com

Record Types:
A - web-server 192.168.1.1
AAAA - web-server 12001:0db8^85a3:0000:0000:8a2e:0370:7334
CNAME - food.web-server eat.web-server,hungry.web-server

$ nslookup www.google.com
only query dns server ignore /etc/hosts
also:
$ dig www.google.com

Network namespaces

$ ip netns add red
$ ip netns add blue
$ ip netns

# link ifs
$ ip link 

$ ip netns exec red ip link
$ ip -n red link

inside container - empty:
$ arp
$ route

linux bridge - virtual switch
$ ip link add v-net-0 type bridge
$ ip link set dev v-net-0 up


$ ip -n red addr add 192.168.1.10/24 dev veth-red

Docker Networking

$ docker run --network none nginx
$ docker run --network host nginx
$ docker run nginx (bridge)

$ docker network ls
$ ip link

1. Create Network Namespace
2. Create Bridge Network/Interface
3. Create VETH Pairs (pipe, virtual cable)
4. Attach vEth to Nemespace
5. Attach Other vEth to Bridge
6. Assign IP Address
7. Bring the interfaces up
8. Enable NAT - IP Masquerade

CNI ^ resposobilities:
* CR must create network namespace
* Identify network the container must attach to
* CR to invoke Network Plugin (bridge) when container is ADDed
* CR to invoke Network Plugin (bridge) when container is DELeted
* JSON format of the Network Configuration

Plugin responsibilities:
* Must support cmd line args ADD/DEL/CHECK
* Must support parameters container id, network ns etc..
* Must manage IP Address assignment to PODs
* Must Return results in a specific format

handy commands:
$ ip link
$ ip addr
$ ip add add 192.168.1.10/24 dev eth0
$ ip route
$ ip route add 192.168.1/24 via 192.168.2.1
$ route
$ cat /proc/sys/net/ipv4/ip_forward
$ arp
$ netstat -plnt

https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/#steps-for-the-first-control-plane-node

Pod Networking

networking model
* every POD should have an IP Addres
* every POD should be able to communicate with every other POD in the same node
* every POD should be abble to communicate with every other POD on other nodes without NAT

kubelet
--cni-conf-dir=/etc/cni/net.d
--cni-bin-dir=/etc/cni/bin

./net-script.sh add <container> <namespace>

Configuring CNI

kubelet.service
--network-plugin=cni
--cni-conf-dir=...
--cni-bin-dir=...

deploy weave: 
$ kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

$ cat /etc/cni/net.d/net-script.conf

Service Networking

forwarding rules on every node in cluster
- userspace
- iptables
- ipvs

kube-api-server --service-cluster-ip-range=IpNet

$ iptables -L -t net | grep db-service
$ cat /var/log/kube-proxy.log

Dns Resolution

service-name.namespace.svc.cluster.local
pod-ip.namespace.svc.cluster.local

$ cat /etc/resolv.conf
nameserver 10.96.0.10

kube-dns -> CoreDNS

deployed as pod in kube-system

$ cat /etc/coredns/Corefile
$ kubectl get configmap -n kube-system

$ cat /var/lib/kubelet/config.yaml
clusterDNS:
- 10.96.0.10
clusterDomain: cluster.local

---
Ingress
ingress-controller
- haproxy
- istio
- nginx
- ...

ingress resource - kind: Ingress


apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  namespace: critical-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /pay # or path: /something(/|$)(.*)
        backend:
          serviceName: pay-service
          servicePort: 8282

---

Designing k8s cluster

api-server - active-active
controller-manager - active-standby

kube-controller-manager --leader-elect true \
	--leader-elect-lease-duration 15s \
        --leader-elect-renew-deadline 10s \
        --leader-elect-retry-period 2s \

scheduler - active-standby
---

Install k8s

1. multiple nodes provisioned
2. container runtime on hosts (all)
3. install kubeadm (all)
4. init master node
5. pod network
6. join node (workers)

e2e tests:
https://www.youtube.com/watch?v=-ovJrIIED88&list=PL2We04F3Y_41jYdadX55fdJplDvgNGENo&index=18
1.5 hours

---
Troubleshooting

1. check service status
$ curl http://<service>:<port>
$ kubectl describpe service <service>
2. check selectors
3.
$ kubectl get pods
$ kubectl describe pod
$ kubectl logs -f
$ kubectl logs -f --previous


$ kubectl -n kube-system get pods

$ systemctl status kube-api...
$ systemctl status kube-proxy

$ kubectl logs kube-apiserver-master -n kube-system
$ journalctl -xe -u kube-apiserver

$ systemctl status kubelet
$ top


- cni-bin-dir:   Kubelet probes this directory for plugins on startup
- network-plugin: The network plugin to use from cni-bin-dir. It must match the name reported by a plugin probed from the plugin directory.

1. Weave Net:
  These is the only plugin mentioned in the kubernetes documentation. To install,
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"


2. Flannel :
   To install, kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/2140ac876ef134e0ed5af15c65e414cf26827915/Documentation/kube-flannel.yml   

Note: As of now flannel does not support kubernetes network policies.

3. Calico :
   To install, curl https://docs.projectcalico.org/manifests/calico.yaml -O
  Apply the manifest using the following command.
      kubectl apply -f calico.yaml
   Calico is said to have most advanced cni network plugin.

---
$ kubeadm token create --print-join-command
$ openssl x509  -noout -text -in /etc/kubernetes/pki/apiserver.crt
$ kubeadm certs check-expiration

