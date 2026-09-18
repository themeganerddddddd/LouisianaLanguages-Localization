#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ROOT / "locales"
SOURCE = LOCALES / "en" / "ui.json"
TARGETS = [LOCALES / "lou" / "ui.json", LOCALES / "frc" / "ui.json"]
IOS_CORPUS = ROOT / "ios-corpus"
IOS_SOURCE = IOS_CORPUS / "en.json"
IOS_TARGETS = [IOS_CORPUS / "lou.json", IOS_CORPUS / "frc.json"]
IOS_SCREENS = IOS_CORPUS / "screens.json"
CLDR_CHECKLISTS = [
    ROOT / "apple-cldr" / "cldr-checklist-lou.json",
    ROOT / "apple-cldr" / "cldr-checklist-frc.json",
]
JSON_FILES = sorted(ROOT.rglob("*.json"))

PLACEHOLDER = re.compile(r"(\{\{[^{}]+\}\}|\{[A-Za-z0-9_.-]+\}|%[sdif])")
CLDR_STAGES = [
    "0. Setup",
    "1. Core Data",
    "2. Basic Coverage",
    "3. Strongly Recommended",
]
CLDR_ITEM_FIELDS = {
    "stage",
    "priority",
    "key",
    "label",
    "help",
    "who",
    "source",
    "type",
    "prefill",
}
CLDR_ANSWER_FIELDS = {"value", "status", "reviewerDate", "notes"}
CLDR_STATUSES = {"Not Started", "In Progress", "Needs Review", "Done"}
CLDR_PRIORITIES = {"Required", "Conditional", "Recommended"}
CLDR_SOURCE_HOSTS = {"cldr.unicode.org", "docs.google.com"}

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


def validate_targets(source_path, target_paths):
    source = flatten(parsed[source_path])

    for target_path in target_paths:
        target = flatten(parsed[target_path])
        missing = sorted(set(source) - set(target))
        extra = sorted(set(target) - set(source))
        if missing:
            errors.append(
                f"{target_path.relative_to(ROOT)}: missing keys: {', '.join(missing)}"
            )
        if extra:
            errors.append(
                f"{target_path.relative_to(ROOT)}: extra keys: {', '.join(extra)}"
            )

        for key in sorted(set(source) & set(target)):
            if target[key] == "":
                continue
            source_ph = sorted(PLACEHOLDER.findall(source[key]))
            target_ph = sorted(PLACEHOLDER.findall(target[key]))
            if source_ph != target_ph:
                errors.append(
                    f"{target_path.relative_to(ROOT)}:{key}: placeholders differ "
                    f"(source={source_ph}, target={target_ph})"
                )

    return source


def validate_ios_screens(source):
    screens = parsed[IOS_SCREENS]
    if not isinstance(screens, list):
        errors.append("ios-corpus/screens.json: root must be an array")
        return

    if len(screens) != 79:
        errors.append(
            f"ios-corpus/screens.json: expected 79 screens, found {len(screens)}"
        )

    screen_ids = []
    referenced_keys = []
    for index, screen in enumerate(screens):
        location = f"ios-corpus/screens.json[{index}]"
        if not isinstance(screen, dict):
            errors.append(f"{location}: screen must be an object")
            continue

        screen_id = screen.get("id")
        if not isinstance(screen_id, str) or not screen_id:
            errors.append(f"{location}.id: must be a non-empty string")
        else:
            screen_ids.append(screen_id)

        for field in ("group", "title"):
            if not isinstance(screen.get(field), str) or not screen[field]:
                errors.append(f"{location}.{field}: must be a non-empty string")

        title_key = screen.get("titleKey")
        if not isinstance(title_key, str) or not title_key:
            errors.append(f"{location}.titleKey: must be a non-empty string")
        else:
            referenced_keys.append(title_key)

        sections = screen.get("sections")
        if not isinstance(sections, list):
            errors.append(f"{location}.sections: must be an array")
            continue

        for section_index, section in enumerate(sections):
            section_location = f"{location}.sections[{section_index}]"
            if not isinstance(section, dict):
                errors.append(f"{section_location}: section must be an object")
                continue

            header_key = section.get("headerKey")
            if header_key is not None:
                if not isinstance(header_key, str) or not header_key:
                    errors.append(
                        f"{section_location}.headerKey: must be null or a non-empty string"
                    )
                else:
                    referenced_keys.append(header_key)

            rows = section.get("rows")
            if not isinstance(rows, list):
                errors.append(f"{section_location}.rows: must be an array")
                continue

            for row_index, row in enumerate(rows):
                row_location = f"{section_location}.rows[{row_index}]"
                if not isinstance(row, dict):
                    errors.append(f"{row_location}: row must be an object")
                    continue
                key = row.get("key")
                if not isinstance(key, str) or not key:
                    errors.append(f"{row_location}.key: must be a non-empty string")
                else:
                    referenced_keys.append(key)
                if not isinstance(row.get("label"), str):
                    errors.append(f"{row_location}.label: must be a string")

    duplicate_ids = sorted(
        screen_id for screen_id in set(screen_ids) if screen_ids.count(screen_id) > 1
    )
    if duplicate_ids:
        errors.append(
            "ios-corpus/screens.json: duplicate screen ids: "
            + ", ".join(duplicate_ids)
        )

    missing_source_keys = sorted(set(referenced_keys) - set(source))
    if missing_source_keys:
        errors.append(
            "ios-corpus/screens.json: references missing English keys: "
            + ", ".join(missing_source_keys)
        )

    unreferenced_source_keys = sorted(set(source) - set(referenced_keys))
    if unreferenced_source_keys:
        errors.append(
            "ios-corpus/en.json: keys not referenced by screens.json: "
            + ", ".join(unreferenced_source_keys)
        )


