#!/usr/bin/env python3
"""
Humanity Chain SHA-256 Hash Verification Script

Automatically verifies that content_hash in records matches the SHA-256 hash
of the actual content field. Used for archive integrity verification.

Usage:
  python src/verify_hashes.py                    # Verify all records
  python src/verify_hashes.py records/pending/   # Verify specific directory
  python src/verify_hashes.py record.json        # Verify single record

Exit codes:
  0 - All records passed verification
  1 - One or more records failed verification
"""

import json
import hashlib
import sys
from pathlib import Path


def calculate_content_hash(content):
    """
    Calculate SHA-256 hash of content.
    
    Args:
        content: String content to hash
        
    Returns:
        Hex string of SHA-256 hash (lowercase, 64 chars)
    """
    if isinstance(content, str):
        content_bytes = content.encode('utf-8')
    else:
        content_bytes = json.dumps(content, separators=(',', ':')).encode('utf-8')
    
    return hashlib.sha256(content_bytes).hexdigest()


def verify_record_hash(record_path):
    """
    Verify that a record's content_hash matches its content.
    
    Args:
        record_path: Path to JSON record file
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        with open(record_path, 'r', encoding='utf-8') as f:
            record = json.load(f)
    except FileNotFoundError:
        return False, f"File not found: {record_path}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {record_path} -> {e}"
    
    # Check required fields
    if 'content_hash' not in record:
        return False, f"Missing 'content_hash' field in {record_path}"
    
    if 'content' not in record:
        return False, f"Missing 'content' field in {record_path}"
    
    content_hash_declared = record['content_hash']
    content = record['content']
    
    # Calculate actual hash
    content_hash_actual = calculate_content_hash(content)
    
    # Compare
    if content_hash_declared == content_hash_actual:
        return True, f"PASS: {record_path} (hash: {content_hash_actual[:16]}...)"
    else:
        return False, (
            f"FAIL: {record_path}\n"
            f"  Expected: {content_hash_declared}\n"
            f"  Got:      {content_hash_actual}"
        )


def find_record_files(search_path="."):
    """
    Find all JSON record files in records/ directory and subdirectories.
    
    Args:
        search_path: Path to search (default: current directory)
        
    Returns:
        Sorted list of Path objects
    """
    search_path = Path(search_path)
    
    if search_path.is_file() and search_path.suffix == '.json':
        return [search_path]
    
    if search_path.is_dir():
        return sorted(search_path.rglob('*.json'))
    
    return []


def main(argv=None):
    """Main entry point."""
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) > 0:
        search_path = argv[0]
    else:
        search_path = "records"
    
    search_path = Path(search_path)
    
    # Find all record files
    record_files = find_record_files(search_path)
    
    if not record_files:
        print(f"No JSON record files found in: {search_path}")
        return 0
    
    print(f"Verifying SHA-256 hashes for {len(record_files)} record(s)...")
    print()
    
    failed_count = 0
    passed_count = 0
    
    for record_path in record_files:
        success, message = verify_record_hash(record_path)
        
        if success:
            passed_count += 1
            print(f"✅ {message}")
        else:
            failed_count += 1
            print(f"❌ {message}")
    
    print()
    print(f"Results: {passed_count} passed, {failed_count} failed")
    
    if failed_count > 0:
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
