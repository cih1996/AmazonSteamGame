# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Query
import imaplib
import email
import string
import sys
import requests


def strMid(rawStr,find1,find2):
    point1 = rawStr.find(find1)
    point2 = rawStr.find(find2,point1)
    return rawStr[point1+len(find1):point2]

# 解析邮件内容
def get_body(msg):
    if msg.is_multipart ():
        return get_body ( msg.get_payload ( 0 ) )
    else:
        return msg.get_payload ( None , decode=True )
    
#search('FROM','abc@outlook.com',conn)  根据输入的条件查找特定的邮件
def search(key,value,conn):
    result , data = conn.search(None,key,'"()"'.format(value))
    return data

#获取附件
def get_attachements(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()

        if bool(filename):
            filepath = os.path.join(attachementdir,filename)
            with open(filepath,'wb') as f:
                f.write(part.get_payload(decode=True))


def getSteamUrl(useranme,password):
    link = None
    code = None
    conn = imaplib.IMAP4_SSL(port = '993',host = 'imap-mail.outlook.com')
    ret = conn.login(useranme , password)
    conn.list()     #列出邮箱中所有的列表，如：收件箱、垃圾箱、草稿箱。。。
    conn.select('INBOX')    #选择收件箱（默认）
    type, data = conn.search(None, 'ALL') 
    mailidlist = data[0].split ()       #转成标准列表,获得所有邮件的ID
    for index in mailidlist:
        esult , data = conn.fetch (index, '(RFC822)' )
        e = email.message_from_bytes(data[0][1])
        subject = email.header.make_header ( email.header.decode_header ( e['SUBJECT'] ) )
        mail_from = email.header.make_header ( email.header.decode_header ( e['From'] ) )

        try:
            body = str(get_body(e))  #,encoding='utf-8'
            
        except:
            pass
        requests.packages.urllib3.disable_warnings()
        if(str(mail_from).find("Amazon") > -1):
            code = strMid(body,"<p class=\"otp\">","</")
            break
    return code

if __name__ == "__main__":
    userPass = sys.argv[1:][0]
    arr = userPass.split("----")
    print(getSteamUrl(arr[0],arr[1]))


