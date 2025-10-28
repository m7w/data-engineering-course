import argparse
import csv
import logging
from time import sleep

from requests import request
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(filename="customs-fetch.log", level=logging.INFO)

def fetch_data():
parser = argparse.ArgumentParser(description="Fetches customs data")
parser.add_argument(
    "-f",
    "--from",
    dest="start_page",
    help="page to start from",
    type=int,
    default=1,
args = parser.parse_args()
    BASE_URL = "http://5.159.103.79:4000/api/v1/logs"
    response = request("GET", BASE_URL, params={"page": 1})
    if response.status_code == 200:
        body = response.json()
        total_entries = body["totalEntries"]
        per_page = body["per_page"]
        total_pages = total_entries // per_page + (1 if total_entries % per_page != 0 else 0)
        header = body["items"][0].keys()
        with open("customs_data.csv", mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter="\t")
            writer.writerow(header)
    
            rows = []
            for i in tqdm(range(1, total_pages + 1)):
            pbar = tqdm(initial=start_page, total=total_pages + 1)
                response = request("GET", BASE_URL, params={"page": i})
                if response.status_code == 200:
                    for item in body["items"]:
                        rows.append(item.values())
                elif response.status_code == 429:
                    logger.info("Waiting for 3 min...")
                    sleep(3 * 60 + 2)
                    logger.info("Continue")
                else:
                    logger.info(
                        f"Error getting data for page {i}. Response status code: {response.status_code}"
                    )
                    raise Exception(
                        f"Error getting data for page {i}. Response status code: {response.status_code}"
                    )
            writer.writerows(rows)
            logger.info(f"Fetched {total_pages} pages")
            pbar.close()
    else:
        raise Exception(f"Error getting first data. Response status code: {response.status_code}")

def main():
    logger.info("Start fetching")
    fetch_data(args.start_page)
    logger.info("Fetching finished")
    print("All data was fetched!")
