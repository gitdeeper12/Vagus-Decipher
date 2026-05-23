# Vagus-Decipher Reports Directory

This directory contains analysis reports, benchmark results, and simulation outputs.

## Directory Structure

```

reports/
├── benchmarks/          # Benchmark results (M1, M2, M3)
├── figures/             # Generated figures and plots
├── logs/                # Processing logs
└── README.md            # This file

```

## Report Formats

- **JSON (.json)**: Structured result data
- **CSV (.csv)**: Time series data
- **TXT (.txt)**: Text summaries

## Generating Reports

```python
from vagus_decipher import VagusDecipherEngine
import json

engine = VagusDecipherEngine()
result = engine.process(signal)

with open('reports/result.json', 'w') as f:
    json.dump(result, f, indent=2)
```

Benchmark Reports

· benchmarks/m1_lps_results.json
· benchmarks/m2_sirs_results.json
· benchmarks/m3_cart_results.json

Note

This directory is gitignored. Large result files are not tracked in version control.
