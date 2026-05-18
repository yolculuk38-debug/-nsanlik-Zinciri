#!/usr/bin/env python3
"""Backward-compatible entrypoint for record normalization."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hc_trust.normalize import *  # noqa: F401,F403,E402
from hc_trust.normalize import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
