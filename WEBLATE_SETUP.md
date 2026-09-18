# Weblate setup

Use Weblate as the browser-based collaborative editor for native speakers.

## Recommended component

Project name:
`Louisiana Languages`

Component:
`App UI`

Repository:
the GitHub URL for this repository

Branch:
`main`

Source language:
`English (en)`

Source file:
`locales/en/ui.json`

Translation file mask:
`locales/*/ui.json`

Target languages:
- Louisiana Creole / Kouri-Vini (`lou`)
- Cajun / Louisiana French (`frc`)

File format:
JSON / nested JSON

## Git behavior

Recommended:
- Weblate pulls from `main`.
- Contributors translate in Weblate.
- Trusted reviewers approve strings.
- Weblate creates commits or pull requests back to GitHub.
- GitHub Actions runs `scripts/validate_locales.py`.

## If Weblate does not already list `lou` or `frc`

Create custom Weblate language entries using:
- code: `lou`, name: `Louisiana Creole / Kouri-Vini`
- code: `frc`, name: `Louisiana French / Cajun French`

Do not substitute generic `fr` for Louisiana French.

## Reviewer roles

Suggested:
- Translator — can suggest/edit
- Reviewer — fluent/native speaker who approves
- Maintainer — controls repository sync and releases

Start with review required rather than automatically publishing every edit.
