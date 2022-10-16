import requests
import re
import json
import numpy as np
import math

uid1=input()
uid2=input()
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
def getRelations(userId):
    relation_text_ff=requests.get("https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(userId),headers=headers).text
    relation_text_l=requests.get("https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp".format(userId),headers=headers).text
    relation_json=json.loads(relation_text_ff)
    fans,follows=relation_json['data']['follower'],relation_json['data']['following']
    relation_json=json.loads(relation_text_l)
    level=relation_json['data']['level']
    return fans,follows,level
merged=list(set(getNames(uid1)[0]).intersection(set(getNames(uid2)[0])))
fans=[]
names_data=merged
total=len(merged)
for i in range(total):
    fans.append(getRelations(names_data[i][0]))
data=np.c_[names_data,fans]
for name in data:
    print(name)