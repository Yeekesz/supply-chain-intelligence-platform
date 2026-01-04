"""
Main script to load data into database
Run from project root: python load_data.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.data_loader import DataLoader

if __name__ == "__main__":
    print("🚀 Starting data loading...\n")
    loader = DataLoader()
    loader.load_all_data(n_orders=1000, clean_first=True)