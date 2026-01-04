"""Quick check of database data"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from src.utils.db_connector import db_connector

engine = db_connector.get_postgres_engine()

print("🔍 Checking database data...\n")

with engine.connect() as conn:
    # Check suppliers
    result = conn.execute(text("SELECT * FROM raw.suppliers LIMIT 5;"))
    print("📦 Sample Suppliers:")
    for row in result:
        print(f"   {row.supplier_id}: {row.supplier_name} ({row.country})")
    
    # Check orders
    result = conn.execute(text("SELECT * FROM raw.orders LIMIT 5;"))
    print("\n🛒 Sample Orders:")
    for row in result:
        print(f"   {row.order_id}: ${row.total_amount:.2f} - {row.status}")
    
    # Check shipments
    result = conn.execute(text("SELECT * FROM raw.shipments LIMIT 5;"))
    print("\n📬 Sample Shipments:")
    for row in result:
        print(f"   {row.shipment_id}: {row.status} - {row.current_location}")
    
    # Summary
    print("\n" + "="*50)
    print("📊 Total Records:")
    tables = ['suppliers', 'carriers', 'products', 'orders', 'shipments', 'inventory']
    for table in tables:
        result = conn.execute(text(f"SELECT COUNT(*) FROM raw.{table};"))
        count = result.fetchone()[0]
        print(f"   {table:15s}: {count:6d}")

print("\n✅ Data check completed!")