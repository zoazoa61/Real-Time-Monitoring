# -*- coding: utf-8 -*-
#https://developer.enertalk.com/api2-tags/


#enertalk_api_device : Get information of all devices belonging to a site
import requests, json
import pandas as pd
from pandas import DataFrame, Series

def enertalk_api_tags(access_token, siteID): #List tags of a site

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/tags' #endpoints: GET /sites/:siteId/tags
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return data

#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }

def enertalk_api_tags_get(access_token, siteID, tagID): #Get tags info.

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/tags/'+tagID #endpoints: /GET /sites/:siteId/tags/:tagId
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return data

#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }