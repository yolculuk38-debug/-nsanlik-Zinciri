#!/usr/bin/env python3
"""Backward-compatible root entrypoint for record normalization."""

from hc_trust.normalize import *  # noqa: F401,F403
from hc_trust.normalize import main


if __name__ == "__main__":
    raise SystemExit(main())
