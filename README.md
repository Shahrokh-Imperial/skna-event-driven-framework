# SKNA Event-Driven Framework

Version **1.0.0** — first public release.

A reproducible Python framework for extracting ECG-derived skin sympathetic nerve activity (SKNA), estimating recording-specific adaptive burst thresholds, calculating burst occupancy, and running sequential replay under real-time information constraints.

## Scientific workflow

1. High-pass filter ECG at 500 Hz using a fourth-order zero-phase Butterworth filter.
2. Rectify and smooth with a 1-s moving average.
3. Combine available channel envelopes using median fusion and represent SKNA at 100 Hz.
4. Estimate the adaptive threshold from up to 60 s immediately before event onset:

   `max(GMM intersection, baseline q95, baseline median + 6×MAD)`

5. Define burst occupancy as the percentage of samples above that threshold.
6. Replay sequentially using a 30-s trailing window updated every 10 s. Trigger activation requires occupancy >5% in two consecutive updates.

## Installation

```bash
git clone https://github.com/Shahrokh-Imperial/skna-event-driven-framework.git
cd skna-event-driven-framework
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
```

## Quick start with synthetic data

```bash
python scripts/05_run_event_analysis.py   examples/synthetic_processed_recording.csv   examples/synthetic_events.csv   --out-dir outputs/synthetic_run
```

Outputs include event-specific replay CSV files, an event summary, threshold components, latency metrics, and a JSON configuration record.

## Main commands

```bash
python scripts/01_preprocess_recording.py INPUT.txt --out outputs/processed.csv
python scripts/02_detect_uap_events.py outputs/processed.csv --out outputs/events.csv
python scripts/03_compute_adaptive_thresholds.py outputs/processed.csv --event-start 80 --out outputs/threshold.csv
python scripts/04_run_sequential_replay.py outputs/processed.csv --threshold 1.2 --out outputs/replay.csv
python scripts/05_run_event_analysis.py outputs/processed.csv outputs/events.csv --out-dir outputs/analysis
```

Use `--help` on each script before analysing new data.

## Input data

See `docs/DATA_SCHEMA.md`. Experimental recordings are not included. The bundled example is synthetic and carries no animal or participant data.

## Repository map

- `src/skna_framework/`: scientific processing and I/O functions
- `scripts/`: command-line entry points
- `config/defaults.json`: frozen manuscript-consistent defaults
- `examples/`: synthetic demonstration data
- `tests/`: numerical and configuration tests
- `docs/`: methods, data schema, reproducibility, and release guidance

## Scope and limitations

This software is research software, not a medical device. Sequential replay is an offline deployment-oriented evaluation and does not replace prospective real-time validation. ECG-derived SKNA is a surrogate measure and should be interpreted in the context of the experimental protocol and signal quality.

## Citation and licence

See `CITATION.cff`. Released under the MIT License.
