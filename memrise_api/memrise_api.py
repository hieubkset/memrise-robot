import pprint
import requests
import webbrowser
import json


def make_headers():
    headers = {}
    with open('headers.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if 'Cookie' not in line]
    for line in lines:
        if line:
            k, v = line.split(':', maxsplit=1)
            headers[k] = v

    pprint.pprint(headers)
    return headers


def make_cookies():
    cookies = {}
    with open('headers.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'Cookie:' in line:
                str_cookies = line.replace('Cookie:', '')
                break;
        lines = str_cookies.split(';')

    for line in lines:
        k, v = line.split('=', maxsplit=1)
        cookies[k.strip()] = v.strip()

    pprint.pprint(cookies)
    return cookies


def make_payload():
    payload = {}
    with open('payload.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip().replace('Content-Disposition: form-data; name="', "") for line in lines if line != "\n" and '---' not in line]
    lines = lines[:-2]
    for k, v in zip(lines[0::2], lines[1::2]):
        payload[k[:-1].strip()] = v.strip()

    pprint.pprint(payload)
    return payload


url = "https://www.memrise.com/ajax/thing/cell/upload_file/"
headers = make_headers()
cookies = make_cookies()
data = make_payload()
file = {'f': open(r"D:\Data\audio\temp.mp3", "rb")}

s = requests.Session()

response = s.post(url=url, headers=headers, cookies=cookies, data=data, files=file, verify=False)

with open('res.html', 'w') as f:
    f.write(response.text)

# webbrowser.open('res.html')

print(response.status_code)

# s.close()
