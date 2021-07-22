'''
Created on 2021年7月9日

@author: qguan
'''


import json
from urllib.parse import urlencode    # python3

import requests


#from urllib import urlencode #python2
city="北京"

with open("pcc.json","r",encoding="utf-8") as pf:
    dic=json.load(pf)

for key,value in dic.items():
    if city in value:
        params = urlencode({'code':"{}".format(key),'type':'1'})
        url = 'https://api.ip138.com/weather/?'+params
        headers = {"token":"eeec8efa42dac1351ce06ecc06adb16f"}#token为示例
        content =requests.get(url=url,headers=headers).json()
        print(content)
        text="地点: "+content.get("province")+ "，时间："+content.get("data").get("time") + \
        "，白天天气："+content.get("data").get("dayWeather") +\
        "，温度："+content.get("data").get("dayTemp")  +\
        "，白天风力："+content.get("data").get("dayWind")  +\
        "，夜晚天气："+content.get("data").get("nightWeather")  +\
        "，夜晚温度："+content.get("data").get("nightTemp") +\
        "，夜晚风向："+content.get("data").get("wind") +\
        "，夜晚风力："+content.get("data").get("nightWind") +\
        "，实时天气："+content.get("data").get("weather") +\
        "，实时温度："+content.get("data").get("temp") +\
        "，实时风力："+content.get("data").get("wind") +\
        "，实时湿度："+content.get("data").get("humidity") +\
        "，PM2.5："+content.get("data").get("pm25")
        
print(text)
        
        