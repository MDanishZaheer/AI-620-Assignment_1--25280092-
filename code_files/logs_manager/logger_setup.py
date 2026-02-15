# Name: M Danish Zaheer
# Roll no: 25280092

# been working with log files 

# importing libraries
import logging
from pathlib import Path

def setup_logger(log_file="logs/pipeline.log"):
    
    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(format)
    logger.addHandler(handler)

    out = logging.FileHandler(log_file, encoding="utf-8")
    out.setFormatter(format)
    logger.addHandler(out)

    return logger
