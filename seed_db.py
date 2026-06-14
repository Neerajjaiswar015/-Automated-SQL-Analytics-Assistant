import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

# 1. Connect to SQLite (this creates the file 'cloud_kitchens.db' if it doesn't exist)
conn = sqlite3.connect('cloud_kitchens.db')
cursor = conn.cursor()

# 2. Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS brands (
    brand_id INTEGER PRIMARY KEY,
    brand_name TEXT,
    category TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    brand_id INTEGER,
    delivery_location TEXT,
    order_value REAL,
    rating INTEGER,
    order_date TEXT,
    FOREIGN KEY(brand_id) REFERENCES brands(brand_id)
)
''')

# 3. Insert Mock Data (Brands)
brands_data = [
    (1, 'Faasos', 'Wraps'),
    (2, 'Behrouz Biryani', 'Biryani'),
    (3, 'Oven Story', 'Pizza'),
    (4, 'Lunchbox', 'Thalis')
]
cursor.executemany('INSERT OR IGNORE INTO brands VALUES (?, ?, ?)', brands_data)

# 4. Generate Mock Data (Orders)
locations = ['Kandivali East', 'Borivali West', 'Malad East', 'Andheri West', 'Goregaon East']
orders_data = []

# Generate 100 random orders over the last 30 days
base_date = datetime.now()
for i in range(1, 101):
    brand_id = random.randint(1, 4)
    loc = random.choice(locations)
    value = round(random.uniform(150.0, 850.0), 2)
    rating = random.randint(1, 5)
    
    # Random date within the last 30 days
    days_ago = random.randint(0, 30)
    order_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    orders_data.append((i, brand_id, loc, value, rating, order_date))

cursor.executemany('INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?, ?)', orders_data)

# Commit and close
conn.commit()
conn.close()

print("Database 'cloud_kitchens.db' created and seeded successfully!")