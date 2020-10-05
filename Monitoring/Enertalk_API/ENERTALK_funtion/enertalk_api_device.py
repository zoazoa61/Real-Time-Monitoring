#enertalk_api_device : Get information of all devices belonging to a site
import requests, json
import pandas as pd
from pandas import DataFrame, Series

def enertalk_api_device(access_token,siteID): #List devices of a site

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/devices' #endpoints: GET /sites/:siteId/devices
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
               }   
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return(data)

#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }

def enertalk_api_device_update(access_token, siteID): #Update device

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/devices' #endpoints: GET /sites/:siteId/devices
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
               }   
    data ={
            "installPurpose": 3,
            "dataPeriod": 10, #(seconds)
            "dataCount": 1, #(Hz)
            "ctCapacities": [200], #Possible values are 0, 50, 100, 200, 300, or 600 (A)
            "powerCapacity": 2000, #device power capacity (W)
            "name": "Updated Device Name1111111111"
            
            }
    response = requests.patch(url=url, headers=headers, data=data)
    data = response.json()
    
    return(data)

#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }
#    
#    curl -X PATCH
#  -H "Authorization: Bearer <access_token>"
#  -H "Content-Type: application/json"
#  -d '{
#    "installPurpose": 3,
#    "dataPeriod": 10,
#    "dataCount": 1,
#    "ctCapacities": [200],
#    "powerCapacity": 2000,
#    "name": "Updated Device Name"
#  }'
#  "https://api2.enertalk.com/devices/12abcdef"