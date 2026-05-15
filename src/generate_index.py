import json
from pathlib import Path

RECORDS_DIR = Path("records")
OUTPUT_FILE = Path("docs/index.md")


def generate_index():
    lines = []

    lines.append("# Humanity Chain Archive Index\n")
    lines.append("Automatically generated archive index.\n")

    if not RECORDS_DIR.exists():
        print("records klasörü bulunamadı.")
        return

    json_files = sorted(RECORDS_DIR.rglob("*.json"))

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            record_id = data.get("record_id", "UNKNOWN")
            timestamp = data.get("timestamp", "UNKNOWN")
            verification = data.get("verification_status", "unknown")

            lines.append(f"## {record_id}")
            lines.append(f"- Timestamp: {timestamp}")
            lines.append(f"- Verification: {verification}")
            lines.append(f"- File: `{file_path}`\n")

        except Exception as e:
            lines.append(f"## ERROR: {file_path}")
            lines.append(f"- {str(e)}\n")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Archive index generated successfully.")


if __name__ == "__main__":
    generate_index()
