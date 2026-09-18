# Louisiana Languages — Localization

This repository is the **canonical community-editable source for Louisiana Languages interface text**.

It is intentionally separate from the main app code so native speakers can improve translations without editing React Native screens, navigation, lesson logic, or other executable code.

The project is community-run and is **not affiliated with, endorsed by, or produced by Apple**. Its phone screens are generic iOS-style reference mockups used only to show interface wording in context; the repository contains no Apple screenshots or proprietary assets.

## Visual translation preview

Open the public editor at:

<https://themeganerddddddd.github.io/LouisianaLanguages-Localization/>

The editor lets contributors:

- switch between Kouri-Vini and Louisiana French;
- browse 79 broad iOS-style reference screens containing 864 English source strings;
- select visible interface text and preview a translation immediately;
- see English fallbacks clearly marked as untranslated;
- keep drafts in their own browser;
- work through the CLDR-readiness stages: Setup, Core Data, Basic Coverage, and Strongly Recommended;
- export draft data and follow official Apple Feedback Assistant or Unicode CLDR submission resources.

The site is a static GitHub Pages project with no paid backend. It never writes directly to GitHub or stores a GitHub token in browser code.

## Languages

- `en` — English source language
- `lou` — Kouri-Vini / Louisiana Creole
- `frc` — Louisiana French / Cajun French

The IETF/ISO language codes `lou` and `frc` are the canonical locale identifiers in this repository.

## What native speakers edit

For interface translations, edit only the values in:

- `locales/lou/ui.json`
- `locales/frc/ui.json`

The English source file is:

- `locales/en/ui.json`

Empty values mean **not translated yet**. The app should fall back to English until an approved translation is available.

The broader iOS-style reference corpus used by the public mockup is stored separately in:

- `ios-corpus/en.json`
- `ios-corpus/lou.json`
- `ios-corpus/frc.json`
- `ios-corpus/screens.json`

The same rule applies there: English is the source, and blank `lou` or `frc` values remain blank until a native/fluent contributor supplies and reviews them.

For locale conventions, terminology, orthography, sources, and review records, work under:

- `apple-cldr/locale-data/`
- `apple-cldr/terminology/`
- `apple-cldr/docs/`
- `apple-cldr/review/`

Do not fill a target-language value by machine translation or guesswork. Kouri-Vini and Louisiana French values must come from community contributors and native/fluent review.

## Apple and Unicode CLDR readiness

The separate `apple-cldr/` layer collects human-readable evidence and reviewed locale conventions for possible future platform and Unicode CLDR work. It covers language identity, characters, punctuation, dates, numbers, currency, plurals, measurement, terminology, orthography, sources, and review decisions.

The JSON files in `apple-cldr/locale-data/` are the canonical human-friendly collection layer. They are not fabricated CLDR XML and do not claim that Apple or Unicode has accepted either locale. See `apple-cldr/README.md` and `apple-cldr/cldr/README.md`.

The browser worksheet mirrors the CLDR working checklist row-for-row. Its committed starting points are:

- `apple-cldr/cldr-checklist-lou.json`
- `apple-cldr/cldr-checklist-frc.json`

Each row records its value, status, reviewer/date, notes, and official source. Existing v2 browser locale data is migrated into matching worksheet rows as `Needs Review` where possible.

## Important app compatibility rule

The existing Louisiana Languages learning app currently uses internal content/storage identifiers such as `cajun` and `kreole`.

Do **not** rename those identifiers as part of localization. Instead map:

- `cajun` → UI locale `frc`
- `kreole` → UI locale `lou`

This avoids breaking learner progress, lessons, audio, or stored state.

## Community workflow

Recommended workflow:

1. A contributor proposes wording in the visual editor, Weblate, or a pull request.
2. A native/fluent reviewer checks accuracy, spelling, naturalness, and regional context.
3. Disagreement is documented with alternatives and context rather than reduced to an arbitrary vote.
4. One reviewed form is selected as the default UI value while accepted alternatives remain recorded.
5. Reviewer and date information is recorded before a value is treated as approved.
6. Automated validation confirms that keys and placeholders still match English.
7. The app repository syncs an approved snapshot of these JSON files for the next release.

See `WEBLATE_SETUP.md`, `CONTRIBUTING.md`, and `apple-cldr/review/REVIEW_PROCESS.md`.

## Repository structure

```text
index.html

locales/
  en/ui.json
  lou/ui.json
  frc/ui.json
  _meta/languages.json

context/
  ui-context.json

apple-cldr/
  locale-lou.json
  locale-frc.json
  cldr-checklist-lou.json
  cldr-checklist-frc.json
  locale-data/{en,lou,frc}/locale.json
  terminology/{lou,frc}.json
  docs/
  review/
  submission/
  cldr/

ios-corpus/
  en.json
  lou.json
  frc.json
  screens.json

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
- every JSON file in the repository parses;
- app and iOS-corpus target languages contain exactly the same keys as English;
- translation values are strings;
- placeholder tokens stay consistent;
- the iOS corpus contains 79 uniquely identified screens and 864 source strings;
- every screen key resolves to the English corpus, with no orphaned source keys;
- both CLDR checklists contain the four expected stages, complete answer records, valid statuses, and official source links.

## Licensing

No license has been selected yet. Before soliciting broad public contributions, choose an explicit license for the translation data and contributor terms.
