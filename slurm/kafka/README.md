Главное отличие Kafka от сервисов очередей (например RabbitMQ или Amazon SQS):
- сообщения в Kafka не удаляются по мере их обработки консьюмерами;
- одни и те же сообщения могут быть обработаны сколько угодно раз, в том числе несколькими сервисами одновременно.

Структура данных:
- Key: "Alice"
- Value: "Registered on out website"
- Timestamp: "Jun. 25 20220 at 02:06 p"
- Headers: [{"X-Generated-By": "web-host-12.eu-west2.slurm.io"}]

Хрнятся в именованный топиках. Топик состоит 1 или из нескольких партиций. 
Сообщение я с одинаковыми ключами (Key) записываются в одну и ту же партицию - Murmurhash. Если ключ отсутствует - RoundRobin.

Кафка гарантирует очередност записи и чтения в рамках одной партиции. Данные записываются согласно replication factor.

У каждой партиции есть 1 брокер лидер, который принимает запись и отдает. У лидера может быть 0..N фолловеров, которые хранят реплики.
Сообщения всегда отправляются лиедру и, в общем случае, читаются с лидера.

Каждому записанному сообщению назнчается offset - уникальный, монотонно возращающий 64-bit unsigned int. Сообщение записывается в голову лога.

Данные не удаляются просле прочитывания. Удаляются согласно заданной конфигурации retension-a:
- retension.ms - минимальное время хранения сообщений
- retension.bytes - максимальный размер партиции

Длительность хранения не влияет на производительность Kafka.

Consumer Groups (CG)
- могут читать из нескольких топиков
- можно добавлять нескольких консумеров в группу при этом чтение из партиций распределятся
- идеально - количество партиций == количество консумеров
- если консумеров внутри группы > количество партиций, то он не будет читать вообще

внутри CG партиции назначаются уникально, чтобы избежать повторной обработки.

партиции - инструмент масштабирования

если какой-то консумер упадет - партиции распределятся между оставшимися консумерами в этой CG




Партиции можно добавлять в любой момент (консумера автоматически перераспределятся), но:
- нужно помнить про гарантию очередности в рамках одной партиции
  - если вы пишите сообщения с ключами и хэшируете номер партиции или номер сообщения исходя из общего числа, то при добавлении новой партиции вы можете сломать порядок этой записи 
- индивидуальные партиции нельзя удалить после создания

Нужно помниьт про конфигурацию auto.offset.reset в консьюмерах: при добавлении новой партии "на проде"
вы наверняка захотите прочитать данные с начала лога (auto.offset.reset=earliest). 
Иначе есть шанс потерять/не прочитать данные которые записались в новую партицию, 
до того как консумеры обновлять метаданные по топику и начнуть читать данные из этой партиции.

[!] Партиции не бесплатны:
- Каждая увеличивает время старта брокера и выбора лидеров после падения. Теоретический лимит на кластер 200k партиций для Kafka 2.0+

Можно добавлять разные CG на один и тот же топик.

Консумер делает commit offset-a с указаем:
- топика
- идентификатора партиции
- своей группы
- и оффсета

Брокер сохраняет это в своем топике __consumer_offsets, при рестарте консумера, тот запрашивает у брокера последний закоммиченный оффсет.

Если требуется пропустить ошибочное сообщение - https://en.wikipedia.org/wiki/Dead_letter_queue

Zookeepeer - распределенное хранилище, клиенты кафки напрямую к нему не соединяются

Broker controller - брокер отвечающий за выбор лидера партиции, знает в каком состоянии находятся лидеры партиций и их реплики


Basic console commands

Создаем топик с регистрациями:
```
./bin/kafka-topics.sh --create --topic registrations --bootstrap-server localhost:9092
```

Посмотрим на его конфигурацию:
```
./bin/kafka-topics.sh --describe --topic registrations --bootstrap-server localhost:9092
```
Давайте запишем первое сообщение
```
./bin/kafka-console-producer.sh --topic registrations --bootstrap-server localhost:9092
>Hello world!
>Hello Slurm!
```

