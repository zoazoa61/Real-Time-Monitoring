# Received code
# readme : Must have installed chromedriver of current version 
# ref : https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.25/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#log_info
usr = ["YOURID"]
pwd = ['YOURPW']
code_ask_url = 'https://auth.enertalk.com/authorization?client_id=YOURCLIENDID&response_type=code&redirect_uri=https://app.getpostman.com/oauth2/callback?'

#load chrome
path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" # define the path of chromedriver
driver = webdriver.Chrome(path)
driver.implicitly_wait(2) #for load delay
driver.get(code_ask_url)

elem = driver.find_element_by_xpath(".//*[@name='email']") # part : Email
elem.send_keys(usr)

elem = driver.find_element_by_xpath(".//*[@name='password']") # part : Password
elem.send_keys(pwd)

elem.send_keys(Keys.RETURN) # ENTER
driver.implicitly_wait(2) #for load delay

#change webpage
code_response_url = driver.current_url # changed url

present_code = code_response_url[49:49+64] #the number of code : 64 characters
