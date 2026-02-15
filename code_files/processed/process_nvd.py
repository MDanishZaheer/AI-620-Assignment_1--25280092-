# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
import json
import csv
import glob
import os
import logging


# taken help from g.p.t muliple times while debugging and implemented its suggested changes in this file
# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def process_nvd_latest(raw_dir, out_dir):

    pattern = os.path.join(raw_dir, "nvd_raw_*.json")
    files = glob.glob(pattern)
    in_file = max(files, key=os.path.getmtime) if files else None
    if not in_file:
        raise FileNotFoundError(f"No file found like {pattern}")

    os.makedirs(out_dir, exist_ok=True)
    out_json = os.path.join(out_dir, "nvd.json")
    out_csv  = os.path.join(out_dir, "nvd.csv")

    logger.info("NVD processing started | input=%s", in_file)

    with open(in_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        descs = cve.get("descriptions", [])

        desc = ""
        if isinstance(descs, list) and len(descs) > 0 and isinstance(descs[0], dict):
            desc = descs[0].get("value", "")

        rows.append({
            "id": cve.get("id", ""),
            "published": cve.get("published", ""),
            "desc": desc
        })

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "published", "desc"])
        w.writeheader()
        w.writerows(rows)

    logger.info("NVD saved JSON")
    logger.info("NVD saved CSV ")

    return out_json, out_csv
