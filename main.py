# -*- coding: UTF-8 -*-

import imaplib
import email
import string
import sys
import requests
import os
import json
from fastapi import FastAPI, Query
import uvicorn as u
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

proxies = {
    "http": "",
    "https": "",
}

token = "9d0c962d47256ad167d3197a4866a071"


def readFileStr(filename):
    str = ""
    with open(filename,'r') as f:
        str+=f.read()
    return str
    
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/index')
async def read_index(request: Request):
    regJs = readFileStr("regJs.txt")

    file = open("email.txt")
    listArr = []
    
    while True:
        text = file.readline()  # 只读取一行内容
        if not text:
            break
        arr = text.split("----")
        emailUser = {}
        emailUser['user'] = arr[0]
        emailUser['pass'] = arr[1]
        listArr.insert(0,emailUser)
    file.close() 

    
    return templates.TemplateResponse("index.html", {"request": request, "listArr": listArr,"regJs":regJs})

@app.get("/sms_getcode")
async def sms_newmobile(
    *,
    mobile:str
):
    code = ""
    try:
        ret = requests.get("http://api.xiaobai188.com:82/apih5/getUserSmsList?token="+token+"&limit=20&phone=&page=1",proxies=proxies)
        retJson = json.loads(ret.text)
        if(retJson['data'][0]['phone'] == mobile):
            code = retJson['data'][0]['code']
    except:
        pass

    return code


@app.get("/sms_newmobile")
async def sms_newmobile():
    ret = requests.get("http://api.xiaobai188.com:82/apih5/getPhone?token="+token+"&sid=4410&type=0&pr=&ci=&sr=0&haoduan=",proxies=proxies)
    retJson = json.loads(ret.text)
    mobile = retJson['data'][0]['phone']
    return mobile

@app.get('/email')
async def email( 
    *,
    user: str
):
    val = ""
  
    with os.popen('python imap.py '+user) as p:
        val = p.read()
    return val.replace("\n","")