читать с `auto.offset.reset=earliest` или `--from-beginning`
```
./bin/kafka-console-consumer.sh --topic registrations --bootstrap-server localhost:9092 --consumer-property auto.offset.reset=earliest
```

можно задавать имя CG явно:
```
./bin/kafka-console-consumer.sh --topic registrations --group slurm --bootstrap-server localhost:9092 --consumer-property auto.offset.reset=earliest
```

посмотреть конфиги CG:
```
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group slurm --describe
```
резетнуть:
```
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group slurm --to-earliest --reset-offsets --execute --topic registrations
```
отключить авто-коммиты:
```
./bin/kafka-console-consumer.sh --topic registrations --bootstrap-server localhost:9092 --group slurm --consumer-property auto.offset.reset=earliest --consumer-property enable.auto.commit=false
```
alter topics:
```
./bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name registrations --alter --add-config retention.ms=60000
```

Кафка удаляет данные посегментно - проверят diff от максимального timestamp (если retension.ms указан). 
Может быть такое, что данные пишутся часто и пока rollup сегмента не случится в сегменте diff будет < retension.ms. 

Настройки rollup-a:
- segment.ms - период роллапа сегмента после открытия (default: 1 weak)
- segment.bytes - максимальный размер сегмента (default: 1GB)

Большая часть настроек Кафки может быть определена на 2-х уровнях:
- broker-level config - уровень сервеа, используется по-умолчанию (часто имеют префикс log.*)
- topic-level config - оверрайды для отдельных топиков, имеют более высокий приоритет

Полный перечень настроек здесь:
https://kafka.apache.org/documentation/#configuration

По-умолчанию, логи хранятся тут:
```
cd /tmp/kafka-logs/registrations-0/
```

Log Compaction - еще один механизм удаления. использует ключи сообщений, чтобы решить удалять или нет.
- cleanup.policy - delete для ретеншена по времени/размеру (включен по-умолчанию), compact для включения compaction

Довольно **трудоемкий** процесс, нагружает память, процессор и диск. 

**Не атомарен** - внутри партиции по-прежнему могут одновременно находиться несколько записей с одинаковым ключом.

**Оффсеты не меняются**, порядок записей остается прежним

Позволяет **"удалять" записи по ключу**, хорошо подходит для снэпшоттинга и восстановления последнего состояния системы после падения/перезагрузки

---
Все брокеры можно скрыть за один VIP для Service discovery. При этом нужно обеспечить прямой доступ клиентов к каждому из них (см. advertised.listeners)

Kafka protocol: https://kafka.apache.org/protocol

Producer посылает сообщения брокеру батчами, улучшая пропускную способность и степень сжатия.

[!] Retries есть из коробки. Могут сломать очередность сообщений, если **max.in.flight.request.per.connection** > 1

#### Producer Idempotence
каждый продюсер получает PID и монотонно возврастающий SEQ, PID+SEQ - не позволяет сделать reordering и дубликаты в брокере
`enable.idempotence=true`
- работает только в пределах жизни инстанса продюсера (каждый инстант получает свой PID)
- не сверяет контент сообщений, только SEQ - не делайте ретраев поверх встроенных
- max.in.flight.request.per.connection <= 5, retries > 0
- acks=all - ждет записи сколько указано в ISR (более высокое летанси)

Гарантии доставки: https://aphyr.com/posts/293-jepson-kafka

Best Practices - для всех топиков:
- min.insync.replicas = 2
- replication factor = 3

Для ценный данных:
- acks = -1
- идемпотентность

Отрабатывать падение брокера и перемещение лидеров партиций - это ответственность клиентов и для Producer и для Consumer

По-умолчанию клиент Consumer-a автоматически коммитит offset-ы раз в `auto.commit.interval.ms`

- `session.timeout.ms` - максимальное время между heartbeat запросами к брокеру (контролируется брокером)
- `max.poll.inverval.ms` - максимальное время между вызовами poll (контролируется самим клиентом)
- `group.id` - идентификатор группы

