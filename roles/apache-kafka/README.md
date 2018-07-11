[![Build Status](https://travis-ci.org/akthodu/apache-kafka.svg?branch=master)](https://travis-ci.org/akthodu/apache-kafka)

Role Name
=========
Install apache Kafka and configures kafka and zookeeper cluster
```
Creates application user and group
Creates required directories for kafka broker and zookeeper
Configures properties requried for kafka and zookeeper and creates systemd services.
Two Zookeeper nodes should be up before starting kafka broker in 3 node kafka cluster to form Quorum among Zookeeper nodes.
Enables JMX on kafka broker.
Heap sizes are set by env  files
kafka.env --> sets heap for kafka broker
zookeeper.env --> sets heap for zookeeper
```

Requirements
------------
Requires Kafka_broker_id and zookeeper_id values in host inventory

```
[kafkaservers]
10.0.15.22 kafka_broker_id=1 zookeeper_id=1
10.0.15.23 kafka_broker_id=2 zookeeper_id=2
10.0.15.15 kafka_broker_id=3 zookeeper_id=3
```

Role Variables
--------------
variables required for apache kafka cluster install are located in vars/main.yml.


Dependencies
------------

Assumes JAVA is already installed on all systems in cluster.
