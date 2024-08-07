import yaml

from xiorbe_scrape import get_rooms, get_basic_description
from tg_bot import send_telegram_message

# load config
CONFIG_DIR = "config/"
COUNTRY, CITY = None, None

try:
    with open(CONFIG_DIR+"config.yaml", "r") as file:
        config = yaml.safe_load(file)
        COUNTRY = config["XIOR_COUNTRY"]
        CITY = config["XIOR_CITY"]
except FileNotFoundError:
    # copy config_example.yaml to config.yaml
    from shutil import copyfile
    copyfile(CONFIG_DIR+"config_example.yaml", CONFIG_DIR+"config.yaml")
    
    print("Please edit config.yaml and re-run the program")
    quit()

def check_rooms():
    print("Checking rooms")
    
    # get rooms
    rooms = get_rooms(COUNTRY, CITY, None, None)
    
    num_rooms = rooms["space_count"]
    
    if num_rooms > 0:
        print(f"Rooms available: {num_rooms}")
        
        is_are = " is" if num_rooms == 1 else "s are"
        
        # send message
        msg = f"{num_rooms} XIOR room{is_are} now available!\n\n"
        
        for r in rooms["spaces"]:
            msg += "- " + get_basic_description(r) + "\n"
        
        send_telegram_message(msg)
    else:
        print("No rooms available")

if __name__ == "__main__":
    
    check_rooms()
