#!/usr/bin/python3 -u

import requests
from requests.auth import HTTPDigestAuth
import json
import datetime
import time
import paho.mqtt.publish as publish

requestTimeout = 10
secondsPerHour = 3600000


def publish_data(current_topic, powerTotal):
    print(current_topic, powerTotal)
    publish.single("myhome/eddi/" + current_topic, powerTotal, hostname="10.0.0.135")

def get_instant():
    urlStatus = 'https://s6.myenergi.net/cgi-jstatus-E10225156'
    try:
        r=requests.get(urlStatus, auth=HTTPDigestAuth('123456796', 'hel105'),timeout=requestTimeout)
        payload = r.json()
        if "gen" in payload["eddi"][0]:
            gen = payload["eddi"][0]["gen"]
        else:
            gen = 0
        grd = payload["eddi"][0]["grd"]
        publish_data("GridPower",grd)
        publish_data("GeneratedPower",gen)
    except requests.exceptions.Timeout:
        print("Request timed out after 10 seconds")
        
while True:

    urlStub = 'https://s6.myenergi.net/cgi-jday-E10225156-'

    dateString = str(datetime.date.today())
    url = urlStub+(dateString)
    try:
        r=requests.get(url, auth=HTTPDigestAuth('123456796', 'hel105'),timeout=requestTimeout)
        payload = r.json()
        # print(payload["U10225156"])
    
        exportTotal = 0
        generationTotal = 0
        divertedTotal = 0
        exportedTotal = 0
        importedTotal = 0
        boostedTotal = 0


        for x in payload["U10225156"]:
            if "exp" in x:
                exportedTotal += int(x["exp"]) 
            if "gep" in x:
                generationTotal += int(x["gep"])
            if "h1d" in x:
                divertedTotal += int(x["h1d"]) 
            if "imp" in x:
                importedTotal += int(x["imp"]) 
            if "h1b" in x:
                boostedTotal += int(x["h1b"])

        exported = float(exportedTotal/secondsPerHour)
        generated = float(generationTotal/secondsPerHour)
        diverted = float(divertedTotal/secondsPerHour)
        imported = float(importedTotal/secondsPerHour)
        boosted = float(boostedTotal/secondsPerHour)

    
        publish_data("Exported",f'{exported:9.2f}')
        publish_data("Generated",f'{generated:9.2f}')
        publish_data("Diverted",f'{diverted:9.2f}')
        publish_data("Imported",f'{imported:9.2f}')
        publish_data("Boosted",f'{boosted:9.2f}')
        
    except requests.exceptions.Timeout:
        print("Request timed out after 10 seconds")

    get_instant()

    time.sleep(60)
