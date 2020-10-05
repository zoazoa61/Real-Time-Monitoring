# Received code & changed 'basic_auth.sh' file
# readme : Must have installed chromedriver of current version 
# ref.1 : https://sites.google.com/a/chromium.org/chromedriver/downloads
# ref.2 : check received_code.py file

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

def code_changed():
#log_info
usr = ["YOURID"]
pwd = ['YOURPW']
code_ask_url = "https://auth.enertalk.com/authorization?client_id=YOURCLIENDID&response_type=code&redirect_uri=https://app.getpostman.com/oauth2/callback?"
#    code_ask_url = "https://naver.com"
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


#+ change the code in 'basic_auth.sh' file 
present_code = present_code #applying 'Enter' to string
os.chdir('t')
notes = open('basic_auth.sh' , 'r+' , encoding='utf-8' ) #read contents of original file 
lines = notes.readlines()
lines[4] = f'CODE=\'{present_code}\''+'\n' # change the previous_code to current_code
#    aaaaa = "'CODE= ' + "'"+ present_code + "'""
#notes.seek( 0 )  
notes.close()     
os.chdir('..')
change_lines = open('./basic_auth.sh', 'wt', encoding='utf-8') # overwrite changed contents of file
change_lines.writelines(lines)
change_lines.close()
time.sleep(10)
#    driver.implicitly_wait(15)
#    driver.close() #close the webpage




