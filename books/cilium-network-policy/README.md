# Конспект: "Kubernetes Network Policies Done the Right Way"

## Основные инсайты

### Ключевые вызовы для enterprise-организаций
- **Баланс безопасности и гибкости**: Как внедрить строгие security guardrails без торможения инноваций
- **Адаптация к постоянным изменениям**: Поддержка новых сервисов без создания policy blind spots
- **Управление сложностью на масштабе**: Обеспечение консистентного policy enforcement без операционных узких мест
- **Доказательство соответствия**: Демонстрация compliance с GDPR, PCI-DSS, HIPAA
- **Быстрое реагирование на угрозы**: Оперативное выявление и ответ на security incidents

### Революционная технология eBPF
- **Беспрецедентная производительность**: Работа на уровне ядра Linux без изменения kernel source code
- **Прозрачность**: Не требует изменений в приложениях
- **Универсальность**: Поддержка как cloud-native, так и legacy workloads

## Важные части

### Network Policies: основы
Network policies в Kubernetes контролируют трафик между pods, services и внешними объектами на уровнях 3-4 OSI:
- **Pod communication**: Спецификация разрешенного взаимодействия между pods
- **Namespace controls**: Правила на уровне namespace для изоляции
- **IP block rules**: Политики на основе IP ranges для внешнего трафика

Важно:
- Политики применяются к Pod’ам, а не к объекту Service как таковому


### Архитектура безопасности Cilium
**Identity-based security вместо IP-based**:
- Cilium присваивает security identity группам pods с одинаковыми labels
- Identity прикрепляется к network packets и валидируется на принимающем узле
- Устраняет необходимость постоянных обновлений firewall rules

Дополнительно:
- Cilium расширяет модель Kubernetes L3/L4 до L7 (например, HTTP/DNS политики), сохраняя совместимость с базовыми NetworkPolicy


### Четыре типа сетевых рисков в Kubernetes
1. **Cluster Ingress Exposure**: Сервисы, доступные из интернета
2. **Cluster Egress Exposure**: Возможность инициировать соединения в интернет
3. **Intra-Cluster Lateral Movement**: Движение внутри кластера (Kubernetes разрешает весь трафик по умолчанию)
4. **Cluster Egress Lateral Movement**: Доступ к VMs, bare metal серверам, cloud metadata, API серверу

## Подводные камни и нюансы

### Default Deny: двойственный подход
**Преимущества**:
- Максимальная безопасность
- Требует явного разрешения всего необходимого трафика

**Риски**:
- Высокий риск misconfiguration
- Может привести к application downtime
- Создает фрикцию для development teams
- **НЕ рекомендуется для brownfield deployments**

### Policy Audit Mode
```bash
--policy-audit-mode=true
```
- Позволяет аудит без блокировки трафика
- **НЕ для production использования**
- Полезен для понимания traffic patterns перед применением политик

### Проблема overfitting
- Прямое преобразование observed flows в policies приводит к операционной сложности
- Динамические IP addresses и ports усложняют управление
- Частые обновления приложений требуют постоянной корректировки policies
- **Решение**: Начинать с coarse-grained policies на уровне namespace

Дополнительные уточнения:
- Политики — аддитивны: несколько разрешающих правил суммируются; явных “deny” в базовом Kubernetes нет (они у Cilium есть как расширение).
- При проектировании избегайте overfitting: группируйте по стабильным признакам (labels, namespace roles), а не по мимолётным портам/IP.
- Для egress на внешние ресурсы предпочтительнее использовать FQDN/DNS-политики Cilium (если он используется), чем статические IP, чтобы уменьшить хрупкость


## Трейд-оффы

### Monitor First vs Apply Policies Later
**Monitor First подход**:
- ✅ Снижает риск misconfiguration
- ✅ Позволяет понять traffic patterns
- ✅ Подходит для evolving applications
- ❌ Оставляет систему временно незащищенной

**Immediate Policy Application**:
- ✅ Немедленная защита
- ❌ Высокий риск блокировки legitimate traffic
- ❌ Требует глубокого понимания application dependencies

### Granularity vs Operability
**Fine-grained policies**:
- ✅ Максимальная безопасность
- ✅ Принцип least privilege
- ❌ Сложность управления
- ❌ Частые updates при изменениях приложений

