
import json
import hashlib

def generate_filters_hash(filters):
    if not filters:
        return None
    
    filters_sorted = json.dumps(filters, sort_keys=True, separators=(',', ':'))

    return hashlib.md5(filters_sorted.encode('utf-8')).hexdigest()
