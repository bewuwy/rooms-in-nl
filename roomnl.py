import requests
# import json

from roomnl_config import ROOMNL_CONFIG, SEARCH_PRIORITY
from tg_bot import send_telegram_message
from datetime import datetime

def get_rooms(priority_rooms: bool):
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
    
    # # save response to json
    # with open("roomnl.json", "w") as f:
    #     json.dump(r, f, indent=4)
        
    rooms = r["data"]
    num_rooms = r["_metadata"]["total_search_count"]
    
    if response.status_code != 200:
        print(f"Failed to get rooms: {response.text}")
        send_telegram_message(f"Failed to get ROOM.nl rooms: {response.text}")
        quit()

    return rooms, num_rooms

if __name__ == "__main__":
    
    rooms, num_rooms = get_rooms(SEARCH_PRIORITY)
    
    if num_rooms > 0:        
        msg = f"{num_rooms} ROOM.nl room{'s' if num_rooms > 1 else ''}{' with PRIORITY' if SEARCH_PRIORITY else ''} " + \
            f"{'are' if num_rooms > 1 else 'is'} now available!\n\n"
        
        closing_dates = {}
        for room in rooms:
            closing_date = room["closingDate"]
            closing_date = datetime.strptime(closing_date, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            
            closing_dates[closing_date] = closing_dates.get(closing_date, 0) + 1
        
        # sort closing dates
        closing_dates_i = sorted(closing_dates.keys())
        
        for closing_date in closing_dates_i:
            count = closing_dates[closing_date]
            in_days = (closing_date - datetime.now().date()).days
            in_days = f"(in {in_days} days)" if in_days > 0 else "(today!)"
            
            msg += f"- {count} room{'s' if count > 1 else ''} closing on {closing_date.strftime('%d.%m')} {in_days}\n"
        
        msg += "\nSee them at https://room.nl/en/offerings/to-rent#?gesorteerd-op=zoekprofiel&voorrang=1"
        
    elif num_rooms == 0:
        msg = f"No ROOM.nl rooms{' with PRIORITY' if SEARCH_PRIORITY else ''} are available. Try again later."

    send_telegram_message(msg)
    print(msg)
