import pytest
from pathlib import Path
from utils.csv_loader import load_csv_as_dicts


def pytest_generate_tests(metafunc):
    """
    Dynamically parametrize tests based on CSV files in `data/`.

    Convention:
    - CSV files live under `data/<module_name>/<function_name>.csv` or `data/<function_name>.csv`.
    - If a CSV is present, the test will be parametrized with a single argument named `csv_data`.
      Each invocation provides one row as a dict.
    """
    # only act when test accepts `csv_data` argument
    if 'csv_data' not in metafunc.fixturenames:
        return

    # Construct potential CSV paths
    # module path: tests/test_xxx.py -> data/test_xxx/<func>.csv
    module_path = Path(metafunc.module.__file__)
    tests_root = Path(__file__).parent
    data_dir = tests_root / 'data'

    candidates = []

    # data/<module_name>/<func>.csv
    module_name = module_path.stem
    candidates.append(data_dir / module_name / f"{metafunc.function.__name__}.csv")

    # data/<func>.csv
    candidates.append(data_dir / f"{metafunc.function.__name__}.csv")

    # data/<module_name>.csv (module-level CSV)
    candidates.append(data_dir / f"{module_name}.csv")

    for p in candidates:
        if p.exists():
            rows = load_csv_as_dicts(p)
            if rows:
                metafunc.parametrize('csv_data', rows)
            return

    # No CSV found: parametrize with a single empty dict so tests still run
    metafunc.parametrize('csv_data', [{}])
