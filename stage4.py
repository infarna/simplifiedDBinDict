def solution(queries):
    db = {}  # In-memory database to store records, now including history for TTL and non-TTL values

    def set_value(timestamp, key, field, value):
        if key not in db:
            db[key] = {}
        db[key][field] = [{"value": value, "start": int(timestamp), "ttl": float('inf')}]
        return ""

    # def set_with_ttl(timestamp, key, field, value, ttl):
    #     if key not in db:
    #         db[key] = {}
    #     expiration_time = int(timestamp) + int(ttl)
    #     if field not in db[key]:
    #         db[key][field] = []
    #     db[key][field].append({"value": value, "start": int(timestamp), "ttl": expiration_time})
    #     return ""
    def set_with_ttl(timestamp, key, field, value, ttl):
        if key not in db:
            db[key] = {}
        expiration_time = int(timestamp) + int(ttl)
        db[key][field] = [{"value": value, "start": int(timestamp), "ttl": expiration_time}]
        return ""

    def compare_and_set(timestamp, key, field, expected_value, new_value):
        if key in db and field in db[key]:
            latest_entry = db[key][field][-1] if db[key][field] else None
            if latest_entry and str(latest_entry["value"]) == expected_value:
                db[key][field].append({"value": new_value, "start": int(timestamp), "ttl": float('inf')})
                return "true"
        return "false"

    # def compare_and_set_with_ttl(timestamp, key, field, expected_value, new_value, ttl):
    #     if key in db and field in db[key]:
    #         latest_entry = db[key][field][-1] if db[key][field] else None
    #         if latest_entry and str(latest_entry["value"]) == expected_value:
    #             expiration_time = int(timestamp) + int(ttl)
    #             db[key][field].append({"value": new_value, "start": int(timestamp), "ttl": expiration_time})
    #             return "true"
    #     return "false"
    def compare_and_set_with_ttl(timestamp, key, field, expected_value, new_value, ttl):
        if key in db and field in db[key]:
            latest_entry = db[key][field][-1] if db[key][field] else None
            if latest_entry and str(latest_entry["value"]) == expected_value and latest_entry["ttl"] > int(timestamp):
                expiration_time = int(timestamp) + int(ttl)
                db[key][field].append({"value": new_value, "start": int(timestamp), "ttl": expiration_time})
                return "true"
        return "false"
    # def compare_and_delete(timestamp, key, field, expected_value):
    #     if key in db and field in db[key]:
    #         latest_entry = db[key][field][-1] if db[key][field] else None
    #         if latest_entry and str(latest_entry["value"]) == expected_value:
    #             db[key][field].append({"value": None, "start": int(timestamp), "ttl": float('inf')})
    #             return "true"
    #     return "false"
    def compare_and_delete(timestamp, key, field, expected_value):
        if key in db and field in db[key]:
            latest_entry = db[key][field][-1] if db[key][field] else None
            if latest_entry and str(latest_entry["value"]) == expected_value:
                db[key][field].append({"value": None, "start": int(timestamp), "ttl": float('inf')})
                return "true"
        return "false"
    # def get_value(timestamp, key, field):
    #     if key in db and field in db[key]:
    #         for entry in reversed(db[key][field]):
    #             if entry["start"] <= int(timestamp) < (entry["ttl"] if entry["value"] is not None else float('inf')):
    #                 return str(entry["value"]) if entry["value"] is not None else ""
    #     return ""
    def get_value(timestamp, key, field):
        if key in db and field in db[key]:
            for entry in reversed(db[key][field]):
                if entry["start"] <= int(timestamp) < entry["ttl"]:
                    return str(entry["value"]) if entry["value"] is not None else ""
        return ""
    def get_when(timestamp, key, field, at_timestamp):
        if at_timestamp == "0":
            return get_value(timestamp, key, field)
        return get_value(at_timestamp, key, field)

    def scan(timestamp, key):
        if key not in db:
            return ""
        result = []
        for field in sorted(db[key]):
            value = get_value(timestamp, key, field)
            if value:
                result.append(f"{field}({value})")
        return ", ".join(result)

    # def scan_by_prefix(timestamp, key, prefix):
    #     if key not in db:
    #         return ""
    #     result = []
    #     for field in sorted(db[key]):
    #         if field.startswith(prefix):
    #             value = get_value(timestamp, key, field)
    #             if value:
    #                 result.append(f"{field}({value})")
    #     return ", ".join(result)
    def scan_by_prefix(timestamp, key, prefix):
        if key not in db:
            return ""
        result = []
        for field in sorted(db[key]):
            if field.startswith(prefix):
                for entry in reversed(db[key][field]):
                    if entry["start"] <= int(timestamp) < entry["ttl"]:
                        if entry["value"] is not None:
                            result.append(f"{field}({entry['value']})")
                        break
        return ", ".join(result)
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
        elif operation == "GET_WHEN":
            result = get_when(timestamp, key, params[0], params[1])
        elif operation == "SCAN":
            result = scan(timestamp, key)
        elif operation == "SCAN_BY_PREFIX":
            result = scan_by_prefix(timestamp, key, params[0])
        else:
            result = "Invalid operation"
        results.append(result)

    return results
