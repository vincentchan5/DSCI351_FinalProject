import pandas as pd
import pymysql

def run_mysql_query(query):
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="dsci-351",
            database="chatdb"
        )
        cursor = conn.cursor()

        if query.strip().lower().startswith("select"):
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            return df.to_string(index=False)

        else:
            cursor.execute(query)
            conn.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"

    except Exception as e:
        return f"SQL Error: {e}"

    finally:
        if conn:
            conn.close()
