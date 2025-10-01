import requests
from mutate import mutate_data
from database_loader import load_data_to_postgres


files = [
    "ufc_event_details.csv",
    "ufc_fight_details.csv",
    "ufc_fight_results.csv",
    "ufc_fight_stats.csv",
    "ufc_fighter_details.csv",
    "ufc_fighter_tott.csv"
]

for fname in files:
    response = requests.get(
        'https://raw.githubusercontent.com/Greco1899/scrape_ufc_stats/refs/heads/main/' + fname)
    with open(fname, 'wb') as f:
        f.write(response.content)

mutate_data()
load_data_to_postgres()