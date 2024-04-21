import requests

from roomnl_config import ROOMNL_CONFIG, SEARCH_PRIORITY
from tg_bot import send_telegram_message

def get_number_of_rooms(priority_rooms: bool):
    url = "https://roomapi.hexia.io/api/v1/actueel-aanbod"
    querystring = {"limit":"30","locale":"en_GB","page":"0"}

    payload = ROOMNL_CONFIG
    payload["filters"] = {"$and": [{"reactionData.toonAlsVoorrangsgroep": {"$eq": "1" if priority_rooms else "0"}}]}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,pl;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.room.nl",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.room.nl/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "TE": "trailers"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    r = response.json()
    num_rooms = r["_metadata"]["total_search_count"]
    
    if response.status_code != 200:
        print(f"Failed to get rooms: {response.text}")
        send_telegram_message(f"Failed to get ROOM.nl rooms: {response.text}")
        quit()

    return num_rooms

if __name__ == "__main__":
    
    num_rooms = get_number_of_rooms(SEARCH_PRIORITY)
    print(num_rooms, f"rooms with{'out' if not SEARCH_PRIORITY else ''} priority found")
    
    if num_rooms > 0:        
        send_telegram_message(f"{num_rooms} ROOM.nl rooms{' with PRIORITY' if SEARCH_PRIORITY else ''} are now available! Quick go to https://www.room.nl/ to book!")
    elif num_rooms == 0:
        send_telegram_message(f"No ROOM.nl rooms{' with PRIORITY' if SEARCH_PRIORITY else ''} are available. Try again later.")
