import sqlite3
import pandas as pd
import re

# The path to the database file we created in Step 2
DB_PATH = 'cloud_kitchens.db'

# A list of destructive SQL commands we want to block
FORBIDDEN_KEYWORDS = [
    'drop', 'delete', 'insert', 'update', 'alter', 
    'truncate', 'grant', 'revoke', 'commit'
]

def execute_query(sql_query):
    """
    Safely executes a SELECT query and returns a Pandas DataFrame.
    """
    # 1. Validation Layer (Guardrails)
    # Convert query to lowercase and remove non-alphanumeric characters for safe checking
    clean_query = sql_query.lower()
    
    for word in FORBIDDEN_KEYWORDS:
        # Use regex to find exact word matches to avoid blocking words like 'update_date'
        if re.search(rf'\b{word}\b', clean_query):
            return {"error": f"Security Alert: Destructive command '{word.upper()}' is not allowed. Only SELECT queries are permitted.", "data": None}

    # 2. Execution Layer
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        
        # Read the SQL query directly into a Pandas DataFrame
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        return {"error": None, "data": df}
    
    except Exception as e:
        # Catch syntax errors or missing tables
        return {"error": str(e), "data": None}

# ==========================================
# Testing the file locally
# ==========================================
if __name__ == "__main__":
    print("Testing Valid Query...")
    result = execute_query("SELECT delivery_location, COUNT(*) as total_orders FROM orders GROUP BY delivery_location")
    if result["error"]:
        print("Error:", result["error"])
    else:
        print(result["data"])
        
    print("\nTesting Malicious Query...")
    bad_result = execute_query("DROP TABLE orders;")
    print(bad_result["error"])