# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
import os
import json
import pandas as pd
import logging

# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def process_ransomware_json(in_json, out_csv, out_json):
    
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    os.makedirs(os.path.dirname(out_json), exist_ok=True)

    logger.info("Ransomware processing started | input=%s", in_json)

    with open(in_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    df.to_csv(out_csv, index=False)
    df.to_json(out_json, orient="records", force_ascii=False, indent=2)

    logger.info("Ransomware saved CSV")
    logger.info("Ransomware saved JSON")

    return out_csv, out_json
