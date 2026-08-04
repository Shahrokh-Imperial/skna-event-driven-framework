# Data schema

## Processed recording CSV
Required: a numeric time column (`time_s` preferred) and a median SKNA column (`skna_med` preferred). Channel-specific SKNA columns such as `compact_skna_1` are optional. Processed cohort SKNA may be stored in mV; the framework records the inferred conversion to µV.

## Event CSV
One row per event with numeric start and end columns, for example `start_s,end_s`.

## Raw recording
The preprocessing CLI accepts LabChart-style TXT or ZIP exports containing a time column and ECG channels. Extra columns are preserved where possible.
