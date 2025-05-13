def preprocess_query(nl_query):
    # Add preprocessing rules for ambiguous queries
    # Example: if query includes "top" without specifying a number, clarify
    if "top" in nl_query and " " not in nl_query.split("top")[1].strip():
        return None, "Please clarify: 'Top how many?'"
    return nl_query, None
