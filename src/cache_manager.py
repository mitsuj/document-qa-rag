import hashlib
import os
from pathlib import Path


def get_file_hash(file_paths):
    """Generate unique hash for files to track changes"""
    hash_str = ""
    for path in sorted(file_paths):
        with open(path, "rb") as f:
            hash_str += str(Path(path).stat().st_mtime)  # File modification time
            hash_str += hashlib.md5(f.read()).hexdigest()
    return hashlib.md5(hash_str.encode()).hexdigest()


def get_cache_path(file_paths):
    os.makedirs("cache", exist_ok=True)
    return f"cache/{get_file_hash(file_paths)}.faiss"
