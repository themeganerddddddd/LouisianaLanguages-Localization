# Contributing translations

Thank you for helping Louisiana French and Kouri-Vini appear accurately in software.

## For native speakers

You do not need to edit app code.

Edit only the value on the right side of a translation key in:

- `locales/lou/ui.json` for Kouri-Vini
- `locales/frc/ui.json` for Louisiana French

Example:

```json
{
  "settings": {
    "title": "YOUR TRANSLATION HERE"
  }
}
```

Do not rename `settings`, `title`, or any other JSON key.

## Translation principles

- Prefer natural language a native speaker would expect in a phone/app interface.
- Do not force metropolitan/standard French wording onto Louisiana French when a normal Louisiana form is preferred.
- For Kouri-Vini, use the project's agreed modern orthography consistently.
- Keep labels concise enough for phone screens.
- Preserve punctuation when it affects meaning.
- Preserve placeholders exactly, e.g. `{{count}}`, `%s`, `{name}`.
- If more than one form is valid, use the review discussion rather than silently deleting a regional alternative.

## Review

A translation should ideally be reviewed by at least one other fluent/native speaker before it is treated as final.

For disputed forms:
1. leave a Weblate comment;
2. describe region/community usage if relevant;
3. cite a reference if there is a published standard or dictionary;
4. let reviewers decide which form is used as the UI default.

The project can document accepted alternatives separately later; the UI file should contain one default string per key.
