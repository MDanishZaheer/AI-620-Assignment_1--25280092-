# Name: M Danish Zaheer
# Roll no: 25280092

# importing libraries
from pathlib import Path
import logging
import time
from datetime import datetime, timedelta
import pandas as pd
from pytrends.request import TrendReq

# tutorials: https://www.youtube.com/watch?v=WSnZrEI-sZ0&t=450s, https://www.youtube.com/watch?v=W2pYB3RjGDc
# Taken help from g.p.t multiple times while debugging and implemented its changes as suggested by it because of rate limit issue
# setting a logger name after the current file name to be shown in logs pipeline
logger = logging.getLogger(__name__)

def download_pytrends(keywords, timeframe, out_dir, out_file, geo="", gprop="", rate_limit_wait=3, chunk_years=2):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    start_s, end_s = timeframe.split()
    start_date = datetime.strptime(start_s, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_s, "%Y-%m-%d").date()

    if start_date.day == 1:
        start_boundary = start_date
    else:
        start_boundary = (start_date.replace(day=1) + timedelta(days=32)).replace(day=1)

    if end_date.day == 1:
        end_boundary = end_date
    else:
        end_boundary = (end_date.replace(day=1) + timedelta(days=32)).replace(day=1)

    logger.info("Pytrends download starting(chunked raw) | keywords=%s | start=%s | end=%s", keywords, start_boundary, end_boundary)

    pytrends = TrendReq(hl="en-US", tz=0)
    all_chunks = []
    chunk_start = start_boundary
    chunk_number = 1

    while chunk_start < end_boundary:
        if chunk_number > 1 and rate_limit_wait > 0:
            logger.info("Rate limit wait | seconds=%s", rate_limit_wait)
            time.sleep(rate_limit_wait)
        chunk_end_excl = (pd.Timestamp(chunk_start) + pd.DateOffset(years=chunk_years)).date()
        if chunk_end_excl > end_boundary:
            chunk_end_excl = end_boundary

        req_end_incl = chunk_end_excl - timedelta(days=1)
        chunk_tf = f"{chunk_start:%Y-%m-%d} {req_end_incl:%Y-%m-%d}"
        logger.info("Requesting chunk %s | timeframe=%s", chunk_number, chunk_tf)

        pytrends.build_payload(keywords, timeframe=chunk_tf, geo=geo, gprop=gprop)
        chunk_df = pytrends.interest_over_time()

        if chunk_df is not None and not chunk_df.empty:
            chunk_df.index = pd.to_datetime(chunk_df.index)
            chunk_df = chunk_df[(chunk_df.index >= pd.Timestamp(chunk_start)) & (chunk_df.index < pd.Timestamp(chunk_end_excl))]
            logger.info("Chunk received | request_start=%s | request_end=%s | rows=%s | first=%s | last=%s",chunk_start, req_end_incl, len(chunk_df), chunk_df.index.min().date() if len(chunk_df) else None, chunk_df.index.max().date() if len(chunk_df) else None)
            all_chunks.append(chunk_df)

        chunk_start = chunk_end_excl
        chunk_number = chunk_number + 1

    if not all_chunks:
        logger.warning("Pytrends returned empty data.")
        raise ValueError("Pytrends returned empty data.")

    df = pd.concat(all_chunks).sort_index()
    df = df[(df.index >= pd.Timestamp(start_boundary)) & (df.index < pd.Timestamp(end_boundary))]

    out_path = out_dir / out_file
    df.to_csv(out_path, index=True)

    logger.info("Pytrends data saved | rows=%s | cols=%s", len(df), len(df.columns))
    return out_path
