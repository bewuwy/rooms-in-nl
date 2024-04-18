import yaml
import schedule
import time

from scrape import get_rooms
from tg_bot import send_telegram_message

# load config
COUNTRY, CITY, CHECK_INTERVAL = None, None, 10

try:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        COUNTRY = config["XIOR_COUNTRY"]
        CITY = config["XIOR_CITY"]
        CHECK_INTERVAL = config["CHECK_INTERVAL"]
except FileNotFoundError:
    # copy config_example.yaml to config.yaml
    from shutil import copyfile
    copyfile("config_example.yaml", "config.yaml")
    
    print("Please edit config.yaml and re-run the program")
    quit()

def check_rooms():
    print("Checking rooms")
    
    # get rooms
    rooms = get_rooms(COUNTRY, CITY, None, None)
    
    num_rooms = rooms["space_count"]
    
    if num_rooms > 0:
        print(f"Rooms available: {num_rooms}")
        
        # send message
        send_telegram_message(f"{num_rooms} XIOR rooms are now available! Quick go to https://www.xior-booking.com/# to book!")

if __name__ == "__main__":
    
    print(f"Checking xior.be offers every {CHECK_INTERVAL} minutes")
    
    # check every 10 minutes
    schedule.every(CHECK_INTERVAL).minutes.do(check_rooms)

    while True:
    
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
