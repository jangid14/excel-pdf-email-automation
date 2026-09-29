from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


INPUT_DIR = BASE_DIR / "input"

OUTPUT_DIR = BASE_DIR / "output"

LOG_DIR = BASE_DIR / "logs"


INPUT_FILE = (
    INPUT_DIR /
    "electricity_bill.xlsx"
)


LOG_FILE = (
    LOG_DIR /
    "automation.log"
)