def validate_cldr_checklists():
    reference_items = None
    item_count = 0

    for checklist_path in CLDR_CHECKLISTS:
        relative_path = checklist_path.relative_to(ROOT)
        checklist = parsed[checklist_path]
        if not isinstance(checklist, dict):
            errors.append(f"{relative_path}: root must be an object")
            continue

        expected_locale = checklist_path.stem.rsplit("-", 1)[-1]
        if checklist.get("locale") != expected_locale:
            errors.append(
                f"{relative_path}: locale must be {expected_locale!r}"
            )

        items = checklist.get("items")
        answers = checklist.get("answers")
        if not isinstance(items, list):
            errors.append(f"{relative_path}: items must be an array")
            continue
        if not isinstance(answers, dict):
            errors.append(f"{relative_path}: answers must be an object")
            continue

        item_count = len(items)
        if item_count != 49:
            errors.append(f"{relative_path}: expected 49 items, found {item_count}")

        item_keys = []
        stages = []
        for index, item in enumerate(items):
            location = f"{relative_path}:items[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{location}: item must be an object")
                continue

            missing_fields = sorted(CLDR_ITEM_FIELDS - set(item))
            extra_fields = sorted(set(item) - CLDR_ITEM_FIELDS)
            if missing_fields:
                errors.append(
                    f"{location}: missing fields: {', '.join(missing_fields)}"
                )
            if extra_fields:
                errors.append(
                    f"{location}: unexpected fields: {', '.join(extra_fields)}"
                )

            for field in ("stage", "priority", "key", "label", "help", "who", "source", "type"):
                if not isinstance(item.get(field), str) or not item[field]:
                    errors.append(f"{location}.{field}: must be a non-empty string")

            stage = item.get("stage")
            if stage not in CLDR_STAGES:
                errors.append(f"{location}.stage: unexpected stage {stage!r}")
            elif stage not in stages:
                stages.append(stage)

            priority = item.get("priority")
            if priority not in CLDR_PRIORITIES:
                errors.append(f"{location}.priority: invalid value {priority!r}")

            key = item.get("key")
            if isinstance(key, str) and key:
                item_keys.append(key)

            source_url = item.get("source")
            if isinstance(source_url, str):
                parsed_url = urlparse(source_url)
                if (
                    parsed_url.scheme != "https"
                    or parsed_url.hostname not in CLDR_SOURCE_HOSTS
                ):
                    errors.append(
                        f"{location}.source: expected an official HTTPS CLDR source"
                    )

        if stages != CLDR_STAGES:
            errors.append(
                f"{relative_path}: expected stages in order: {', '.join(CLDR_STAGES)}"
            )

        duplicate_keys = sorted(
            key for key in set(item_keys) if item_keys.count(key) > 1
        )
        if duplicate_keys:
            errors.append(
                f"{relative_path}: duplicate item keys: {', '.join(duplicate_keys)}"
            )

        missing_answers = sorted(set(item_keys) - set(answers))
        extra_answers = sorted(set(answers) - set(item_keys))
        if missing_answers:
            errors.append(
                f"{relative_path}: missing answers: {', '.join(missing_answers)}"
            )
        if extra_answers:
            errors.append(
                f"{relative_path}: extra answers: {', '.join(extra_answers)}"
            )

        for key in sorted(set(item_keys) & set(answers)):
            answer = answers[key]
            location = f"{relative_path}:answers.{key}"
            if not isinstance(answer, dict):
                errors.append(f"{location}: answer must be an object")
                continue

            missing_fields = sorted(CLDR_ANSWER_FIELDS - set(answer))
            extra_fields = sorted(set(answer) - CLDR_ANSWER_FIELDS)
            if missing_fields:
                errors.append(
                    f"{location}: missing fields: {', '.join(missing_fields)}"
                )
            if extra_fields:
                errors.append(
                    f"{location}: unexpected fields: {', '.join(extra_fields)}"
                )

            for field in CLDR_ANSWER_FIELDS:
                if field in answer and not isinstance(answer[field], str):
                    errors.append(f"{location}.{field}: must be a string")

            if answer.get("status") not in CLDR_STATUSES:
                errors.append(
                    f"{location}.status: invalid value {answer.get('status')!r}"
                )

        if reference_items is None:
            reference_items = items
        elif items != reference_items:
            errors.append(
                f"{relative_path}: item definitions differ from the other locale"
            )

    return item_count

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

source = validate_targets(SOURCE, TARGETS)
ios_source = validate_targets(IOS_SOURCE, IOS_TARGETS)
validate_ios_screens(ios_source)
cldr_item_count = validate_cldr_checklists()

if len(ios_source) != 864:
    errors.append(
        f"ios-corpus/en.json: expected 864 source strings, found {len(ios_source)}"
    )

if errors:
    print("Localization validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(
    f"Localization validation passed: {len(source)} app source strings, "
    f"{len(ios_source)} iOS corpus source strings across "
    f"{len(parsed[IOS_SCREENS])} reference screens; "
    f"{cldr_item_count} CLDR checklist rows per locale; "
    f"{len(JSON_FILES)} JSON files parsed."
)
