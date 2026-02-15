# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
import os
import requests
import logging
from datetime import datetime

#Taken help from: https://github.com/ahur4/nvd-client
#Taken help from: https://dev.to/gug_31c7ba64d1c563490bc42/fetching-and-storing-cve-data-from-nvd-api-using-python-4dog
#Taken help from: https://www.youtube.com/watch?v=EgmHjgmAGfs

# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def download_nvd_raw(keyword, out_dir, results_per_page=5, api_key=None):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    os.makedirs(out_dir, exist_ok=True)

    headers = {"apiKey": api_key} if api_key else print("{No API key}")
    params = {"keywordSearch": keyword, "resultsPerPage": results_per_page}

    logger.info("NVD request starting | keyword=%s | resultsPerPage=%s", keyword, results_per_page)
    r = requests.get(url, headers=headers, params=params, timeout=60)
    logger.info("NVD response received | status=%s", r.status_code)
    r.raise_for_status()
    filename = f"nvd_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(out_dir, filename)
    with open(path, "wb") as f:
        f.write(r.content)
    logger.info("NVD raw saved | bytes=%s",len(r.content))

    return path