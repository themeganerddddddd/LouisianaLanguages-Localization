# Recommended GitHub Repository Structure

Keep the existing visual editor at the repository root, then add this folder structure:

```text
LouisianaLanguages-Localization/
├── index.html
│
├── locales/
│   ├── en/ui.json
│   ├── lou/ui.json
│   └── frc/ui.json
│
├── apple-cldr/
│   ├── README.md
│   ├── locale-data/
│   │   ├── en/locale.json
│   │   ├── lou/locale.json
│   │   └── frc/locale.json
│   ├── terminology/
│   │   ├── lou.json
│   │   └── frc.json
│   ├── docs/
│   │   ├── ORTHOGRAPHY_LOU.md
│   │   ├── ORTHOGRAPHY_FRC.md
│   │   └── SOURCES.md
│   ├── review/
│   │   ├── REVIEW_PROCESS.md
│   │   ├── reviewers.csv
│   │   └── decisions.csv
│   ├── submission/
│   │   ├── APPLE_REQUEST_TEMPLATE.md
│   │   └── EVIDENCE_CHECKLIST.md
│   └── cldr/
│       └── README.md
│
└── screenshots/
    └── README.md
```

The visual editor and translation files are what contributors use most often.
The `apple-cldr/` folder is the standards/evidence layer.
