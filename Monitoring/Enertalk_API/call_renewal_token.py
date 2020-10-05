#ENERTALK MAIN FUNCTION

 
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
from ENERTALK_funtion import ask_token
import requests
import json

def renewal_token():
  
    usr = ["Your id"]
    pwd = ['Your PW']
    code_ask_url = "https://auth.enertalk.com/authorization?client_id=Your_Client_ID&response_type=code&redirect_uri=https://app.getpostman.com/oauth2/callback?"
    
    #load chrome
    #path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" # define the path of chromedriver
    path = "/usr/bin/chromedriver" # define the path of chromedriver
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(10) #for load delay
    driver.get(code_ask_url)
    
    elem = driver.find_element_by_xpath(".//*[@name='email']") # part : Email
    elem.send_keys(usr)
    
    elem = driver.find_element_by_xpath(".//*[@name='password']") # part : Password
    elem.send_keys(pwd)
    
    elem.send_keys(Keys.RETURN) # ENTER
    driver.implicitly_wait(5) #for load delay
    
    #change webpage
    code_response_url = driver.current_url # changed url
    present_code = code_response_url[49:49+64] #the number of code : 64 characters
    
    #    os.chdir(path_token) #location of save token.out
    
    #command of asking access token
    cmd_ask_access_token = "curl -k https://auth.enertalk.com/token -d \"grant_type=authorization_code&code="+present_code+"&redirect_uri=https://app.getpostman.com/oauth2/callback?\" --user c2poOTFAZ2lzdC5hYy5rcl8x:t51ye56i1iw4ge7ix2ve3qv29a2430815d530o3 -v -o token.out"
    os.system(cmd_ask_access_token)
        
    notes = open('token.out' , 'r+' , encoding='utf-8' ) #read contents of original file 
    token_tot = notes.readlines()
    notes.close()
    
    #token
    global token_refresh
    global token_access
    
    token_refresh = token_tot[0][40:168]
    token_access = token_tot[0][215:343]
    
    driver.close()    
    
    #threading.Timer(3600, renewal_token).start() #1h repetition

    
    

# 1 day, 1 sec
try :    
    while True:
        renewal_token()
        
        
        print(token_access)
        time.sleep(7200)
            
    
except:   
    mail_alarm.mailalarm()
   
