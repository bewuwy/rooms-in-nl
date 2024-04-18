import requests
import yaml

def send_telegram_message(message, bot_token=None, chat_id=None):
    if not bot_token or not chat_id:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
            bot_token = config["TG_TOKEN"]
            chat_id = config["TG_CHAT"]
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

if __name__ == "__main__":
    
    print("Sending message")
    
    send_telegram_message('Your message here')
