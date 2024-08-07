import requests

from tg_bot import send_telegram_message

def check_rooms():
    url = "https://api.5huizenvastgoedbeheer.nl/v2/buildings"
    
    print("Checking rooms on VijfHuizen")
    
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"Failed to get buildings: {r.text}")
        send_telegram_message(f"Failed to get VijfHuizen buildings: {r.text}")
        quit()
    
    buildings = r.json()
        
    for b in buildings:
        total_rooms = b['rooms']['total']
        available_rooms = b['rooms']['available']
        
        address = b['address']['street'] + " " + str(b['address']['houseNumber'])
        
        print(f"{address}: {available_rooms}/{total_rooms} available")
        
        if available_rooms > 0:
            msg = f"{available_rooms} room{'s' if available_rooms > 1 else ''} available at {address} on VijfHuizen!\n\nhttps://5huizenvastgoedbeheer.nl/#/student-housing"
            send_telegram_message(msg)

if __name__ == "__main__":
    check_rooms()
