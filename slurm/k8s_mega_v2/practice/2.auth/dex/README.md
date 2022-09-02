# Аутентификация в кластере с помощью OIDC

---

## Цели практики

Целью данной практической работы является демонстрация работы
аутентификации в кластере Kubernetes с использованием OIDC.

В качестве базы данных пользователей будет использоваться Active Directory.
Active Directory уже настроен: в нем заведены все учетные записи,
учетные записи находятся в группе system:masters.

В качестве OIDC будет использоваться Dex.
`Dex` будет доступен по адресу: `auth.s<Ваш номер студента>.edu.slurm.io`.
Так же будет использоваться приложение `Gangway`,
которое является удобным `Dashboard` для генерации конфигурации `kubectl`.
Gangway будет располагаться по адресу: `kubectl.s<Ваш номер студента>.edu.slurm.io`.

Для аутентификации запросов в кластере, необходимо будет
подключиться к UI Gangway и ввести свои учетные данные.
Gangway отправляет эти учетные данные в Dex, который производит аутентификацию
учетных данных в Active Directory и в ответ возвращает: `ID token`,
который является `jwt` и содержит информацию о пользователе,
сроке жизни этого токена и так далее. Так же Dex возвращает `refresh token`,
который используется для обновления ID token. После получения этого набора
токенов Gangway генерирует список команд, которые необходимо выполнить
в консоли, чтобы настроить аутентификацию с использованием oidc tokens.

При отправке запросов в kube-api передается `ID token`.
Если ID token истек, kubectl самостоятельно его продлит используя `refresh token`.

## С чем будем работать

* `Каталог deploy` - содержит все манифесты для установки в кластер Kubernetes.
* `cert_gen.sh` - скрипт генерации сертификатов для устанавливаемых компонентов.

## Где будем выполнять практику

* Данная практика выполняется на сервере `master-1.s<Ваш номер студента>`.
* Практика выполняется под учетной записью `root`.
* Материалы для прохождения практики находятся в каталоге `megakube/2.auth/dex`. Все команды должны выполняться из этого каталога.

```
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/2.auth/dex
```

## Практика

**1. Генерация сертификатов для Dex и Gangway**

* Генерируем сертификаты

Kubernetes взаимодействует с OIDC только по HTTPS протоколу,
поэтому нам необходимо сгенерировать самоподписанный сертификат.
В реальной жизни, скорее всего, будет использоваться не самоподписной сертификат.

Потребуются следующие сертификаты:
  * `root certificate` - сертификат, которым будут подписаны все остальные сертификаты. Так же, он будет использоваться kube-api сервером для валидации сертификатов Dex.
  * `сертификат для Dex`
  * `сертификат для Gangway`

Для генерации сертификатов будет использоваться утилита `openssl`.
Для упрощение процесса генерации всех необходимых сертификатов подготовлен
скрипт. Для его запуска выполняем в консоли команду:

```bash
bash cert_gen.sh
```

В результате выполнения данного скрипта будут сгенерированы все необходимые
сертификаты, а также данные сертификаты будут загружены
в кластер Kubernetes в виде Secret. 

* Проверяем результаты

Для проверки, что скрипт отработал корректно, выполните команду:

```bash
kubectl get secret -n kube-system
```

В результате выполнения данной команды будут выведены все `Secret` для namespace
`kube-system`. В выводе должны присутствовать следующие Secret:

```bash
ca
dex-tls
gangway-tls
```

`!! Повторный запуск скрипта закончится ошибкой`, так как kubernetes не может
обновить Secret. Если необходимо пересоздать Secrets,
то необходимо удалить Secret, выполнив команду:

```bash
kubectl delete secret -n kube-system ca dex-tls gangway-tls
```

После удаления можно запускать скрипт повторно.

**2. Установка OIDC в кластер Kubernetes**

* Задаем внешние адреса для Gangway и Dex

Gangway взаимодействует с Dex по внешнему адресу, адрес указан в configmap для
Gangway, так же в Ingress манифестах задаются адреса, по которым будут
доступны Gangway и Dex. В первую очередь нам надо внести изменения
в манифесты и подставить реальные адреса, для этого выполните команду:

```bash
find ./deploy/ -type f -exec sed -i 's/<Ваш номер студента>/<ВАШ РЕАЛЬНЫЙ НОМЕР студента>/g' {} \;
```

* Создаем секрет для Gangway

Создадим секрет для Gangway, который будет содержать random строку в формате
base64, он будет использовать для генерации Cookie. Для этого выполним команду:

```bash
kubectl -n kube-system create secret generic gangway-key --from-literal=sessionkey=$(openssl rand -base64 32)
```

