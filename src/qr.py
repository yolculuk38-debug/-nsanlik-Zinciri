#!/usr/bin/env python3

import qrcode
import json
import hashlib
import sys

from pathlib import Path

BASE_URL = "https://yolculuk38-debug.github.io/Insanlik-Zinciri"

def generate_signature(record_id, content_hash, archive_ref):
    raw = f"{record_id}:{content_hash}:{archive_ref}"
    return hashlib.sha256(raw.encode()).hexdigest()

def generate_qr(record_id, content_hash, archive_ref, output_dir="qr"):

    Path(output_dir).mkdir(exist_ok=True)

    signature = generate_signature(
        record_id,
        content_hash,
        archive_ref
    )

    verification_url = (
        f"{BASE_URL}/?"
        f"record={record_id}"
        f"&hash={content_hash}"
        f"&ref={archive_ref}"
        f"&sig={signature}"
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    output_path = Path(output_dir) / f"{record_id}.png"

    img.save(output_path)

    print(f"✅ Secure QR oluşturuldu: {output_path}")
    print(f"🔗 URL: {verification_url}")

    return str(output_path)

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print(
            "Kullanım: python src/qr.py "
            "<record_id> <content_hash> <archive_ref>"
        )
        sys.exit(1)

    record_id = sys.argv[1]
    content_hash = sys.argv[2]
    archive_ref = sys.argv[3]

    generate_qr(
        record_id,
        content_hash,
        archive_ref
    )
