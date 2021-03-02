#!/usr/bin/python3

from kafka import KafkaAdminClient

admin = KafkaAdminClient(bootstrap_servers=['155.98.36.76:9092'])

print(admin.list_consumer_groups())
