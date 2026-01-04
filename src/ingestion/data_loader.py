"""
Data Loader - Load generated data into PostgreSQL
"""

import pandas as pd
from sqlalchemy import text
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.db_connector import db_connector
from src.utils.logger import setup_logger
from src.ingestion.data_generator import SupplyChainDataGenerator

logger = setup_logger(__name__)


class DataLoader:
    """Load data into PostgreSQL database"""
    
    def __init__(self):
        self.engine = db_connector.get_postgres_engine()
    
    def load_dataframe(self, df: pd.DataFrame, table_name: str, schema: str = 'raw'):
        """Load DataFrame to PostgreSQL table"""
        try:
            # Load data
            df.to_sql(
                name=table_name,
                con=self.engine,
                schema=schema,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            logger.info(f"✅ Loaded {len(df)} records into {schema}.{table_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load {table_name}: {e}")
            return False
    
    def truncate_table(self, table_name: str, schema: str = 'raw'):
        """Clear table data"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name} CASCADE;"))
                conn.commit()
            logger.info(f"🗑️  Truncated {schema}.{table_name}")
        except Exception as e:
            logger.error(f"❌ Failed to truncate {table_name}: {e}")
    
    def load_all_data(self, n_orders: int = 1000, clean_first: bool = True):
        """Generate and load all data"""
        logger.info("🚀 Starting data loading process...")
        
        # Generate data
        generator = SupplyChainDataGenerator()
        data = generator.generate_all_data(n_orders=n_orders)
        
        # Clean tables if requested
        if clean_first:
            logger.info("🗑️  Cleaning existing data...")
            tables = ['inventory', 'shipments', 'orders', 'products', 'carriers', 'suppliers']
            for table in tables:
                self.truncate_table(table)
        
        # Load data in correct order (respecting foreign keys)
        logger.info("\n📥 Loading data into database...")
        
        # 1. Suppliers (no dependencies)
        self.load_dataframe(data['suppliers'], 'suppliers')
        
        # 2. Carriers (no dependencies)
        self.load_dataframe(data['carriers'], 'carriers')
        
        # 3. Products (depends on suppliers)
        self.load_dataframe(data['products'], 'products')
        
        # 4. Orders (depends on products)
        self.load_dataframe(data['orders'], 'orders')
        
        # 5. Shipments (depends on orders and carriers)
        self.load_dataframe(data['shipments'], 'shipments')
        
        # 6. Inventory (depends on products)
        self.load_dataframe(data['inventory'], 'inventory')
        
        logger.info("\n✅ Data loading completed successfully!")
        
        # Show summary
        self.show_summary()
    
    def show_summary(self):
        """Show database summary"""
        logger.info("\n📊 Database Summary:")
        
        tables = ['suppliers', 'carriers', 'products', 'orders', 'shipments', 'inventory']
        
        with self.engine.connect() as conn:
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM raw.{table};"))
                count = result.fetchone()[0]
                logger.info(f"   {table:15s}: {count:6d} records")


if __name__ == "__main__":
    loader = DataLoader()
    loader.load_all_data(n_orders=1000, clean_first=True)