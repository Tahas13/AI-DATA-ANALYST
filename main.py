#Step1: Extract Schema
from sqlalchemy import create_engine, inspect
import json
import re
import sqlite3
import time

db_url = "sqlite:///amazon.db"

def extract_schema(db_url):
    t0 = time.time()
    print("[TIMER] extract_schema: started")
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]
    result = json.dumps(schema)
    print(f"[TIMER] extract_schema: done in {time.time() - t0:.2f}s")
    return result


#Step2: Text to SQL (DeepSeek with Ollama)
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


def text_to_sql(schema, prompt, error_feedback=None):
    SYSTEM_PROMPT = """
    You are an expert SQL generator for SQLite. Given a database schema and a user prompt, generate a valid SQL query.
    Rules:
    - ONLY use tables and columns that exist in the schema.
    - When a query needs columns from multiple tables, always use proper JOINs with correct ON conditions.
    - Never reference a column without its table name if it exists in more than one table.
    - Use aggregate functions (SUM, COUNT, etc.) with GROUP BY when needed.
    - Output ONLY the raw SQL query. No explanation, no markdown, no <think> tags.
    """

    t0 = time.time()
    print("[TIMER] text_to_sql: building prompt template")

    user_message = "Schema:\n{schema}\n\nQuestion: {user_prompt}\n\nSQL Query:"
    if error_feedback:
        user_message += f"\n\nThe previous query failed with this error: {error_feedback}\nPlease fix the SQL."

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", user_message)
    ])

    print(f"[TIMER] text_to_sql: loading OllamaLLM model ({time.time() - t0:.2f}s so far)")
    model = OllamaLLM(model="llama3.2:3b", temperature=0, num_predict=200) # fast non-reasoning model

    chain = prompt_template | model

    print(f"[TIMER] text_to_sql: sending prompt to LLM ({time.time() - t0:.2f}s so far)")
    raw_response = chain.invoke({"schema": schema, "user_prompt": prompt})
    print(f"[TIMER] text_to_sql: LLM responded ({time.time() - t0:.2f}s so far)")

    cleaned_response = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL)
    print(f"[TIMER] text_to_sql: done in {time.time() - t0:.2f}s")
    return cleaned_response.strip()



def get_data_from_database(prompt):
    total_t0 = time.time()
    print("\n[TIMER] ── get_data_from_database: START ──")

    print("[TIMER] Step 1: Extracting schema...")
    schema = extract_schema(db_url)

    print(f"[TIMER] Step 2: Generating SQL via LLM... ({time.time() - total_t0:.2f}s elapsed)")
    sql_query = text_to_sql(schema, prompt)
    print(f"[TIMER] Generated SQL: {sql_query}")

    print(f"[TIMER] Step 3: Querying database... ({time.time() - total_t0:.2f}s elapsed)")
    conn = sqlite3.connect("amazon.db")
    cursor = conn.cursor()
    try:
        res = cursor.execute(sql_query)
    except Exception as e:
        print(f"[TIMER] SQL failed: {e}. Retrying with error feedback...")
        conn.close()
        sql_query = text_to_sql(schema, prompt, error_feedback=str(e))
        print(f"[TIMER] Retry SQL: {sql_query}")
        conn = sqlite3.connect("amazon.db")
        cursor = conn.cursor()
        res = cursor.execute(sql_query)

    rows = res.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    conn.close()

    print(f"[TIMER] ── TOTAL TIME: {time.time() - total_t0:.2f}s ──\n")
    return {
        "query": sql_query,
        "columns": columns,
        "rows": rows
    }