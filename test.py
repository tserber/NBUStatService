import requests as requests
headers = {'Authentication': 'SdrakadukakKilo122334tera'}
while 1:
    r = requests.get('http://0.0.0.0:8080/exchange?from=2020-10-001&to=2020-10-03', headers=headers)
    print(r.text)
    input()
