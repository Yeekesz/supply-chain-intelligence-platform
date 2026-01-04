-- Create Airflow database
CREATE DATABASE airflow_db;

-- Connect to main database
\c dataflow_supply_chain;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Orders Table
CREATE TABLE IF NOT EXISTS raw.orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    expected_delivery_date TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    shipping_address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shipments Table
CREATE TABLE IF NOT EXISTS raw.shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    carrier_id VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(100),
    current_location VARCHAR(200),
    status VARCHAR(20) NOT NULL,
    shipped_date TIMESTAMP,
    estimated_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Table
CREATE TABLE IF NOT EXISTS raw.inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    warehouse_id VARCHAR(50) NOT NULL,
    quantity_available INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE IF NOT EXISTS raw.products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    supplier_id VARCHAR(50),
    unit_price DECIMAL(10, 2) NOT NULL,
    weight_kg DECIMAL(8, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers Table
CREATE TABLE IF NOT EXISTS raw.suppliers (
    supplier_id VARCHAR(50) PRIMARY KEY,
    supplier_name VARCHAR(200) NOT NULL,
    country VARCHAR(100),
    rating DECIMAL(3, 2),
    lead_time_days INTEGER,
    reliability_score DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Carriers Table
CREATE TABLE IF NOT EXISTS raw.carriers (
    carrier_id VARCHAR(50) PRIMARY KEY,
    carrier_name VARCHAR(100) NOT NULL,
    avg_rating DECIMAL(3, 2),
    cost_per_kg DECIMAL(8, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_orders_date ON raw.orders(order_date);
CREATE INDEX idx_shipments_order ON raw.shipments(order_id);
CREATE INDEX idx_inventory_product ON raw.inventory(product_id);

-- Analytics: Dimension Tables
CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

-- Analytics: Fact Tables
CREATE TABLE IF NOT EXISTS analytics.fact_orders (
    order_fact_key SERIAL PRIMARY KEY,
    order_id VARCHAR(50),
    date_key INTEGER,
    quantity INTEGER,
    total_amount DECIMAL(12, 2),
    delivery_days INTEGER,
    was_delayed BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA raw TO dataflow_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO dataflow_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO dataflow_admin;