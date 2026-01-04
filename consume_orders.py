"""
Kafka Consumer - Process Orders
Run: python3 consume_orders.py
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from kafka import KafkaConsumer
    print("✅ Kafka library loaded")
except ImportError:
    print("❌ Installing kafka-python...")
    import os
    os.system("pip install kafka-python")
    from kafka import KafkaConsumer

from sqlalchemy import text
from src.utils.db_connector import db_connector

print("🚀 Starting Kafka Consumer...")
print("📡 Connecting to localhost:9092...\n")

try:
    consumer = KafkaConsumer(
        'orders-stream',
        bootstrap_servers='localhost:9092',
        group_id='order-processor',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest'
    )
    
    print("✅ Connected!")
    print("📥 Waiting for orders...\n")
    
    engine = db_connector.get_postgres_engine()
    count = 0
    
    for message in consumer:
        order = message.value
        
        try:
            # Save to database
            with engine.connect() as conn:
                query = text("""
                    INSERT INTO raw.orders 
                    (order_id, customer_id, product_id, quantity, unit_price, 
                     total_amount, order_date, status, city, country)
                    VALUES 
                    (:order_id, :customer_id, :product_id, :quantity, :unit_price,
                     :total_amount, :order_date, :status, :city, :country)
                    ON CONFLICT (order_id) DO NOTHING
                """)
                
                conn.execute(query, order)
                conn.commit()
            
            count += 1
            print(f"✅ [{count}] Saved: {order['order_id']} | ${order['total_amount']:.2f} | {order['country']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
except KeyboardInterrupt:
    print(f"\n\n⏹️  Stopped. Total: {count} orders")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Check Kafka: docker ps | grep kafka")
    print("   2. Check DB: python3 check_data.py")
finally:
    try:
        consumer.close()
    except:
        pass