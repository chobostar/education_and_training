# Cilium: Up and Running — Конспект книги

> **Authors:** Nico Vibert, Filip Nikolic, James Laverack
> **Publisher:** O'Reilly Media
---

## Общая информация
- **Авторы: Нико Виберт, Филип Николич, Джеймс Лаверак (инженеры Isovalent, создатели eBPF и Cilium).**
- **Основная цель: Предоставить практическое руководство по использованию Cilium для networking, security и observability в Kubernetes.**
- **Целевая аудитория: Платформенные инженеры, сетевые архитекторы, DevOps-специалисты, уже знакомые с Kubernetes и основами IP-сетей.**
- **Версия Cilium: В книге рассматривается версия v1.18.**

## Глава 1: Why Cilium?

**Summary:** Глава объясняет, почему традиционные CNI (Flannel, Calico) на основе iptables неэффективны для динамичной среды Kubernetes. Рассказывается об истории возникновения eBPF и Cilium, его эволюции, принятии индустрией (Google, AWS, Microsoft) и ключевых сценариях использования: от базового networking до service mesh без sidecar-прокси и мультикластерной связанности.

**Key Takeaways:**
- iptables не масштабируется для тысяч сервисов в Kubernetes из-за линейного роста правил и их последовательной обработки.
- eBPF позволяет безопасно запускать пользовательский код в ядре Linux, что дает «суперсилы» для networking, security и observability.
- Cilium — это не просто CNI, а платформа, которая может заменить kube-proxy, ingress-контроллер и даже sidecar-прокси (например, Istio).
- Cilium — единственный graduated проект CNCF в категории Cloud Native Networking, что подтверждает его зрелость.
- Основные сценарии: высокопроизводительный networking, бессайдкарный service mesh, мультикластер (Cluster Mesh), прозрачное шифрование, observability через Hubble.

**Важные концепции или термины:**
- eBPF (extended Berkeley Packet Filter): Технология ядра Linux, позволяющая выполнять изолированные программы в ответ на события (например, получение пакета).
- CNI (Container Network Interface): Стандарт для настройки сети для контейнеров в Kubernetes.
- Cluster Mesh: Функция Cilium для соединения нескольких кластеров Kubernetes, обеспечивающая единую сеть и политики безопасности.
- Hubble: Система observability, построенная на основе eBPF и Cilium, предоставляющая детальную информацию о сетевых потоках.

**Практические идеи / применения:**
- Начинать можно с Cilium как простого CNI, постепенно включая observability (Hubble), затем шифрование (WireGuard/IPsec) и только потом — Cluster Mesh и service mesh.
- Использовать Cilium для замены громоздкого kube-proxy на eBPF-базовый KPR (Kube-Proxy Replacement) для повышения производительности.
- Ключевые цитаты:
- «Brendan Gregg once described it as giving Linux "superpowers", and the label has stuck.» (о eBPF)
- «Cilium is fluid. It adapts as the cloud native ecosystem evolves... You can begin with Cilium as a simple CNI and, over time, enable capabilities... as your requirements grow.»

## Глава 2: Inside Cilium

**Summary:** В главе описывается архитектура Cilium и функции каждого из его основных компонентов. Рассматривается, как Cilium Agent, Operator, CNI плагин, eBPF-программы, прокси (Envoy и DNS) и Hubble взаимодействуют друг с другом, чтобы обеспечить работу сети, политик безопасности и наблюдаемости.

**Key Takeaways:**
- Cilium Agent — главный компонент (DaemonSet), который загружает eBPF-программы в ядро и следит за состоянием Kubernetes.
- Cilium Operator отвечает за обще-кластерные задачи, такие как управление IP-адресами (IPAM) и обновление CRD.
- CNI Plugin — это лишь интерфейс между контейнерным рантаймом и Cilium Agent'ом, который выполняет ADD/DEL для подов.
- eBPF maps — это структуры данных в ядре, используемые для обмена состоянием между eBPF-программами и агентом (например, для хранения бэкендов сервисов).
- Hubble состоит из сервера (в агенте), Relay (для агрегации по кластеру), CLI и UI.

**Важные концепции или термины:**
- DaemonSet: Тип ресурса Kubernetes, обеспечивающий запуск пода на каждой ноде кластера.
- CRD (Custom Resource Definition): Механизм расширения API Kubernetes для создания собственных объектов (например, CiliumNetworkPolicy).
- CiliumEnvoyConfig (CEC): Низкоуровневый CRD для прямой конфигурации Envoy.
- Identity: Уникальный числовой идентификатор, присваиваемый Cilium группе подов с одинаковыми лейблами (используется для политик).

**Практические идеи / применения:**
- Для диагностики состояния конкретной ноды использовать kubectl exec -it -n kube-system <cilium-pod> -- cilium-dbg status.
- Для установки и обновления Cilium использовать cilium-cli, который автоматически определяет окружение.
- Для глубокого понимания трафика на L7 (HTTP/gRPC) использовать Hubble, который получает данные от Envoy.
- Ключевые цитаты:
- «The Cilium agent... loads and manages the eBPF programs and maps in the kernel... to keep the datapath state up-to-date.»
- «Hubble is not a separate sidecar; it's a subsystem built directly into Cilium's eBPF datapath.»

## Глава 3: Getting Started with Cilium

**Summary:** Практическое руководство по развертыванию Cilium в локальном кластере kind. Описываются шаги: установка CLI, создание кластера без CNI, установка Cilium (через CLI и Helm), деплой тестового приложения (nginx), применение сетевой политики L3/L7 и мониторинг трафика с помощью Hubble.

