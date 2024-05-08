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

    # load old available rooms from text file
    r_ids_old = []
    try:
        with open("roomnl_rooms.txt", "r", encoding='utf-8') as f:
            r_ids_old = f.read().splitlines()
    except FileNotFoundError:
        pass
    
    # save available rooms to text file
    r_ids = []
    for r in rooms:
        r_id = f"{r['street']} {r['houseNumber']}" # - {r['id']}
        r_ids.append(r_id)
    r_ids = sorted(r_ids)
    with open("roomnl_rooms.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(r_ids))

    if num_rooms == 0:
        send_telegram_message(f"No ROOM.nl rooms{' with PRIORITY' if SEARCH_PRIORITY else ''} are available. Try again later.")
        quit()
    
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
        in_days = f"(in {in_days} day{'s' if in_days > 1 else ''})" if in_days > 0 else "(today!)"
        
        msg += f"- {count} room{'s' if count > 1 else ''} closing on {closing_date.strftime('%d.%m')} {in_days}\n"
        
    # find rooms which are new
    new_rooms = set(r_ids) - set(r_ids_old)
    
    if new_rooms:
        msg += "\nNew rooms:"
        for new_room in new_rooms:
            msg += f"\n- {new_room}"
    else:
        msg += "\nNo new rooms :("
        
    # find rooms which are no longer available
    removed_rooms = set(r_ids_old) - set(r_ids)
    
    if removed_rooms:
        msg += "\n\nRooms no longer available:"
        for removed_room in removed_rooms:
            msg += f"\n- {removed_room}"
    
    # send message
    send_telegram_message(msg)
    print(msg)
