#!/usr/bin/env python3
"""Regenerate the committed VS Code color-ID registry.

The registry is a snapshot of the color IDs used by the themes, checked against
a local VS Code installation. CI uses the committed snapshot and does not need
VS Code installed.

Usage:
    python3 scripts/update-color-registry.py
    python3 scripts/update-color-registry.py --code-root /path/to/vscode/resources/app
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = Path(__file__).with_name("vscode-color-registry.json")
THEMES = ROOT / "themes"
DYNAMIC_PREFIXES = ("gitDecoration.", "terminal.ansi")
DEFAULT_CODE_ROOT = Path("/usr/share/code/resources/app")


def parse_workbench_registry(bundle: Path) -> dict[str, bool]:
    source = bundle.read_text(errors="ignore")
    registry: dict[str, bool] = {}
    for match in re.finditer(r'ae\("([^"]+)",', source):
        key = match.group(1)
        tail = source[match.end() : match.end() + 1200]
        next_registration = tail.find('ae("')
        if next_registration >= 0:
            tail = tail[:next_registration]
        registration = re.search(r"d\(\d+,[^)]*\)", tail)
        needs_transparency = False
        if registration:
            needs_transparency = tail[registration.end() : registration.end() + 3].startswith(",!0")
        registry[key] = needs_transparency
    return registry


def parse_extension_registry(extensions_root: Path) -> dict[str, bool]:
    registry: dict[str, bool] = {}
    for package in sorted(extensions_root.glob("*/package.json")):
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for color in data.get("contributes", {}).get("colors", []):
            color_id = color.get("id")
            if color_id:
                registry.setdefault(color_id, False)
    return registry


def load_theme_ids() -> set[str]:
    ids: set[str] = set()
    for path in (THEMES / "color-dark.json", THEMES / "color-light.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        ids.update(data.get("colors", {}))
    return ids


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--code-root",
        type=Path,
        default=DEFAULT_CODE_ROOT,
        help="VS Code resources/app directory (default: %(default)s)",
    )
    parser.add_argument(
        "--extensions-root",
        type=Path,
        default=None,
        help="Built-in extensions directory (default: <code-root>/extensions)",
    )
    args = parser.parse_args()

    bundle = args.code_root / "out/vs/workbench/workbench.desktop.main.js"
    extensions_root = args.extensions_root or args.code_root / "extensions"
    package_json = args.code_root / "package.json"

    if not bundle.is_file():
        print(f"error: workbench bundle not found: {bundle}", file=sys.stderr)
        return 1
    if not extensions_root.is_dir():
        print(f"error: extensions directory not found: {extensions_root}", file=sys.stderr)
        return 1

    try:
        version = json.loads(package_json.read_text(encoding="utf-8")).get("version", "unknown")
    except (OSError, json.JSONDecodeError):
        version = "unknown"

    registry = parse_workbench_registry(bundle)
    for key, value in parse_extension_registry(extensions_root).items():
        registry.setdefault(key, value)
    if len(registry) < 500:
        print(
            f"error: only found {len(registry)} color IDs; the workbench bundle format may have changed",
            file=sys.stderr,
        )
        return 1

    used = load_theme_ids()
    dynamic = [key for key in used if key.startswith(DYNAMIC_PREFIXES)]
    literal = sorted(used - set(dynamic))
    missing = sorted(key for key in literal if key not in registry)
    if missing:
        print("error: theme colors not registered by this VS Code installation:", file=sys.stderr)
        for key in missing:
            print(f"  {key}", file=sys.stderr)
        return 1

    transparency_required = sorted(key for key in literal if registry.get(key))
    payload = {
        "vscodeVersion": version,
        "source": "VS Code workbench bundle and built-in extensions",
        "dynamicPrefixes": list(DYNAMIC_PREFIXES),
        "colorIds": literal,
        "transparencyRequired": transparency_required,
    }
    REGISTRY_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {REGISTRY_PATH}")
    print(f"  VS Code: {version}")
    print(f"  literal color IDs: {len(literal)}")
    print(f"  dynamic theme IDs: {len(dynamic)}")
    print(f"  transparency-required IDs: {len(transparency_required)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
