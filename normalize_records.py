import json
import hashlib
from pathlib import Path
from datetime import datetime

RECORDS_DIR = Path("records")


def generate_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def normalize_record(record_path):
    with open(record_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False

    # timestamp kontrolü
    if "timestamp" not in data:
        data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        updated = True

    # status kontrolü
    if "status" not in data:
        data["status"] = "draft"
        updated = True

    # content_hash üret
    if "content" in data:
        calculated_hash = generate_hash(data["content"])

        if data.get("content_hash") != calculated_hash:
            data["content_hash"] = calculated_hash
            updated = True

    # metadata kontrolü
    if "metadata" not in data:
        data["metadata"] = {}
        updated = True

    # normalize edilmiş dosyayı kaydet
    if updated:
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[UPDATED] {record_path}")

    else:
        print(f"[OK] {record_path}")


def main():
    if not RECORDS_DIR.exists():
        print("records directory not found.")
        return

    json_files = RECORDS_DIR.rglob("*.json")

    for record_file in json_files:
        normalize_record(record_file)


if __name__ == "__main__":
    main()
