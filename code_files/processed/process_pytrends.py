# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
from pathlib import Path
import pandas as pd
import logging

# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def process_pytrends_csv(in_dir, out_dir):

    in_dir = Path(in_dir)
    out_dir = Path(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    csv_files = list(in_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No .csv found in {in_dir}")

    csv_file = csv_files[0] 
    logger.info("Pytrends processing started | input=%s", csv_file)

    df = pd.read_csv(csv_file)
    logger.info("Loaded pytrends")

    out_csv = out_dir / csv_file.name
    out_json = out_dir / (csv_file.stem + ".json")

    df.to_csv(out_csv, index=False)
    df.to_json(out_json, orient="records", lines=True)

    logger.info("Pytrends saved CSV")
    logger.info("Pytrends saved JSON")

    return out_csv, out_json
