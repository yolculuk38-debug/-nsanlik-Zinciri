#!/usr/bin/env python3
"""Unified hc-trust CLI."""

import argparse

from hc_trust import normalize as normalize_mod
from hc_trust import qr as qr_mod
from hc_trust import verify_hashes as verify_hashes_mod


def build_parser():
    parser = argparse.ArgumentParser(
        prog="hc-trust",
        description="Humanity Chain trust utilities.",
    )
    subparsers = parser.add_subparsers(dest="command")

    normalize_parser = subparsers.add_parser(
        "normalize",
        help="Normalize records/*.json files",
        description="Normalize records by setting missing fields and recalculating content_hash.",
    )
    normalize_parser.add_argument(
        "records_dir",
        nargs="?",
        default="records",
        help="Directory containing JSON records (default: records)",
    )

    subparsers.add_parser("verify-hashes", help="Verify content_hash values")
    subparsers.add_parser("qr", help="Generate verification QR codes")

    return parser


def main(argv=None):
    parser = build_parser()
    args, remainder = parser.parse_known_args(argv)

    if args.command == "normalize":
        return normalize_mod.main([args.records_dir])
    if args.command == "verify-hashes":
        return verify_hashes_mod.main()
    if args.command == "qr":
        return qr_mod.main()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
