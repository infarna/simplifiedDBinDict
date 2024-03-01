def solution(queries):
    db = {}  # In-memory database to store records, now including TTL

    def set_value(timestamp, key, field, value):
        # For operations without TTL, we consider them as having an infinite TTL by default.
        if key not in db:
            db[key] = {}
        db[key][field] = {"value": value, "ttl": float('inf')}
        return ""

    def set_with_ttl(timestamp, key, field, value, ttl):
        if key not in db:
            db[key] = {}
        expiration_time = int(timestamp) + int(ttl)
        db[key][field] = {"value": value, "ttl": expiration_time}
        return ""

    def compare_and_set(timestamp, key, field, expected_value, new_value):
        if key in db and field in db[key] and str(db[key][field]["value"]) == expected_value and db[key][field]["ttl"] > int(timestamp):
            db[key][field]["value"] = new_value
            return "true"
        return "false"

    def compare_and_set_with_ttl(timestamp, key, field, expected_value, new_value, ttl):
        if key in db and field in db[key] and str(db[key][field]["value"]) == expected_value and db[key][field]["ttl"] > int(timestamp):
            expiration_time = int(timestamp) + int(ttl)
            db[key][field] = {"value": new_value, "ttl": expiration_time}
            return "true"
        return "false"

    def compare_and_delete(timestamp, key, field, expected_value):
        if key in db and field in db[key] and str(db[key][field]["value"]) == expected_value and db[key][field]["ttl"] > int(timestamp):
            del db[key][field]
            return "true"
        return "false"

    def get_value(timestamp, key, field):
        if key in db and field in db[key] and db[key][field]["ttl"] > int(timestamp):
            return str(db[key][field]["value"])
        return ""

    def scan(timestamp, key):
        if key not in db:
            return ""
        valid_fields = [
            f"{field}({db[key][field]['value']})"
            for field in sorted(db[key])
            if db[key][field]["ttl"] > int(timestamp)
        ]
        return ", ".join(valid_fields)

    def scan_by_prefix(timestamp, key, prefix):
        if key not in db:
            return ""
        valid_fields = [
            f"{field}({db[key][field]['value']})"
            for field in sorted(db[key])
            if field.startswith(prefix) and db[key][field]["ttl"] > int(timestamp)
        ]
        return ", ".join(valid_fields)

    results = []
    for query in queries:
        operation, timestamp, key, *params = query
        if operation == "SET":
            result = set_value(timestamp, key, params[0], params[1])
        elif operation == "SET_WITH_TTL":
            result = set_with_ttl(timestamp, key, params[0], params[1], params[2])
        elif operation == "COMPARE_AND_SET":
            result = compare_and_set(timestamp, key, params[0], params[1], params[2])
        elif operation == "COMPARE_AND_SET_WITH_TTL":
            result = compare_and_set_with_ttl(timestamp, key, params[0], params[1], params[2], params[3])
        elif operation == "COMPARE_AND_DELETE":
            result = compare_and_delete(timestamp, key, params[0], params[1])
        elif operation == "GET":
            result = get_value(timestamp, key, params[0])
        elif operation == "SCAN":
            result = scan(timestamp, key)
        elif operation == "SCAN_BY_PREFIX":
            result = scan_by_prefix(timestamp, key, params[0])
        else:
            result = "Invalid operation"
        results.append(result)

    return results
