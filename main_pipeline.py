from llm_helper import generate_sql
from db_handler import execute_query

def run_analytics_pipeline(english_question):
    """
    Orchestrates the full natural language to data result pipeline.
    """
    print(f"\nStep 1: Receiving user question: '{english_question}'")
    
    # 1. Ask the LLM to write the SQL
    generated_sql = generate_sql(english_question)
    print(f"Step 2: LLM Generated SQL:\n   {generated_sql}")
    
    # Check if the LLM generation itself errored out
    if generated_sql.startswith("Error"):
        print(f"Pipeline halted: {generated_sql}")
        return
        
    # 2. Run the generated SQL through our safe DB handler
    print("Step 3: Validating and executing query against database...")
    execution_result = execute_query(generated_sql)
    
    # 3. Handle and print the results
    if execution_result["error"]:
        print(f"Execution Error: {execution_result['error']}")
    else:
        df = execution_result["data"]
        print("\nStep 4: Success! Retrieved Data Frame:")
        if df.empty:
            print("   (The query executed successfully, but returned 0 rows.)")
        else:
            print(df.to_string(index=False))

# ==========================================
# Testing the complete pipeline
# ==========================================
if __name__ == "__main__":
    print("=== PIPELINE RUN 1 ===")
    run_analytics_pipeline("Show me the top 3 best rated orders along with their brand names")
    
    print("\n" + "="*40 + "\n")
    
    print("=== PIPELINE RUN 2 ===")
    run_analytics_pipeline("What is the total revenue generated in Kandivali East?")