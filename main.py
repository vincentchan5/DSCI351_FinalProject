from llm.query_generator import generate_query
from db.mysql_runner import run_mysql_query
from db.mongo_runner import run_mongo_query

def main():
    print("Welcome to ChatDB!")

    while True:
        user_input = input("\nAsk a question (or type 'exit'): ").strip()

        if user_input.lower() == "exit":
            print("Exiting ChatDB.")
            break

        if not user_input:
            print("No input detected. Please ask a question or type 'exit'.")
            continue

        try:
            db_type, query = generate_query(user_input)
            print(f"\nInterpreted as a {db_type.upper()} query:\n{query}\n")

            if db_type == "sql":
                result = run_mysql_query(query)
            elif db_type == "mongo":
                result = run_mongo_query(query)
            else:
                result = "Unknown database type returned."

            print("Result:\n", result)
            print("Ready for your next question...")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
