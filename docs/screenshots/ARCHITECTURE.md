# 🏗️ System Architecture

## Overview

DataFlow Supply Chain Platform follows a modern data engineering architecture with clear separation of concerns across ingestion, processing, storage, and presentation layers.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES LAYER                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📊 PostgreSQL    📦 MongoDB    🌐 External APIs    📄 Files        │
│  (Orders DB)      (Catalog)     (Weather, Maps)     (CSV/JSON)      │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        INGESTION LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ⚡ Kafka Producers          🔄 Data Generators                      │
│  • Order Stream              • Suppliers (50)                        │
│  • Shipment Updates          • Products (200)                        │
│  • Inventory Changes         • Orders (1000+)                        │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Stream Processing           Batch Processing                        │
│  ┌─────────────────┐        ┌──────────────────┐                   │
│  │ Kafka Consumer  │        │  Airflow DAGs    │                   │
│  │ • Validation    │        │  • Extract       │                   │
│  │ • Transform     │        │  • Transform     │                   │
│  │ • Load to DB    │        │  • Load          │                   │
│  └─────────────────┘        └──────────────────┘                   │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        STORAGE LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  🗄️ Data Warehouse (PostgreSQL)                                     │
│  ├─ Raw Schema (Bronze)      - Source data as-is                    │
│  ├─ Staging Schema (Silver)  - Cleaned & validated                  │
│  └─ Analytics Schema (Gold)  - Star schema (Facts & Dimensions)     │
│                                                                       │
│  📦 MongoDB                   ⚡ Redis                               │
│  Product catalog              Caching layer                          │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📊 Streamlit Dashboard                                              │
│  • Real-time KPIs                                                    │
│  • Interactive Charts                                                │
│  • Geospatial Maps                                                   │
│  • Auto-refresh (30s)                                                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Real-time Flow (Kafka Streaming)

1. **Producer** generates new order → Sends to Kafka topic `orders`
2. **Kafka** buffers and distributes messages
3. **Consumer** receives order → Validates data → Inserts into PostgreSQL
4. **Dashboard** queries database → Updates metrics in real-time

### Batch Flow (Airflow ETL)

1. **Airflow Scheduler** triggers DAG daily at 2 AM
2. **Extract**: Pull data from raw tables
3. **Transform**: Clean, enrich, calculate metrics
4. **Load**: Insert into analytics star schema
5. **Report**: Generate daily summary

## Technology Decisions

### Why Kafka?
- ✅ Real-time data streaming
- ✅ Decouples producers from consumers
- ✅ Handles high throughput (1000+ msgs/sec)
- ✅ Fault-tolerant and scalable

### Why Star Schema?
- ✅ Optimized for analytical queries
- ✅ Easy to understand and maintain
- ✅ Supports complex aggregations
- ✅ Separates facts from dimensions

### Why Docker Compose?
- ✅ Consistent environment across machines
- ✅ Easy to spin up/down services
- ✅ Simulates production setup locally
- ✅ Version-controlled infrastructure

## Scalability Considerations

- **Kafka**: Can scale to multiple brokers and partitions
- **PostgreSQL**: Supports read replicas and sharding
- **Docker**: Can deploy to Kubernetes for orchestration
- **Airflow**: Supports multiple executors (Celery, Kubernetes)

## Security (Production Enhancements)

- [ ] SSL/TLS for all connections
- [ ] Database credentials in secrets manager
- [ ] API authentication tokens
- [ ] Network isolation with VPCs
- [ ] Audit logging for all operations