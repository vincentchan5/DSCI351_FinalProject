import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure it's set in your .env file.")

client = OpenAI(api_key=api_key)

def generate_query(nl_query):
    if any(keyword in nl_query.lower() for keyword in ["sql", "mysql", "relational"]):
        nl_query += "\n\nRespond using SQL only."

    system_prompt = """
Converts natural language questions into database queries.

Assume the following schema:

🔸 MySQL (Structured):

  Table: patients
  Columns:
    - id (int)
    - name (string)
    - gender (string)
    - state (string)

  Table: diabetes
  Columns:
    - id (int)
    - Pregnancies (int)
    - Glucose (int)
    - BloodPressure (int)
    - SkinThickness (int)
    - Insulin (int)
    - BMI (float)
    - DiabetesPedigreeFunction (float)
    - Age (int)
    - Outcome (int)

🔹 MongoDB (Document):

  Note: All NBA player data is stored in MongoDB in the `players` collection.
  Note: All ecommerce product data is stored in MongoDB in the `ecommerce` collection.

  Collection: players
    Fields:
      - RANK (int)
      - NAME (string)
      - TEAM (string)
      - POS (string)
      - AGE (float)
      - GP (int)
      - MPG (float)
      - USG% (float)
      - TO% (float)
      - FTA (int)
      - FT% (float)
      - 2PA (int)
      - 2P% (float)
      - 3PA (int)
      - 3P% (float)
      - eFG% (float)
      - TS% (float)
      - PPG (float)
      - RPG (float)
      - APG (float)
      - SPG (float)
      - BPG (float)
      - TPG (float)
      - P+R (float)
      - P+A (float)
      - P+R+A (float)
      - VI (float)
      - ORtg (float)
      - DRtg (float)

  Collection: ecommerce
    Fields:
      - _id (string)
      - actual_price (string, formatted like "2,999")
      - average_rating (float)
      - brand (string)
      - category (string)
      - crawled_at (datetime)
      - description (string)
      - discount (string)
      - images (array of URLs)
      - out_of_stock (boolean)
      - pid (string)
      - product_details (array)

SPECIAL RULE:
The field `actual_price` is a string and must be cast to a number.

NEVER sort directly on `actual_price`.
INSTEAD:
1. Use `$replaceAll` to remove commas
2. Use `$toDouble` to convert the result to a number
3. Add "onError": null and "onNull": null to handle empty/invalid values
4. Use `$match` to exclude null results before sorting

Example:
{
  "$addFields": {
    "numeric_price": {
      "$toDouble": {
        "input": {
          "$replaceAll": {
            "input": "$actual_price",
            "find": ",",
            "replacement": ""
          }
        },
        "onError": null,
        "onNull": null
      }
    }
  }
},
{ "$match": { "numeric_price": { "$ne": null } } },
{ "$sort": { "numeric_price": -1 } },
{ "$limit": 5 }

Always sort using `numeric_price`, not `actual_price`.

ONLY respond using one of the following formats:

TYPE: sql
SELECT * FROM diabetes WHERE Glucose > 150;

OR

TYPE: mongo
{
  "collection": "ecommerce",
  "operation": "aggregate",
  "pipeline": [...]
}

NEVER explain the query. Just return the code block only.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": nl_query}
            ],
            max_tokens=300,
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()
        print("GPT Output:\n", content)

        lines = content.split("\n")
        if not lines or ":" not in lines[0]:
            print("Raw GPT response did not follow format:\n", content)
            raise ValueError("Invalid response from language model.")

        db_type = lines[0].split(":")[1].strip().lower()
        query = "\n".join(lines[1:]).strip()

        return db_type, query

    except Exception as e:
        print("LLM Error:", e)
        raise ValueError("Invalid response from language model.")
