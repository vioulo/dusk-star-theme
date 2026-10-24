#!/usr/bin/env python3
"""Validate Dusk Star theme data, package metadata, and color registry.

The script is dependency-free (Python 3.11+) and is used by CI. It does not
need VS Code installed; color IDs are checked against the committed registry
snapshot in scripts/vscode-color-registry.json.

Usage:
    python3 scripts/validate.py
    python3 scripts/validate.py --verbose
    python3 scripts/validate.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DARK_PATH = ROOT / "themes/color-dark.json"
LIGHT_PATH = ROOT / "themes/color-light.json"
ICON_PATH = ROOT / "themes/file-icon.json"
PACKAGE_PATH = ROOT / "package.json"
LOCK_PATH = ROOT / "package-lock.json"
EXPECTED_PATH = Path(__file__).with_name("expected-theme-values.json")
REGISTRY_PATH = Path(__file__).with_name("vscode-color-registry.json")

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{3,4}$|^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
DARK_ONLY_ALLOWED = {"searchEditor.findMatchBorder"}

SEARCH_SYNTAX_COLORS = {
    "foreground": "#F8F8F2",
    "comment": "#918C7F",
    "string": "#E6DB74",
    "number": "#AE81FF",
    "orange": "#FD971F",
    "green": "#A6E22E",
    "cyan": "#66D9EF",
    "pink": "#FF4D82",
    "mint": "#A8FDB3",
    "blue": "#7FB4FF",
    "lightblue": "#99C4FF",
    "muted": "#BFC9D8",
    "light": "#EAF3FF",
}

TERMINAL_ANSI = {
    "red": "#FF6B6B",
    "green": "#A6E22E",
    "yellow": "#E6DB74",
    "blue": "#7FB4FF",
    "magenta": "#AE81FF",
    "cyan": "#66D9EF",
    "white": "#F8F8F2",
}

DARK_CONTRAST_PAIRS = [
    {"label": "editor foreground", "fg": "editor.foreground", "bg": "editor.background", "min": 4.5},
    {"label": "comment", "fg": "#918C7F", "bg": "editor.background", "min": 4.5},
    {"label": "keyword", "fg": "#FF4D82", "bg": "editor.background", "min": 4.5},
    {"label": "string", "fg": "#E6DB74", "bg": "editor.background", "min": 4.5},
    {"label": "number", "fg": "#AE81FF", "bg": "editor.background", "min": 4.5},
    {"label": "function/type", "fg": "#A6E22E", "bg": "editor.background", "min": 4.5},
    {"label": "parameter", "fg": "#FD971F", "bg": "editor.background", "min": 4.5},
    {"label": "namespace/type parameter", "fg": "#66D9EF", "bg": "editor.background", "min": 4.5},
    {"label": "line number", "fg": "editorLineNumber.foreground", "bg": "editor.background", "min": 3.0},
    {"label": "active line number", "fg": "editorLineNumber.activeForeground", "bg": "editor.background", "min": 4.5},
    {"label": "selection", "fg": "editor.selectionForeground", "bg": "editor.selectionBackground", "min": 4.5},
    {"label": "find match", "fg": "editor.findMatchForeground", "bg": "editor.findMatchBackground", "min": 4.5},
    {"label": "find highlight", "fg": "editor.findMatchHighlightForeground", "bg": "editor.findMatchHighlightBackground", "min": 4.5},
    {"label": "terminal selection", "fg": "terminal.selectionForeground", "bg": "terminal.selectionBackground", "base": "terminal.background", "min": 4.5},
    {"label": "list active selection", "fg": "list.activeSelectionForeground", "bg": "#31527777", "base": "sideBar.background", "min": 4.5},
    {"label": "list inactive selection", "fg": "list.inactiveSelectionForeground", "bg": "#2B496C66", "base": "sideBar.background", "min": 4.5},
    {"label": "git added", "fg": "gitDecoration.addedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "git modified", "fg": "gitDecoration.modifiedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "git deleted", "fg": "gitDecoration.deletedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "git renamed", "fg": "gitDecoration.renamedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "git conflicting", "fg": "gitDecoration.conflictingResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "git ignored", "fg": "gitDecoration.ignoredResourceForeground", "bg": "sideBar.background", "min": 3.0},
    {"label": "blame", "fg": "git.blame.editorDecorationForeground", "bg": "editor.background", "min": 4.5},
    {"label": "blame on line highlight", "fg": "git.blame.editorDecorationForeground", "bg": "editor.lineHighlightBackground", "base": "editor.background", "min": 4.5},
    {"label": "button", "fg": "button.foreground", "bg": "button.background", "min": 4.5},
    {"label": "button hover", "fg": "button.foreground", "bg": "button.hoverBackground", "min": 4.5},
    {"label": "debug status", "fg": "statusBar.debuggingForeground", "bg": "statusBar.debuggingBackground", "min": 4.5},
    {"label": "status error", "fg": "statusBarItem.errorForeground", "bg": "statusBarItem.errorBackground", "min": 4.5},
    {"label": "status warning", "fg": "statusBarItem.warningForeground", "bg": "statusBarItem.warningBackground", "min": 4.5},
]

for _name, _fg in TERMINAL_ANSI.items():
    DARK_CONTRAST_PAIRS.append(
        {
            "label": f"terminal ANSI {_name} on find match",
            "fg": _fg,
            "bg": "terminal.findMatchBackground",
            "base": "terminal.background",
            "min": 4.5,
        }
    )

for _name, _fg in SEARCH_SYNTAX_COLORS.items():
    DARK_CONTRAST_PAIRS.append(
        {
            "label": f"search editor {_name} on find match",
            "fg": _fg,
            "bg": "searchEditor.findMatchBackground",
            "base": "editor.background",
            "min": 4.5,
        }
    )

LIGHT_CONTRAST_PAIRS = [
    {"label": "light editor foreground", "fg": "editor.foreground", "bg": "editor.background", "min": 4.5},
    {"label": "light line number", "fg": "editorLineNumber.foreground", "bg": "editor.background", "min": 3.0},
    {"label": "light blame", "fg": "git.blame.editorDecorationForeground", "bg": "editor.background", "min": 3.0},
    {"label": "light selection", "fg": "editor.selectionForeground", "bg": "editor.selectionBackground", "min": 4.5},
    {"label": "light find match", "fg": "editor.findMatchForeground", "bg": "editor.findMatchBackground", "min": 4.5},
    {"label": "light find highlight", "fg": "editor.findMatchHighlightForeground", "bg": "editor.findMatchHighlightBackground", "min": 4.5},
    {"label": "light git added", "fg": "gitDecoration.addedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "light git modified", "fg": "gitDecoration.modifiedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "light git deleted", "fg": "gitDecoration.deletedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "light git renamed", "fg": "gitDecoration.renamedResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "light git conflicting", "fg": "gitDecoration.conflictingResourceForeground", "bg": "sideBar.background", "min": 4.5},
    {"label": "light button", "fg": "button.foreground", "bg": "button.background", "min": 4.5},
    {"label": "light debug status", "fg": "statusBar.debuggingForeground", "bg": "statusBar.debuggingBackground", "min": 4.5},
]


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def parse_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)


def parse_json_text(text: str):
    return json.loads(text, object_pairs_hook=no_duplicates)


def normalize_hex(value: str) -> str:
    h = value.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(ch * 2 for ch in h)
    return h


def alpha_ok(value: str) -> bool:
    h = normalize_hex(value)
    if len(h) == 8:
        return h[-2:].lower() != "ff"
    return False


def luminance(value: str) -> float:
    h = normalize_hex(value)[:6]
    channels = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    def linear(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(c) for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def blend(value: str, under: str) -> str:
    h = normalize_hex(value)
    if len(h) != 8:
        return value
    u = normalize_hex(under)
    alpha = int(h[6:8], 16) / 255
    result = "#"
    for i in (0, 2, 4):
        c = round(int(h[i : i + 2], 16) * alpha + int(u[i : i + 2], 16) * (1 - alpha))
        result += f"{c:02X}"
    return result


def resolve_ref(colors: dict, ref: str, base: str):
    if ref.startswith("#"):
        value = ref
    else:
        value = colors.get(ref)
        if value is None:
            return None
    if len(normalize_hex(value)) == 8:
        return blend(value, base)
    return value


def evaluate_contrast(colors: dict, pair: dict):
    base_ref = pair.get("base")
    base = colors.get(base_ref) if base_ref else colors.get("editor.background")
    if not base:
        return None, f"missing base color {base_ref!r}"
    bg = resolve_ref(colors, pair["bg"], base)
    if bg is None:
        return None, f"missing background color {pair['bg']!r}"
    fg = resolve_ref(colors, pair["fg"], bg)
    if fg is None:
        return None, f"missing foreground color {pair['fg']!r}"
    return (contrast(fg, bg), fg, bg), None


def validate_package(fail) -> dict | None:
    try:
        pkg = parse_json(PACKAGE_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"package.json: {exc}")
        return None

    for key in (
        "name",
        "displayName",
        "description",
        "version",
        "publisher",
        "engines",
        "license",
        "repository",
        "bugs",
        "homepage",
        "contributes",
        "scripts",
        "devDependencies",
    ):
        if key not in pkg:
            fail(f"package.json missing {key!r}")

    description = pkg.get("description", "")
    if not isinstance(description, str) or not description.strip():
        fail("package.json description must be non-empty")
    elif len(description) > 120:
        fail(f"package.json description is too long ({len(description)} > 120)")

    if pkg.get("license") != "MIT":
        fail(f"package.json license must be MIT, got {pkg.get('license')!r}")
    if not pkg.get("publisher"):
        fail("package.json publisher must be non-empty")
    if "Themes" not in pkg.get("categories", []):
        fail("package.json categories must include 'Themes'")
    if not pkg.get("engines", {}).get("vscode"):
        fail("package.json engines.vscode must be set")

    repository = pkg.get("repository", {})
    if not str(repository.get("url", "")).startswith("https://github.com/"):
        fail("package.json repository.url must be a GitHub HTTPS URL")
    bugs = pkg.get("bugs", {})
    if not str(bugs.get("url", "")).startswith("https://"):
        fail("package.json bugs.url must be an HTTPS URL")
    if not str(pkg.get("homepage", "")).startswith("https://"):
        fail("package.json homepage must be an HTTPS URL")

    icon = ROOT / str(pkg.get("icon", ""))
    if not icon.is_file():
        fail(f"package.json icon not found: {icon}")
    else:
        data = icon.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            fail(f"package.json icon is not a PNG: {icon}")
        elif len(data) >= 24:
            width = int.from_bytes(data[16:20], "big")
            height = int.from_bytes(data[20:24], "big")
            if width != height or width < 128:
                fail(f"package.json icon must be square and at least 128px, got {width}x{height}")

    contributes = pkg.get("contributes", {})
    themes = contributes.get("themes", [])
    if not isinstance(themes, list) or not themes:
        fail("package.json contributes.themes must be a non-empty list")
        themes = []
    labels = set()
    for theme in themes:
        if not isinstance(theme, dict):
            fail("package.json contributes.themes contains a non-object")
            continue
        label = theme.get("label")
        path = theme.get("path")
        ui_theme = theme.get("uiTheme")
        if not label:
            fail("package.json theme is missing label")
        elif label in labels:
            fail(f"package.json duplicate theme label: {label}")
        else:
            labels.add(label)
        if not path or not (ROOT / path).is_file():
            fail(f"package.json theme path not found: {path!r}")
        if ui_theme not in {"vs-dark", "vs", "hc", "hc-light"}:
            fail(f"package.json theme {label!r} has invalid uiTheme {ui_theme!r}")

    icon_themes = contributes.get("iconThemes", [])
    if not isinstance(icon_themes, list):
        fail("package.json contributes.iconThemes must be a list")
        icon_themes = []
    if not any(item.get("id") == "dusk-star-icon" for item in icon_themes if isinstance(item, dict)):
        fail("package.json must contribute the dusk-star-icon icon theme")
    for item in icon_themes:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        if not path or not (ROOT / path).is_file():
            fail(f"package.json icon theme path not found: {path!r}")

    scripts = pkg.get("scripts", {})
    if scripts.get("validate") != "python3 scripts/validate.py":
        fail("package.json scripts.validate must run python3 scripts/validate.py")
    for script in ("package", "publish"):
        if not str(scripts.get(script, "")).startswith("vsce "):
            fail(f"package.json scripts.{script} must invoke vsce")

    dev_dependencies = pkg.get("devDependencies", {})
    if "@vscode/vsce" not in dev_dependencies:
        fail("package.json devDependencies must include @vscode/vsce")

    try:
        lock = parse_json(LOCK_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"package-lock.json: {exc}")
    else:
        if lock.get("lockfileVersion") != 3:
            fail(f"package-lock.json lockfileVersion must be 3, got {lock.get('lockfileVersion')!r}")
        lock_root = lock.get("packages", {}).get("", {})
        lock_dev = lock_root.get("devDependencies", {})
        if lock_dev.get("@vscode/vsce") != dev_dependencies.get("@vscode/vsce"):
            fail("package-lock.json is out of sync with @vscode/vsce")

    for path in (ROOT / ".vscodeignore", ROOT / ".gitignore", ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "LICENSE"):
        if not path.is_file():
            fail(f"required file missing: {path.relative_to(ROOT)}")

    return pkg


def validate_icon_theme(fail) -> dict | None:
    try:
        data = parse_json(ICON_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"file-icon.json: {exc}")
        return None

    definitions = data.get("iconDefinitions")
    if not isinstance(definitions, dict) or not definitions:
        fail("file-icon.json iconDefinitions must be a non-empty object")
        definitions = {}

    for name, definition in definitions.items():
        if not isinstance(definition, dict):
            fail(f"file-icon.json iconDefinitions[{name!r}] must be an object")
            continue
        icon_path = definition.get("iconPath")
        if not icon_path:
            fail(f"file-icon.json iconDefinitions[{name!r}] is missing iconPath")
            continue
        resolved = (ICON_PATH.parent / icon_path).resolve()
        if not resolved.is_file():
            fail(f"file-icon.json icon path not found: {icon_path}")
            continue
        if resolved.suffix.lower() == ".svg":
            try:
                text = resolved.read_text(encoding="utf-8")
                root = ET.fromstring(text)
            except (OSError, ET.ParseError) as exc:
                fail(f"file-icon.json SVG parse error {icon_path}: {exc}")
                continue
            if not root.tag.endswith("svg"):
                fail(f"file-icon.json SVG root is not <svg>: {icon_path}")
            if "svgrepo" in text.lower():
                fail(f"file-icon.json SVG still contains an SVG Repo source comment: {icon_path}")
            for element in root.iter():
                for attribute in ("href", "{http://www.w3.org/1999/xlink}href"):
                    value = element.attrib.get(attribute, "")
                    if value.startswith(("http://", "https://")):
                        fail(f"file-icon.json SVG contains an external reference: {icon_path}")

    folder = data.get("folder")
    folder_expanded = data.get("folderExpanded")
    if folder not in definitions:
        fail(f"file-icon.json folder definition not found: {folder!r}")
    if folder_expanded not in definitions:
        fail(f"file-icon.json folderExpanded definition not found: {folder_expanded!r}")

    light = data.get("light", {})
    if not isinstance(light, dict):
        fail("file-icon.json light must be an object")
        light = {}
    for key in ("folder", "folderExpanded"):
        if light.get(key) not in definitions:
            fail(f"file-icon.json light.{key} definition not found: {light.get(key)!r}")

    if data.get("hidesExplorerArrows") is not True:
        fail("file-icon.json hidesExplorerArrows must be true")
    for key in ("file", "fileExtensions", "fileNames"):
        if key in data:
            fail(f"file-icon.json must stay folder-only; found {key!r}")

    return data


def validate_theme(
    name: str,
    path: Path,
    expected_colors: dict,
    expected_semantic: dict | None,
    expected_tokens: dict | None,
    fail,
    check_token_contrast: bool,
) -> dict | None:
    try:
        data = parse_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"{name} theme: {exc}")
        return None

    if data.get("$schema") != "vscode://schemas/color-theme":
        fail(f"{name} theme: $schema must be vscode://schemas/color-theme")
    if data.get("semanticHighlighting") is not True:
        fail(f"{name} theme: semanticHighlighting must be true")

    colors = data.get("colors")
    if not isinstance(colors, dict) or not colors:
        fail(f"{name} theme: colors must be a non-empty object")
        colors = {}
    for key, value in colors.items():
        if not isinstance(value, str) or not HEX_RE.fullmatch(value):
            fail(f"{name} theme: invalid color {key}={value!r}")

    token_colors = data.get("tokenColors")
    if not isinstance(token_colors, list):
        fail(f"{name} theme: tokenColors must be a list")
        token_colors = []
    scopeless = [index for index, entry in enumerate(token_colors) if isinstance(entry, dict) and "scope" not in entry]
    if scopeless and scopeless != [0]:
        fail(f"{name} theme: only the first token entry may omit scope, found {scopeless}")
    for index, entry in enumerate(token_colors):
        if not isinstance(entry, dict):
            fail(f"{name} theme: tokenColors[{index}] must be an object")
            continue
        settings = entry.get("settings")
        if not isinstance(settings, dict):
            fail(f"{name} theme: tokenColors[{index}].settings must be an object")
            continue
        foreground = settings.get("foreground")
        if foreground is not None and (not isinstance(foreground, str) or not HEX_RE.fullmatch(foreground)):
            fail(f"{name} theme: invalid token foreground {foreground!r}")
        font_style = settings.get("fontStyle")
        if font_style is not None:
            if not isinstance(font_style, str):
                fail(f"{name} theme: invalid fontStyle {font_style!r}")
            else:
                for style in font_style.split():
                    if style not in {"italic", "bold", "underline", "strikethrough"}:
                        fail(f"{name} theme: invalid fontStyle token {style!r}")

    semantic = data.get("semanticTokenColors")
    if not isinstance(semantic, dict):
        fail(f"{name} theme: semanticTokenColors must be an object")
        semantic = {}
    for key, value in semantic.items():
        foreground = value.get("foreground") if isinstance(value, dict) else value
        if foreground is not None and (not isinstance(foreground, str) or not HEX_RE.fullmatch(foreground)):
            fail(f"{name} theme: invalid semantic color {key}={value!r}")

    for entry in token_colors:
        if entry.get("scope") == "meta.function-call":
            fail(f"{name} theme: broad meta.function-call entry still present")
        if entry.get("name") == "Function call":
            fail(f"{name} theme: old Function call entry still present")

    for key, expected in expected_colors.items():
        actual = colors.get(key)
        if actual != expected:
            fail(f"{name} theme: {key} expected {expected}, got {actual}")

    if expected_tokens is not None:
        by_name = {entry.get("name"): entry for entry in token_colors if entry.get("name")}
        for token_name, expected in expected_tokens.items():
            entry = by_name.get(token_name)
            if entry is None:
                fail(f"{name} theme: missing token entry {token_name!r}")
                continue
            if "scope" in expected and entry.get("scope") != expected["scope"]:
                fail(f"{name} theme: token {token_name!r} scope expected {expected['scope']!r}, got {entry.get('scope')!r}")
            actual_fg = entry.get("settings", {}).get("foreground")
            if "foreground" in expected and actual_fg != expected["foreground"]:
                fail(f"{name} theme: token {token_name!r} foreground expected {expected['foreground']!r}, got {actual_fg!r}")
            if "fontStyle" in expected:
                actual_style = entry.get("settings", {}).get("fontStyle")
                if actual_style != expected["fontStyle"]:
                    fail(f"{name} theme: token {token_name!r} fontStyle expected {expected['fontStyle']!r}, got {actual_style!r}")

    if expected_semantic is not None:
        for key, expected in expected_semantic.items():
            actual = semantic.get(key)
            if actual != expected:
                fail(f"{name} theme: semantic {key} expected {expected!r}, got {actual!r}")
        for key in sorted(set(semantic) - set(expected_semantic)):
            fail(f"{name} theme: unexpected semantic key {key!r}")

    if check_token_contrast:
        background = colors.get("editor.background")
        if not background:
            fail(f"{name} theme: missing editor.background for token contrast")
        else:
            token_failures = 0
            checked_tokens = 0
            for entry in token_colors:
                foreground = entry.get("settings", {}).get("foreground")
                if not foreground:
                    continue
                checked_tokens += 1
                if len(normalize_hex(foreground)) != 6:
                    fail(f"{name} theme: token foreground must be opaque 6-digit hex: {foreground!r}")
                    token_failures += 1
                    continue
                ratio = contrast(foreground, background)
                if ratio < 4.5:
                    token_failures += 1
                    fail(f"{name} theme: token {entry.get('name') or entry.get('scope')!r} is {ratio:.2f}:1 < 4.5:1")
            semantic_failures = 0
            checked_semantic = 0
            for key, value in semantic.items():
                foreground = value.get("foreground") if isinstance(value, dict) else value
                if foreground is None:
                    continue
                checked_semantic += 1
                if len(normalize_hex(foreground)) != 6:
                    fail(f"{name} theme: semantic foreground must be opaque 6-digit hex: {foreground!r}")
                    semantic_failures += 1
                    continue
                ratio = contrast(foreground, background)
                if ratio < 4.5:
                    semantic_failures += 1
                    fail(f"{name} theme: semantic {key!r} is {ratio:.2f}:1 < 4.5:1")
            print(
                f"  {name} token colors: {checked_tokens - token_failures}/{checked_tokens} at or above 4.5:1"
            )
            print(
                f"  {name} semantic colors: {checked_semantic - semantic_failures}/{checked_semantic} at or above 4.5:1"
            )

    return data


def validate_registry(dark: dict | None, light: dict | None, fail) -> None:
    try:
        registry = parse_json(REGISTRY_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"vscode-color-registry.json: {exc}")
        return

    color_ids = registry.get("colorIds")
    if not isinstance(color_ids, list) or not color_ids:
        fail("vscode-color-registry.json colorIds must be a non-empty list")
        return
    if len(color_ids) != len(set(color_ids)):
        fail("vscode-color-registry.json contains duplicate color IDs")
    color_id_set = set(color_ids)

    transparency = registry.get("transparencyRequired", [])
    if not isinstance(transparency, list):
        fail("vscode-color-registry.json transparencyRequired must be a list")
        transparency = []
    transparency_set = set(transparency)
    if not transparency_set <= color_id_set:
        fail("vscode-color-registry.json transparencyRequired contains unknown IDs")

    prefixes = registry.get("dynamicPrefixes", [])
    if not isinstance(prefixes, list) or not prefixes:
        fail("vscode-color-registry.json dynamicPrefixes must be a non-empty list")
        prefixes = []
    prefixes_tuple = tuple(prefixes)

    for theme_name, data in (("dark", dark), ("light", light)):
        colors = (data or {}).get("colors", {})
        dynamic = sorted(key for key in colors if key.startswith(prefixes_tuple))
        literal = sorted(key for key in colors if not key.startswith(prefixes_tuple))
        missing = sorted(key for key in literal if key not in color_id_set)
        if missing:
            fail(f"{theme_name} theme: color IDs not in registry: {missing}")
        bad_alpha = []
        for key in literal:
            if key not in transparency_set:
                continue
            value = colors.get(key)
            if not isinstance(value, str) or not alpha_ok(value):
                bad_alpha.append(f"{key}={value!r}")
        if bad_alpha:
            message = f"{theme_name} theme: transparency-required IDs without alpha: {', '.join(bad_alpha)}"
            if theme_name == "dark":
                fail(message)
            else:
                print(f"WARN: {message} (light theme is out of scope)")
        print(
            f"  {theme_name} registry: {len(colors)} colors; {len(literal)} literal; "
            f"{len(dynamic)} dynamic; {len(set(literal) & transparency_set)} transparency-required"
        )

    required_ids = {"git.blame.editorDecorationForeground", "searchEditor.findMatchBorder"}
    missing_required = sorted(required_ids - color_id_set)
    if missing_required:
        fail(f"vscode-color-registry.json is missing required IDs: {missing_required}")

    dark_ids = set((dark or {}).get("colors", {}))
    light_ids = set((light or {}).get("colors", {}))
    if light_ids - dark_ids:
        fail(f"light theme has IDs missing from dark theme: {sorted(light_ids - dark_ids)}")
    extras = dark_ids - light_ids
    if extras != DARK_ONLY_ALLOWED:
        fail(f"unexpected dark-only IDs: {sorted(extras)}")

    print(
        f"  registry: VS Code {registry.get('vscodeVersion')}; {len(color_id_set)} literal IDs; "
        f"{len(transparency_set)} transparency-required"
    )


def validate_contrast(theme_name: str, data: dict | None, pairs: list[dict], fail, verbose: bool) -> None:
    colors = (data or {}).get("colors", {})
    passed = 0
    failed = 0
    for pair in pairs:
        try:
            result, error = evaluate_contrast(colors, pair)
        except (KeyError, TypeError, ValueError) as exc:
            fail(f"{theme_name} contrast {pair['label']!r}: {exc}")
            failed += 1
            continue
        if error:
            fail(f"{theme_name} contrast {pair['label']!r}: {error}")
            failed += 1
            continue
        ratio, fg, bg = result
        if verbose:
            print(f"  {theme_name:5} {pair['label']:44} {ratio:5.2f}:1  {fg} on {bg}")
        if ratio < pair["min"]:
            fail(f"{theme_name} contrast {pair['label']!r}: {ratio:.2f}:1 < {pair['min']}:1")
            failed += 1
        else:
            passed += 1
    print(f"  {theme_name} contrast pairs: {passed}/{len(pairs)} passed")


def validate_readme(fail) -> None:
    readme_path = ROOT / "README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"README.md: {exc}")
        return

    for heading in ("## Installation", "## Themes", "## File Icon Theme", "## Development", "## License"):
        if heading not in readme:
            fail(f"README.md is missing section {heading!r}")

    for tag in re.findall(r"<img[^>]*>", readme, flags=re.IGNORECASE):
        src_match = re.search(r'src="([^"]+)"', tag)
        alt_match = re.search(r'alt="([^"]*)"', tag)
        if not src_match:
            fail(f"README.md image tag has no src: {tag}")
            continue
        src = src_match.group(1)
        if not src.startswith(("http://", "https://", "data:")) and not (ROOT / src).is_file():
            fail(f"README.md image not found: {src}")
        if not alt_match or not alt_match.group(1).strip():
            fail(f"README.md image has no alt text: {src}")

    for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", readme):
        if not alt.strip():
            fail(f"README.md markdown image has no alt text: {src}")
        if not src.startswith(("http://", "https://", "data:")) and not (ROOT / src).is_file():
            fail(f"README.md markdown image not found: {src}")

    if "Dusk Star Dark" not in readme or "Dusk Star Light" not in readme:
        fail("README.md must mention both Dusk Star Dark and Dusk Star Light")
    if "Dusk Star" not in readme or "File Icon Theme" not in readme:
        fail("README.md must document the file icon theme")
    if "MIT" not in readme:
        fail("README.md must mention the MIT license")
    if "PixPin" in readme:
        fail("README.md still references the removed PixPin image")

    license_path = ROOT / "LICENSE"
    if license_path.is_file() and not license_path.read_text(encoding="utf-8").startswith("MIT License"):
        fail("LICENSE must start with 'MIT License'")


def run_self_tests() -> int:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)
            print(f"FAIL: {message}")

    check(abs(contrast("#FFFFFF", "#000000") - 21.0) < 0.01, "contrast white/black must be 21:1")
    check(abs(contrast("#777777", "#777777") - 1.0) < 0.01, "contrast same color must be 1:1")
    check(blend("#FF000080", "#000000") == "#800000", "blend 50% red over black")
    check(blend("#00000000", "#FFFFFF") == "#FFFFFF", "blend transparent over white")
    check(alpha_ok("#7FB4FF14"), "alpha_ok must accept 8-digit alpha")
    check(alpha_ok("#00000000"), "alpha_ok must accept fully transparent")
    check(not alpha_ok("#7FB4FF"), "alpha_ok must reject opaque 6-digit colors")
    check(not alpha_ok("#FFFFFFFF"), "alpha_ok must reject alpha FF")

    try:
        parse_json_text('{"a": 1, "a": 2}')
    except ValueError:
        pass
    else:
        check(False, "duplicate JSON keys must raise ValueError")

    colors = {"editor.background": "#222222", "editor.foreground": "#222222"}
    pair = {"label": "test", "fg": "editor.foreground", "bg": "editor.background", "min": 4.5}
    result, error = evaluate_contrast(colors, pair)
    check(error is None and result is not None and result[0] < 4.5, "low contrast must be detected")

    colors["editor.foreground"] = "#FFFFFF"
    result, error = evaluate_contrast(colors, pair)
    check(error is None and result is not None and result[0] >= 4.5, "sufficient contrast must pass")

    alpha_colors = {
        "editor.background": "#222222",
        "editor.foreground": "#FFFFFF",
        "test.background": "#FFFFFF80",
    }
    alpha_pair = {
        "label": "alpha",
        "fg": "editor.foreground",
        "bg": "test.background",
        "base": "editor.background",
        "min": 1.0,
    }
    result, error = evaluate_contrast(alpha_colors, alpha_pair)
    check(error is None and result is not None and result[2] != "#FFFFFF", "alpha background must be composited")

    if failures:
        print(f"\n{len(failures)} self-test(s) failed")
        return 1
    print("All validator self-tests passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run validator self-tests")
    parser.add_argument("--verbose", action="store_true", help="print every contrast pair")
    args = parser.parse_args()

    if args.self_test:
        return run_self_tests()

    failures: list[str] = []

    def fail(message: str) -> None:
        failures.append(message)
        print(f"FAIL: {message}")

    try:
        fixture = parse_json(EXPECTED_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: expected-theme-values.json: {exc}")
        return 1

    for key in ("dark", "light", "semantic", "tokens"):
        if key not in fixture:
            fail(f"expected-theme-values.json missing {key!r}")

    dark = validate_theme(
        "dark",
        DARK_PATH,
        fixture.get("dark") or {},
        fixture.get("semantic") or {},
        fixture.get("tokens") or {},
        fail,
        True,
    )
    light = validate_theme(
        "light",
        LIGHT_PATH,
        fixture.get("light") or {},
        None,
        None,
        fail,
        True,
    )

    if dark and light:
        dark_semantic = set(dark.get("semanticTokenColors", {}))
        light_semantic = set(light.get("semanticTokenColors", {}))
        if dark_semantic != light_semantic:
            fail(
                "dark/light semantic token keys differ: "
                f"dark-only={sorted(dark_semantic - light_semantic)}, "
                f"light-only={sorted(light_semantic - dark_semantic)}"
            )

    validate_package(fail)
    validate_icon_theme(fail)
    validate_registry(dark, light, fail)
    validate_contrast("dark", dark, DARK_CONTRAST_PAIRS, fail, args.verbose)
    validate_contrast("light", light, LIGHT_CONTRAST_PAIRS, fail, args.verbose)
    validate_readme(fail)

    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nAll theme, package, registry, and contrast checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
