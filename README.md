# 🚀 DataFlow Supply Chain Intelligence Platform

<div align="center">

![Supply Chain](https://img.shields.io/badge/Supply_Chain-Real--Time-blue)
![Data Engineering](https://img.shields.io/badge/Data_Engineering-Pipeline-green)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-red)

**Real-time supply chain intelligence platform with predictive analytics and automated data pipelines**

[Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Components](#-components)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**DataFlow Supply Chain Platform** is an end-to-end data engineering project that demonstrates real-time supply chain intelligence capabilities. The platform processes and analyzes logistics data across orders, shipments, inventory, and suppliers to provide actionable insights for supply chain optimization.

### Key Highlights

- 🏗️ **Production-grade infrastructure** with Docker Compose
- 📊 **Real-time streaming** with Apache Kafka
- ⚙️ **Workflow orchestration** with Apache Airflow
- 📈 **Interactive dashboards** with Streamlit
- 🗄️ **Scalable data architecture** with Star Schema
- 🔄 **Complete ETL pipeline** from ingestion to visualization

---

## ✨ Features

### Data Engineering
- ✅ **Multi-source data ingestion** (PostgreSQL, MongoDB, Kafka)
- ✅ **Real-time streaming pipeline** with Kafka producers/consumers
- ✅ **Batch processing** with scheduled ETL jobs
- ✅ **Data quality validation** and monitoring
- ✅ **Star schema data warehouse** design

### Analytics & Visualization
- ✅ **Real-time KPI dashboards** (Orders, Revenue, Delivery Performance)
- ✅ **Interactive charts** (Bar, Pie, Line, Maps)
- ✅ **Geospatial analysis** with shipment tracking
- ✅ **Auto-refreshing metrics** from live data streams

### Infrastructure
- ✅ **Containerized services** with Docker Compose
- ✅ **Scalable architecture** supporting 1000+ orders/day
- ✅ **Monitoring & logging** capabilities
- ✅ **CI/CD ready** structure

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL  │  MongoDB  │  Kafka Stream  │  External APIs      │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                     INGESTION LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  • Kafka Producers (Real-time Orders)                           │
│  • Data Generators (Suppliers, Products, Inventory)             │
│  • API Connectors                                                │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  • Kafka Consumers (Stream Processing)                           │
│  • Airflow DAGs (Batch ETL)                                      │
│  • Data Transformation & Validation                              │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  • PostgreSQL (Raw, Staging, Analytics)                          │
│  • MongoDB (Product Catalog)                                     │
│  • Redis (Caching)                                               │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  • Streamlit Dashboard (Real-time Metrics)                       │
│  • FastAPI (REST API - Optional)                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Technologies

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.12 |
| **Orchestration** | Apache Airflow 2.10 |
| **Streaming** | Apache Kafka 7.5, Zookeeper |
| **Databases** | PostgreSQL 15, MongoDB 7.0, Redis 7.0 |
| **Visualization** | Streamlit, Plotly |
| **Containerization** | Docker, Docker Compose |
| **Data Processing** | Pandas, SQLAlchemy |
| **Testing** | Pytest |

### Python Libraries
```
confluent-kafka==2.3.0
sqlalchemy==2.0.25
pandas==2.1.4
streamlit==1.30.0
plotly==5.18.0
faker==22.0.0
```

---

## 📁 Project Structure
```
dataflow-supply-chain/
├── src/
│   ├── ingestion/          # Data generation & loading
│   ├── streaming/          # Kafka producers/consumers
│   ├── transformation/     # Data transformations
│   ├── warehouse/          # Star schema logic
│   └── utils/              # DB connectors, logging
│
├── airflow/
│   └── dags/               # ETL workflow definitions
│
├── dashboards/
│   ├── main_dashboard.py   # Streamlit dashboard
│   ├── pages/              # Multi-page layouts
│   └── components/         # Reusable UI components
│
├── kafka/
│   ├── producers/          # Order stream producers
│   └── consumers/          # Stream processors
│
├── infrastructure/
│   └── docker/
│       ├── docker-compose.yml
│       └── init-scripts/   # Database initialization
│
├── data/
│   ├── raw/                # Bronze layer
│   ├── processed/          # Silver layer
│   └── analytics/          # Gold layer
│
├── config/
│   └── config.yaml         # Application configuration
│
├── producer.py             # Kafka order producer
├── consumer.py             # Kafka order consumer
├── check_data.py           # Database verification
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- 8GB RAM minimum
- WSL2 (for Windows users)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/dataflow-supply-chain.git
cd dataflow-supply-chain
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start infrastructure**
```bash
docker-compose up -d
```

Wait 2-3 minutes for all services to start.

5. **Initialize database & load data**
```bash
python load_data.py
```

6. **Start Kafka streaming** (Optional - for real-time demo)

Terminal 1 - Producer:
```bash
python3 producer.py
```

Terminal 2 - Consumer:
```bash
python3 consumer.py
```

7. **Launch dashboard**
```bash
streamlit run dashboards/main_dashboard.py
```

Open browser: `http://localhost:8501`

---

## 🔧 Components

### 1. Data Generation
- Generates realistic supply chain data (Orders, Products, Suppliers)
- Faker library for realistic names and locations
- Configurable data volumes

### 2. Real-time Streaming
- **Producer**: Streams new orders every 3 seconds
- **Consumer**: Processes and stores orders in PostgreSQL
- **Kafka UI**: Monitor topics at `http://localhost:8080`

### 3. Batch Processing
- **Airflow DAGs**: Scheduled ETL pipelines
- **Airflow UI**: `http://localhost:8081` (admin/admin)
- Daily transformations from Raw → Staging → Analytics

### 4. Data Warehouse
- **Star Schema** design with fact and dimension tables
- **Layers**: Bronze (raw) → Silver (cleaned) → Gold (analytics)
- Optimized for analytical queries

### 5. Dashboard
- Real-time KPIs and metrics
- Interactive charts and maps
- Auto-refresh every 30 seconds

---

## 📸 Screenshots

### Dashboard Overview
*Real-time supply chain metrics and KPIs*

![Dashboard](docs/screenshots/dashboard.png)

### Kafka Streaming
*Live order processing*

![Streaming](docs/screenshots/streaming.png)

### Airflow Pipeline
*Automated ETL workflows*

![Airflow](docs/screenshots/airflow.png)

---

## 🔮 Future Enhancements

- [ ] ML-based demand forecasting
- [ ] Delivery time prediction model
- [ ] Anomaly detection system
- [ ] Great Expectations data quality framework
- [ ] Spark for large-scale processing
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Cloud deployment (AWS/Azure)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

## 👤 Author

**Buthainah**

- GitHub: [@Buthainah3524](https://github.com/Buthainah3524)

---

## 📧 Contact

For questions or collaboration opportunities, feel free to reach out!

- 📧 Email: [Contact via GitHub](https://github.com/Buthainah3524)
- 🐙 GitHub: [@Buthainah3524](https://github.com/Buthainah3524)

---

## 🙏 Acknowledgments

- Inspired by real-world supply chain challenges
- Built as a Data Engineering portfolio project
- Special thanks to the open-source community

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for Data Engineering Excellence

</div>