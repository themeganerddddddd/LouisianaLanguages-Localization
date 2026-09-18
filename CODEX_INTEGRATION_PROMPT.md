# Codex task: integrate community localization into LouisianaFrench

Repository to modify:
`themeganerddddddd/LouisianaFrench`

Localization source:
the new `LouisianaLanguages-Localization` repository containing:
- `locales/en/ui.json`
- `locales/lou/ui.json`
- `locales/frc/ui.json`

## Goal

Make all user-facing interface text translatable without changing lesson/content identifiers or learner data.

Native speakers must be able to edit JSON translations independently of React Native screen code.

## Non-negotiable compatibility constraint

The existing app uses `cajun` and `kreole` as internal course/data/storage identifiers.

DO NOT rename or migrate those identifiers in this task.

Create a UI-locale mapping:

```js
const COURSE_TO_UI_LOCALE = {
  cajun: 'frc',
  kreole: 'lou'
};
```

English must also be available as `en`.

## Implement

1. Add bundled locale snapshots under:
   `src/locales/en/ui.json`
   `src/locales/lou/ui.json`
   `src/locales/frc/ui.json`

2. Add a small localization layer under `src/localization/`:
   - `LocalizationProvider.js`
   - `useTranslation.js` if useful
   - locale selection persisted with AsyncStorage
   - English fallback for missing/empty translations
   - `t("home.todaysPlan")`-style lookup
   - no network dependency required at runtime

3. Keep UI language selection separate from the course being learned.
   A person studying Kouri-Vini should eventually be able to use an English, Kouri-Vini, or Louisiana French interface.

4. Add a Settings screen if none exists, with:
   - Settings
   - Interface language
   - English
   - Louisiana French
   - Kouri-Vini
   The language selection must update the interface immediately and persist across launches.

5. Replace hard-coded user-facing strings across active `src/screens/` and `src/components/` with translation keys.
   Do not translate:
   - internal route names
   - test IDs
   - storage keys
   - file paths
   - analytics/debug identifiers
   - lesson vocabulary/content in this task

6. Preserve accessibility labels by localizing them too.

7. Tests:
   - English fallback works when a `lou` or `frc` value is empty.
   - `cajun` maps to `frc` only for UI locale purposes.
   - `kreole` maps to `lou` only for UI locale purposes.
   - switching UI locale updates rendered labels.
   - persisted locale loads on restart.
   - existing learner progress/storage tests keep passing.

8. Add `scripts/sync_localizations.py` or equivalent so an approved snapshot from the localization repository can be copied into `src/locales/` before a release.
   The app build should use committed locale snapshots, not depend on GitHub being online.

9. Run:
   - `npm test -- --runInBand`
   - `npm run lint`
   Fix regressions caused by this task.

## Important

Do not invent Kouri-Vini or Louisiana French translations. Empty translation values are intentional until native speakers approve them in Weblate.

Do not change lesson CSV/JSON content in this task.
Do not change keyboard or autocorrect features in this task.
