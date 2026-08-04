# Scientific defaults

The public release matches the manuscript analysis:

- ECG high-pass filter: fourth-order zero-phase Butterworth, 500 Hz
- Rectification: absolute value
- Envelope: 1-s moving average
- Processed SKNA sampling: 100 Hz
- Primary signal: median across available ECG-derived SKNA channels
- Threshold calibration: up to 60 s immediately before event onset; onset excluded
- Adaptive threshold: maximum of weighted two-component GMM intersection, baseline 95th percentile, and baseline median + 6×MAD
- Burst occupancy: percentage of samples above the adaptive threshold
- Sequential replay: 30-s trailing window, 10-s update, >5% occupancy, two consecutive qualifying updates

No INAP or post-INAP samples are used to estimate the event threshold.
