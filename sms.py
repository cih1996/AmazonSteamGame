import requests
import json
import time

proxies = {
    "http": "",
    "https": "",
}

token = "9d0c962d47256ad167d3197a4866a071"

ret = requests.get("http://api.xiaobai188.com:82/apih5/getPhone?token="+token+"&sid=4410&type=0&pr=&ci=&sr=0&haoduan=",proxies=proxies)
retJson = json.loads(ret.text)
mobile = retJson['data'][0]['phone']
print(mobile)
while True:
    try:
        ret = requests.get("http://api.xiaobai188.com:82/apih5/getUserSmsList?token="+token+"&limit=20&phone=&page=1",proxies=proxies)
        retJson = json.loads(ret.text)
        if(retJson['data'][0]['phone'] == mobile):
            print("yes:" + retJson['data'][0]['code'])
            break
        else:
            print("nonono:" + retJson['data'][0]['phone'])

    except:
        pass
    time.sleep(4)