#!/usr/bin/env python3
"""Copy entry.png beside this file to the output directory.

Output directory: $MAKEFUN_OUTPUT_DIR, or /output when unset.
Standard library only. Deterministic: the output bytes are exactly
the bytes of entry.png next to this script.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
