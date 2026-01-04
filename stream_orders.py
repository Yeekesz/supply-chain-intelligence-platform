"""
Kafka Producer - Stream Orders
Run: python3 stream_orders.py
"""

import json
import time
import random
from datetime import datetime
from faker import Faker

try:
    from kafka import KafkaProducer
    print("✅ Kafka library loaded")
except ImportError:
    print("❌ Installing kafka-python...")
    import os
    os.system("pip install kafka-python")
    from kafka import KafkaProducer

fake = Faker()

CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
COUNTRIES = ['USA', 'UAE', 'UK', 'Germany', 'China']

def create_order():
    """Generate random order"""
    quantity = random.randint(1, 5)
    unit_price = round(random.uniform(10, 500), 2)
    
    return {
        'order_id': f"ORD{random.randint(100000, 999999)}",
        'customer_id': f"CUST{random.randint(1000, 9999)}",
        'product_id': f"PROD{random.randint(1, 200):06d}",
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': round(quantity * unit_price, 2),
        'status': random.choice(['pending', 'confirmed']),
        'country': random.choice(COUNTRIES),
        'city': fake.city(),
        'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

print("🚀 Starting Kafka Producer...")
print("📡 Connecting to localhost:9092...\n")

try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print("✅ Connected!")
    print("📦 Streaming orders (Ctrl+C to stop)...\n")
    
    count = 0
    while True:
        order = create_order()
        producer.send('orders-stream', value=order)
        count += 1
        
        print(f"✅ [{count}] Sent: {order['order_id']} | ${order['total_amount']:.2f} | {order['country']}")
        
        time.sleep(random.uniform(2, 4))
        
except KeyboardInterrupt:
    print(f"\n\n⏹️  Stopped. Total: {count} orders")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 Make sure Docker is running:")
    print("   docker-compose ps")
finally:
    try:
        producer.close()
    except:
        pass