**Coarse-grained policies**:
- ✅ Простота управления
- ✅ Меньше friction для developers
- ❌ Больший blast radius при compromise

## Конкретные рецепты и Best Practices

### Стратегия внедрения Coarse-Grained Network Policies

Практические советы:
- Начните с coarse‑grained: default‑deny + DNS + пара меж‑namespace разрешений.
- Постепенно сужайте: заменяйте podSelector: {} на role‑based метки (app, tier, role), ограничивайте порты.
- Документируйте назначение каждого потока между namespace, чтобы не появлялись “скрытые” зависимости.

#### Шаг 1: Intra-Namespace Communication
```yaml
# Разрешить весь трафик внутри namespace
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-all-traffic-within-namespace
  namespace: microservices-demo
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - {}
  egress:
  - toEndpoints:
    - {}
```

#### Шаг 2: Intra-Cluster Traffic
```yaml
# Разрешить egress только к kube-dns (TCP/UDP 53) для всех Pod'ов вне kube-system; разрешены любые DNS-запросы
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: intercept-all-dns
spec:
  endpointSelector:
    matchExpressions:
      - key: "io.kubernetes.pod.namespace"
        operator: "NotIn"
        values:
        - "kube-system"
  enableDefaultDeny:
    egress: false
    ingress: false
  egress:
    - toEndpoints:
        - matchLabels:
            io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
          - port: "53"
            protocol: TCP
          - port: "53"
            protocol: UDP
          rules:
            dns:
              - matchPattern: "*"
```
`enableDefaultDeny` - If this field is disabled, the rule will be applied without placing the endpoint into default-deny mode


#### Шаг 3: External Access
**Ingress**: Использовать LoadBalancer, NodePort, или Ingress с ограничением source scope
**Egress**: Ограничить destinations используя IP, CIDR prefixes, или FQDN

#### Шаг 4: Layer 7 Enhancement
```yaml
# HTTP method и path filtering
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: frontend-to-backend-l7
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/api/v1/products"
```

### Приоритизация Namespaces
Критерии для определения приоритета:
1. **Security Sensitivity**: Приложения с sensitive data
2. **Mission-criticality**: Критически важные для бизнеса сервисы
3. **Exposure Level**: Текущий уровень внешнего exposure
4. **Connectivity Needs**: Соотношение необходимых и фактических connections

### Cluster Wide Network Policies
Типичные правила для cluster-wide политик:
1. **Allow Within Namespace**: Разрешить весь ingress/egress внутри namespace
2. **Egress to External Services**: Доступ к shared services (kube-dns, Prometheus)
3. **Ingress to Internal Services**: Controlled external access через LoadBalancer/Gateway
4. **Default Deny**: Explicit denial для unauthorized traffic
5. **Embargo destinations**: Блокировка specific IP addresses/countries

### Measuring Risk: конкретные метрики
```bash
# Ключевые метрики для приоритизации
- Количество сервисов через NodePort, LoadBalancer, ExternalIP
- Количество сервисов через Ingress/Gateway API  
- Количество сервисов, доступных из других Namespaces
- Количество сервисов с доступом к External Networks/Internet
```

### Hubble Commands для мониторинга
```bash
# Мониторинг flows в specific namespace
hubble observe -n microservices-demo

# Проверка policy verdicts
hubble observe flows -t policy-verdict --last 1

# Мониторинг denied traffic
hubble observe --verdict DENIED
```

### Anti-patterns (чего избегать)
1. **Не создавать pair-wise rules** для каждого networking flow
2. **Не применять default deny** на brownfield deployments без предварительного анализа
3. **Не игнорировать infrastructure dependencies** (DNS, monitoring, logging)
4. **Не полагаться только на IP-based filtering** в динамических средах
5. **Не пренебрегать observability** - всегда мониторить traffic patterns

### Рекомендуемый workflow внедрения
1. **Deploy Cilium** с включенным Hubble
2. **Monitor traffic** в течение репрезентативного периода
3. **Analyze patterns** используя Hubble UI/CLI
4. **Start with coarse-grained policies** на namespace level
5. **Gradually refine** к более specific rules
6. **Implement cluster-wide policies** для shared infrastructure
7. **Continuous monitoring** и refinement

Этот подход обеспечивает balance между безопасностью и операционной эффективностью, минимизируя риски disruption при максимизации security posture.