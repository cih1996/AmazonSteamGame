import requests
import json
import time

proxies = {
    "http": "",
    "https": "",
}

ret = requests.get("http://api.xiaobai188.com:82/apih5/getPhone?token=5eda78b411b4de25041627ea8a9b3253&sid=4410&type=0&pr=&ci=&sr=0&haoduan=",proxies=proxies)
retJson = json.loads(ret.text)
mobile = retJson['data'][0]['phone']
print(mobile)
while True:
    try:
        ret = requests.get("http://api.xiaobai188.com:82/apih5/getMsg?token=5eda78b411b4de25041627ea8a9b3253&phone="+ mobile+"&sid=4410",proxies=proxies)
        #retJson = json.loads(ret.text)
        print(ret.text)
    except:
        pass
    time.sleep(4)