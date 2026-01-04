"""
Data Generator for Supply Chain Platform
Generates realistic orders, shipments, products, suppliers, and carriers
"""

import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
from typing import List, Dict
import uuid

fake = Faker()

# Global configurations
COUNTRIES = ['USA', 'UAE', 'UK', 'Germany', 'China', 'France', 'Japan', 'Canada', 'Australia', 'India']
CITIES = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'UAE': ['Dubai', 'Abu Dhabi', 'Sharjah'],
    'UK': ['London', 'Manchester', 'Birmingham'],
    'Germany': ['Berlin', 'Munich', 'Hamburg'],
    'China': ['Shanghai', 'Beijing', 'Shenzhen']
}

PRODUCT_CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Food']
ORDER_STATUSES = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
SHIPMENT_STATUSES = ['pending', 'in_transit', 'delivered', 'delayed', 'cancelled']
CARRIER_NAMES = ['DHL', 'FedEx', 'UPS', 'Aramex', 'USPS']


class SupplyChainDataGenerator:
    """Generate realistic supply chain data"""
    
    def __init__(self, seed: int = 42):
        """Initialize generator with seed for reproducibility"""
        random.seed(seed)
        Faker.seed(seed)
        self.fake = Faker()
    
    def generate_suppliers(self, n: int = 50) -> pd.DataFrame:
        """Generate supplier data"""
        suppliers = []
        
        for i in range(n):
            supplier_id = f"SUP{str(i+1).zfill(5)}"
            country = random.choice(COUNTRIES)
            
            supplier = {
                'supplier_id': supplier_id,
                'supplier_name': self.fake.company(),
                'country': country,
                'city': random.choice(CITIES.get(country, ['Unknown'])),
                'contact_email': self.fake.email(),
                'contact_phone': self.fake.phone_number(),
                'rating': round(random.uniform(3.0, 5.0), 2),
                'lead_time_days': random.randint(5, 30),
                'reliability_score': round(random.uniform(0.7, 1.0), 4),
                'quality_score': round(random.uniform(0.75, 1.0), 4),
                'on_time_delivery_rate': round(random.uniform(0.80, 0.99), 4),
                'created_at': datetime.now()
            }
            suppliers.append(supplier)
        
        return pd.DataFrame(suppliers)
    
    def generate_carriers(self, n: int = 10) -> pd.DataFrame:
        """Generate carrier data"""
        carriers = []
        
        for i, carrier_name in enumerate(CARRIER_NAMES):
            carrier_id = f"CAR{str(i+1).zfill(5)}"
            
            carrier = {
                'carrier_id': carrier_id,
                'carrier_name': carrier_name,
                'avg_rating': round(random.uniform(3.5, 5.0), 2),
                'cost_per_kg': round(random.uniform(2.0, 8.0), 2),
                'created_at': datetime.now()
            }
            carriers.append(carrier)
        
        return pd.DataFrame(carriers)
    
    def generate_products(self, n: int = 200, supplier_ids: List[str] = None) -> pd.DataFrame:
        """Generate product data"""
        products = []
        
        if supplier_ids is None:
            supplier_ids = [f"SUP{str(i+1).zfill(5)}" for i in range(50)]
        
        for i in range(n):
            product_id = f"PROD{str(i+1).zfill(6)}"
            category = random.choice(PRODUCT_CATEGORIES)
            
            product = {
                'product_id': product_id,
                'product_name': f"{category} - {self.fake.word().title()} {random.randint(100, 999)}",
                'category': category,
                'supplier_id': random.choice(supplier_ids),
                'unit_price': round(random.uniform(10.0, 500.0), 2),
                'weight_kg': round(random.uniform(0.1, 10.0), 3),
                'created_at': datetime.now()
            }
            products.append(product)
        
        return pd.DataFrame(products)
    
    def generate_orders(
        self, 
        n: int = 1000, 
        start_date: datetime = None,
        product_ids: List[str] = None
    ) -> pd.DataFrame:
        """Generate order data"""
        orders = []
        
        if start_date is None:
            start_date = datetime.now() - timedelta(days=90)
        
        if product_ids is None:
            product_ids = [f"PROD{str(i+1).zfill(6)}" for i in range(200)]
        
        for i in range(n):
            order_id = f"ORD{str(i+1).zfill(8)}"
            customer_id = f"CUST{random.randint(1, 5000):06d}"
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(10.0, 500.0), 2)
            total_amount = round(quantity * unit_price, 2)
            
            order_date = start_date + timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            expected_delivery_date = order_date + timedelta(days=random.randint(3, 10))
            
            country = random.choice(COUNTRIES)
            city = random.choice(CITIES.get(country, ['Unknown']))
            
            order = {
                'order_id': order_id,
                'customer_id': customer_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': total_amount,
                'order_date': order_date,
                'expected_delivery_date': expected_delivery_date,
                'status': random.choice(ORDER_STATUSES),
                'shipping_address': self.fake.address(),
                'city': city,
                'country': country,
                'created_at': datetime.now()
            }
            orders.append(order)
        
        return pd.DataFrame(orders)
    
    def generate_shipments(
        self,
        orders_df: pd.DataFrame,
        carrier_ids: List[str] = None
    ) -> pd.DataFrame:
        """Generate shipment data based on orders"""
        shipments = []
        
        if carrier_ids is None:
            carrier_ids = [f"CAR{str(i+1).zfill(5)}" for i in range(len(CARRIER_NAMES))]
        
        for idx, order in orders_df.iterrows():
            if order['status'] in ['shipped', 'delivered']:
                shipment_id = f"SHIP{str(idx+1).zfill(8)}"
                carrier_id = random.choice(carrier_ids)
                
                shipped_date = order['order_date'] + timedelta(days=random.randint(1, 3))
                estimated_delivery = order['expected_delivery_date']
                
                # Simulate delays
                is_delayed = random.random() < 0.15  # 15% delay rate
                if is_delayed:
                    actual_delivery = estimated_delivery + timedelta(days=random.randint(1, 5))
                    status = random.choice(['in_transit', 'delayed'])
                else:
                    if order['status'] == 'delivered':
                        actual_delivery = estimated_delivery - timedelta(hours=random.randint(1, 24))
                        status = 'delivered'
                    else:
                        actual_delivery = None
                        status = 'in_transit'
                
                # Random location
                latitude = round(random.uniform(-90, 90), 7)
                longitude = round(random.uniform(-180, 180), 7)
                
                shipment = {
                    'shipment_id': shipment_id,
                    'order_id': order['order_id'],
                    'carrier_id': carrier_id,
                    'tracking_number': f"TRK{uuid.uuid4().hex[:12].upper()}",
                    'current_location': f"{order['city']}, {order['country']}",
                    'status': status,
                    'shipped_date': shipped_date,
                    'estimated_delivery': estimated_delivery,
                    'actual_delivery': actual_delivery,
                    'latitude': latitude,
                    'longitude': longitude,
                    'last_updated': datetime.now()
                }
                shipments.append(shipment)
        
        return pd.DataFrame(shipments)
    
    def generate_inventory(
        self,
        product_ids: List[str] = None,
        n_warehouses: int = 5
    ) -> pd.DataFrame:
        """Generate inventory data"""
        inventory = []
        
        if product_ids is None:
            product_ids = [f"PROD{str(i+1).zfill(6)}" for i in range(200)]
        
        warehouse_ids = [f"WH{str(i+1).zfill(3)}" for i in range(n_warehouses)]
        
        for product_id in product_ids:
            for warehouse_id in random.sample(warehouse_ids, random.randint(1, 3)):
                quantity_available = random.randint(0, 500)
                
                inventory_record = {
                    'product_id': product_id,
                    'warehouse_id': warehouse_id,
                    'quantity_available': quantity_available,
                    'reorder_level': random.randint(50, 100),
                    'last_updated': datetime.now()
                }
                inventory.append(inventory_record)
        
        return pd.DataFrame(inventory)
    
    def generate_all_data(self, n_orders: int = 1000) -> Dict[str, pd.DataFrame]:
        """Generate complete dataset"""
        print("🔄 Generating supply chain data...")
        
        # Generate base data
        print("   📦 Generating suppliers...")
        suppliers_df = self.generate_suppliers(50)
        
        print("   🚚 Generating carriers...")
        carriers_df = self.generate_carriers()
        
        print("   📦 Generating products...")
        products_df = self.generate_products(200, suppliers_df['supplier_id'].tolist())
        
        print("   🛒 Generating orders...")
        orders_df = self.generate_orders(n_orders, product_ids=products_df['product_id'].tolist())
        
        print("   📬 Generating shipments...")
        shipments_df = self.generate_shipments(orders_df, carriers_df['carrier_id'].tolist())
        
        print("   📊 Generating inventory...")
        inventory_df = self.generate_inventory(products_df['product_id'].tolist())
        
        print("✅ Data generation completed!")
        
        return {
            'suppliers': suppliers_df,
            'carriers': carriers_df,
            'products': products_df,
            'orders': orders_df,
            'shipments': shipments_df,
            'inventory': inventory_df
        }


# Quick test
if __name__ == "__main__":
    generator = SupplyChainDataGenerator()
    data = generator.generate_all_data(n_orders=100)
    
    print("\n📊 Dataset Summary:")
    for name, df in data.items():
        print(f"   {name}: {len(df)} records")