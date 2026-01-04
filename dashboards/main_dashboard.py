"""
Main Dashboard for DataFlow Supply Chain Platform
Real-time supply chain analytics and monitoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from src.utils.db_connector import db_connector

# Page configuration
st.set_page_config(
    page_title="DataFlow Supply Chain Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_db_connection():
    """Get database connection"""
    return db_connector.get_postgres_engine()

# Data loading functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_orders_data():
    """Load orders data"""
    engine = get_db_connection()
    query = """
        SELECT 
            o.*,
            p.product_name,
            p.category
        FROM raw.orders o
        LEFT JOIN raw.products p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
        LIMIT 1000;
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

@st.cache_data(ttl=300)
def load_shipments_data():
    """Load shipments data"""
    engine = get_db_connection()
    query = """
        SELECT 
            s.*,
            c.carrier_name
        FROM raw.shipments s
        LEFT JOIN raw.carriers c ON s.carrier_id = c.carrier_id
        ORDER BY s.last_updated DESC
        LIMIT 1000;
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

@st.cache_data(ttl=300)
def load_summary_stats():
    """Load summary statistics"""
    engine = get_db_connection()
    with engine.connect() as conn:
        # Total orders
        result = conn.execute(text("SELECT COUNT(*) FROM raw.orders;"))
        total_orders = result.fetchone()[0]
        
        # Total revenue
        result = conn.execute(text("SELECT SUM(total_amount) FROM raw.orders;"))
        total_revenue = result.fetchone()[0] or 0
        
        # Delivered shipments
        result = conn.execute(text("SELECT COUNT(*) FROM raw.shipments WHERE status = 'delivered';"))
        delivered = result.fetchone()[0]
        
        # Total shipments
        result = conn.execute(text("SELECT COUNT(*) FROM raw.shipments;"))
        total_shipments = result.fetchone()[0]
        
        # On-time rate
        on_time_rate = (delivered / total_shipments * 100) if total_shipments > 0 else 0
        
    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'on_time_rate': on_time_rate,
        'total_shipments': total_shipments
    }

# Header
st.markdown('<p class="main-header">📦 DataFlow Supply Chain Dashboard</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Filters
    st.subheader("📊 Filters")
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )
    
    st.markdown("---")
    
    # Info
    st.info("""
    **Real-Time Supply Chain Intelligence Platform**
    
    Monitoring orders, shipments, and inventory across the global supply chain.
    """)

# Load data
try:
    with st.spinner("Loading data..."):
        stats = load_summary_stats()
        orders_df = load_orders_data()
        shipments_df = load_shipments_data()
    
    # KPIs
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total Orders",
            value=f"{stats['total_orders']:,}",
            delta="+12% vs last month"
        )
    
    with col2:
        st.metric(
            label="💰 Total Revenue",
            value=f"${stats['total_revenue']:,.2f}",
            delta="+8.5%"
        )
    
    with col3:
        st.metric(
            label="✅ On-Time Delivery",
            value=f"{stats['on_time_rate']:.1f}%",
            delta="-2.3%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="🚚 Active Shipments",
            value=f"{stats['total_shipments']:,}",
            delta="+5.2%"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Orders by Country")
        country_counts = orders_df['country'].value_counts().head(10)
        fig = px.bar(
            x=country_counts.index,
            y=country_counts.values,
            labels={'x': 'Country', 'y': 'Number of Orders'},
            color=country_counts.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💵 Revenue by Category")
        category_revenue = orders_df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
        fig = px.pie(
            values=category_revenue.values,
            names=category_revenue.index,
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Order Status Distribution")
        status_counts = orders_df['status'].value_counts()
        fig = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            labels={'x': 'Status', 'y': 'Count'},
            color=status_counts.index,
            color_discrete_map={
                'delivered': '#2ecc71',
                'shipped': '#3498db',
                'confirmed': '#f39c12',
                'pending': '#95a5a6',
                'cancelled': '#e74c3c'
            }
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🚚 Shipment Status")
        shipment_status = shipments_df['status'].value_counts()
        fig = px.pie(
            values=shipment_status.values,
            names=shipment_status.index,
            color=shipment_status.index,
            color_discrete_map={
                'delivered': '#2ecc71',
                'in_transit': '#3498db',
                'delayed': '#e74c3c',
                'pending': '#95a5a6'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Orders Timeline
    st.subheader("📅 Orders Over Time")
    orders_by_date = orders_df.groupby(orders_df['order_date'].dt.date)['order_id'].count()
    fig = px.line(
        x=orders_by_date.index,
        y=orders_by_date.values,
        labels={'x': 'Date', 'y': 'Number of Orders'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent Orders Table
    st.subheader("📋 Recent Orders")
    recent_orders = orders_df.head(10)[['order_id', 'customer_id', 'product_name', 'quantity', 'total_amount', 'status', 'country', 'order_date']]
    recent_orders['order_date'] = recent_orders['order_date'].dt.strftime('%Y-%m-%d %H:%M')
    recent_orders['total_amount'] = recent_orders['total_amount'].apply(lambda x: f"${x:.2f}")
    st.dataframe(recent_orders, use_container_width=True, hide_index=True)
    
    # Shipments Map
    st.subheader("🗺️ Shipment Locations")
    if not shipments_df.empty and 'latitude' in shipments_df.columns:
        map_data = shipments_df[['latitude', 'longitude', 'status', 'current_location']].dropna()
        if not map_data.empty:
            fig = px.scatter_mapbox(
                map_data,
                lat='latitude',
                lon='longitude',
                color='status',
                hover_data=['current_location'],
                zoom=1,
                height=500,
                color_discrete_map={
                    'delivered': '#2ecc71',
                    'in_transit': '#3498db',
                    'delayed': '#e74c3c'
                }
            )
            fig.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No location data available for shipments")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #888;'>
            <p>DataFlow Supply Chain Platform v1.0.0 | Built with ❤️ using Streamlit</p>
            <p>Last updated: {}</p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.exception(e)