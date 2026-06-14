import google.generativeai as genai

# Paste your free Gemini API key here
genai.configure(api_key="GEMINI_API_KEY") 

SYSTEM_PROMPT = """
You are an expert SQL assistant for a food delivery cloud kitchen company. 
Your job is to translate natural language questions into valid, syntactically correct SQLite queries.

Here is the database schema:
- `brands` (brand_id, brand_name, category)
- `orders` (order_id, brand_id, delivery_location, order_value, rating, order_date)

Rules:
1. Return ONLY the raw SQL code. 
2. Do not include markdown formatting like ```sql.
3. Do not explain the code.
4. Never use destructive commands (DROP, DELETE, UPDATE, INSERT). Only use SELECT.
"""

def generate_sql(user_question):
    """
    Sends the user's question and the database schema to the LLM to get a SQL query.
    """
    try:
        # Using gemini-3.1-flash for fast, free text generation
        model = genai.GenerativeModel(
            'gemini-3.1-flash-lite',
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(user_question)
        
        # Extract and clean the text
        raw_sql = response.text.strip()
        clean_sql = raw_sql.replace("```sql", "").replace("```", "").strip()
        
        return clean_sql
        
    except Exception as e:
        return f"Error generating SQL: {str(e)}"

# ==========================================
# Testing the file locally
# ==========================================
if __name__ == "__main__":
    test_question = "What is the total order value for Behrouz Biryani?"
    print(f"Question: {test_question}")
    
    generated_sql = generate_sql(test_question)
    print(f"\nGenerated SQL:\n{generated_sql}")