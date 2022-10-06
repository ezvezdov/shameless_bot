import json
from time import sleep
import requests
from os import path
from datetime import datetime

# https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup
# https://curlconverter.com/
# https://medium.com/@CodeYogi/how-to-scrape-websites-behind-a-login-with-python-b8e4efa9f5dd

def get_time_now():
    now = datetime.now()
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
        '_ga': 'GA1.2.1636079464.1663663307',
        '_gid': 'GA1.2.587350131.1663663307',
        '_fbp': 'fb.1.1663663307123.629889463',
        'Sinch_app_cookie_shameless_g': '4gq3bk96p9dh6g30pc5f6cdevr',
    }

    headers = {
    'authority': 'shameless.sinch.cz',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'cs-CZ,cs;q=0.9,ru-BY;q=0.8,ru;q=0.7,be-BY;q=0.6,be;q=0.5,en-US;q=0.4,en;q=0.3',
    'baggage': 'sentry-environment=production,sentry-release=1.38.3,sentry-public_key=daf1e1519a034b19b5aff38211bc0012,sentry-trace_id=3a1afc5c56f64588a80e7476f7bff1e9,sentry-sample_rate=0.25',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'Sinch_app_cookie_shameless_g=00smif5kvhl7mtjbltat5fo6dk',
    'origin': 'https://shameless.sinch.cz',
    'referer': 'https://shameless.sinch.cz/react/position?ignoreRating=true',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '3a1afc5c56f64588a80e7476f7bff1e9-81b77e5fac239fb2-0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

    json_data = {
        'key': 'worker/Positions/Index',
        'meta': {
            'page': 1,
            'limit': 100,
        },
        'params': {},
    }

    response = session.post('https://shameless.sinch.cz/api', cookies=cookies, headers=headers, json=json_data)

    parsed = json.loads(response.content)

    json_object = json.dumps(parsed, indent=4)
    
    # Writing to sample.json
    with open(path.join('data',"parsed_data.json"), "w") as outfile:
        outfile.write(json_object)