**Synchronization Barrier** - процесс между JoinRequest и AssignPartition между consumer-ами - вся обработка прекращается в это время (stop the world)

Consumer Rebalancing может происходит при:
- подписка на новые топики
- создание новых партиций
- подключение новых членов группы
- падение членов группы
- рестарт одного из членов группы

Consumer static Membership - фича для сохранения group.instance.id статического id консьюмера, 
при этом рестарт должен уложиться в session.timeout.ms, за исключение рестарта Group Leader

Consumer Cooperative Rebalancing
- Перемещает только минимальный необходимый набор партиций между консьюмерами
- Разбивает одну большую балансировку на две
- Снижает длительность stop-the-world эффекта при ребелансировке

partition.assignment.strategy="org.apache.kafka.clients.consumer.CooperativeStickyAssignor"

Transactions & Exactly Once

Главные принципы транзакционности в Kafka:
1. Атомарная запись в несколько партиций одновременно
2. Защита от "зомби" из коробки
3. Изоляция: консьюмеры получают сообщения только успешно завершенных транзакций


Транзакционные маркеры - обычные сообщения и несколько ломают логику поиска сообщений по timestamp (offsetByTime()), 
если вы пользуетесь CreateTime

Ущерб производительности на мелких стримах не заметен (+3% degradation, 1KB of records per/sec). 
Растет нагрузка на брокеры с ростом количества транзакций.

Открытые транзакции не дают консьюмерам с isolation.level=read_committed читать сообщения выше Last Stable Offset (LSO)

**Траназкции обеспечивают exactly-once только в read-process-write приложениях читающих и пишуших в Кафку**

Чтобы сделать exactly-once в сторонее хранилище нужно хранение offset-ов перенести в это самое хранилище.

Репликация данных:
- rack awareness
- хороший default:
  - min.insync.replicas=2
    - isr - replica.lag.time.max.ms
  - replication.factor=3

коммитом считается сообщение записанное во все реплики

Варианты отказа:
- отказ фолловер-партиции
  - offset реплицируется с лидера на реплики - last committed offset, high-watermark offset, при падении фолловер транкетить все после lco/hwo и перечитывает все с лидера
- отказ лидер-партиции
  - один из брокеров выполняет роль контроллера, подписывается на падения брокеров через zookepeer, получает список лидер партиций находившихся на лидер партиции и назначает новых лидеров

Контроллер:
- решает задачи по координаций изменений (либо 0, либо 1)
- создание и удаление партиций
- вход/выход брокеров
- подписан на zookeeper
- уведомляет других брокер

preffered leaders - старые лидеры

controllerEpoch - эпоха, увеличивается при смерти контроллера, монотонно возрастающая

https://www.confluent.io/blog/apache-kafka-supports-200k-partitions-per-cluster/

Настройка числа партиций:
- не больше 4к партиций на брокер
- не больше 200к партиций на кластер

Помогает держать нагрузку равномерной
- auto.leader.rebalance.enable
- leader.imbalance.check.interval.seconds
- leader.imbalance.per.broker.percentage

event -> dirty buffer -> disk, защищается через репликацию, а не через fsync:
- flush.messages
- flush.ms

защита от шторма коннектов - KIP-402:
- max.connections
- max.connections.per.ip
- max.connection.creation.rate

num.partitions - увеличивает время failover-a

Бэкапы
- Zookeeper
  - нересурсоемкие
    - validate
- broker-ы
  - Kafka connect -> s3 sink -> s3 buckets
    - restore: s3 source connector -> topic

Полезные практики:
- Disaster recovery plan
- Disaster tests
- Runbooks and on-call дежурства
- Knowledge sharing and bus-factor 2+
- LSR -> action items

Ограничение одного ДЦ:
- потеря ДЦ
- физически ограниченное место для горизонтального роста (нет стоек, нет площадки)
- не всегда можно соблюсти требования юристов

