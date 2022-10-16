import requests
import re
import datetime
import openpyxl
import os
import time
import json
import numpy as np
import math

uid=input()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'}


def getNames(uid):
    url='https://api.bilibili.com/x/relation/followings?vmid='+uid+'&pn=1'
    page_data=requests.get(url=url,headers=headers).text
    names='"mid":(.*?),".*?"uname":"(.*?)"'
    
    names_data=re.findall(names,page_data,re.S)
    
    follow_json=json.loads(page_data)
    total=follow_json['data']['total']
    if total>250:
        total=250
    pn=math.ceil(total/50)
    for i in range(2,pn+1):
        url_follow=url='https://api.bilibili.com/x/relation/followings?vmid='+uid+'&pn='+str(i)
        page_data_follow=requests.get(url=url_follow,headers=headers).text
        names_data.extend(re.findall(names,page_data_follow,re.S))
    return names_data,total
names_data,total=getNames(uid)
for name in names_data:
    print(name)
print(len(names_data))