**Key Takeaways:**
- При создании кластера нужно отключать встроенный CNI (например, disableDefaultCNI: true в kind), иначе Cilium будет конфликтовать.
- Cilium можно установить через cilium install (просто) или Helm (рекомендуется для GitOps).
- По умолчанию Cilium использует VXLAN в режиме туннелирования для связи между нодами.
- CiliumNetworkPolicy (CNP) позволяет применять политики безопасности на L3/L4 и даже на L7 (HTTP методы, пути).
- Hubble дает возможность в реальном времени видеть разрешенные и заблокированные соединения, а также L7-информацию (например, HTTP 403).

**Важные концепции или термины:**
- kind (Kubernetes in Docker): Инструмент для запуска мультинодовых кластеров Kubernetes в Docker-контейнерах.
- ClusterIP: Тип сервиса Kubernetes с виртуальным IP, доступным только внутри кластера.
- Hubble Relay: Компонент, агрегирующий потоки со всех Cilium Agent'ов для получения кластерного представления.

**Практические идеи / применения:**
- Команда для проверки: cilium status --wait — следить за статусом установки.
- Тест политики: После применения L7-политики (разрешающей только GET /index.html) запрос к /50x.html возвращает 403 Forbidden, а не таймаут, что помогает отладке.
- Фильтрация Hubble: hubble observe --from-pod <pod> --http-path "/index.html" для точного поиска нужных флоу.
- Ключевые цитаты:
- «When an endpoint is selected by a network policy, it transitions to a default deny state...»
- «While enforced layer 3 rules lead to dropped packets, enforced layer 7 rules applied by Envoy return deny codes for the application protocol.»

## Глава 4: IP Address Management

**Summary:** Глава посвящена критическому выбору режима управления IP-адресами (IPAM) для подов. Рассматриваются режимы: Kubernetes Host Scope, Cluster Scope (Cluster Pool), Multi-Pool, ENI (для AWS) и CRD-backed. Обсуждается поддержка IPv4, IPv6 и dual-stack, а также компромиссы между гибкостью и сложностью каждого режима.

**Key Takeaways:**
- Kubernetes Host Scope — самый простой, но негибкий (нельзя менять размер CIDR без пересоздания кластера).
- Cluster Scope (Cluster Pool) — Cilium сам выдает подсети нодам из пула, можно задать несколько CIDR блоков, но статически.
- Multi-Pool — самый гибкий режим, позволяет назначать IP для подов из разных пулов на основе неймспейса или аннотаций, поддерживает динамическое выделение новых подсетей.
- ENI IPAM — используется в AWS EKS, выделяет IP из вторичных IP эластичных сетевых интерфейсов.
- Выбор между IPv4, IPv6 или dual-stack должен основываться на организационной стратегии и готовности инфраструктуры.

**Важные концепции или термины:**
- IPAM (IP Address Management): Процесс назначения IP-адресов подам.
- PodCIDR: Блок IP-адресов, выделенный ноде для назначения подам.
- Multi-Pool: Режим IPAM, использующий ресурс CiliumPodIPPool для гибкого выделения адресов.
- Dual-stack: Режим сети, в котором поды и сервисы получают одновременно IPv4 и IPv6 адреса.

**Практические идеи / применения:**
- В мультитенантных кластерах использовать Multi-Pool IPAM с аннотацией неймспейса ipam.cilium.io/ip-pool=<pool-name> для изоляции IP-пространств.
- Если используете AWS, включите prefix delegation для ENI режима, чтобы обойти лимит на количество IP на ноду.
- При планировании миграции на IPv6 выбирайте dual-stack как промежуточный этап.
- Ключевые цитаты:
- «Changing it later may disrupt connectivity for running workloads or may not be supported at all.» (о выборе IPAM режима)
- «Multi-Pool is the most flexible IPAM mode in Cilium... especially for multitenant clusters.»

## Глава 5: The Cilium Datapath

**Summary:** В главе объясняется, как Cilium передает пакеты между подами внутри одной ноды и между нодами. Рассматривается роль veth-pairs, eBPF-программ, attached к интерфейсам. Детально разбираются два режима межнодовой маршрутизации: native routing (с использованием BGP или статических маршрутов) и encapsulation (VXLAN или Geneve).

**Key Takeaways:**
- Внутри ноды: трафик идет через veth-пару в host namespace, где eBPF программы (cil_from_container) принимают решение о пересылке.
- Native routing требует, чтобы L3-сеть знала о PodCIDR'ах нод (через BGP или статику), но работает быстрее без оверхэда туннелирования.
- Encapsulation (overlay) — режим по умолчанию. Прячет pod-сети внутри туннелей VXLAN (порт 8472) или Geneve (порт 6081).
- В VXLAN/Geneve поле VNI используется для кодирования идентификатора (Cilium Identity) источника, что ускоряет применение политик на узле назначения.
- Netkit — новая технология, альтернатива veth, позволяющая запускать eBPF программы прямо в пространстве имен пода для повышения производительности.

**Важные концепции или термины:**
- veth pair: Виртуальный Ethernet-кабель, соединяющий два сетевых пространства имен (пода и хоста).
- Native routing: Режим, при котором Cilium полагается на таблицу маршрутизации хоста для доставки пакетов между нодами.
- VXLAN (Virtual eXtensible LAN): Протокол туннелирования L2-over-UDP, используемый для оверлейных сетей.
- Geneve (Generic Network Virtualization Encapsulation): Более гибкий протокол туннелирования, поддерживающий TLV-поля для метаданных.

