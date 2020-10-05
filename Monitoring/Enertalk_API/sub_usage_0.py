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
#import pyautogui
from pandas import DataFrame, Series

# 1 day, 1 sec
try :
    
##    global current_path
#    current_path = os.getcwd()
##    exe_file_location = "C:\\Users\\user\\Downloads\\ENERTALK" # need to modified 
#    exe_file_location = "C:\\Users\\ISP-MINI\\Desktop\\ENERTALK_test" # need to modified 
#    while True:
#        if current_path != exe_file_location : # move to the location of exe file 
#            os.chdir(exe_file_location)
#        else:
#            break            
    
    print(time.ctime())
    iter_a = 1
    iter_b = 1 
    previous_filesize = 0
    chk_size=0
    current_time = datetime.datetime.now()
    
    while iter_a > 0 :
#        iteration = 1
        tot = [1]
        data_finish_time = datetime.datetime.now() + datetime.timedelta(days=1)      
        current_time_cond = datetime.datetime.now() # download_time       
        finish_minute_chk_size = current_time_cond + datetime.timedelta(minutes=30)
        
        notes = open('token.out' , 'r+' , encoding='utf-8' ) #read contents of original file 
        token_tot = notes.readlines()
        notes.close()
        
        token_refresh = token_tot[0][40:168]
        token_access = token_tot[0][215:343]
        
        data_sites = enertalk_api_sites.enertalk_api_sites(token_access)
        data_devices = enertalk_api_device.enertalk_api_device(token_access, data_sites[0]['id']) # #change number 0 to 8 -> site id(except 1, 4 )    
      
        
        current_data_usage={}
        
#        name_current_time = str(current_time)[0:22] # time asked to server
        finish_day = data_finish_time.day # condition of ending 1 day's data
        check_data = '0' # ok
        
        while iter_b > 0: #token renewal every 5 hour = 18000 sec
                      
            current_time = datetime.datetime.now()
            finish_second = (current_time + datetime.timedelta(seconds=1)).second # condition of 1 second resolution
            
            start = time.time() # execute time
            
            current_data_usage = {} #space for variants of usage data
#            del(current_data_usage)
            
            for no_devices in range(0, len(data_devices)): 
#                    current_data_usage[no_devices] ={1}

                 # setting directory
                os.chdir('./Data_collection')
                file_name = 'Enertalk_1sec_deviceID_'+ data_devices[no_devices]['id'] +'_'+str(current_time)[0:10]
                folder_name = data_devices[no_devices]['name']

                if not(os.path.isdir(folder_name)):
                    os.makedirs(os.path.join(folder_name))
                    
                #check file size every 30 min = 1800 sec       
                if current_time.minute == finish_minute_chk_size:
                    chk_size = os.path.getsize(file_name+'.csv')          
                    if chk_size < previous_filesize:
                        mail_alarm.mailalarm()
                        
                previous_filesize = chk_size
                                    
                #collection data to file
                
                d = {} # d= {label[:] : l[:]}
                l = []
                label = []
#                                                    
                # call sub-function  
                
                os.chdir('..')
                
                notes = open('token.out' , 'r+' , encoding='utf-8' ) #read contents of original file 
                token_tot = notes.readlines()
                notes.close()
                          
                token_refresh = token_tot[0][40:168]
                token_access = token_tot[0][215:343]      

                os.chdir('./Data_collection')
                 
                url = 'https://api2.enertalk.com/devices/'+data_devices[no_devices]['id']+'/usages/realtime' # siteID = DeviceID

                headers = {
                        'Authorization': 'Bearer ' + token_access,
                        'accept-version' : '2.0.0'
                           }

                response = requests.get(url=url, headers=headers)
                
                print('Execution')
                current_data_usage[no_devices] = response.json()
                
#                current_data_usage[no_devices] = enertalk_api_usages_realtime.enertalk_api_usages_realtime(token_access, data_devices[no_devices]['id']) # save value same as prev.
                
                l.append(str(datetime.datetime.now())[0:22])
                label.append('current_time')
                
                l.append(check_data)
                label.append('check_data')
             
                d= {label[0] : l[0], label[1] : l[1]} # 0: current_time , 1: check_data
                df1 = pd.DataFrame(current_data_usage[no_devices], index=tot, columns=current_data_usage[no_devices].keys())
                df2 = pd.DataFrame(d, index=tot, columns=d.keys())
                df_dict = {**df2, **df1} # merge df1, 2 , type: dictionary / {**xs, **ys, **zs} 
                
                df = pd.DataFrame(df_dict, index=tot, columns=df_dict.keys()) # type : DataFrame
        
                os.chdir(folder_name)
                
                #check file existence
                chk_file = os.path.exists(str(file_name)+'.csv')
          
#                    df.to_csv(r'%s.csv' %file_name, mode='a',header =False ,index=False, encoding='cp949')  
#                
                if chk_file==True : #non-header
                    df.to_csv(r'%s.csv' %file_name, mode='a',header =False ,index=False, encoding='cp949')   
                else:
                    df.to_csv(r'%s.csv' %file_name, mode='a',header =True ,index=False, encoding='cp949')  
              
#                tot = tot + 1 # = index of df                    
                os.chdir('../..')
                
                while current_time.second < finish_second:
                    current_time = datetime.datetime.now() # download_time       
                    time.sleep(0.5)
                    
                print(time.time()-start)
#                print(token_access[0:10])
                print(datetime.datetime.now())
                
           
            if current_time.day == finish_day :
                iter_b = iter_b - 1
                

except:   
    mail_alarm.mailalarm()
   
