# Делаем бекапы с помощью Velero


> Для работы нам потребуется утилита командой строки velero, kubectl и рабочий кластер Kubernetes.
На master-1 заходим в 9.heptio_velero и копируем бинарник velero в /usr/bin

## Запускаем velero

1) Копируем утилиту velero

```bash
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/9.heptio_velero
cp velero /usr/bin/
```

2) Запускаем minio и velero:

```bash
kubectl apply -f examples/minio/00-minio-deployment.yaml

velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.1.0 \
    --bucket velero \
    --secret-file ./credentials-velero \
    --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.velero.svc:9000 \
    --snapshot-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.velero.svc:9000 \
    --velero-pod-cpu-request 0.1 --velero-pod-mem-request 128Mi \
    --use-restic --restic-pod-cpu-request 0.1 --restic-pod-mem-request 128Mi \
    --wait
```

Давайте разберемся, что же мы натворили.

Во-первых, поставили minio с логином minio и паролем minio123, причем minio будет хранить bucket'ы внутри себя, и если убить pod с minio, то все backup'ы пропадут — уже неплохо.
Далее создали секрет с теми же логином, паролем и запустили job minio-setup, в котором создали bucket velero. Сервер backup'ов не умеет самостоятельно создавать bucket'ы, и, например, при вводе его в production для работы с Amazon S3 надо самостоятельно создать bucket и юзера с ключами доступа к этому bucket'у.

В процессе установки velero создал CRD, запустил обработчик этих CRD и создал DaemonSet с Restic. На каждом узле будет запущена утилита backup'а томов, которая сможет backup'ить тома, подключенные к pod'ам на каждом из узлов. 
Restic не умеет работать с hostPath томами, но зато умеет backup'ить тома типа local.

## Делаем бекап простого приложения

3) Создаем приложение:

```bash
kubectl apply -f examples/nginx-app/base.yaml
```

Ждем пока все поднимется

```bash
kubectl get deployments -l component=velero --namespace=velero
kubectl get deployments --namespace=nginx-example
```

4) Создадим бекап всех объектов, у которых есть метка app=nginx

```bash
velero backup create nginx-backup --selector app=nginx

> Backup request "nginx-backup" submitted successfully.
> Run `velero backup describe nginx-backup` for more details.

```

На самом деле команда создала CRD-ресурс в Kubernetes, в котором описано наше требование на создание backup'а. Теперь надо дождаться, пока velero обработает этот ресурс и создаст backup. Подробности можно смотреть командой 

5) Посмотрим подробности

```bash
velero backup describe nginx-backup
```

Чтобы смотреть логи, утилите velero надо подключиться к minio. Она к нему обращается по внутри кластерному DNS имени `minio.velero.svc`, а так как мы запускаем утилиту на master сервере, у которого в resolv.conf не прописан кластерный DNS, то и velero не может подключиться к minio.

Проще всего решить эту проблему, прописав на мастере в `/etc/hosts` соответствие ip-адреса сервиса `minio.velero.svc`.
```
echo $(kubectl get svc minio --no-headers -n velero | awk '{print $3}') minio.velero.svc >>/etc/hosts
```
Смотрим логи
```
velero backup logs nginx-backup
```
В логах видно, как velero перебирает все типы объектов в кластере, и backup'ит те, у которых есть метка `app=nginx`.

6) Удалим ns

```bash
kubectl delete ns nginx-example
```

7) И восстановим в другой неймспейс:
```bash
velero restore create --from-backup nginx-backup --namespace-mappings nginx-example:nginx-restored
```

Velero сообщит, что требование на восстановление создано и предложит посмотреть подробности. Логи можно будет посмотреть только после окончания восстановления.
```
velero restore describe nginx-backup-20190728185413
```
Восстановление из backup'а — процесс не быстрый, так что в выводе `describe` можно увидеть сообщение `Phase:  InProgress`

Когда восстановление будет завершено, фаза сменится на `Phase:  Completed`

Это был простой случай backup'а манифестов по метке, теперь попробуем создать backup приложения с данными. Создадим pod с redis'ом и используем restic, чтобы backup'ить данные на нем.

### Добавим бекапы PV

8) Запустим редис и создадим в нем ключ

```bash
kubectl apply -f redis.yaml
kubectl -n red exec -it redis redis-cli
set mykey testik
get mykey
save
```

> save - чтобы редис сохранил ключ в бекапный файл на диске. Если этого не сделать, то каталог будет пустой и restic не сможет сделать его снепшот.

9) Добавим аннотацию, что этот том надо бекапить:

```bash
kubectl -n red annotate pod/redis backup.velero.io/backup-volumes=redis-storage
```

10) Создаем бекап

```bash
velero backup create redis1 --include-namespaces red
```

11) Смотрим ``describe``` и видим что там появился раздел, в котором restic рапортует, что создал backup тома с данными
```
velero backup describe redis1 --details
...
Restic Backups:
  Completed:
    red/redis: redis-storage
```
12) Восстанавливаем в другой ns

```bash
velero restore create --from-backup redis1 --namespace-mappings red:red2
```

12) Проверяем, что ключ восстановился:

```bash
kubectl -n red2 exec -it redis redis-cli
get mykey
```

13) Удаляем

```bash
kubectl delete namespace/velero clusterrolebinding/velero
kubectl delete crds -l component=velero
kubectl delete ns nginx-restored red red2
```

Аннотацию мы добавили. Потому что том у нас был типа empty dir и backup'им мы его с помощью restic.
Если в список объекта backup'а попадают pvc, то и соответствующие pv также попадают в backup.
Если velero сможет, то будет сделан snapshot. Если velero не умеет делать snapshot'ы для такого типа тома, то в pod'е, куда подключен этот том, надо указать аннотацию, чтобы backup тома был сделан с помощью restic.

С restic'ом есть небольшая проблема: название backup'а тома привязано к имени pod'а. Если pod умрет и вместо него будет запущен другой, то следующий backup тома будет делаться с нуля и pod новым именем, а не продолжит пополняться предыдущий инкрементальный backup.