* Устанавливаем Dex и Gangway в кластер Kubernetes

Для установки необходимо применить в кластер все манифесты из каталога `deploy`, выполнив команду:

```bash
kubectl apply -f ./deploy -n kube-system
```

В результате в кластере Kubernetes будут созданы:
Deployment, Service, Ingress и RBAC для Dex и Gangway.

* Проверяем что все необходимые компоненты запустились

Проверяем статус всех необходимых компонентов, выполнив команду: 

```bash
kubectl get all -n kube-system -l component=oidc-auth  
```

В результате выполнения данной команды будет выведен список компонентов
с label `component: oidc-auth`. Обратите внимание - данные об Ingress выведены не будут.

Для проверки Ingress выполните команду:

```bash
kubectl get ingress -n kube-system -l component=oidc-auth
```

На экран должно быть выведена информация о двух Ingress.
В поле HOST одного должно быть указано:

```bash
auth.s<Ваш номер студента>.edu.slurm.io
```

в поле HOST второго должно быть указано:

```bash
kubectl.s<Ваш номер студента>.edu.slurm.io
```

Если значение не верное, то отредактируйте файл:
`deploy/dex-ingress.yaml` или `deploy/gangway-ingress.yaml`
и примените изменения для Ingress, выполнив команду:

```bash
kubectl apply -f deploy/dex-ingress.yaml
kubectl apply -f deploy/gangway-ingress.yaml
```

**3. Настройка kube-api сервера для аутентификации с использованием oidc**

* Копируем корневые сертификаты на master сервера

Для того, чтобы kube-api сервер мог провалидировать сертификат Dex, необходимо
корневой сертификат, которым подписан сертификат Dex, скопировать
на все мастер сервера в каталог: `/etc/ssl/certs/`.
Данный каталог монтируется в Pod с kube-api сервером.
Для копирования корневого сертификата выполните команды:

```bash
cp ssl/ca.pem /etc/ssl/certs/ca.crt
scp ssl/ca.pem master-2.s<Ваш номер студента>:/etc/ssl/certs/ca.crt
scp ssl/ca.pem master-3.s<Ваш номер студента>:/etc/ssl/certs/ca.crt
```

* Настроим kube-api сервер

По умолчанию плагин для аутентификации с использованием OIDC выключен,
для его включения необходимо внести изменения в настройки kube-api.
Настройки kube-api сервера генерируются из Сonfigmap `kubeadm-config`
каждый раз при обновлении кластера с использованием утилиты kubeadm и для того,
чтобы наши изменения не затирались при манипуляциях с кластером,
внесем изменения в Configmap.
Для это откроем Configmap на редактирование, выполнив команду:

```bash
kubectl edit configmap -n kube-system kubeadm-config
```

И добавим следующие поля, для избежания выхода кластера из строя поля
`лучше копировать, а не вводить руками`:

```bash
extraArgs:
  authorization-mode: Node,RBAC
  # вот отсюда
  oidc-ca-file: /etc/ssl/certs/ca.crt
  oidc-client-id: oidc-auth-client
  oidc-groups-claim: groups
  oidc-issuer-url: https://auth.s<Ваш номер студента>.edu.slurm.io/
  oidc-username-claim: email
```

* Теперь применим изменения поочередно для всех kube-api серверов

Для этого узнаем текущую версию Kubernetes

```bash
kubeadm upgrade plan
```

Далее на каждом из трех мастеров выполняем

```bash
kubeadm upgrade apply v1.21.4 -y
```

**4. Проверяем, что все работает**

Для проверки работы необходимо:

* Открываем в браузере kubectl.s<Ваш номер студента>.edu.slurm.io. Так как сертификаты самоподписные, необходимо воспользоваться анонимным режимом браузера. 
* Авторизуемся и получаем инструкции для настройки доступа к кластеру.

    Единственное ограничение — так как у нас все сертификаты самоподписанные, то в предоставленной инструкции по адресу kubectl.s<Ваш номер логина>.edu.slurm.io нужно убрать сертификат сервера и вместо него вписать insecure-skip-tls-verify: true
    Эту строку
    ```
    kubectl config set-cluster Slurm.io --server=https://api.s010248.edu.slurm.io:6443 --certificate-authority=ca-Slurm.io.pem --embed-certs
    ```
    Заменить на эту
    ```
    kubectl config set-cluster Slurm.io --server=https://api.s010248.edu.slurm.io:6443 --insecure-skip-tls-verify=true
    ```

**5. Обследуем настройки kubectl**

* Выводим текущие настройки для kubectl

