# Устанавливаем кластер с помощью Kubeadm

> :exclamation: Все работы проводим из админбокса по адресу sbox.slurm.io

### Добавляем свой публичный SSH ключ в Gitlab

> Публичный ключ пользователя root с серверов площадки для практических заданий 
> уже добавлен в gitlab

Для этого заходим в gitlab.slurm.io
В правом верхнем углу нажимаем на значок своей учетной записи.
В выпадающем меню нажимаем Settings.
Дальше в левом меню выбираем раздел SSH Keys
И в поле key вставляем свой ПУБЛИЧНЫЙ SSH ключ.

### Первый мастер

1) Из админбокса заходим по SSH на первый мастер (все работы выполняем под рутом!)

```bash
ssh master-1.s<Ваш номер логина>
sudo -i
```

> :exclamation: Обратите внимание, что во всех шаблонах
> <Ваш номер логина> подразумевает только цифры
> второе "s" добавлять не нужно

2) Клонируем репозиторий Kubernetes Мега и переходим в директорию практики

```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/1.kubeadm
```

3) Ставим, настраиваем и запускаем Containerd

```bash
yum-config-manager \
  --add-repo \
  https://download.docker.com/linux/centos/docker-ce.repo

yum install -y containerd.io-1.4.4-3.1.el7

mkdir -p /etc/containerd

cat > /etc/containerd/config.toml <<EOF
version = 2

[grpc]
  max_recv_message_size = 16777216
  max_send_message_size = 16777216

[debug]
  level = "info"

[metrics]
  address = ""
  grpc_histogram = false

[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "k8s.gcr.io/pause:3.3"
    max_container_log_line_size = -1
    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "runc"
      snapshotter = "overlayfs"
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          runtime_engine = ""
          runtime_root = ""
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            systemdCgroup = true
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["http://172.20.100.52:5000","https://mirror.gcr.io","https://registry-1.docker.io"]
EOF

systemctl enable --now containerd
```

4) Скачиваем и распаковываем утилиты crictl и nerdctl

```
curl -L https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.21.0/crictl-v1.21.0-linux-amd64.tar.gz | tar -zxf - -C /usr/bin
curl -L https://github.com/containerd/nerdctl/releases/download/v0.8.1/nerdctl-0.8.1-linux-amd64.tar.gz | tar -zxf - -C /usr/bin

cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint: unix:///var/run/containerd/containerd.sock
timeout: 30
debug: false
EOF

```

5) Настраиваем sysctl, выключаем selinux, включаем ntpd

```bash
modprobe br_netfilter
cat <<EOF > /etc/modules-load.d/br_netfilter.conf
br_netfilter
EOF

cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

sysctl --system

setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

systemctl enable --now ntpd
```

6) Ставим kubelet, kubectl и kubeadm

```bash
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

yum install -y kubelet-1.21.4-0 kubeadm-1.21.4-0 kubectl-1.21.4-0

systemctl enable --now kubelet
```

7) Правим файл с конфигурацией для kubeadm `cluster.yaml`

Меняем второй и третий октеты сети в параметре **controlPlaneEndpoint**

```yaml
controlPlaneEndpoint: 172.<xx>.<yyy>.5:6443
```

8) Создаем кластер

```bash
kubeadm init --config cluster.yaml --upload-certs --ignore-preflight-errors NumCPU | tee -a kubeadm_init.log
```

9) Копируем две строки из вывода предыдущей команды и сохраняем например в файл join.txt

> Если вы случайно затерли вывод от выполнения kubeadm init, то он, вместе с нужными строками лежит в файле kubeadm_init.log

Строки вида

```bash
kubeadm join 172.<xx>.<yyy>.5:6443 --token xxxxxxxxxxxxx \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxx \
  --control-plane --certificate-key xxxxxxxxxxxxxxxxxxxxxxxx
kubeadm join 172.<xx>.<yyy>.5:6443 --token xxxxxxxxxxxxxxxxxxxxx \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxx
```
понадобятся в следующих шагах

10) Копируем kubeconfg

```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
```

11) Ставим сетевой плагин

```bash
kubectl apply -f calico.yaml
```

12) Проверяем, что всё заработало

```bash
kubectl get node
kubectl get po -A
```

### Второй и третий мастера

13) Из админбокса заходим по SSH на второй мастер (все работы выполняем под рутом!)

```bash
ssh master-2.s<Ваш номер логина>
sudo -i
```

14) Ставим, настраиваем и запускаем Containerd

```bash
yum-config-manager \
  --add-repo \
  https://download.docker.com/linux/centos/docker-ce.repo

yum install -y containerd.io-1.4.4-3.1.el7

mkdir -p /etc/containerd

cat > /etc/containerd/config.toml <<EOF
version = 2

[grpc]
  max_recv_message_size = 16777216
  max_send_message_size = 16777216

[debug]
  level = "info"

[metrics]
  address = ""
  grpc_histogram = false

[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "k8s.gcr.io/pause:3.3"
    max_container_log_line_size = -1
    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "runc"
      snapshotter = "overlayfs"
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          runtime_engine = ""
          runtime_root = ""
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            systemdCgroup = true
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["http://172.20.100.52:5000","https://mirror.gcr.io","https://registry-1.docker.io"]
EOF

systemctl enable --now containerd
```

15) Скачиваем и распаковываем утилиты crictl и nerdctl

```
curl -L https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.21.0/crictl-v1.21.0-linux-amd64.tar.gz | tar -zxf - -C /usr/bin
curl -L https://github.com/containerd/nerdctl/releases/download/v0.8.1/nerdctl-0.8.1-linux-amd64.tar.gz | tar -zxf - -C /usr/bin

cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint: unix:///var/run/containerd/containerd.sock
timeout: 30
debug: false
EOF

```

