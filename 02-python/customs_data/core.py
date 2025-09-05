import csv
from time import sleep

from requests import request
from tqdm import tqdm


def fetch_data():
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
                response = request("GET", BASE_URL, params={"page": i})
                if response.status_code == 200:
                    for item in body["items"]:
                        rows.append(item.values())
                elif response.status_code == 429:
                    print("Waiting...") 
                    sleep(3 * 60 + 2)
                    print("Continuing")
                else:
                    raise Exception(f"Error getting data for page {i}. Response status code: {response.status_code}")
                if i % 5000:
                    writer.writerows(rows)
                    rows = []
    else:
        raise Exception(f"Error getting first data. Response status code: {response.status_code}")

def main():
    fetch_data()
    print("All data was fetched!")