**Практические идеи / применения:**
- Для просмотра прикрепленных eBPF-программ использовать bpftool net show на ноде.
- Для дампа трафика внутри туннеля использовать tcpdump -i cilium_vxlan (на ноде) или смотреть предоставленные в репозитории книги .pcap файлы.
- Выбирать native routing с BGP для on-premise сред, где вы управляете маршрутизацией, и VXLAN/Geneve для облаков, где управлять underlay-сетью нельзя.
- Ключевые цитаты:
- «Cilium attaches eBPF programs to the interfaces on the host side so that packets are inspected and forwarded as soon as they leave or enter the pod.»
- «The key benefit of encapsulation mode is that it abstracts the pod network from the underlying infrastructure.»

## Глава 6: Service Networking

**Summary:** В главе сравнивается традиционная реализация сервисов через kube-proxy (iptables) и eBPF-базовая замена от Cilium (KPR). Показано, как iptables не масштабируется при росте числа сервисов. Описаны преимущества KPR: независимость datapath от control plane, поддержка Maglev, session affinity, traffic policies. Также рассматривается LoadBalancer IPAM для присвоения внешних IP сервисам в средах без облачного контроллера.

**Key Takeaways:**
- kube-proxy на iptables имеет сложность O(n) по числу сервисов, что приводит к гигантским цепочкам правил и задержкам при обновлении.
- KPR (Kube-Proxy Replacement) использует eBPF maps (хеш-таблицы), что дает O(1) производительность независимо от числа сервисов.
- Даже при остановке Cilium Agent'а, eBPF datapath продолжает форвардить трафик, но не может обновлять бэкенды, что может привести к таймаутам при перезапуске подов.
- KPR поддерживает sessionAffinity: ClientIP и политики internalTrafficPolicy: Local, externalTrafficPolicy: Local.
- Cilium LoadBalancer IPAM позволяет назначать IP сервисам типа LoadBalancer в on-premise средах через ресурс CiliumLoadBalancerIPPool.

**Важные концепции или термины:**
- KPR (Kube-Proxy Replacement): Функция Cilium, полностью заменяющая kube-proxy на eBPF.
- Maglev: Алгоритм последовательного хеширования от Google для стабильного распределения трафика.
- LB IPAM (LoadBalancer IP Address Management): Функция Cilium Operator для выделения IP-адресов сервисам LoadBalancer.
- DNAT (Destination Network Address Translation): Изменение IP-адреса назначения (например, с ClusterIP на PodIP).

**Практические идеи / применения:**
- Проверить масштабируемость: создать 100 сервисов в кластере без Cilium и с Cilium (KPR) и сравнить число правил iptables (iptables-save | grep KUBE-SEP | wc -l).
- Для приложений, которым нужно сохранять сессии, включать sessionAffinity: ClientIP, но стараться проектировать stateless приложения.
- Для внутреннего трафика, который должен оставаться на ноде (например, логирование), использовать internalTrafficPolicy: Local.
- Ключевые цитаты:
- «Because hash table lookups and insertions are done by key instead of by matching against chains of rules, the lookup time stays the same regardless of how many services you have.»
- «The datapath itself continues to operate as long as the kernel state is intact.» (о независимости от Cilium Agent)

## Глава 7: Ingress and Gateway API

**Summary:** Глава посвящена входящему трафику. Описывается, как Cilium выступает в роли Ingress Controller'а (поддержка стандартного Ingress API) и реализует современный Gateway API. Показаны примеры маршрутизации на основе path, header'ов, query parameters, трафик-сплиттинг (канареечные развертывания), модификация хедеров и проброс gRPC. Вводится концепция GAMMA для внутренней L7-маршрутизации.

