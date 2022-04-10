
Producer Benchmark:
```
$ cd /opt/kafka_2.13-2.7.0/bin/
$ ./kafka-producer-perf-test.sh

usage: producer-performance [-h] --topic TOPIC --num-records NUM-RECORDS [--payload-delimiter PAYLOAD-DELIMITER] --throughput THROUGHPUT
                            [--producer-props PROP-NAME=PROP-VALUE [PROP-NAME=PROP-VALUE ...]] [--producer.config CONFIG-FILE] [--print-metrics] [--transactional-id TRANSACTIONAL-ID]
                            [--transaction-duration-ms TRANSACTION-DURATION] (--record-size RECORD-SIZE | --payload-file PAYLOAD-FILE)
```

```
./kafka-topics.sh --bootstrap-server node-1.$USER:9092 --topic producer-benchmark --replication-factor 3 --partitions 1 --create
```

```
./kafka-producer-perf-test.sh --producer-props bootstrap.servers=node-1.$USER:9092 --topic producer-benchmark --throughput -1 --num-records 500000 --record-size 100
```

```
./kafka-producer-perf-test.sh --producer-props bootstrap.servers=node-1.$USER:9092 acks=0 --topic producer-benchmark --throughput -1 --num-records 500000 --record-size 100
```

Consumer Benchmark:

```
./kafka-consumer-perf-test.sh --bootstrap-server node-1.$USER:9092 --topic consumer-benchmark --messages 1000000 --print-metrics
```