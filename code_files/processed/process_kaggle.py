# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
from pathlib import Path
import zipfile
import pandas as pd
import logging

# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def process_kaggle_zip(raw_zip_path, out_dir, tmp_dir):

    raw_zip_path = Path(raw_zip_path)
    out_dir = Path(out_dir)
    tmp_dir = Path(tmp_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Kaggle processing started | zip=%s", raw_zip_path)

    with zipfile.ZipFile(raw_zip_path, "r") as z:
        z.extractall(tmp_dir)

    csv_files = list(tmp_dir.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV found in {tmp_dir} after unzip.")
    if len(csv_files) > 1:
        raise ValueError(f"Expected 1 CSV, found {len(csv_files)} in {tmp_dir}.")

    csv_file = csv_files[0]
    logger.info("Found CSV: %s", csv_file.name)

    df = pd.read_csv(csv_file)
    logger.info("Loaded CSV ")

    out_base = out_dir / csv_file.stem
    csv_out = out_base.with_suffix(".csv")
    json_out = out_base.with_suffix(".json")

    df.to_csv(csv_out, index=False)
    df.to_json(json_out, orient="records", lines=True)

    logger.info("Saved processed CSV.")
    logger.info("Saved processed JSON.")

    return csv_out, json_out
