# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
import os
import getpass
from pathlib import Path
import papermill as pm
import logging
from dotenv import load_dotenv

# importing logger file 
from code_files.logs_manager.logger_setup import setup_logger
# importing functions from sub folders as required modular coding each have its own working
from code_files.extract.extract_kaggle import download_kaggle_zip
from code_files.extract.extract_pytrends import download_pytrends
from code_files.extract.extract_ransomware_live import download_allcyberattacks
from code_files.extract.extract_nvd import download_nvd_raw
# importing functions from sub folders as required modular coding each have its own working
from code_files.processed.process_kaggle import process_kaggle_zip
from code_files.processed.process_pytrends import process_pytrends_csv
from code_files.processed.process_ransomware_live import process_ransomware_json
from code_files.processed.process_nvd import process_nvd_latest 

# adding conditions helps in testing and breaking code into parts
RUN_EXTRACT_KAGGLE = True
RUN_EXTRACT_PYTRENDS = True
RUN_EXTRACT_RANSOMWARE = True
RUN_EXTRACT_NVD = True
RUN_PROCESS_KAGGLE = True
RUN_PROCESS_PYTRENDS = True
RUN_PROCESS_RANSOMWARE = True
RUN_PROCESS_NVD = True
RUN_TRANSFORMATION = True
RUN_VISUALIZATIONS = True

# setting and calling logs
setup_logger("logs/pipeline.log")
logger = logging.getLogger(__name__)

def main():
    logger.info("Pipeline started")

    # extracting data from each source
    if RUN_EXTRACT_KAGGLE:
        dataset_slug = "atharvasoundankar/global-cybersecurity-threats-2015-2024"
        raw_dir = Path("data/raw/kaggle")

        load_dotenv() # loading api keys from .env file
        username = (os.getenv("KAGGLE_USERNAME") or "").strip()
        key = (os.getenv("KAGGLE_KEY") or "").strip()

        # if api key not finded then it will ask for it on runtime terminal
        if not username:
            username = input("Enter Kaggle username: ").strip()
        if not key:
            key = getpass.getpass("Enter Kaggle API key (hidden): ").strip()

        zip_path = download_kaggle_zip(dataset_slug, raw_dir, kaggle_username=username, kaggle_key=key)
        logger.info("Downloaded Kaggle zip to: %s", zip_path)

    if RUN_EXTRACT_PYTRENDS:
        keywords = ["cybersecurity", "SQL injection", "ransomware", "phishing"] 
        timeframe = "2020-01-01 2025-12-31"
        geo = ""
        gprop = ""

        out_dir = "data/raw/pytrends"
        out_file = "pytrends_2020_2025.csv"

        path = download_pytrends(keywords=keywords, timeframe=timeframe, out_dir=out_dir, out_file=out_file, geo=geo, gprop=gprop)
        logger.info("Saved pytrends CSV at: %s", path)

    if RUN_EXTRACT_RANSOMWARE:
        load_dotenv()# loading api keys from .env file

        # if api key not finded then it will ask for it on runtime terminal
        api_key = (os.getenv("RANSOMWARE_LIVE_API_KEY") or "").strip()
        while not api_key:
            api_key = getpass.getpass("Enter Ransomware.live API key (hidden): ").strip()

        out_dir = "data/raw/ransomware_live"

        out_file = download_allcyberattacks(api_key=api_key, out_dir=out_dir)
        logger.info("Saved ransomware json to: %s", out_file)

    if RUN_EXTRACT_NVD:
        load_dotenv() # loading api keys from .env file

        # if api key not finded then it will ask for it on runtime terminal
        nvd_api_key = (os.getenv("NVD_API_KEY") or "").strip()
        if not nvd_api_key:
            nvd_api_key = getpass.getpass("Enter NVD API key (hidden): ").strip()

        out_dir = "data/raw/nvd_raw"
        keyword = "sql injection"

        saved_path = download_nvd_raw(keyword=keyword, out_dir=out_dir, results_per_page=5, api_key=nvd_api_key)
        logger.info("Saved NVD raw response to: %s", saved_path)
 
    # code to process files 
    if RUN_PROCESS_KAGGLE:
        zips = list(Path("data/raw/kaggle").glob("*.zip"))
        if not zips:
            raise FileNotFoundError("No Kaggle zip found in data/raw/kaggle")
        raw_zip = zips[0] 

        csv_out, json_out = process_kaggle_zip(raw_zip_path=raw_zip, out_dir="data/processed/kaggle", tmp_dir="data/raw/kaggle/_tmp_extract")
        
        logger.info("Kaggle processed CSV: %s", csv_out)
        logger.info("Kaggle processed JSON: %s", json_out)

    if RUN_PROCESS_PYTRENDS:
        # i have already handled exception handling for this case in process_pytrends function file
        py_csv, py_json = process_pytrends_csv(in_dir="data/raw/pytrends", out_dir="data/processed/pytrends")

        logger.info("Pytrends processed CSV: %s", py_csv)
        logger.info("Pytrends processed JSON: %s", py_json)

    if RUN_PROCESS_RANSOMWARE:
        # i have already handled exception handling for this case in process_pytrends function file
        out_csv, out_json = process_ransomware_json( in_json="data/raw/ransomware_live/allcyberattacks.json", out_csv="data/processed/ransomware/allcyberattacks.csv", out_json="data/processed/ransomware/allcyberattacks.json")
        
        logger.info("Ransomware processed CSV: %s", out_csv)
        logger.info("Ransomware processed JSON: %s", out_json)

    if RUN_PROCESS_NVD:
        # i have already handled exception handling for this case in process_pytrends function file
        out_json, out_csv = process_nvd_latest(raw_dir="data/raw/nvd_raw", out_dir="data/processed/nvd")

        logger.info("NVD saved JSON: %s", out_json)
        logger.info("NVD saved CSV: %s", out_csv)

    # implemeneted the transformation and visulizations in .ipynb for easy debugging
    if RUN_TRANSFORMATION:
        pm.execute_notebook(
            r"code_files\transformation\processed_data_transformation.ipynb",
            r"code_files\transformation\processed_data_transformation.ipynb",
            parameters={},
            kernel_name= "data_engg"
        )
        logger.info("Transformation notebook executed")

    if RUN_VISUALIZATIONS:
        pm.execute_notebook(
            r"visualizations\visualization_code_file.ipynb",
            r"visualizations\visualization_code_file.ipynb",
            parameters={},
            kernel_name= "data_engg"
        )
        logger.info("Visualization notebook executed")

    logger.info("Pipeline finished")

if __name__ == "__main__":
    main()