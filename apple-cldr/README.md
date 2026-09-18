# Louisiana Languages — Apple / CLDR Readiness

This folder collects the language and locale information needed to make Kouri-Vini (`lou`)
and Louisiana French (`frc`) technically ready for broader platform localization work.

It is separate from the visual iOS translation editor. The editor collects screen/UI wording.
This folder collects language-wide locale rules and the evidence needed for review.

## Goals

1. Build a reviewed, machine-readable locale dataset for `lou` and `frc`.
2. Record native-speaker and expert review decisions.
3. Document orthography, terminology, punctuation, dates, numbers, and other system conventions.
4. Produce a clean evidence package for Apple and for future Unicode CLDR work.
5. Never treat machine-generated translations as approved language data.

## Language codes

- `lou` — Louisiana Creole / Kouri-Vini
- `frc` — Cajun French / Louisiana French

## What native speakers should edit

- `locale-data/lou/locale.json`
- `locale-data/frc/locale.json`
- `terminology/lou.json`
- `terminology/frc.json`
- `docs/ORTHOGRAPHY_LOU.md`
- `docs/ORTHOGRAPHY_FRC.md`

## Review rule

A value should not be marked `approved` until it has been reviewed by at least one trusted
native/fluent reviewer other than the original contributor, unless the project documents a
different rule.

Blank values mean "not yet established."
