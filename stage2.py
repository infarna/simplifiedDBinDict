def solution(queries):
    db = {}  # In-memory database to store records
    results = []

    def set_value(timestamp, key, field, value):
        if key not in db:
            db[key] = {}
        db[key][field] = value
        return ""

    def compare_and_set(timestamp, key, field, expected_value, new_value):
        if key in db and field in db[key] and str(db[key][field]) == expected_value:
            db[key][field] = new_value
            return "true"
        return "false"

    def get_value(timestamp, key, field):
        if key in db and field in db[key]:
            return str(db[key][field])
        return ""

    def compare_and_delete(timestamp, key, field, expected_value):
        if key in db and field in db[key] and str(db[key][field]) == expected_value:
            del db[key][field]
            return "true"
        return "false"

    def scan(timestamp, key):
        if key not in db or not db[key]:
            return ""
        fields = db[key]
        sorted_fields = sorted(fields.items())  # Sort by field name
        return ", ".join([f"{field}({value})" for field, value in sorted_fields])

    def scan_by_prefix(timestamp, key, prefix):
        if key not in db or not db[key]:
            return ""
        fields = db[key]
        filtered_fields = {field: value for field, value in fields.items() if field.startswith(prefix)}
        sorted_filtered_fields = sorted(filtered_fields.items())  # Sort by field name
        return ", ".join([f"{field}({value})" for field, value in sorted_filtered_fields])

    # Parse and execute each query
    for query in queries:
        operation, timestamp, key, *params = query
        if operation == "SET":
            result = set_value(timestamp, key, params[0], params[1])  # Keep value as string
        elif operation == "COMPARE_AND_SET":
            result = compare_and_set(timestamp, key, params[0], params[1], params[2])
        elif operation == "GET":
            result = get_value(timestamp, key, params[0])
        elif operation == "COMPARE_AND_DELETE":
            result = compare_and_delete(timestamp, key, params[0], params[1])
        elif operation == "SCAN":
            result = scan(timestamp, key)
        elif operation == "SCAN_BY_PREFIX":
            result = scan_by_prefix(timestamp, key, params[0])
        else:
            result = "Invalid operation"
        results.append(result)

    return results
