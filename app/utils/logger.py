def log_sql(query, params=None):
    print("\n===== EXECUTING SQL =====")
    print(query)
    print("PARAMS:", params or [])
    print("=========================\n")