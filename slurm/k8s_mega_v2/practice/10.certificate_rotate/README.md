# Тестируем продление сертификатов в кластере

## !! Заходим в двух терминалах на sbox.slurm.io и далее будем работать на двух серверах:
## !! kube.s<номер студента>
## !! node.s<номер студента>

Будут созданы два сервера kube.s<номер студента> и node.s<номер студента>.

С помощью kubeadm установите на них кластер kubernetes из одного master-узла с control plane и одного рабочего узла. Можно воспользоваться инструкцией из первой практики.

>    Внимание! При установке используйте файл cluster.yml из каталога практики 10.certificate_rotate.
    После установки кластера из одного мастер узла и одного рабочего можно приступать к выполнению практики.


1) Заходим на kube (мастер)

```bash
ssh kube.s<номер студента>
sudo -s
```

2) Во втором терминале заходим на node (рабочий узел)

```bash
ssh node.s<номер студента>
sudo -s
```

3) Запускаем тестовый под

```bash
kubectl run red --image redis
```

### Исследуем сертификаты с помощью kubeadm

4) Проверяем срок действия сертификатов на kube

```bash
kubeadm certs check-expiration
```

Видим красивую табличку со сроками действия сертификатов control plane, тут нет только сертификата для kubelet
Версия 1.18 уже показывает длительность действия корневых сертификатов, а сертификат kubelet на мастере теперь обновляется автоматически.


### Примерно тоже самое можно посмотреть с помощью скрипта shcert

5) Клонируем репозиторий slurm и копируем скрипт shcert

```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/10.certificate_rotate/
cp shcert /usr/bin
scp shcert root@node.s<номер студента>:/usr/bin
```

6) Заходим в /etc/kubernetes/pki и смотрим на сертификаты:

```bash
cd /etc/kubernetes/pki

# 10 лет
shcert ca.crt

# 1 год
shcert apiserver.crt
```

7) Смотрим на сертификат kubelet

```bash
shcert /var/lib/kubelet/pki/kubelet-client-current.pem
```

8) Смотри на сертификат администратора из конфигурации доступа в кластер

```bash
shcert /etc/kubernetes/admin.conf
```

### Обновляем сертификаты

9) Выключаем ntp на мастере и на node

```bash
systemctl disable --now ntpd
```

10) Устанавливаем дату чуть меньше, чем на год вперед. На master и node

```bash
date -s 20220501
```

11) Смотрим сколько дней осталось жить сертификатам

```bash
kubeadm certs check-expiration
```

### Обновляем сертификат kubelet на node

На всех узлах сертификаты обновляются автоматически
Проверяем как работаете ротация сертификатов на узле на kube и node

12) Выполняем на node

```bash
systemctl restart kubelet
shcert /var/lib/kubelet/pki/kubelet-client-current.pem
```

13) Смотрим в логи

```bash
grep rotat /var/log/kubernetes.log
```

### Обновляем сертификаты на мастере

Возвращаемся на узел kube, где запущен control plane и тут также сначала рестартим kubelet

14) Выполняем на kube

```bash
systemctl restart kubelet
shcert /var/lib/kubelet/pki/kubelet-client-current.pem
```

15) Обновление сертификатов в /etc/kubernetes/pki

```bash
kubeadm certs renew all
```

16) Проверяем, что все сертификаты продлились

```bash
kubeadm certs check-expiration
shcert /etc/kubernetes/pki/apiserver.crt
```

Начиная с версии 1.18 API сервер научили перечитывать свой сертификат с диска при его обновлении.
И теперь можно ничего не перегружать, оно само.


> Если у вас версия k8s меньше 1.18
> Если в файле kubelet.conf лежит не ссылка на файл, а сертификат, закодированный в base64
> То можно посмотреть пример команды для обновления сертификата в файле update.user.cert
> А можно изменить на /var/lib/kubelet/pki/kubelet-client-current.pem, точно так же как на рабочих узлах.


### Перемещаемся еще на месяц в будущее и проверяем работу кластера

17) устанавливаем дату на август на kube и node

```bash
date -s 20220701
```

18) Чтобы заработал kubectl необходимо скопировать обновленный конфиг на kube:

```bash
cp /etc/kubernetes/admin.conf ~/.kube/config
```

19) Все должно работать

```bash
kubectl get node
kubectl get pod -A
```

Не забыть проверить что с сертификатами метрик, они должны быть актуальными:

```
# Cert from controller manager
echo -n | openssl s_client -connect localhost:10257 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -text -noout | grep Not

# Cert from scheduler
echo -n | openssl s_client -connect localhost:10259 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -text -noout | grep Not
```
