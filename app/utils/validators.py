def validate_sort_request(data):
    if not data or 'array' not in data or 'algorithm' not in data:
        return False, "Missing 'array' or 'algorithm' field"
    if not isinstance(data['array'], list):
        return False, "'array' must be a list"
    if 'user_id' not in data:
        return False, "Missing 'user_id'"
    return True, None