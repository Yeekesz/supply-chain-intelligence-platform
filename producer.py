#!/usr/bin/env python3
import json, time, random
from datetime import datetime
from confluent_kafka import Producer
from faker import Faker

fake = Faker()

def create_order():
    qty = random.randint(1, 5)
    price = round(random.uniform(10, 500), 2)
    return {
        'order_id': f"ORD{random.randint(100000, 999999)}",
        'customer_id': f"CUST{random.randint(1000, 9999)}",
        'quantity': qty,
        'unit_price': price,
        'total_amount': round(qty * price, 2),
        'country': random.choice(['USA', 'UAE', 'UK']),
        'city': fake.city(),
    }

print("🚀 Producer Starting...")
producer = Producer({'bootstrap.servers': 'localhost:9092'})
print("✅ Sending orders...\n")

count = 0
try:
    while True:
        order = create_order()
        producer.produce('orders', json.dumps(order).encode())
        producer.poll(0)
        count += 1
        print(f"✅ {count}. {order['order_id']} - ${order['total_amount']:.2f}")
        time.sleep(3)
except KeyboardInterrupt:
    print(f"\n⏹️ Total: {count}")
finally:
    producer.flush()