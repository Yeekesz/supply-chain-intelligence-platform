#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from confluent_kafka import Consumer, KafkaError
from sqlalchemy import text
from src.utils.db_connector import db_connector

print("🚀 Consumer Starting...")
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'orders-group',
    'auto.offset.reset': 'latest'
})
consumer.subscribe(['orders'])
print("✅ Listening...\n")

engine = db_connector.get_postgres_engine()
count = 0

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        
        order = json.loads(msg.value().decode())
        
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO raw.orders 
                (order_id, customer_id, quantity, unit_price, 
                 total_amount, order_date, status, city, country)
                VALUES 
                (:order_id, :customer_id, :quantity, :unit_price,
                 :total_amount, NOW(), 'pending', :city, :country)
                ON CONFLICT (order_id) DO NOTHING
            """), order)
            conn.commit()
        
        count += 1
        print(f"✅ {count}. {order['order_id']} - ${order['total_amount']:.2f}")

except KeyboardInterrupt:
    print(f"\n⏹️ Total: {count}")
finally:
    consumer.close()