16) Настраиваем sysctl, выключаем selinux, включаем ntpd

```bash
modprobe br_netfilter
cat <<EOF > /etc/modules-load.d/br_netfilter.conf
br_netfilter
EOF

cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

sysctl --system

setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

systemctl enable --now ntpd
```

17) Ставим kubelet, kubectl и kubeadm

```bash
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

yum install -y kubelet-1.21.4-0 kubeadm-1.21.4-0 kubectl-1.21.4-0

systemctl enable --now kubelet
```

18) Выполняем команду из сохраненного вывода kubeadm init.

Дополнительно к ней нужно добавить ключ `--ignore-preflight-errors=NumCPU`

> Нужна команда, в которой есть ключи `--control-plane` и `--certificate-key`

```bash
kubeadm join 172.<xx>.<yyy>.5:6443 --token xxxxxxxxxxxxx \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxx \
  --control-plane --certificate-key xxxxxxxxxxxxxxxxxxxxxxxx --ignore-preflight-errors=NumCPU
```

19) Повторяем всё то же самое на третьем мастере

### Ноды

> Подготавливаем всё то же самое что и для мастеров

20) Из админбокса заходим по SSH на первую ноду (все работы выполняем под рутом!)

```bash
ssh node-1.s<Ваш номер логина>
sudo -i
```

21) Ставим, настраиваем и запускаем Containerd

```bash
yum-config-manager \
  --add-repo \
  https://download.docker.com/linux/centos/docker-ce.repo

yum install -y containerd.io-1.4.4-3.1.el7

mkdir -p /etc/containerd

cat > /etc/containerd/config.toml <<EOF
version = 2

[grpc]
  max_recv_message_size = 16777216
  max_send_message_size = 16777216

[debug]
  level = "info"

[metrics]
  address = ""
  grpc_histogram = false

[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "k8s.gcr.io/pause:3.3"
    max_container_log_line_size = -1
    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "runc"
      snapshotter = "overlayfs"
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          runtime_engine = ""
          runtime_root = ""
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            systemdCgroup = true
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["http://172.20.100.52:5000","https://mirror.gcr.io","https://registry-1.docker.io"]
EOF

systemctl enable --now containerd
```

22) Скачиваем и распаковываем утилиты crictl и nerdctl

```
curl -L https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.21.0/crictl-v1.21.0-linux-amd64.tar.gz | tar -zxf - -C /usr/bin
curl -L https://github.com/containerd/nerdctl/releases/download/v0.8.1/nerdctl-0.8.1-linux-amd64.tar.gz | tar -zxf - -C /usr/bin

cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint: unix:///var/run/containerd/containerd.sock
timeout: 30
debug: false
EOF

```

23) Настраиваем sysctl, выключаем selinux, включаем ntpd

```bash
modprobe br_netfilter
cat <<EOF > /etc/modules-load.d/br_netfilter.conf
br_netfilter
EOF

cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

sysctl --system

setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

systemctl enable --now ntpd
```

24) Ставим kubelet, kubectl и kubeadm

```bash
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

yum install -y kubelet-1.21.4-0 kubeadm-1.21.4-0 kubectl-1.21.4-0

systemctl enable --now kubelet
```

25) Выполняем команду из сохраненного вывода kubeadm init.

> Нужна команда, в которой нет ключа `--control-plane`

```bash
kubeadm join 172.<xx>.<yyy>.5:6443 --token xxxxxxxxxxxxxxxxxxxxx \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxx
```

26) Повторяем все тоже самое на второй ноде

Шаги с 20 по 25

27) На первом мастере ставим на ноды лэйблы с ролью

```bash
kubectl label node node-1.s<Ваш номер логина>.slurm.io node-role.kubernetes.io/node=""
kubectl label node node-2.s<Ваш номер логина>.slurm.io node-role.kubernetes.io/node=""
```

### Установка и настройка дополнительного ПО

28) Ставим Helm

```bash
yum install -y helm
```

29) Ставим ингресс-контроллер

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade -i ingress-nginx ingress-nginx/ingress-nginx -f ingress-values.yaml --version 3.31.0 --namespace ingress-nginx --create-namespace
```

### Тюним Coredns

30) Смотрим, в чем суть проблемы с 8 запросами к DNS:

Запускаем тестовый под, заходим в него с двух консолей и смотрим на вывод tcpdump
```bash
kubectl run -t -i --rm --image centosadmin/utils test bash

tcpdump -neli eth0 port 53
```

```bash
# из второй консоли:
kubectl exec -it test -- bash
curl ya.ru
```

Возвращаемся в tcpdump и видим там 8 DNS запросов


```bash
kubectl edit configmap -n kube-system coredns
```

В открывшемся файле меняем

```bash
pods insecure
```

на

```bash
pods verified
```

и дописываем под словом ready

```bash
autopath @kubernetes
```

В итоге должно получиться

```yaml
Corefile: |
  .:53 {
      errors
      health {
         lameduck 5s
      }
      ready
      autopath @kubernetes
      kubernetes cluster.local in-addr.arpa ip6.arpa {
         pods verified
         fallthrough in-addr.arpa ip6.arpa
         ttl 30
      }
      prometheus :9153
      forward . /etc/resolv.conf
      cache 30
      loop
      reload
      loadbalance
  }
```

Сохраняем и закрываем файл

## Добавление kubectl bash completion

```bash
cp k8s_completion.sh /etc/profile.d
```

Выходим из sudo-сессии root, заходим назад, чтобы профиль перечитался.
