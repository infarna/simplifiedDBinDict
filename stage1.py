def solution(queries):
    db = {}  # In-memory database to store records
    results = []

    def set_value(timestamp, key, field, value):
        if key not in db:
            db[key] = {}
        db[key][field] = value
        return ""

    def compare_and_set(timestamp, key, field, expected_value, new_value):
        if key in db and field in db[key] and db[key][field] == expected_value:
            db[key][field] = new_value
            return "true"
        return "false"

    def get_value(timestamp, key, field):
        if key in db and field in db[key]:
            return str(db[key][field])
        return ""

    def compare_and_delete(timestamp, key, field, expected_value):
        if key in db and field in db[key] and db[key][field] == expected_value:
            del db[key][field]
            return "true"
        return "false"

    # Parse and execute each query
    for query in queries:
        operation, timestamp, key, field, *values = query
        if operation == "SET":
            result = set_value(timestamp, key, field, int(values[0]))
        elif operation == "COMPARE_AND_SET":
            result = compare_and_set(timestamp, key, field, int(values[0]), int(values[1]))
        elif operation == "GET":
            result = get_value(timestamp, key, field)
        elif operation == "COMPARE_AND_DELETE":
            result = compare_and_delete(timestamp, key, field, int(values[0]))
        else:
            result = "Invalid operation"
        results.append(result)

    return results
