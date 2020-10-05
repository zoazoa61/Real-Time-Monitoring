#enertalk_api_usages_realtime
#https://developer.enertalk.com/api2-usages/

import requests, json
import pandas as pd
from pandas import DataFrame, Series

def enertalk_api_usages_realtime(access_token, siteID): #endpoints : GET /sites/:siteId/usages/realtime, GET /devices/:deviceId/usages/realtime
#    f = open("./t/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
#    url = 'https://api2.enertalk.com/sites/'+siteID+'/usages/realtime'
    url = 'https://api2.enertalk.com/devices/'+siteID+'/usages/realtime' # siteID = DeviceID
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }
    response = requests.get(url=url, headers=headers)
    data = response.json()
    return(data)

def enertalk_api_billing_usages_realtime(access_token, siteID): #endpoints : GET /sites/:siteId/usages/realtime
#    f = open("./t/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
#    url = 'https://api2.enertalk.com/sites/'+siteID+'/usages/billing'
    url = 'https://api2.enertalk.com/devices/'+siteID+'/usages/billing' # siteID = DeviceID

    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }
    response = requests.get(url=url, headers=headers)
    data = response.json()
    return(data)
    
