import os
import sys
import time
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from random import randint
from pprint import pprint
from seleniumwire import webdriver
from datetime import datetime

logs = []
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")
logs.append(date)

URL = 'https://goo.gl/forms/IVYWrdBKmVAtg3ru2'

def automation():
	try:
		headers = pd.read_excel('Database/header.xlsx')
		logs.append("Data Loaded Correctly")	
	except:
		logs.append("Data NOT Loaded Correctly EXITING ....")		
		return None

	for i in range(0,headers.shape[0]):
		dict_headers = {}
		header = headers.loc[i]
		dict_headers['Referer'] = header['Referrer']
		dict_headers[header['Option']] = header['IP']
		dict_headers['User-Agent'] = header['USERAGENT']
		try:				
			user_agent = "user-agent="+header['USERAGENT']
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument(user_agent) 
			driver = webdriver.Chrome(
				chrome_options=chrome_options,
				executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')
		
			driver._client.set_header_overrides(headers=dict_headers)
			logs.append("Driver Loaded Successfully")
		except:
			logs.append("Driver NOT Loaded Successfully EXITING ....")
			return None

		try:
			driver.get(URL)
			sleep_time = randint(3, 20)
			time.sleep(sleep_time)
			logs.append('Site Opened Correctly for ' + str(sleep_time) + ' seconds')
		except:
			logs.append('Site Not Opened Correctly')
			
		driver.quit()
	logs.append("Closing Script")
	return None    
automation()

df = pd.DataFrame(logs)
with open('logs_user_case1.csv', 'a') as f:
    df.to_csv(f, header=False,index=False)