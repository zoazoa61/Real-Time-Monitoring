#enertalk_api_sites : Get information of all sites belonging to a user
import requests, json
import pandas as pd
from pandas import DataFrame, Series

def enertalk_api_sites(access_token):

#    f = open("./ENERTALK_API-getting_token/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    
    url = 'https://api2.enertalk.com/sites'
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }   
    response = requests.get(url=url, headers=headers)
    data = response.json()
    
    return(data)

#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }
