# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
import json
from pathlib import Path
import requests
import logging

# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def download_allcyberattacks(api_key, out_dir):
    url = "https://api.ransomware.live/v2/allcyberattacks"

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Ransomware.live request starting | url=%s", url)
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else ('')
    
    r = requests.get(url, headers=headers, timeout=120)
    logger.info("Ransomware.live response received | status=%s", r.status_code)
    
    r.raise_for_status()
    data = r.json()

    out_file = out_dir / "allcyberattacks.json"
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info("Ransomware_live saved")

    return out_file