Посмотреть настройки `kubectl` можно двумя способами:

1. В конфигурационном файле `~/.kube/config`
2. Выполнив команду:

```bash
kubectl config view
```

В настройках наиболее интересными являются поля:

* `id-token` - в данном поле содержится ID token в формате `jwt`. Содержимое токена в расшифрованном виде можно посмотреть, например, на сайте [jwt.io](https://jwt.io/).
* `refresh-token` -  в данном поле указан Refresh token, который используется для продления ID token.
* `idp-issuer-url` - в данном поле указан адрес OIDC провайдера и его `kubectl` использует для обновления ID token. При этом для продления kubectl подключается на стандартный End Point `/.well-known/openid-configuration`, который выступает службой Service Discovery и выдает информацию о других End Points.

#### Troubleshooting

* Проверяем, что все kube-api сервера работают

Наиболее распространенной ошибкой при выполнении данной практики является
ошибка при настройке kube-api сервера. Сначала необходимо убедиться,
что все kube-api сервера работают. Это можно сделать, выполнив команду:

```bash
kubectl get po -n kube-system -l component=kube-apiserver
```

Должно быть 3 Pod со STATUS `Running` и READY `1/1`.
Если это не так необходимо выполнить describe для Pod и посмотреть ошибки.

Если все kube-api запущены, проверяем настройки. Выполняем команды:

```bash
kubectl get po -o yaml -n kube-system kube-apiserver-master-1.s<Ваш номер студента>.slurm.io 
kubectl get po -o yaml -n kube-system kube-apiserver-master-2.s<Ваш номер студента>.slurm.io 
kubectl get po -o yaml -n kube-system kube-apiserver-master-3.s<Ваш номер студента>.slurm.io 
```

Если kubectl не получается выполнить команду, значит все API сервера
не доступны. Для диагностики необходимо получить логи kube-api сервера
на любом из master серверов с помощью утилиты `nerdctl` или `crictl`, выполнив команду:

```bash
nerdctl -n k8s.io logs k8s_kube-apiserver_kube-apiserver-master-1.s<TAB>
```

В логе необходимо найти ошибку и исправить ее в файле `/etc/kubernetes/manifests/kube-apiserver.yaml`
Подождав пока API сервера запустятся необходимо исправить ошибку в configmap kubeadm-config. 
Смотрим шаг 2 этой инструкции.

* Проверяем настройки kube-api серверов

Для этого получим манифесты kube-api выполняем команды:

```bash
kubectl get po -o yaml -n kube-system kube-apiserver-master-1.s<Ваш номер студента>.slurm.io 
kubectl get po -o yaml -n kube-system kube-apiserver-master-2.s<Ваш номер студента>.slurm.io 
kubectl get po -o yaml -n kube-system kube-apiserver-master-3.s<Ваш номер студента>.slurm.io 
```

Данные команды выводят манифесты (в формате yaml) для kube-api Pod. В манифестах должны присутствовать следующие строки:

```yaml
...
- --oidc-ca-file=/etc/ssl/certs/ca.crt
- --oidc-client-id=oidc-auth-client
- --oidc-groups-claim=groups
- --oidc-issuer-url=https://auth.s<Ваш номер студента>.edu.slurm.io/
- --oidc-username-claim=email
```

Если данные настройки отсутствуют во всех манифестах или
не верно указан `oidc-issuer-url`, необходимо выполнить пункты начиная с третьего.
Если отсутствуют только в некоторых,
то необходимо повторить пункт два, начиная с команды:

```bash
kubeadm upgrade plan
```

* Проверяем настройки kubectl

Проверяем адрес Dex. Для этого выполните команду:

```bash
kubectl config view | grep idp-issuer-url
```

Адрес должен быть: `idp-issuer-url: https://auth.s<Ваш номер студента>.edu.slurm.io/`.

Если адрес отличается, то необходимо его исправить в файле:
`deploy/gangway-configmap.yaml` в поле `authorizeURL`
и применить изменения в кластер выполнив команды:

```bash
kubectl apply -f deploy/gangway-configmap.yaml
kubectl delete po -n kube-system gangway-<TAB>
```

Далее необходимо выполнить настройку начиная с пункта три.

Если `idp-issuer-url` отсутствует в настройках `kubectl`, необходимо выполнить
настройку, начиная с пункта три.

#### Полезные ссылки

1. [Dex](https://github.com/dexidp/dex)
2. [Gangway](https://github.com/heptiolabs/gangway)
3. [Jwt info](https://jwt.io)
4. [k8s doc: OpenID Connect Tokens](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens)
