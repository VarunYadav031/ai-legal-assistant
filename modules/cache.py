import hashlib
import json
import os

CACHE_FILE = "cache_store.json"

# load cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}


def make_key(text: str):
    return hashlib.md5(text.encode()).hexdigest()


def get_cache(key):
    return cache.get(key)


def set_cache(key, value):
    cache[key] = value
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)