> **Все работы все еще проводим с первого мастера**

### Хакнем наш Kubernetes

1) Переходим в директорию с практикой.
```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/4.secure-and-highlyavailable-apps/psp
```

2) Cоздаем тестового пользователя
```bash
kubectl create serviceaccount user --namespace=default
kubectl create rolebinding user --clusterrole=edit --serviceaccount=default:user
```

3) Проверяем права созданного пользователя
```bash
kubectl get po --as=system:serviceaccount:default:user --all-namespaces
```

> Куб должен запрещать просмотр всех Pod'ов во всем кластере

4) Пробуем хакнуть ограничения

Запускаем Pod хацкера, так же от имени пользователя user

```bash
kubectl create -f hackers-pod.yaml --as=system:serviceaccount:default:user
```

5) Проверяем Pod

```bash
kubectl get pod
```

Видим

```bash
NAME          READY   STATUS    RESTARTS   AGE
hackers-pod   1/1     Running   0          1m
```

6) Заходим внутрь и осматриваемся (все это делаем от имени пользователя без прав админа)

```bash
kubectl exec -t -i hackers-pod --as=system:serviceaccount:default:user bash
```

Например

```bash
cat /host/etc/kubernetes/admin.conf
```

Радуемся полученному доступу к сертификатам кластера

7) Удаляем хацкерский Pod

```bash
kubectl delete -f hackers-pod.yaml
```

### Подключаем PSP

1) Применяем psp и rbac

```bash
kubectl apply -f psp-system.yaml
kubectl apply -f rbac-system.yaml
kubectl apply -f psp-default.yaml -f rbac-default.yaml
```

2) Смотрим, что получилось

```bash
kubectl get psp
```

Видим

```bash
NAME      PRIV    CAPS   SELINUX    RUNASUSER   FSGROUP    SUPGROUP   READONLYROOTFS   VOLUMES
default   false          RunAsAny   RunAsAny    RunAsAny   RunAsAny   false            configMap,emptyDir,projected,secret,downwardAPI,persistentVolumeClaim
system    true    *      RunAsAny   RunAsAny    RunAsAny   RunAsAny   false            *
```

3) Обновляем конфигурацию kube-api

```bash
kubectl edit configmap --namespace=kube-system kubeadm-config
```

И добавляем

```yaml
apiServer:
  extraArgs:
    authorization-mode: Node,RBAC
# вот отсюда
    enable-admission-plugins: PodSecurityPolicy
```

4) Далее узнаем текущую версию Kubernetes

```bash
kubeadm upgrade plan
```

5) Далее на каждом из трех мастеров выполняем

```bash
kubeadm upgrade apply vX.XX.X -y
```

6) Пробуем еще раз создать хацкерский Pod

```bash
kubectl create -f hackers-pod.yaml --as=system:serviceaccount:default:user
```

В ответ должны увидеть что-то типа

```bash
Error from server (Forbidden): error when creating "hackers-pod.yaml": pods "hackers-pod" is forbidden: unable to validate against any pod security policy: [spec.securityContext.hostNetwork: Invalid value: true: Host network is not allowed to be used spec.securityContext.hostPID: Invalid value: true: Host PID is not allowed to be used spec.volumes[0]: Invalid value: "hostPath": hostPath volumes are not allowed to be used]
```

7) Чистим за собой кластер

> **Созданные PSP и RBAС НЕ удаляем!**

```bash
kubectl delete -f hackers-pod.yaml
kubectl delete serviceaccount user
kubectl delete rolebinding user
```

> Удаление pod'а вернет ошибку, если прошлая команда (как и задумано) не смогла создать Pod
