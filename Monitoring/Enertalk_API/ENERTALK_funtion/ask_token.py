# -*- coding: utf-8 -*-
# Ask token : method 1 & 2
# method 1: refresh code -> ask access token, inital start / if any error happens
# method 2: use refresh -> ask new access and refresh(renewable) token
# ref. code_change from ENERTALK_function (orginal.ver)

"""
Created on Wed Jul 10 20:43:43 2019

@author: user
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import sys

#path_token = './Users/user/Downloads/ENERTALK/ENERTALK_funtion' #token file save path

#method 1
def ask_token():

#    log_info
    usr = ["YOURID"]
    pwd = ['YOURPW']
    code_ask_url = "https://auth.enertalk.com/authorization?client_id=YOURCLIENDTID&response_type=code&redirect_uri=https://app.getpostman.com/oauth2/callback?"

    #load chrome
    path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" # define the path of chromedriver
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
      
    #command of asking access token
    cmd_ask_access_token = "curl -k https://auth.enertalk.com/token -d \"grant_type=authorization_code&code="+present_code+"&redirect_uri=https://app.getpostman.com/oauth2/callback?\" --user c2poOTFAZ2lzdC5hYy5rcl8x:t51ye56i1iw4ge7ix2ve3qv29a2430815d530o3 -v -o token.out"
    os.system(cmd_ask_access_token)
        
    notes = open('token.out' , 'r+' , encoding='utf-8' ) #read contents of original file 
    token_tot = notes.readlines()
    notes.close()
    
    #token
    token_refresh = token_tot[0][40:168]
    token_access = token_tot[0][215:343]
    
    return(token_access, token_refresh)


#method 2
def renew_token(token_refresh): #token_refresh : str type

    prev_token_refresh = token_refresh # previous_refresh_token
    
    #command of asking access token
    cmd_ask_new_token = "curl -k https://auth.enertalk.com/token -d \"grant_type=refresh_token&refresh_token="+prev_token_refresh+"\" --user c2poOTFAZ2lzdC5hYy5rcl8x:t51ye56i1iw4ge7ix2ve3qv29a2430815d530o3 -v -o token2.out"    
    os.system(cmd_ask_new_token)
        
    notes = open('token2.out' , 'r+' , encoding='utf-8' ) #read contents of original file 
    token_new_tot = notes.readlines()
    notes.close()
    
    #token
    token_new_access = token_new_tot[0][39:168] #128 char
    token_new_refresh = token_new_tot[0][186:315]
    
    return(token_new_access, token_new_refresh)
