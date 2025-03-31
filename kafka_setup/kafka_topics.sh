#!/bin/bash
bin/kafka-topics.sh --create --topic order_topic --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic payment_topic --bootstrap-server localhost:9092
