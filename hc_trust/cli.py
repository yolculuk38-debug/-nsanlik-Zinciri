#!/usr/bin/env python3
"""Unified hc-trust CLI."""

import argparse
from pathlib import Path

from hc_trust import hash as hash_mod
from hc_trust import normalize as normalize_mod
from hc_trust import qr as qr_mod
from hc_trust import verify_hashes as verify_hashes_mod


class HcTrustArgumentParser(argparse.ArgumentParser):
    """ArgumentParser with clearer error hints for hc-trust."""

    def error(self, message):
        command_hint = (
            "\nTry one of: verify, hash, qr, normalize. "
            "Use 'hc-trust <command> --help' for command-specific usage."
        )
        super().error(f"{message}{command_hint}")


def build_parser():
    parser = HcTrustArgumentParser(
        prog="hc-trust",
        description="Humanity Chain trust utilities.",
        epilog=(
            "Commands:\n"
            "  verify      Verify content_hash values in JSON records\n"
            "  hash        Calculate SHA-256 of a file\n"
            "  qr          Generate verification QR codes\n"
            "  normalize   Normalize JSON records and refresh content_hash\n"
            "\n"
            "Quick examples:\n"
            "  hc-trust verify\n"
            "  hc-trust hash records/pending/HC-2026-0002.json\n"
            "  hc-trust qr --batch\n"
            "  hc-trust normalize records\n"
            "\n"
            "Tip: run 'hc-trust <command> --help' for detailed usage examples."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify content_hash values in JSON records",
        description="Verify content_hash values for a record file or directory.",
        epilog=(
            "Examples:\n"
            "  hc-trust verify\n"
            "  hc-trust verify records\n"
            "  hc-trust verify records/pending"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    verify_parser.add_argument(
        "path",
        nargs="?",
        default="records",
        help="Record file or directory to verify (default: records)",
    )

    verify_hashes_parser = subparsers.add_parser(
        "verify-hashes",
        help="(Deprecated alias) same as verify",
        description="Backward-compatible alias for 'verify'.",
        epilog="Example: hc-trust verify-hashes records",
    )
    verify_hashes_parser.add_argument(
        "path",
        nargs="?",
        default="records",
        help="Record file or directory to verify (default: records)",
    )

    hash_parser = subparsers.add_parser(
        "hash",
        help="Calculate SHA-256 of a file",
        description="Calculate SHA-256 hash for any file path.",
        epilog=(
            "Examples:\n"
            "  hc-trust hash records/pending/HC-2026-0002.json\n"
            "  hc-trust hash README.md"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    hash_parser.add_argument("file", help="File path to hash")

    qr_parser = subparsers.add_parser(
        "qr",
        help="Generate verification QR codes",
        description="Generate one QR code or batch-generate for verified records.",
        epilog=(
            "Examples:\n"
            "  hc-trust qr HC-CHATGPT-2026-0001 <content_hash> <archive_ref>\n"
            "  hc-trust qr --batch"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    qr_parser.add_argument("record_id", nargs="?", help="Record identifier (single-record mode)")
    qr_parser.add_argument("content_hash", nargs="?", help="SHA-256 content hash (single-record mode)")
    qr_parser.add_argument("archive_ref", nargs="?", help="Archive reference (single-record mode)")
    qr_parser.add_argument(
        "--batch",
        action="store_true",
        help="Scan records/**/*.json and generate QR codes for verified records automatically",
    )

    normalize_parser = subparsers.add_parser(
        "normalize",
        help="Normalize records/*.json files",
        description="Normalize records by setting missing fields and recalculating content_hash.",
        epilog=(
            "Examples:\n"
            "  hc-trust normalize\n"
            "  hc-trust normalize records"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    normalize_parser.add_argument(
        "records_dir",
        nargs="?",
        default="records",
        help="Directory containing JSON records (default: records)",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"verify", "verify-hashes"}:
        return verify_hashes_mod.main([args.path])

    if args.command == "hash":
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: file not found: {file_path}")
            print("Tip: use a valid file path, e.g. 'hc-trust hash README.md'")
            return 1
        if file_path.is_dir():
            print(f"Error: expected a file but got a directory: {file_path}")
            print("Tip: pass a file path, not a folder.")
            return 1
        print(f"SHA256: {hash_mod.calculate_sha256(file_path)}")
        return 0

    if args.command == "qr":
        if args.batch:
            if args.record_id or args.content_hash or args.archive_ref:
                parser.error("--batch cannot be used with positional arguments.")
            return qr_mod.run_batch_mode()
        if not (args.record_id and args.content_hash and args.archive_ref):
            parser.error(
                "single-record mode requires <record_id> <content_hash> <archive_ref>. "
                "Alternatively, use --batch."
            )
        qr_mod.generate_qr(args.record_id, args.content_hash, args.archive_ref)
        return 0

    if args.command == "normalize":
        return normalize_mod.main([args.records_dir])

    parser.print_help()
    print("\nError: missing command. Choose one of: verify, hash, qr, normalize.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
