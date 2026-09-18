# CLDR Mapping

This directory is for future mapping of the reviewed locale data into Unicode CLDR structures.

Do not create CLDR XML by guessing.

First establish approved values in `locale-data/lou/locale.json` and
`locale-data/frc/locale.json`, then map them to the appropriate CLDR fields.

Likely areas include:
- locale display names;
- exemplar characters;
- date/time formats;
- month/day names;
- number symbols and formats;
- currency formats;
- plural rules;
- measurement preferences;
- quotation marks;
- week data.

Before submitting anything upstream, compare against current CLDR requirements and existing
coverage for `lou` and `frc`.
