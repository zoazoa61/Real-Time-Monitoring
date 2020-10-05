# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:32:46 2019

@author: user

This program is designed to execute the program which is infinite loop and the user desired to execute continuously,  if it is quitted.
Please refer to below remarks in code.
"""
#
# 

import os, sys, time
import subprocess
import ctypes
from email.mime.text import MIMEText
from ENERTALK_funtion import mail_alarm 
#from win32com.client import GetObject

  
def process_info_manual():
    task_result = os.popen("tasklist") #Command this string in command prompt
    
    #Arrange list type of tasklist's contents (exe.file)
    task_read = task_result.readlines()   
    exe_string = ".exe"
    task_list = []
    
    for i in range (0, len(task_read)):
    
        if exe_string in task_read[i]:
            
            temp_exe = task_read[i][0:task_read[i].find(exe_string)] + exe_string
            task_list.append(temp_exe)
            
    return(task_list)
     

##main
try :
#Desired file lists for executing 
    check_exefiles = ["call_renewal_token.exe", 
                      "call_sub_post_process.exe",
                      "sub_bill_function.exe",
                      "sub_usage_0.exe",
                      "sub_usage_2.exe",
                      "sub_usage_3.exe",
                      "sub_usage_5.exe",
                      "sub_usage_6.exe",
                      "sub_usage_7.exe",
                      "sub_usage_8.exe"
                      ]
    #check_exefiles = ["call_sub_post_process.exe", "call_renewal_token.exe", "sub_usage_0.exe"]
    current_dir = os.getcwd()                  
        
    while True:
        
        print("Checking process")
        ProcessList_current = []
        # get info of current processes of windows
        ProcessList_current = process_info_manual()
        
        # check if working process       
        for i in range(0, len(check_exefiles)):
            
            if not check_exefiles[i] in ProcessList_current:
    #                command_execute = "C:\\Users\\user\\Downloads\\ENERTALK\\" + check_exefiles[i]
                command_execute = current_dir + "\\" + check_exefiles[i]        
                os.startfile(command_execute) # run exe file 
    #            
                print("restart!", check_exefiles[i])
                    
        print("waiting")
    #    time.sleep(600) #check every 10 minitues
        time.sleep(10) #check every 10 minitues

except:   
    mail_alarm.mailalarm()

    
"""
ref code.
"""

#def process_info():
#    WMI_current = GetObject('winmgmts:')   
#    ProcessList_current = []
#    processes_current = WMI_current.instancesOf('Win32_Process')     
#    for process_current in processes_current:
#        ProcessList_current.append(process_current.Properties_('Name').Value)
#    
#    return(ProcessList_current)
#get info of initial processes of windows (= standard)     
#WMI = GetObject('winmgmts:')
#ProcessList = []
#processes = WMI.instancesOf('Win32_Process')
#for process in processes:
#     ProcessList.append(process.Properties_('Name').Value)
#     
##    
    


