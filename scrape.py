import requests
from bs4 import BeautifulSoup
import brotli

from tg_bot import send_telegram_message

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
}

def get_csrf():
    r = requests.get("https://www.xior-booking.com/#", headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
        
    # get value of meta with name=csrf-token
    token = soup.find('meta', {'name': 'csrf-token'})
    cookies = r.cookies
    
    return token['content'], cookies

def get_rooms(country, city, csrf_token, cookies):
    if not csrf_token:
        csrf_token, cookies = get_csrf()
    
    url = "https://www.xior-booking.com/ajax/space-search"

    payload = f"country={country}&city={city if city else ""}&=location%3D&=space_type%3D&=order%3D&=unlock_key%3D&min_price=0&max_price=6180&min_surface=10&max_surface=116&page=1&pagination=true"
    
    headers = {
        # "cookie": f"laravel_session=eyJpdiI6ImoxRW15c1pqUTA5ZTZpcnY5dkhmcFE9PSIsInZhbHVlIjoiek1JY2FpSWpYMzdxUFkzK0pyUEtFbzd3RFJneDQ4ZW1rRjZVdkcwODBVNnArYy9WTjJ2d3NQMWN4MjRoR0l3clkrYVowa2pwR2dRQ1QvZ2ZyTUhZR05SbVVCVjFIR0tKY0NyUTB4bngyVHZjUWQydWI1TTl1RTFRMHRTQ2RqZ2YiLCJtYWMiOiJlZTU3Mjk2Nzg3YjU4ZjU0ODgwNDRjMDg3NmNkMjI4M2RlOWMzNWM5MjExNWJkMTFiZjM2YzUyNmM2Nzc2MWQ4In0%253D; XSRF-TOKEN=${csrf_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,pl;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.xior-booking.com/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-TOKEN": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.xior-booking.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "TE": "trailers",
    }
    
    r = requests.post(url, headers=headers, data=payload, cookies=cookies)
    
    if r.status_code != 200:
        print(f"Failed to get rooms: {r.text}")
        send_telegram_message(f"Failed to get rooms: {r.text}")
        quit()
    
    rooms = r.json() # brotli.decompress(r.content)
    
    return rooms

if __name__ == "__main__":
    token, cookies = get_csrf()
        
    rooms = get_rooms(528, 21, token, cookies)
    print(rooms)