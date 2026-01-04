import os
from sqlalchemy import create_engine
from pymongo import MongoClient
import redis
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnector:
    """Unified database connection manager"""
    
    def __init__(self):
        self.postgres_engine = None
        self.mongo_client = None
        self.redis_client = None
    
    def get_postgres_engine(self):
        """Get PostgreSQL connection engine"""
        if not self.postgres_engine:
            connection_string = (
                f"postgresql://{os.getenv('POSTGRES_USER')}:"
                f"{os.getenv('POSTGRES_PASSWORD')}@"
                f"{os.getenv('POSTGRES_HOST')}:"
                f"{os.getenv('POSTGRES_PORT')}/"
                f"{os.getenv('POSTGRES_DB')}"
            )
            self.postgres_engine = create_engine(connection_string)
        return self.postgres_engine
    
    def get_mongo_client(self):
        """Get MongoDB client"""
        if not self.mongo_client:
            connection_string = (
                f"mongodb://{os.getenv('MONGO_USER')}:"
                f"{os.getenv('MONGO_PASSWORD')}@"
                f"{os.getenv('MONGO_HOST')}:"
                f"{os.getenv('MONGO_PORT')}/"
            )
            self.mongo_client = MongoClient(connection_string)
        return self.mongo_client
    
    def get_redis_client(self):
        """Get Redis client"""
        if not self.redis_client:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST'),
                port=int(os.getenv('REDIS_PORT')),
                password=os.getenv('REDIS_PASSWORD'),
                decode_responses=True
            )
        return self.redis_client

db_connector = DatabaseConnector()