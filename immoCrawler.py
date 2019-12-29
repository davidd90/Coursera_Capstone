import bs4 as bs
import urllib.request 
import time 
from datetime import datetime 
import pandas as pd
import json
import os
import re

start_time = time.time()
count = 1

l=[]
df = pd.DataFrame()
for page in range(1,360):
    if(page % 10 ==0):
        df.to_csv("Rohdaten/"+str(datetime.now())[:19].replace(":","").replace(".","")+".csv",sep=";",decimal=",",encoding = "utf-8",index_label="timestamp")
        time.sleep(600)
        l=[]
        df = pd.DataFrame()        
    print("Loop " + str(page) + " startet.")
    try:
        soup = bs.BeautifulSoup(urllib.request.urlopen('https://www.immobilienscout24.de/Suche/de/sachsen/leipzig/wohnung-mieten?pagenumber='+str(page)).read(),'lxml')
        for paragraph in soup.find_all("a"):
            if r"/expose/" in str(paragraph.get("href")): 
                l.append(paragraph.get("href").split("#")[0]) 
                l = list(set(l))
        for item in l:
            try:
                soup = bs.BeautifulSoup(urllib.request.urlopen('https://www.immobilienscout24.de'+item).read(),'lxml')
                scripts = str(soup.find_all("script"))
                data = pd.DataFrame(json.loads(scripts.split("keyValues = ")[1].split("}")[0]+str("}")),index=[str(datetime.now())])
                data["URL"] = str(item)
                beschreibung = [] 

                for i in soup.find_all("pre"): 
                    beschreibung.append(i.text)
                position = soup.find_all("script", type="text/javascript")
                
                position = str(soup.find_all("script")).split("IS24.expose.mapModel = ")[1].split("{")[4].split("}")[0].split("\n")
                if(len(position)!=4):
                    continue
                else:
                    split = position[1].split(":")
                    data["lat"] = float(split[1][1:-2])
                    split = position[2].split(":")        
                    data["long"] = float(split[1])
                    
                data["beschreibung"] = str(beschreibung)
                df = df.append(data)
            except Exception as e:
                print(str(datetime.now())+": " + str(e)) 
                l = list(filter(lambda x: x != item, l))
                print("ID " + str(item) + " entfernt.")
    except Exception as e: 
        print(str(datetime.now())+": " + str(e)) 
    print("Loop " + str(count) + " endet.")  

print("FERTIG!")
