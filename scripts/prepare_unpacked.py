#!/usr/bin/env python3
"""Build a flat extension folder for Load unpacked (Windows / ZIP-friendly)."""

from __future__ import annotations

import argparse
import os
import shutil
import sys


def copy_resolved(src: str, dst: str) -> None:
    src = os.path.abspath(src)
    if os.path.islink(src):
        link_target = os.readlink(src)
        if not os.path.isabs(link_target):
            link_target = os.path.normpath(
                os.path.join(os.path.dirname(src), link_target)
            )
        copy_resolved(link_target, dst)
        return
    if os.path.isdir(src):
        os.makedirs(dst, exist_ok=True)
        for name in sorted(os.listdir(src)):
            copy_resolved(os.path.join(src, name), os.path.join(dst, name))
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve symlinks into a folder Edge/Chrome can load."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default="isrc",
        help="Extension source dir (default: isrc). Use imoz for Firefox.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory (default: build/<source>-unpacked)",
    )
    args = parser.parse_args()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source = os.path.join(repo_root, args.source)
    if not os.path.isdir(source):
        print(f"error: source not found: {source}", file=sys.stderr)
        return 1
    output = args.output or os.path.join(
        repo_root, "build", f"{os.path.basename(source)}-unpacked"
    )
    output = os.path.abspath(output)
    if os.path.exists(output):
        shutil.rmtree(output)
    print(f"Building {output} from {source} ...")
    copy_resolved(source, output)
    manifest = os.path.join(output, "manifest.json")
    locales = os.path.join(output, "_locales", "en", "messages.json")
    if not os.path.isfile(manifest):
        print("error: manifest.json missing in output", file=sys.stderr)
        return 1
    if not os.path.isfile(locales):
        print(
            "error: _locales/en/messages.json missing — "
            "localization will fail in the browser",
            file=sys.stderr,
        )
        return 1
    print("Done. In Edge: Load unpacked → select:")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
