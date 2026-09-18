#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ROOT / "locales"
SOURCE = LOCALES / "en" / "ui.json"
TARGETS = [LOCALES / "lou" / "ui.json", LOCALES / "frc" / "ui.json"]
JSON_FILES = sorted(ROOT.rglob("*.json"))

PLACEHOLDER = re.compile(r"(\{\{[^{}]+\}\}|\{[A-Za-z0-9_.-]+\}|%[sdif])")

def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def flatten(obj, prefix=""):
    out = {}
    if not isinstance(obj, dict):
        raise TypeError(f"Expected object at {prefix or '<root>'}")
    for key, value in obj.items():
        here = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            out.update(flatten(value, here))
        elif isinstance(value, str):
            out[here] = value
        else:
            raise TypeError(f"{here}: value must be a string")
    return out

errors = []
parsed = {}

for json_path in JSON_FILES:
    try:
        parsed[json_path] = load(json_path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{json_path.relative_to(ROOT)}: invalid JSON: {exc}")

if errors:
    print("Localization validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

source = flatten(parsed[SOURCE])

for target_path in TARGETS:
    target = flatten(parsed[target_path])
    missing = sorted(set(source) - set(target))
    extra = sorted(set(target) - set(source))
    if missing:
        errors.append(f"{target_path}: missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{target_path}: extra keys: {', '.join(extra)}")

    for key in sorted(set(source) & set(target)):
        if target[key] == "":
            continue
        source_ph = sorted(PLACEHOLDER.findall(source[key]))
        target_ph = sorted(PLACEHOLDER.findall(target[key]))
        if source_ph != target_ph:
            errors.append(
                f"{target_path}:{key}: placeholders differ "
                f"(source={source_ph}, target={target_ph})"
            )

if errors:
    print("Localization validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(
    f"Localization validation passed: {len(source)} source strings; "
    f"{len(JSON_FILES)} JSON files parsed."
)
