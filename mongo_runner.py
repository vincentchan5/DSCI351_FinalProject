import ast
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]


def run_mongo_query(query_string):
    try:
        query_dict = ast.literal_eval(query_string)
        collection_name = query_dict["collection"]
        collection = db[collection_name]

        if query_dict["operation"] == "find":
            cursor = collection.find(query_dict.get("filter", {}), query_dict.get("projection", {}))
            return list(cursor)

        elif query_dict["operation"] == "aggregate":
            pipeline = query_dict["pipeline"]
            return list(collection.aggregate(pipeline))

        elif query_dict["operation"] == "insertOne":
            return collection.insert_one(query_dict["document"]).inserted_id

        elif query_dict["operation"] == "insertMany":
            return collection.insert_many(query_dict["documents"]).inserted_ids

        elif query_dict["operation"] == "updateOne":
            return collection.update_one(query_dict["filter"], query_dict["update"]).raw_result

        elif query_dict["operation"] == "deleteOne":
            return collection.delete_one(query_dict["filter"]).raw_result

        else:
            return "Unsupported Mongo operation."

    except Exception as e:
        return f"MongoDB Error: {e}"