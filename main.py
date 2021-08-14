# -*- coding: UTF-8 -*-

import imaplib
import email
import string
import sys
import requests
import os

from fastapi import FastAPI, Query
import uvicorn as u
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/index')
async def read_index(request: Request):
    file = open("email.txt")
    listArr = []
    while True:
        text = file.readline()  # 只读取一行内容
        if not text:
            break
        print(text)
        listArr.insert(0,text)
    file.close()
    
    return templates.TemplateResponse("index.html", {"request": request, "listArr": listArr})

@app.get('/email')
async def email(
    *,
    user: str
):
    val = ""
    with os.popen('python3 imap.py '+user) as p:
        val = p.read()
    return val.replace("\n","")