**Key Takeaways:**
- Cilium Ingress заменяет необходимость в отдельном Ingress-контроллере (например, NGINX), используя Envoy в качестве прокси.
- Gateway API — это более гибкая и ролевая модель, чем Ingress, с разделением ответственности (инфраструктура vs разработчики).
- Основные ресурсы Gateway API: GatewayClass (имя контроллера), Gateway (точка входа с listener'ами), HTTPRoute (правила маршрутизации).
- Gateway API поддерживает нативное traffic splitting (например, 99%/1% для canary), модификацию хедеров (Request/ResponseHeaderModifier) и редиректы.
- GAMMA (Gateway API for Mesh Management and Administration) позволяет использовать HTTPRoute для маршрутизации внутреннего (east-west) трафика между подами, заменяя sidecar-меши.

**Важные концепции или термины:**
- Gateway API: Стандартизированный набор ресурсов Kubernetes для управления входящим трафиком (L4-L7), наследник Ingress.
- HTTPRoute: Ресурс Gateway API для описания правил маршрутизации HTTP-трафика.
- GAMMA: Инициатива по использованию Gateway API для Service Mesh.
- Traffic Splitting / Weighted Routing: Разделение процента трафика между разными бэкендами.

**Практические идеи / применения:**
- Для A/B тестирования или canary-релиза использовать HTTPRoute с weight: 90 и weight: 10.
- Для обеспечения безопасности добавлять RequestHeaderModifier для прокидывания tenant ID или аутентификационных данных.
- Для gRPC-сервисов использовать GRPCRoute вместо HTTPRoute для более точного матчинга по методу и сервису.
- Ключевые цитаты:
- «Gateway API was created to overcome the limitations of Ingress... a more expressive, extensible model for managing ingress traffic.»
- «GAMMA... allows Gateway API to be used to manage east-west traffic, minimizing resource utilization by removing the need for a separate ingress or service mesh system.»
- *(Продолжение следует, так как книга большая. Я подготовлю конспекты для глав 8-16 и общий итог в следующем сообщении.)*
- давай следующие главы
- Продолжаю конспект книги «Cilium: Up and Running». Начинаю с главы 8.

## Глава 8: Performance Networking and Traffic Optimization

**Summary:** Глава посвящена функциям Cilium для оптимизации производительности сети. Рассматриваются механизмы уменьшения задержек и накладных расходов: топологически-осведомленная маршрутизация сервисов (Service Traffic Distribution), локальное перенаправление трафика (Local Redirect Policy), Direct Server Return для сохранения source IP, XDP для ранней обработки пакетов, алгоритм consistent hashing Maglev и технология netkit — замена устаревшим veth-парам.

**Key Takeaways:**
- Service Traffic Distribution с trafficDistribution: PreferClose (или PreferSameZone) позволяет предпочитать бэкенды в той же зоне, снижая задержки и межзональные расходы.
- Local Redirect Policy (LRP) перенаправляет трафик к сервису на локальный (нодальный) бэкенд, избегая межнодовых хопов. Идеально для NodeLocal DNS Cache.
- Direct Server Return (DSR) сохраняет исходный IP клиента и позволяет бэкенду отправлять ответ напрямую клиенту, минуя входную ноду. Требует native routing и не работает с VXLAN.
- XDP (eXpress Data Path) обрабатывает пакеты на уровне драйвера NIC до того, как они попадут в сетевой стек ядра, что идеально для DDoS-защиты и высокоскоростной фильтрации.
- Maglev — алгоритм consistent hashing, обеспечивающий попадание одного и того же 5-кортежа (источник/назначение: IP, port, protocol) на один и тот же бэкенд даже при изменении числа нод.
- Netkit — замена veth, позволяющая запускать eBPF-программы прямо в пространстве имен пода, сокращая накладные расходы на переходы между неймспейсами.

**Важные концепции или термины:**
- Service Traffic Distribution: Механизм Kubernetes для предпочтения близких (топологически) бэкендов.
- LRP (Local Redirect Policy): CRD Cilium для перенаправления трафика к локальному бэкенду (например, node-local-dns).
- DSR (Direct Server Return): Режим работы load balancer'а, при котором ответ идет напрямую клиенту, минуя балансировщик.
- Maglev: Алгоритм consistent hashing, используемый Cilium для балансировки (устойчив к изменению числа бэкендов).
- Netkit: Новый тип виртуального устройства в Linux (kernel 6.7+), оптимизированный для контейнеров.

**Практические идеи / применения:**
- В мультизонном кластере включить trafficDistribution: PreferClose на сервисах, чтобы трафик оставался в пределах availability zone и не платить за межзонный трафик.
- Использовать LRP для NodeLocal DNSCache: трафик к kube-dns перенаправляется на локальный кэш, что снижает задержки DNS на 30-50%.
- Для внешних сервисов, которым нужен реальный IP клиента (например, для логов или геотаргетинга), включить DSR вместо externalTrafficPolicy: Local.
- В высоконагруженных средах включить loadBalancer.algorithm: "maglev" для стабильности соединений при обновлениях.
- Ключевые цитаты:
- «Traffic should remain within the same zone whenever possible... to reduce interzone egress costs.»
- *«Maglev provides consistent hashing, ensuring that client connections identified by the same 5-tuple are routed to the same backend, regardless of which external node handles the request.»*
- «Early adopters have noticed significant performance improvements, with Bytedance experiencing a 10% improvement in throughput.» (о netkit)

## Глава 9: Multicluster Networking

**Summary:** Глава объясняет, как Cilium Cluster Mesh решает проблемы мультикластерной связанности. Описывается архитектура: обмен метаданными через Cluster Mesh API Server (etcd), синхронизация идентичностей и эндпоинтов. На практическом примере (три кластера: red, green, blue) показано, как настраивается mesh, TLS-доверие, глобальные сервисы (с аффинити к локальному кластеру) и кросс-кластерные network policies.

**Key Takeaways:**
- Cluster Mesh не создает единую точку отказа: каждый кластер имеет свой API Server и etcd, метаданные реплицируются между ними.
- Global services (аннотация service.cilium.io/global: "true") позволяют сервису в одном кластере иметь бэкенды в других кластерах mesh'а.
- Аффинити к локальному кластеру (service.cilium.io/affinity: local) заставляет трафик сначала пытаться попасть в локальный бэкенд, и только при его отсутствии — в удаленные.
- Кросс-кластерные политики используют лейбл io.cilium.k8s.policy.cluster для выбора эндпоинтов в конкретном удаленном кластере.
- Требования к кластерам для mesh: уникальные непересекающиеся PodCIDR, одинаковый routing mode (native/encap), L3-связность между всеми нодами.

**Важные концепции или термины:**
- Cluster Mesh: Функция Cilium для соединения нескольких кластеров Kubernetes.
- Global Service: Kubernetes сервис, бэкенды для которого собираются из всех кластеров mesh'а.
- Cluster Mesh API Server: Компонент, который читает локальный Kubernetes API и предоставляет данные (эндпоинты, идентичности) удаленным кластерам через etcd.
- KVStoreMesh: Компонент, кэширующий информацию об удаленных кластерах для локальных Cilium Agent'ов.

**Практические идеи / применения:**
- Всегда выделять уникальные непересекающиеся PodCIDR для кластеров, даже если вы пока не планируете Cluster Mesh — это упростит будущее соединение.
- Для балансировки трафика между кластерами использовать глобальные сервисы с affinity: local, чтобы предпочитать локльный датацентр/облако, но иметь fallback.
- Использовать io.cilium.k8s.policy.cluster в CiliumNetworkPolicy для ограничения доступа к сервису только из определенного кластера.
- Для автоматической генерации TLS-сертификатов между кластерами использовать метод cronJob (в книге) или единый CA.
- Ключевые цитаты:
- «Cluster Mesh is designed to avoid a single point of failure. There is no coordinator cluster or centralized control plane.»
- «The only problem is the static IPs in such policies... If only we could somehow automate that synchronization, we could make this approach much more robust. Enter FQDN policy.»
- «Our parting advice is to always pick a unique pod IP range for each cluster, even if you think you may never mesh them.»

## Глава 10: Cluster Access

**Summary:** Глава рассматривает механизмы Cilium для доступа к приложениям в кластере извне. Сравниваются два подхода: L2 Announcements (ARP/ND) для простых L2-сетей и BGP для масштабируемых L3-сетей. Показано, как настроить L2-анонсы с leader election и как работает BGP Control Plane v2 с ресурсами CiliumBGPClusterConfig, CiliumBGPPeerConfig, CiliumBGPAdvertisement.

**Key Takeaways:**
- L2 Announcements подходят для небольших сред, где все ноды в одном L2-домене. Одна нода получает "lease" на VIP и отвечает на ARP-запросы. Недостатки: нет балансировки между нодами, медленный failover (зависит от ARP cache клиентов).
- BGP — производственный стандарт. Cilium устанавливает BGP-сессии с роутерами (например, FRR) и анонсирует VIP (сервисы) через BGP.
- BGP Control Plane v2 использует три CRD: CiliumBGPClusterConfig (выбор нод и AS), CiliumBGPPeerConfig (параметры пира), CiliumBGPAdvertisement (что анонсировать: сервисы, PodCIDR).
- BGP в сочетании с ECMP на роутерах дает балансировку трафика между несколькими нодами (в отличие от L2).
- Рекомендуется анонсировать сервисы, а не PodCIDR, чтобы клиентам не нужно было знать об эфемерных IP подов.

**Важные концепции или термины:**
- L2 Announcement: Механизм, при котором Cilium отвечает на ARP-запросы для VIP, "привязывая" IP к MAC-адресу ноды.
- BGP (Border Gateway Protocol): Основной протокол динамической маршрутизации в интернете и больших сетях.
- ECMP (Equal-Cost Multi-Path): Механизм балансировки трафика по нескольким равнозначным маршрутам.
- BGP Speaker: Нода Cilium, которая устанавливает BGP-сессию с внешним роутером.
- ASN (Autonomous System Number): Уникальный номер автономной системы в BGP.

**Практические идеи / применения:**
- Для on-premise кластеров без BGP-инфраструктуры использовать L2 Announcements.
- Для production с собственными датацентрами использовать BGP Control Plane с анонсом сервисов.
- Включать Graceful Restart в CiliumBGPPeerConfig, чтобы при перезапуске Cilium Agent'а роутер не удалял маршруты немедленно.
- Использовать CiliumBGPAdvertisement с advertisementType: "Service" и service.addresses: ["LoadBalancerIP"].
- Ключевые цитаты:
- «BGP is particularly useful in production environments where high availability, fast failover, and load balancing across nodes are important requirements.»
- «With BGP enabled, Cilium selects which services to advertise using label selectors... External clients can then reach these services using standard IP routing.»
- «It is recommended to advertise services rather than pods.»

## Глава 11: Cluster Egress

**Summary:** Глава посвящена управлению исходящим трафиком из кластера. Рассматривается стандартное маскарадинг (SNAT) трафика подов за IP ноды, его настройка и режимы (iptables vs eBPF). Затем подробно разбирается Egress Gateway — функция, позволяющая назначать детерминированные egress IP для тенантов или неймспейсов. В конце рассматривается Bandwidth Manager для ограничения пропускной способности подов.

**Key Takeaways:**
- Маскарадинг по умолчанию скрывает реальный IP пода за IP ноды, что необходимо для маршрутизации ответов, но мешает идентификации источника.
- Egress Gateway позволяет назначить статический egress IP для группы подов (по лейблам или неймспейсу), которые будут видны внешним системам.
- Трафик от пода до egress gateway ноды идет внутри VXLAN-туннеля (даже в native routing режиме), чтобы сохранить идентичность источника.
- Egress Gateway не обеспечивает балансировку или failover между gateway нодами (в enterprise версии Isovalent есть HA).
- Bandwidth Manager (аннотации kubernetes.io/egress-bandwidth) позволяет ограничить исходящую пропускную способность пода, предотвращая "шумных соседей".

**Важные концепции или термины:**
- Masquerading (SNAT): Замена source IP пода на IP ноды при выходе трафика из кластера.
- Egress Gateway: Функция Cilium для маршрутизации исходящего трафика через выделенные ноды с фиксированными IP.
- CEGP (CiliumEgressGatewayPolicy): CRD для конфигурации Egress Gateway (selectors, destinationCIDRs, egressIP).
- Bandwidth Manager: Функция Cilium для rate-limiting трафика подов через eBPF (EDT — Earliest Departure Time).

**Практические идеи / применения:**
- Для мультитенантных кластеров, где внешние системы требуют аудит по source IP, использовать Egress Gateway с выделенным egress IP на тенант.
- Включать eBPF-based masquerade (bpf.masquerade=true), так как Egress Gateway зависит от него.
- Для подов, генерирующих большой трафик (например, бэкапы, стриминг), добавить аннотацию kubernetes.io/egress-bandwidth: "10M".
- Для тестирования Bandwidth Manager использовать netperf с тестом TCP_MAERTS (передача от сервера к клиенту).
- Ключевые цитаты:
- «Masquerading is necessary for connectivity in many cases, it also introduces a loss of source identity.»
- «Egress Gateway enables you to assign deterministic and predictable IP addresses to traffic leaving the cluster, based on characteristics such as pod labels and namespaces.»
- «Configuring Egress Gateway ensures that traffic leaves the cluster with a deterministic source IP, while using Bandwidth Manager prevents noisy neighbor problems.»

## Глава 12: Network Policy

**Summary:** Глава закладывает основы security в Cilium. Вводится понятие Cilium Identity, которое строится на основе лейблов подов. Объясняется, как работает policy datapath (IP cache → identity → policy map). Рассматриваются компоненты политик: endpointSelector, ingress/egress, toPorts, fromEndpoints, toEntities. Описываются reserved identities (world, host, cluster) и принципы deny-правил.

**Key Takeaways:**
- Identity — это числовой ID, общий для всех подов с одинаковым набором security labels. Он используется для принятия решений в datapath.
- Default deny: если политика выбирает endpoint, весь трафик, не разрешенный явно, блокируется.
- IP cache — eBPF-карта, отображающая IP-адрес в Identity. Работает по принципу longest prefix match (LPM).
- fromEndpoints/toEndpoints выбирают идентичности по лейблам (k8s labels). fromEntities/toEntities — предопределенные группы (world, cluster, host).
- Deny правила имеют приоритет над allow правилами.
- CiliumClusterwideNetworkPolicy действует на все неймспейсы.

**Важные концепции или термины:**
- CiliumIdentity: CRD, представляющий уникальный ID для группы подов с одинаковыми лейблами.
- IP Cache: eBPF map для быстрого разрешения IP → Identity.
- Entities: Предопределенные группы идентичностей: world (все вне кластера), cluster (все внутри кластера), host, kube-apiserver.
- Longest Prefix Match (LPM): Алгоритм выбора наиболее конкретного CIDR из ipcache.

**Практические идеи / применения:**
- Ограничивать число identity-relevant лейблов через labels в Helm, иначе каждый уникальный лейбл (например, task ID) создает новую identity и вызывает policy regeneration.
- Для политик, которые должны применяться ко всем подам кластера (например, разрешить метрики), использовать CiliumClusterwideNetworkPolicy с endpointSelector: {}.
- Для запрета доступа к API server из всех неймспейсов, кроме kube-system, использовать egressDeny с toEntities: [kube-apiserver].
- Для разрешения трафика от внешних клиентов, прошедших через Ingress, использовать fromEntities: [ingress].
- Ключевые цитаты:
- «If an endpoint is not selected by any policy, all traffic to and from that endpoint is permitted. This is known as a default allow model.»
- «Deny always takes priority over allow, no matter what.»
- *«Cilium's policy engine ascribes identity at layer 3 based on the source or destination IP address of the packet, but it uses Kubernetes's knowledge of the entire cluster to accurately and automatically map in-cluster IP addresses to concrete identities.»*

## Глава 13: Layer 7 and FQDN Policy

**Summary:** Глава углубляется в L7-политики. Объясняется, как Cilium через Envoy перехватывает HTTP/HTTPS трафик для фильтрации по методам, путям, хедерам. Вводится DNS-политика и FQDN-политика (автоматическое разрешение доменов в CIDR). Рассматривается TLS Interception — возможность расшифровывать, инспектировать и снова шифровать исходящий TLS-трафик.

**Key Takeaways:**
- L7 HTTP-политики (rules.http) позволяют фильтровать по method, path (regex), headers. Трафик перенаправляется в Envoy, что добавляет задержку, но дает детальный контроль.
- DNS-политики (rules.dns) ограничивают, какие доменные имена можно резолвить.
- FQDN-политики (toFQDNs) автоматически извлекают IP из DNS-ответов и создают временные CIDR-правила. Это позволяет разрешить доступ к cilium.io без указания IP, который может меняться.
- TLS Interception требует собственного CA, который клиент должен доверять. Cilium выступает в роли man-in-the-middle: расшифровывает трафик, инспектирует, шифрует заново.
- L7-политики дают observability (через Hubble видны URL, методы, статусы), но ценой производительности.

**Важные концепции или термины:**
- FQDN (Fully Qualified Domain Name): Полное доменное имя с точкой в конце (например, cilium.io.).
- TLS Interception: Механизм, при котором прокси (Envoy) завершает TLS-соединение от клиента, инспектирует трафик и устанавливает новое TLS-соединение к серверу.
- Trust Bundle: Набор корневых сертификатов CA, которым доверяет клиент.
- Envoy DaemonSet: Пер-нода инстанс Envoy, используемый Cilium для L7-политик и Gateway API.

**Практические идеи / применения:**
- Для ограничения egress трафика к внешним API использовать toFQDNs вместо toCIDR.
- Для sensitive-данных (API keys, токены) использовать hubble.redact.http.headers.deny, чтобы скрыть их из логов Hubble.
- При использовании TLS Interception обязательно подписывать сертификаты для конкретных доменов (cilium.io), иначе клиент получит ошибку mismatch.
- Избегать применения L7-политик к высоконагруженным сервисам, если это не критично — throughput может упасть в 2 раза (как в примере с Siege).
- Ключевые цитаты:
- *«Envoy is a high-performance layer 7 proxy... However, it can never be as fast as eBPF.»*
- «FQDN policy works much like a CIDR policy that auto-updates based on the response to the DNS request that's being proxied by the node.»
- «TLS interception isn't well suited to being a blanket policy... Instead, it's best used for targeted policy where layer 3 or layer 4 policy isn't enough.»

## Глава 14: Transparent Encryption

**Summary:** Глава описывает функцию прозрачного шифрования трафика между нодами с помощью WireGuard (и IPsec). Объясняется, как Cilium автоматически генерирует ключи, обменивается ими через аннотации CiliumNode и шифрует весь трафик между подами на разных нодах. Трафик внутри ноды не шифруется. Показано, как проверить шифрование через tcpdump.

**Key Takeaways:**
- Transparent Encryption шифрует только трафик между подами на разных нодах. Трафик внутри ноды и до внешнего мира не шифруется.
- Поддерживаются два протокола: WireGuard (рекомендуется, автоматическое управление ключами) и IPsec (больше контроля, но сложнее настройка).
- Ключи генерируются автоматически и распространяются через Kubernetes API (аннотация network.cilium.io/wg-pub-key на CiliumNode).
- При включении шифрования на существующем кластере ожидайте кратковременных сбоев (restart Cilium Agent).
- WireGuard инкапсулирует весь IP-пакет в UDP (порт 51871). Даже в native routing режиме трафик между нодами инкапсулируется.

**Важные концепции или термины:**
- Transparent Encryption: Шифрование трафика между нодами без изменения приложений.
- WireGuard: Современный, простой и высокопроизводительный VPN-протокол.
- IPsec (Internet Protocol Security): Набор протоколов для защиты IP-трафика.
- Encapsulation: Заворачивание одного пакета в другой (в данном случае оригинального pod-пакета в WireGuard-пакет).

**Практические идеи / применения:**
- Включить шифрование через Helm: encryption.enabled=true, encryption.type=wireguard.
- Проверить, что шифрование работает: на ноде запустить tcpdump -i <interface> udp port 51871 и увидеть WireGuard-трафик.
- Показать, что без шифрования можно увидеть Bearer токен в plaintext, а с шифрованием — только зашифрованные данные.
- Не ожидать шифрования для трафика к hostNetwork: true подам — он не шифруется.
- Ключевые цитаты:
- «It's called transparent because it is not visible to the pods on each end and requires no coordination from the workloads themselves.»
- «Cilium does not encrypt traffic between pods on the same node... it would encrypt traffic only to immediately decrypt it again, so it would provide no benefit.»
- «The security of the WireGuard encryption is predicated on the security of the Kubernetes API plane.»

## Глава 15: Observability with Hubble

**Summary:** Глава подробно описывает Hubble — систему observability Cilium. Рассматривается архитектура: Hubble Agent (в Cilium Agent), Hubble Relay (агрегатор), Hubble CLI и UI. Показано, как использовать Hubble для отладки (например, просмотр DROPPED пакетов из-за политик), L7-observability (HTTP методы, статусы, DNS), redaction sensitive data и экспорт метрик в Prometheus.

**Key Takeaways:**
- Hubble Agent работает на каждой ноде и собирает flow events из eBPF. Hubble Relay агрегирует их в кластерный вид.
- L7-observability требует наличия L7-политики (даже пустой rules: http: - {}), чтобы трафик пошел через Envoy.
- Hubble CLI (hubble observe) поддерживает мощные фильтры: -t drop, --from-pod, --http-path, -o json.
- Flow redaction (hubble.redact.http.headers.deny) позволяет скрыть sensitive хедеры (Authorization, Cookie) из логов.
- Hubble Exporter может писать flow logs в файл для интеграции с Loki, Splunk и др.
- Prometheus метрики Hubble включают hubble_flows_processed_total, hubble_drop_total, hubble_http_requests_total.

**Важные концепции или термины:**
- Hubble Relay: Компонент, агрегирующий потоки со всех нод.
- Hubble UI: Веб-интерфейс для визуализации сервис-мапы.
- Flow redaction: Функция для удаления чувствительных данных из flow-логов.
- Hubble Exporter: Компонент для записи flow-логов в файл.

**Практические идеи / применения:**
- При отладке политик использовать hubble observe -t drop и смотреть drop_reason_desc.
- Для анализа зависимостей использовать Hubble UI: видно, какой сервис к какому обращается.
- Для интеграции с Prometheus включить hubble.metrics.enabled с нужными контекстами (sourceContext, destinationContext).
- Скрывать Authorization header: добавить в Helm hubble.redact.http.headers.deny=[Authorization].
- Ключевые цитаты:
- «Hubble is built on top of Cilium and eBPF, providing deep visibility into how applications communicate and behave.»
- «Avoid the temptation to blindly allow every dropped connection you see... Each policy should be deliberate.»
- «L7 visibility is not a complete security solution — it's just one layer of observability that can help you understand a significant portion of traffic patterns.»

## Глава 16: Operations

**Summary:** Заключительная глава посвящена production-операциям. Рассматриваются стратегии установки (Helm vs CLI, GitOps), обновления (preflight, влияние на dataplane), миграция с других CNI. Даются рекомендации по мониторингу (Prometheus, Grafana), диагностике (cilium status, cilium connectivity test, cilium sysdump). Обсуждаются operational аспекты L2 Announcements (leader election, ARP) и BGP (graceful restart, анонс сервисов vs pod CIDR).

**Key Takeaways:**
- Helm + GitOps (ArgoCD/Flux) предпочтительнее Cilium CLI для production.
- Перед обновлением Cilium запускать preflight для предварительной загрузки образов.
- При обновлении Cilium Agent'а dataplane продолжает работать, но не обновляется — stale backends могут вызывать таймауты.
- Cilium connectivity test — лучший способ проверить работоспособность после изменений.
- Для диагностики использовать cilium status, cilium-health status, cilium sysdump.
- В BGP включать Graceful Restart, чтобы при перезапуске Agent'а роутер не удалял маршруты.

**Важные концепции или термины:**
- GitOps: Подход к управлению инфраструктурой через Git-репозиторий как источник истины.
- Preflight: Компонент Cilium для предварительной загрузки образов перед обновлением.
- Cilium connectivity test: Встроенный тест для проверки сети, политик, DNS.
- Graceful Restart: Механизм BGP, позволяющий не удалять маршруты при кратковременном разрыве сессии.

**Практические идеи / применения:**
- Не использовать Cilium CLI для установки в production — только Helm.
- Включить l2announcements.leaseDuration на уровне, соответствующем вашей сети (не меньше RTT до API server).
- При миграции с Calico/Flannel использовать гибридный режим (Cilium с отдельным PodCIDR и overlay).
- Регулярно запускать cilium connectivity test в CI/CD пайплайнах.
- Ключевые цитаты:
- «We generally prefer Helm [over Cilium CLI]... because the Cilium CLI is difficult to operate at scale.»
- «The same is not true for layer 7 functionality... If these components are unavailable, problems may occur.»
- «The datapath continues to forward traffic without the Cilium agent, giving operators resiliency during upgrades or restarts. But until the agent resumes, eBPF maps remain stale.»

## Общий итог (Overall Summary)

Книга «Cilium: Up and Running» представляет собой исчерпывающее руководство по современной платформе для networking, security и observability в Kubernetes. Авторы последовательно ведут читателя от ответа на вопрос «Почему Cilium?» через архитектуру и установку к глубокому погружению в ключевые компоненты: IPAM, datapath, сервисы, Ingress/Gateway API, производительность, мультикластер, доступ в кластер, egress, политики безопасности, прозрачное шифрование и observability с Hubble.

Главная идея книги: Cilium — это не просто CNI, а универсальная платформа, которая использует возможности eBPF для замены множества разрозненных инструментов (kube-proxy, sidecar-прокси, ingress-контроллеров, external load balancers) одним связным и высокопроизводительным решением. Книга подчеркивает важность правильного выбора IPAM режима, понимания datapath (native vs overlay), грамотного применения L7-политик (с учетом их влияния на производительность), использования Hubble для отладки и мониторинга, а также ответственного подхода к production-операциям (GitOps, graceful upgrades, BGP для L3-доступа).

## 10 главных идей всей книги
- eBPF — это фундамент. Cilium использует eBPF для перехвата и обработки пакетов в ядре, что дает линейную масштабируемость и производительность, недостижимую для решений на основе iptables.
- Kube-Proxy Replacement (KPR) — must-have. Замена kube-proxy на eBPF-базовый KPR устраняет узкие места iptables, обеспечивает стабильность соединений (Maglev) и независимость dataplane от control plane.
- Выбор IPAM режима критичен. Multi-Pool IPAM — самый гибкий режим для production, позволяющий назначать IP из разных пулов разным неймспейсам. Изменить режим после развертывания кластера крайне сложно.
- Native routing vs Overlay. Native routing (с BGP) дает лучшую производительность, но требует маршрутизации PodCIDR в underlay сети. VXLAN/Geneve overlay проще, но добавляет overhead.
- Gateway API заменяет Ingress. Gateway API предлагает более гибкую, ролевую модель для входящего трафика с поддержкой traffic splitting, модификации хедеров, gRPC и (через GAMMA) даже east-west маршрутизации.
- Безопасность через идентичность. Cilium строит политики не на IP, а на лейблах (Identity). Это позволяет применять fromEndpoints и fromEntities, абстрагируясь от эфемерных IP подов.
- L7-политики и FQDN. L7-политики дают контроль над HTTP-методами и путями, а FQDN-политики автоматически разрешают доменные имена в CIDR, решая проблему динамических IP (CDN, cloud APIs).
- Hubble — observability из коробки. Hubble предоставляет детальную информацию о потоках, политиках (DROP verdicts) и L7-данных (HTTP status, latency), что критически важно для отладки и построения zero-trust модели.
- Cluster Mesh для мультикластера. Cilium Cluster Mesh объединяет кластеры на уровне идентичности и сервисов, позволяя глобальным сервисам иметь бэкенды в разных кластерах с прозрачным failover.
- GitOps и плановые обновления. В production Cilium должен управляться через Helm и GitOps (ArgoCD/Flux). Обновления требуют preflight-проверок и понимания, что L7-компоненты (Envoy, DNS proxy) могут вызвать кратковременные разрывы соединений
