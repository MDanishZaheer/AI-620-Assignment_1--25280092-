# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
from pathlib import Path
import logging
import os

# tutorial helped: https://www.youtube.com/watch?v=hzcV0hDkfzs&t=135s
# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def download_kaggle_zip(dataset_slug: str, raw_dir: Path, kaggle_username: str, kaggle_key: str):

    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    os.environ["KAGGLE_USERNAME"] = kaggle_username.strip()
    os.environ["KAGGLE_KEY"] = kaggle_key.strip()
    
    from kaggle.api.kaggle_api_extended import KaggleApi
    logger.info("Kaggle download starting | dataset=%s | dir=%s", dataset_slug, raw_dir)
    
    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(dataset_slug, path=str(raw_dir), unzip=False, force=True)
    expected_zip = raw_dir / f"{dataset_slug.split('/')[-1]}.zip"
    logger.info("Kaggle download finished")
    
    return expected_zip
