#!/usr/bin/env python3

import argparse
import hashlib
import json
import sys
from pathlib import Path

import qrcode

BASE_URL = "https://yolculuk38-debug.github.io/Insanlik-Zinciri"


def generate_signature(record_id, content_hash, archive_ref):
    raw = f"{record_id}:{content_hash}:{archive_ref}"
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_qr(record_id, content_hash, archive_ref, output_dir="qr"):
    Path(output_dir).mkdir(exist_ok=True)

    signature = generate_signature(record_id, content_hash, archive_ref)

    verification_url = (
        f"{BASE_URL}/?"
        f"record={record_id}"
        f"&hash={content_hash}"
        f"&ref={archive_ref}"
        f"&sig={signature}"
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(verification_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    output_path = Path(output_dir) / f"{record_id}.png"
    img.save(output_path)

    print(f"✅ Secure QR oluşturuldu: {output_path}")
    print(f"🔗 URL: {verification_url}")

    return str(output_path)


def find_verified_records(records_dir="records"):
    records = []
    for path in sorted(Path(records_dir).rglob("*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"❌ Hata: {path} okunamadı ({exc})", file=sys.stderr)
            return None

        verification_status = str(data.get("verification_status", "")).lower()
        if verification_status != "verified":
            continue

        record_id = data.get("record_id") or data.get("id")
        content_hash = data.get("content_hash")
        archive_ref = data.get("archive_ref")

        if not (record_id and content_hash and archive_ref):
            print(
                f"❌ Hata: {path} gerekli alanları içermiyor "
                "(record_id/id, content_hash, archive_ref)",
                file=sys.stderr,
            )
            return None

        records.append((record_id, content_hash, archive_ref, path))

    return records


def run_batch_mode():
    verified_records = find_verified_records("records")
    if verified_records is None:
        return 1

    if not verified_records:
        print("ℹ️ Verified kayıt bulunamadı, QR üretimi atlandı.")
        return 0

    print(f"{len(verified_records)} verified kayıt için QR üretiliyor...")

    for record_id, content_hash, archive_ref, source_path in verified_records:
        print(f"- Kaynak: {source_path}")
        generate_qr(record_id, content_hash, archive_ref)

    print("✅ Batch QR üretimi tamamlandı.")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Generate secure QR verification links for Humanity Chain records. "
            "Use positional arguments for a single record or --batch for all "
            "records with verification_status=verified."
        )
    )
    parser.add_argument("record_id", nargs="?", help="Record identifier (single-record mode)")
    parser.add_argument("content_hash", nargs="?", help="SHA-256 content hash (single-record mode)")
    parser.add_argument("archive_ref", nargs="?", help="Archive reference (single-record mode)")
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Scan records/**/*.json and generate QR codes for verified records automatically",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.batch:
        if args.record_id or args.content_hash or args.archive_ref:
            parser.error("--batch positional parametrelerle birlikte kullanılamaz.")
        return run_batch_mode()

    if not (args.record_id and args.content_hash and args.archive_ref):
        parser.error(
            "single-record mode için <record_id> <content_hash> <archive_ref> zorunludur. "
            "Alternatif olarak --batch kullanın."
        )

    generate_qr(args.record_id, args.content_hash, args.archive_ref)
    return 0


if __name__ == "__main__":
    sys.exit(main())
