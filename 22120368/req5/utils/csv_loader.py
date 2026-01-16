import csv
from pathlib import Path


def load_csv_as_dicts(path):
    """Load a CSV file and return list of dict rows. Empty lines are skipped."""
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader if any(v.strip() for v in row.values())]
