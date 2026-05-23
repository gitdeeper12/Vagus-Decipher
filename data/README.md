# Vagus-Decipher Data Directory

## Example Datasets

| File | Description |
|------|-------------|
| `lps_endotoxemia.csv` | LPS endotoxemia challenge (M1) |
| `sterile_sirs.csv` | Sterile SIRS challenge (M2) |
| `car_t_crs.csv` | CAR-T CRS analog (M3) |

## Data Format

Each CSV contains:
- `time_min`: Time in minutes
- `ISI`: Inflammatory Storm Index
- `TNF_a_pgml`: TNF-alpha concentration (pg/mL)
- `IL_6_pgml`: IL-6 concentration (pg/mL)
- `IL_10_pgml`: IL-10 concentration (pg/mL)
- `alert_level`: Clinical alert level

## Usage

```python
import pandas as pd
df = pd.read_csv('examples/lps_endotoxemia.csv')
print(df.head())
```

