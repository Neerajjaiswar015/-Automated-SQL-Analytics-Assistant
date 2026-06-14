from flask import Flask, render_template, request, jsonify
from llm_helper import generate_sql
from db_handler import execute_query
import json

app = Flask(__name__)

@app.route('/')
def home():
    # Renders the main interface page
    return render_template('index.html')

@app.route('/get_analytics', methods=['POST'])
def get_analytics():
    user_data = request.json
    english_question = user_data.get('question', '')
    
    if not english_question:
        return jsonify({"error": "Please enter a valid question."}), 400
        
    # 1. Generate SQL from natural language
    generated_sql = generate_sql(english_question)
    
    if generated_sql.startswith("Error"):
        return jsonify({"error": generated_sql, "sql": ""}), 500
        
    # 2. Execute against the database safely
    execution_result = execute_query(generated_sql)
    
    # ==========================================
    # PHASE 7: Dynamic Error Recovery (AI Retry)
    # ==========================================
    # If there is an error AND it's not our intentional security guardrail blocking a DROP/DELETE command
    # if execution_result["error"] and "Security Alert" not in execution_result["error"]:
    #     print(f"SQL execution failed. Attempting auto-correction...")
        
    #     # Craft a corrective prompt to fix the syntax error
    #     fix_prompt = f"""
    #     The previous SQL query you generated failed with this error: {execution_result["error"]}
    #     The query was: {generated_sql}
    #     Please regenerate a corrected, valid SQLite query to answer the user's question: '{english_question}'
    #     """
        
    #     # Re-run through the LLM and Database one more time
    #     generated_sql = generate_sql(fix_prompt)
    #     execution_result = execute_query(generated_sql)
    # ==========================================
    
    # If it STILL fails after the retry (or if it was a security alert), return the error
    if execution_result["error"]:
        return jsonify({
            "error": execution_result["error"], 
            "sql": generated_sql
        }), 400
        
    df = execution_result["data"]
    
    # 3. Format the data for the frontend
    # Convert dataframe into a dictionary list for HTML table mapping
    table_data = df.to_dict(orient='records')
    columns = list(df.columns)
    
    # 4. Auto-Visualization Rules Engine
    chart_type = "none"
    chart_labels = []
    chart_values = []
    
    if not df.empty and len(columns) >= 2:
        # Rule: If we have a text/date column and a numeric column, let's chart it!
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        
        if numeric_cols and categorical_cols:
            chart_type = "bar" # Default to bar chart
            
            # Use the first categorical column as X axis and first numeric as Y axis
            x_col = categorical_cols[0]
            y_col = numeric_cols[0]
            
            # Rule exception: If the X axis contains dates, make it a Line chart
            if 'date' in x_col.lower() or 'month' in x_col.lower():
                chart_type = "line"
                
            chart_labels = df[x_col].astype(str).tolist()
            chart_values = df[y_col].tolist()
    
    return jsonify({
        "sql": generated_sql,
        "columns": columns,
        "table_data": table_data,
        "chart_type": chart_type,
        "chart_labels": chart_labels,
        "chart_values": chart_values
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)