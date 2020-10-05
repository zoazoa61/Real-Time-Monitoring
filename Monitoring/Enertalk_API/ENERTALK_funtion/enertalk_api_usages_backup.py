#enertalk_api_usages_realtime
#https://developer.enertalk.com/api2-usages/

import requests, json
import pandas as pd
from pandas import DataFrame, Series
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import pandas as pd
import datetime
import csv
import smtplib
from email.mime.text import MIMEText
import threading
from ENERTALK_funtion import mail_alarm 
from ENERTALK_funtion import enertalk_api_users
from ENERTALK_funtion import enertalk_api_sites
from ENERTALK_funtion import enertalk_api_teams
from ENERTALK_funtion import enertalk_api_bills
from ENERTALK_funtion import enertalk_api_device
from ENERTALK_funtion import enertalk_api_tags
from ENERTALK_funtion import enertalk_api_usages_realtime
from ENERTALK_funtion import enertalk_api_usages_backup
from ENERTALK_funtion import ask_token
import requests
import json


def enertalk_api_usages_backup(access_token, siteID, start_time, end_time): #endpoints : GET /sites/:siteId/usages/realtime, GET /devices/:deviceId/usages/realtime
#    f = open("./t/access_token.txt", 'r') 
#    access_token = f.readline()
#    f.close()
#    url = 'https://api2.enertalk.com/sites/'+siteID+'/usages/realtime'
    
    start_time = str(start_time)
    end_time = str(end_time)
    url = 'https://api2.enertalk.com/devices/'+siteID+'/channels/usages/periodic/?period=15min&start='+start_time+'&end='+end_time # siteID = DeviceID    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'accept-version' : '2.0.0'
               }
    response = requests.get(url=url, headers=headers)
    data = response.json()
    return(data)

notes = open('token.out' , 'r+' , encoding='utf-8' ) #read contents of original file 
token_tot = notes.readlines()
notes.close()

#token
token_refresh = token_tot[0][40:168]
token_access = token_tot[0][215:343]


