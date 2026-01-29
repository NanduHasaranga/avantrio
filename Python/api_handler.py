import re
import datetime
from concurrent.futures import ThreadPoolExecutor

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_record(record):
    errors = []

    #required fields
    require_fields = ["user_id", "email", "timestamp", "items"]
    for field in require_fields:
        if field not in record:
            errors.append(f"Missing field:{field}")
    
    #user_id
    if not record.get("user_id"):
        errors.append("user_id should be non-empty.")
    
    #email
    if not re.match(EMAIL_REGEX, record["email"]):
        errors.append("Email is not correct.")
    
    #timestamp
    try:
        datetime.fromisoformat(record["timestamp"])
    except:
        errors.append("Invalid ISO timestamp")

    #items
    items = record.get("items", [])
    if not isinstance(items, list) or len(items) == 0:
        errors.append("Items should be non-empty list")
    else:
        for i,item in enumerate(items):
            if not item.get("item_id"):
                errors.append(f"{i} item_id should not be empty.")
            if not item.get("quantity") or not isinstance(item["quantity"], int) or not item["quantity"] > 0:
                errors.append(f"{i} quantity has a problem" )
            if not item.get("price") or not isinstance(item["price"], float) or not item["price"] > 0.0:
                errors.append(f"{i} price has a problem" )

    return errors

ACCESS_LEVEL = {
    "read_access": "read",
    "write_access": "write"
}

def authorization(api_key, access = "read"):
    if ACCESS_LEVEL[api_key] == access:
        return True, "Give the access"
    elif ACCESS_LEVEL[api_key] == "read" and access == "write":
        return False, "Don't give the access"
    return True, "Give the access"
    
def chunk_generator(data, chunk_size = 1000):
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def map_function(records):
    #total revenue
    total = 0
    for r in records:
        for item in r["items"]:
            total += item["quantity"] * item["price"]
    return total

def reduce_function(results):
    return sum(results)

def process_large_data(data):
    chunks = chunk_generator(data, 10000)
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(map_function, c) for c in chunks]
        for f in futures:
            results.append(f.result())
        
    return reduce_function(results)

def api_handler(data, api_key):
    #Authorization
    ok, msg = authorization(api_key, "read")
    if not ok:
        return {"error": msg}

    #validation
    all_errors = []
    valid_records = []

    for i,record in enumerate(data):
        errors = validate_record(record)
        if errors:
            all_errors.append(errors)
        else:
            valid_records.append(record)
    
    #process valid records
    total_revenue = process_large_data(valid_records)

    return {
        "errors" : all_errors,
        "total_revenue" : total_revenue
    }

if __name__ == "__main__":
    data = [{
        "user_id": "abc123",
        "email": "user1@example.com",
        "timestamp": "2024-09-03T12:30:00Z",
        "items": [
            {"item_id": "item001", "quantity": 3, "price": 9.99},
            {"item_id": "item002", "quantity": 1, "price": 19.99}
        ]
        },
        {
        "user_id": "xyz789",
        "email": "user2@invalid-email",
        "timestamp": "2024-09-03T15:45:00Z",
        "items": []
        },
        {
        "user_id": "",
        "email": "user3@example.com",
        "timestamp": "invalid-timestamp", 
        "items": [
            {"item_id": "item003", "quantity": 2, "price": -5.99}
        ]
        }
            ]
    
    api_key = "write_access"

    output = api_handler(data, api_key)
    print(output)

