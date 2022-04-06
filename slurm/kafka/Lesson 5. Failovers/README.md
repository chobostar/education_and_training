1. Проверьте, что вы находитесь в каталоге с Kafka, а если нет - перейдите туда:
```
cd kafka_2.13-2.7.0
```
2. Запускаем Zookeeper.
```
rm -rf /tmp/zookeeper
./bin/zookeeper-server-start.sh ./config/zookeeper.properties
```
3. Запускаем брокеры Кафки
```
cat << 'EOF' > kafka-distributed-start.sh

#!/usr/bin/env bash
for i in {0..2}
do
cp ./config/server.properties "./config/server$i.properties"
sed -i "s/broker.id=0/broker.id=$i/g" ./config/server$i.properties
echo "listeners=PLAINTEXT://:909$i" >> ./config/server$i.properties
echo "broker.rack=my-rack-$i" >> ./config/server$i.properties
mkdir /tmp/kafka-logs$i
sed -i "s/log.dirs=\/tmp\/kafka-logs/log.dirs=\/tmp\/kafka-logs$i/g" ./config/server$i.properties
(./bin/kafka-server-start.sh config/server$i.properties &)
done
EOF
chmod +x kafka-distributed-start.sh
rm -rf /tmp/kafka-logs*
./kafka-distributed-start.sh
```
4. Создаем топик ( min.isr=3, unclean = false)
```
./bin/kafka-topics.sh --create \
--bootstrap-server localhost:9092 \
--topic registrations \
--partitions 1  \
--replication-factor 3 \
--config min.insync.replicas=3 \
--config unclean.leader.election.enable=false
```
5. Проверим, что топик создан
```
./bin/kafka-topics.sh --describe --topic registrations --bootstrap-server localhost:9092 | head -n1
```
6. Запустим producer
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
7. Остановим первый брокер, видим ошибки записи на producer NOT_ENOUGH_REPLICAS (запись прекратилась)
```kill -s ${SIGNAL:-TERM} $(ps ax | grep -i 'kafka\.Kafka' | grep 'server0.properties' | grep java | grep -v grep | awk '{print $1}' | head -n1)```
8. Уменьшим min.insync.replicas для топика до 2 и подождем пока запись возобновится
```
./bin/kafka-configs.sh \
--alter \
--bootstrap-server localhost:9092 \
--entity-type topics \
--entity-name registrations \
--add-config min.insync.replicas=2
```
9. Остановим второй брокер, видим ошибки записи на producer NOT_ENOUGH_REPLICAS (запись прекратилась)
```
kill -s ${SIGNAL:-TERM} $(ps ax | grep -i 'kafka\.Kafka' | grep 'server1.properties' | grep java | grep -v grep | awk '{print $1}' | head -n1)
```
10. Уменьшим min.insync.replicas для топика до 1 и подождем пока запись возобновится
```
./bin/kafka-configs.sh \
--alter \
--bootstrap-server localhost:9092 \
--entity-type topics \
--entity-name registrations \
--add-config min.insync.replicas=1
```
11. Остановим третий брокер, через несколько секунд увидим ошибки записи на producer “Connection to node could not be established. Broker may not be available” (запись прекратилась)
```
kill -s ${SIGNAL:-TERM} $(ps ax | grep -i 'kafka\.Kafka' | grep 'server2.properties' | grep java | grep -v grep | awk '{print $1}' | head -n1)
```
12. Запустим первый и второй брокеры Кафки (на продюсере все еще ошибки “TimeoutException”, запись по прежнему не возобновилась)
```
./bin/kafka-server-start.sh config/server0.properties &

./bin/kafka-server-start.sh config/server1.properties &
```
13. Проверим, есть ли в топике лидер, для этого будем использовать флаг --unavailable-partitions  (видим, что Leader: none, т.е. партиция осталась без лидера)
```
./bin/kafka-topics.sh --describe --topic registrations --bootstrap-server localhost:9090 --unavailable-partitions
```
14. Выставим для топика unclean.leader.election.enable=true (разрешаем выбрать лидером даже партицию с неконсистентным набором данных)
```
./bin/kafka-configs.sh \
--alter \
--bootstrap-server localhost:9090 \
--entity-type topics \
--entity-name registrations \
--add-config unclean.leader.election.enable=true
```

15. Проверим, есть ли в топике лидер (видим, что лидер появился и продюсер продолжил запись)
```
./bin/kafka-topics.sh --describe --topic registrations --bootstrap-server localhost:9090
```