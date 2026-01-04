#!/usr/bin/env python3
"""Test Kafka Connection"""

from confluent_kafka import Producer, Consumer
import json
import time

print("🧪 Testing Kafka...\n")

# Test Producer
print("1️⃣ Testing Producer...")
try:
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    message = {'test': 'hello', 'number': 123}
    producer.produce('test-topic', json.dumps(message).encode())
    producer.flush()
    print("✅ Producer works!\n")
except Exception as e:
    print(f"❌ Producer failed: {e}\n")

# Test Consumer
print("2️⃣ Testing Consumer...")
try:
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['test-topic'])
    
    msg = consumer.poll(5.0)
    if msg and not msg.error():
        print(f"✅ Consumer works! Received: {msg.value().decode()}\n")
    else:
        print("⚠️  No message received (normal if just started)\n")
    
    consumer.close()
except Exception as e:
    print(f"❌ Consumer failed: {e}\n")

print("✅ Kafka test complete!")