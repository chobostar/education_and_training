# Operator in Kubernetes cluster

---

#### Цели практики

Целью данной практической работы является демонстрация работы Operator, созданного с использованием Operator SDK и Ansible. В процессе выполнения практической работы в кластере будут установлены:  `Team Operator`  и  `Custom Resource Defenition`  с именем  `Team`. Данный Operator отслеживает появления в кластере объектов типа Team(custom resource), при появлении объекта данного типа, Operator создает namespaces описанные в манифесте объекта Team и устанавливает limits и requests на данные namespaces. Limits и requests задаются так же в описание объекта типа Team.

#### С чем будем работать

* В `каталоге operator/deploy` содержатся все манифесты, которые необходимо применить в процессе практики.
* В `каталоге operator/roles` находится роль Ansible, которая выполняет Operator при появлении в кластере custom resource Team.
* `operator/build/Dockerfile`, который используется для сборки образа Operator.
* В `каталоге operator/molecule` содержится набор тестов для роли Ansible.
* Файл `watches.yaml` содержит описание объектов, появление которых отслеживает Operator и описания ролей, которые необходимо запускать.
Ansible Role и Dockerfile для прохождения практики не потребуются и приведены для ознакомления.

#### Где будем выполнять практику

* Данная практика выполняется на сервере `master-1.s<Ваш номер студента>`.
* Практика выполняется под учетной записью `root`.
* Материалы для прохождения практики находятся в каталоге `megakube/5.controllers-and-operators`. Все команды должны выполняться из этого каталога.

```
cd ~
git clone git@gitlab.slurm.io:edu/megakube.git
cd ~/megakube/5.controllers-and-operators
```

#### Практика

**1. Установка Team Operator в кластер Kubernetes**

Установку Operator будет производиться в неймспейс `kube-system` и может быть выполнена в одну команду, но для большей наглядности разделим его на несколько шагов.

* Установка в кластер RBAC и Service Account

Operator взаимодействует с kube-api и для аутентификации и авторизации используются RBAC и Service Account. Первым шагом применим манифесты в которых описаны все необходимые RBAC и Serice Account. Для этого выполним команду:

```bash
kubectl apply -f operator/deploy/role.yaml -f operator/deploy/service_account.yaml -f operator/deploy/role_binding.yaml -n kube-system
```

* Создаем Custom Resource Definition 

Следующим шагом создадим CRD, для этого выполним команду:

```bash
kubectl apply -f operator/deploy/crds/ops_v1beta1_team_crd.yaml -n kube-system
```

* Устанавливаем Operator

Последним шагом установим в кластер Operator. Для установки будем использовать уже готовый образ и подготовленный манифест, который необходимо применить в кластер, выполнив команду:

```bash
kubectl apply -f operator/deploy/operator.yaml -n kube-system
```

* Проверка, что оператор установился

Для проверки оператора, проверим что Pod с Operator запустился. Для этого выполним команду: 

```bash
kubectl get po -n kube-system -l name=team-operator
```

В выводе должен быть 1 Pod со STATUS `Running` и READY `1/1`. Если это не так, необходимо выполнить describe для Pod и посмотреть ошибки.

**2. Проверка работы Team Operator**

Для проверки работы Team Operator создадим custom resource в котором будет описано 2 namespace: `stage` и `qa`. Для этого необходимо применить в кластер заранее подготовленный манифест, выполнив команду:

```bash
kubectl apply -f operator/deploy/crds/ops_v1beta1_team_cr.yaml
```

Последним шагом проверим, что оператор отработал корректно. В результате должно было создаться 2 namespace. Для проверки необходимо выполнить команду:

```bash
kubectl get ns
```
В результате выполнения команды на экран будет выведен список всех namespaces, в этом списке должны присутствовать namespaces с именами: `qa` и `stage`.

Теперь проверим, что на данные namespace выставлены limits и requests. Для этого выполним команды:

```bash
kubectl describe ns example-team-qa
kubectl describe ns example-team-stage
```

В результате выполнения данных команд, на экран будут выведены описания для указанных namespaces, в частности данные по limits и requests.

#### Troubleshooting

* Проверяем, что Operator установлен в кластер

Для проверки оператора, проверим что Pod с Operator запустился. Для этого выполним команду: 

```bash
kubectl get po -n kube-system -l name=team-operator
```

Должно быть 1 Pod со STATUS `Running` и READY `1/1`. Если это не так, необходимо выполнить describe для Pod и посмотреть ошибки.

* Проверяем, что в кластере установлен custom resource definition

Выполним команду:

```bash
kubectl get crd teams.ops.southbridge.io
```

#### Полезные ссылки

1. [k8s doc: Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
2. [GitHub: Operator SDK](https://github.com/operator-framework/operator-sdk)
3. [Ansible Operator Base](https://indico.cern.ch/event/829468/attachments/1936132/3210643/Ansible_Operator_CERN_2019.pdf)
