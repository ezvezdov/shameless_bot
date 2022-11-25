import json
from time import sleep
import requests
from os import path
from datetime import datetime, timezone
import pytz

# https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup
# https://curlconverter.com/
# https://medium.com/@CodeYogi/how-to-scrape-websites-behind-a-login-with-python-b8e4efa9f5dd

f = open(path.join('data','empty_data.json'))
empty_data = json.load(f)


def get_time_now():
    now = datetime.now()
    now = now.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone('Europe/Prague'))
    return now.strftime("%d.%m.%Y %H:%M:%S")

def write_log(str):
    logfile = open(path.join('data',"log.txt"), "a")
    logfile.write(str)
    logfile.close()

def generate_data():

    cookies = {
    'Sinch_app_cookie_shameless_g': '00smif5kvhl7mtjbltat5fo6dk',
    }

    headers = {
        'authority': 'shameless.sinch.cz',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'cs-CZ,cs;q=0.9,ru-BY;q=0.8,ru;q=0.7,be-BY;q=0.6,be;q=0.5,en-US;q=0.4,en;q=0.3',
        'cache-control': 'max-age=0',
        # 'cookie': 'Sinch_app_cookie_shameless_g=00smif5kvhl7mtjbltat5fo6dk',
        'origin': 'https://shameless.sinch.cz',
        'referer': 'https://shameless.sinch.cz/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    data = {
        '_method': 'POST',
        'data[_Token][key]': '7dbe30778d858efdebb37cc6c70688465d3179504ca5b1313a6ec2d2e103199216be107a81c89ebfc07ca21efc2411d0aee91860b9127c6fae3ccf41ec8ba064',
        'data[User][email]': 'gikexeg799@edxplus.com',
        'data[User][password]': 'cau_lidi0_0',
        'data[_Token][fields]': '9718e2427144cfee59faab3f566e928633c75c75%3A',
        'data[_Token][unlocked]': '',
    }

    session = requests.session()
    
    try:
        login_req = session.post("https://shameless.sinch.cz/users/login", cookies=cookies, headers=headers, data=data)
    except:
        login_req = -3
        write_log("Update error in " + get_time_now() + " :(\n")

    

    while login_req.status_code != 200:
        sleep(60)
        try:
            login_req = session.post("https://shameless.sinch.cz/users/login", cookies=cookies, headers=headers, data=data)
        except:
            login_req = -3
            write_log("Update error in " + get_time_now() + " :(\n")

    write_log("Succesfully updated in " + get_time_now() + "\n")
    
    

    cookies = {
        'Sinch_app_cookie_shameless_g': 'l2e1o1rjp8qi1v2vlua9fd9nqb',
    }

    headers = {
        'authority': 'shameless.sinch.cz',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'cs-CZ,cs;q=0.9,ru-BY;q=0.8,ru;q=0.7,be-BY;q=0.6,be;q=0.5,en-US;q=0.4,en;q=0.3',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': 'Sinch_app_cookie_shameless_g=l2e1o1rjp8qi1v2vlua9fd9nqb',
        'origin': 'https://shameless.sinch.cz',
        'referer': 'https://shameless.sinch.cz/react/position?ignoreCapacity=true&ignoreRating=true',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    json_data = {
        'key': 'worker/Positions/Index',
        'meta': {
            'page': 1,
            'limit': 100,
        },
        'params': {
            'ignoreCapacity': True,
            'ignoreRating': True,
            'attend': True,
        },
    }


    response = session.post('https://shameless.sinch.cz/api', cookies=cookies, headers=headers, json=json_data)
    parsed = json.loads(response.content)
    json_object = json.dumps(parsed, indent=4)
    with open(path.join('data',"parsed_data.json"), "w") as outfile:
            outfile.write(json_object)
        
    f = open(path.join('data','parsed_data.json'))
    parsed_data = json.load(f)

    while(response.status_code != 200 or parsed_data == empty_data):
        write_log("Update error in " + get_time_now() + " :(\n")
        sleep(30)
        response = session.post('https://shameless.sinch.cz/api', cookies=cookies, headers=headers, json=json_data)
        parsed = json.loads(response.content)
        json_object = json.dumps(parsed, indent=4)

        with open(path.join('data',"parsed_data.json"), "w") as outfile:
            outfile.write(json_object)
        
        f = open(path.join('data','parsed_data.json'))
        parsed_data = json.load(f)

    
    
    # Writing to sample.json
    with open(path.join('data',"parsed_data.json"), "w") as outfile:
        outfile.write(json_object)