нужно чтобы бизнес (овнеры) ответил:
- страшно ли подаунтаймить
- нужно ли расти дальше

```
./bin/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance  \
--topic=registrations  \
--num-records=100000000 \
--throughput=100 \
--record-size=100 \
--producer-props \
bootstrap.servers=localhost:9090,localhost:9091,localhost:9092 \
batch.size=64000 \
acks=all \
--print-metrics
```

Какие задачи решает несколько ДЦ:
- Гео, пинг
- Политические, юридические аспекты
- Физическое место
- Отказоустойчивость

Компромисс
- низкая задержка/высокая пропуская способность
- консистентность

https://eventsizer.io - калькулятор ресурсов

Подходы мульти-ДЦ
- Streched cluster
  - 1 zoocluster
  - у брокера broker.rack - в каком датацентре
  - KIP-392: Allow consumers to fetch from closest replica (consumers)
    - replica.selector.class=RackAwareReplicaSelector
      - client.rack
    - producer всегда в лидера пишет
  - синхронная репликация
  - простой
  - нет проблем с failover
  - есть поддержка локального чтения
  - работает только при низком latency (<=30ms)
  - нет поддержки локальной записи
  - полный отказ кластера = даунтайм

Асинхронный кластер - логическое объединение нескольких физических кластеров
- Replicator - доп клиент, читает, потом записает в другой кластер (асинхронно)
- Active-Active - довольно сложная архитектура. offset-ы будут различатся. предотвратить кольцевую синхронизацию.
- **Active-Active только для запись, 1 Stretched Cluster только для чтения**
- Репликаторы
  - MirrorMaker - внутри обычный консумер+продюсер, топик discovery
    - прост в использовании
    - подходит для ad-hoc скриптов
    - Опенсорс
    - нет динамического отслеживания топиков, не копирует конфиги, создает с конфигами по-умолчанию
    - нет защиты от циклического репликации
    - нет синхронизации оффсетов
    - подвержен проблемам consumer rebalance
  - uReplicator - объертка над MirrorMaker
    - uRelicator worker - сам репликатор
      - Helix Agent
      - Dynamic Kafka Consumer
    - Helix controller - управление топиками, управление воркерами, REST API
    - динамическое отслеживание топиков
    - нет проблемы consumer rebalance
    - нет проблем с масштабированием
    - нет защиты от циклической репликации
  - Confluent Replicator - платный
    - динамическое отслеживание топиков
    - нет проблем с consumer rebalance
    - нет проблем с масштабированием
    - синхронизация оффсетов
    - не опенсорс
    - дорогой
  - **MirrorMaker 2.0**
    - является коннекторами для KafkaConnect
    - префиксы перед топиками
    - динамическое отслеживание топиков
    - нет проблем с consumer rebalance
    - нет проблем с масштабированием
    - синхронизации оффсетов
    - защита от циклической репликации
    - синхронизация ACL
    - опенсорс
    - KIP-382

Особенности работы в двух ДЦ
- 2 zk + 1 zk
  - 1 zk в DC или Cloud
- 2 cluster-a zookeeper, иерархический кворум
  - потенциальный split-brain

Мониторинг Кафки
- отслеживание поведения системы в реальном времени
- трекинг изменений в поведении с течением времени
- заблаговременное планирование ресурсов

Собрать метрики:
- Zookeeper
- Kafka
- JVM (менеджить память, GC (stop the world))
  - частоту GC
  - длительность GC
- Host
  - network
  - disk
    - io/latency
    - capacity
  - cpu
  - mem

Способы мониторинга:
- JVM -> JMX -> JmxTrans Sidecar -> push -> graphite -> grafana
- JVM -> JMX Exporter -> get -> Prometheus
- JVM -> Custom Reporter (metric.reporters) -> Produce -> Metrics Topic -> Druid, Presto, Flink

Подводные камни
- перцентили считаются с помощью EDR. Иногда использует исторические метрики - когда нет данных.
- статьи о проблемах с EDR
  - https://medium.com/expedia-group-tech/your-latency-metrics-could-be-misleading-you-how-hdrhistogram-can-help-9d545b598374
  - https://engineering.salesforce.com/be-careful-with-reservoirs-708884018daf

