# Louisiana Languages — Localization

This repository is the **canonical community-editable source for Louisiana Languages interface text**.

It is intentionally separate from the main app code so native speakers can improve translations without editing React Native screens, navigation, lesson logic, or other executable code.

## Languages

- `en` — English source language
- `lou` — Kouri-Vini / Louisiana Creole
- `frc` — Louisiana French / Cajun French

The IETF/ISO language codes `lou` and `frc` are the canonical locale identifiers in this repository.

## What native speakers edit

Native speakers should edit only:

- `locales/lou/ui.json`
- `locales/frc/ui.json`

The English source file is:

- `locales/en/ui.json`

Empty values mean **not translated yet**. The app should fall back to English until an approved translation is available.

## Important app compatibility rule

The existing Louisiana Languages learning app currently uses internal content/storage identifiers such as `cajun` and `kreole`.

Do **not** rename those identifiers as part of localization. Instead map:

- `cajun` → UI locale `frc`
- `kreole` → UI locale `lou`

This avoids breaking learner progress, lessons, audio, or stored state.

## Community workflow

Recommended workflow:

1. A native speaker proposes or edits a translation in Weblate.
2. Another trusted speaker/reviewer checks the translation.
3. Approved translations are committed to this repository.
4. Automated validation confirms that keys and placeholders still match English.
5. The app repository syncs an approved snapshot of these JSON files for the next release.

See `WEBLATE_SETUP.md` and `CONTRIBUTING.md`.

## Repository structure

```text
locales/
  en/ui.json
  lou/ui.json
  frc/ui.json
  _meta/languages.json

context/
  ui-context.json

scripts/
  validate_locales.py

.github/
  workflows/validate-locales.yml
  CODEOWNERS
  pull_request_template.md

CODEX_INTEGRATION_PROMPT.md
CONTRIBUTING.md
WEBLATE_SETUP.md
```

## Validation

Run:

```bash
python scripts/validate_locales.py
```

The validator checks that:
- locale JSON parses;
- target languages contain exactly the same keys as English;
- translation values are strings;
- placeholder tokens stay consistent.

## Licensing

No license has been selected yet. Before soliciting broad public contributions, choose an explicit license for the translation data and contributor terms.
