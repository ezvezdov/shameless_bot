import json
import requests
from os import path
from datetime import datetime

# https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup
# https://curlconverter.com/
# https://medium.com/@CodeYogi/how-to-scrape-websites-behind-a-login-with-python-b8e4efa9f5dd



def generate_data():

    cookies = {
        '_ga': 'GA1.2.2031000827.1663445701',
        '_gid': 'GA1.2.1058947656.1663445701',
        '_fbp': 'fb.1.1663445701426.133793152',
        'Sinch_app_cookie_shameless_g': 'eue1nvjah1qjvv99lsidmtu4oa',
    }

    headers = {
        'authority': 'shameless.sinch.cz',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'cs-CZ,cs;q=0.9',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.2.2031000827.1663445701; _gid=GA1.2.1058947656.1663445701; _fbp=fb.1.1663445701426.133793152; Sinch_app_cookie_shameless_g=eue1nvjah1qjvv99lsidmtu4oa',
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
        'data[_Token][key]': 'ddac833b7bf6db94cb4b3db93ccace6bf5acca6de161fdd7d476eab1c75e4a414b7a0841071051ebea8bf127049d28adc232dbef129e8adc13062373034966c4',
        'data[User][email]': 'gikexeg799@edxplus.com',
        'data[User][password]': 'cau_lidi0_0',
        'data[_Token][fields]': '9718e2427144cfee59faab3f566e928633c75c75%3A',
        'data[_Token][unlocked]': '',
    }

    response = requests.post('https://shameless.sinch.cz/users/login', cookies=cookies, headers=headers, data=data)
    session = requests.session()


    login_req = session.post("https://shameless.sinch.cz/users/login", cookies=cookies, headers=headers, data=data)
    if login_req.status_code == 200:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Succesfully updated in " + current_time)
    else:
        print("Update error :(")

    cookies = {
        '_ga': 'GA1.2.2031000827.1663445701',
        '_gid': 'GA1.2.1058947656.1663445701',
        '_fbp': 'fb.1.1663445701426.133793152',
        'Sinch_app_cookie_shameless_g': '1588v4tnarfbh5on6hmqrinu2n',
    }

    headers = {
        'authority': 'shameless.sinch.cz',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'cs-CZ,cs;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.2.2031000827.1663445701; _gid=GA1.2.1058947656.1663445701; _fbp=fb.1.1663445701426.133793152; Sinch_app_cookie_shameless_g=1588v4tnarfbh5on6hmqrinu2n',
        'origin': 'https://shameless.sinch.cz',
        'referer': 'https://shameless.sinch.cz/react/position?ignoreRating=true',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    json_data = {
        'key': 'worker/Positions/Index',
        'meta': {
            'page': 1,
            'limit': 100,
        },
        'params': {
            'ignoreRating': True,
        },
    }

    response = requests.post('https://shameless.sinch.cz/api', cookies=cookies, headers=headers, json=json_data)

    parsed = json.loads(response.content)

    json_object = json.dumps(parsed, indent=4)
    
    # Writing to sample.json
    with open(path.join('data',"parsed_data.json"), "w") as outfile:
        outfile.write(json_object)