Ключевые метрики:
- Доступность
  - UnderReplicatePartitions
  - UnderMinIsrPartionCount
  - Isr[Shrink|Expands]PerSec
  - LeaderElectionRateAndTimeMs
  - ErrorPerSec
  - SessionState
- Скорость
  - TotalTimeMs
  - PurgatorySize
  - ZooKeeperRequestLatencyMs
  - GC CollectionCount
  - GC CollectionTime
- Загруженность
  - PartitionCount
  - LeaderCount
  - NetworkProcessorAvgIdlePercent
  - RequestHandlerAvgIdlePercent
  - Free Disk Space
  - DISK IOPS/Latency
  - CPU Usage
  - Network Bytes In/Out
- Трафик
  - MessagesInPerSec
  - Bytes[In|Out]PerSec
  - RequestsPerSec

Zookepeer metrics:
- Доступность
  - Leader (sum == 1)
  - PartOfEnsemble (sum == N)
- Скорость
  - AvgRequestLatency
  - GC CollectionCount
  - GC CollectionTime
- Загруженность
  - NodeCount
  - WatchCount
  - OutstandingRequest
  - Free Disk Space
  - Disk IOPS/Latency
- Трафик
  - PacketsSent
  - PacketsReceived
  - NumAliveConnections

Клиенты:
- Желательно оборачивать ванильных клиентов в собственную библиотеку
- Consumer Lag
  - разница между log head (highest offset) и committed offset
- Burrow - мониторинг лага консюмеров (https://github.com/linkedin/Burrow)

Примеры SLI/SLO:
- write
  - SLI: (Total Produce Request - Produce Request Errors / Total Produce Request) * 100%
  - SLO: >= 99% в течение последних 14 дней
  - Как считать write SLI ?
    - [нет] Агрегировать серверные метрики в одну
    - [нет] Агрегировать клиентские метрики в одну
    - [нет] Агрегировать клиентские метрики для каждого сервиса
    - [да] использовать метрики внешнего монитора
      - Xinfra Monitor: https://github.com/linkedin/kafka-monitor
        - create and rebalance the monitoring
        - product every N ms
        - consume back
        - JmxTrans Sider -> calc SLI -> SLO Report


Kafka Performance

- Кафка оптимизирована под high-throughput
- Платит она за это сравнительно высокими и неравномерными latency

- append-only подразумевает линейный (sequential) I/O
  - read-ahead - данные при чтении предзагружаются системой
  - write-behind - мелкие логические операции записи группируются в большие физические
    - dirty-write

Линейный доступ к диску может быть быстрее чтения из памяти:
- https://queue.acm.org/detail.cfm?id=1563874

Batching & Compression
- кафка аккумулирует записи в батчи перед отправкой, снижая количество запросов к диску и пакетов, летящих по сети
- встроенная компрессия батчей дополнительно снижает нагрузку на сеть и диск, и улучшает пропускную способность

Легковесные консьюмеры
- при чтении не меняют данные
- коммит - запись в конец топика __consumer_offsets
- real-time консюмеры фактически читают данные из page cache брокера

No fsync
- На самом деле Кафка - это in-memory queue с отложенной записью на диск
- Сохранноть данных обеспечивается репликами и acks

Zero Copy
- внутри Kernel Context-a  из read buffer через transferTo() передается информация от дескрипторе данных (его позиция и length) в NIC buffer
  - данные не копируются из буфера в буффер
  - нет context switch между application context / kernel context

Benchmarking
- bin/kafka-producer-perf-test.sh
- bin/kafka-consumer-perf-test.sh
- bin/kafka-run-class.sh kafka.tools.EndToEndLatency
- Trogdor - https://github.com/apache/kafka/blob/trunk/TROGDOR.md- 
- OpenMessaging Benchmark: https://openmessaging.cloud/docs/benchmarks/kafka/

