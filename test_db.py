from src.utils.db_connector import db_connector
from sqlalchemy import text

print("🧪 Testing database connections...\n")

# Test PostgreSQL
try:
    engine = db_connector.get_postgres_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ PostgreSQL: Connected!")
        print(f"   Version: {version[:50]}...")
except Exception as e:
    print(f"❌ PostgreSQL: Failed - {e}")

# Test MongoDB
try:
    client = db_connector.get_mongo_client()
    client.admin.command('ping')
    print("\n✅ MongoDB: Connected!")
    dbs = client.list_database_names()
    print(f"   Databases: {', '.join(dbs)}")
except Exception as e:
    print(f"\n❌ MongoDB: Failed - {e}")

# Test Redis
try:
    redis_client = db_connector.get_redis_client()
    redis_client.ping()
    print("\n✅ Redis: Connected!")
    info = redis_client.info('server')
    print(f"   Version: {info['redis_version']}")
except Exception as e:
    print(f"\n❌ Redis: Failed - {e}")

print("\n" + "="*50)
print("✅ All database tests completed!")