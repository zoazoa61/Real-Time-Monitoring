# -*- coding: utf-8 -*-
#https://developer.enertalk.com/api2-bill/

#enertalk_api_device : Get information of all devices belonging to a site
import requests, json
import pandas as pd
from pandas import DataFrame, Series

def enertalk_api_bills(access_token, siteID): #Get a site’s billing information

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/bills' #endpoints: GET /sites/:siteId/bills
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return(data)
# response : "meterDate": 1, "supplierId": "eversource", "ratePlanId": "A1", "billSettings": null



#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }

def enertalk_api_bills_update(access_token, siteID): #Update site’s billing information.

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
#    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/bills' #endpoints: PATCH /sites/:siteId/bills
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0',
            'Content-Type': 'application/json'
               }   
    data = {
            'meterDate': '2',
            'supplierId': 'nationalGrid',
            'ratePlanId': 'R1',
            'billSettings': {
              'contractOption': '[1,3]',
              'contractType': '1',
              'discount': '2',
              'contractDate': '2017-01-01',
              'contractPower': 299
            }
          }
            
    response = requests.patch(url=url, headers=headers, data=data)
    datas = response.json()
    
    return(datas)


def enertalk_api_bills_schema(access_token): #Get a supplier’s rate plan schema.

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/kepco/eversource/rateplans/generalA1/schema' #endpoints: GET /suppliers/:supplierId/rateplans/:ratePlanId/schema
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
            
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return(data)
    
def enertalk_api_bills_suppeliers(access_token): #Get a supplier’s rate plan schema.

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/suppliers/?countryCode=KR' #endpoints: GET /suppliers/:supplierId/rateplans/:ratePlanId/schema
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
            
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return(data)

def enertalk_api_bills_usage(access_token, siteID): #Get a supplier’s rate plan schema.

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites/'+siteID+'/usages/billing' #endpoints: GET /suppliers/:supplierId/rateplans/:ratePlanId/schema
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
            
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return(data)

