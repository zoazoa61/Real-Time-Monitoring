#enertalk_api_users information

import requests, json
import pandas as pd
from pandas import DataFrame, Series

def enertalk_api_users(access_token):
#    f = open("./t/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }
    
    response = requests.get('https://api2.enertalk.com/users/me', headers=headers)
    data = response.json()
    return(data)
    
#data = { 'client_id': 'CLIENTID', 'client_secret': 'CLIENTSECRET', 'grant_type': 'authorization_code', 'code': 'CODE' }
