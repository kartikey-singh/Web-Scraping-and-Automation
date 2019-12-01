import os
import sys
import time
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from random import randint
from seleniumwire import webdriver
from datetime import datetime

logs = {}
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")
logs['Timestamp']  = date

Columns = ['Timestamp','Headers','Status']
df = pd.DataFrame(columns = Columns)

URL = 'https://goo.gl/forms/IVYWrdBKmVAtg3ru2'

def automation():
	try:
		headers = pd.read_excel('Database/header.xlsx')	
	except:
		logs['Status'] = 'Failed Data not Loaded Successfully'		
		return None

	for i in range(0,headers.shape[0]):
		dict_headers = {}
		header = headers.loc[i]
		if header['Referrer'] != 'NONE':
			dict_headers['Referer'] = header['Referrer']		
		dict_headers[header['Option']] = header['IP']
		dict_headers['User-Agent'] = header['USERAGENT']
		try:				
			path = os.getcwd()
			path_chromedriver = path + "\\Drivers\\chromedriver.exe"
			user_agent = "user-agent="+header['USERAGENT']
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument(user_agent) 
			driver = webdriver.Chrome(
				chrome_options=chrome_options,
				executable_path=path_chromedriver)	
			driver._client.set_header_overrides(headers=dict_headers)			
		except:
			logs['Status'] = logs['Status'] + ' - Failed due to Chromedriver not loading properly'
			return None

		try:
			driver.get(URL)
			sleep_time = randint(3, 20)
			time.sleep(sleep_time)
			logs['Headers'] = str(dict_headers)			
			logs['Status'] = 'Successful'			
		except:
			logs['Status'] = logs['Status'] + ' - Failed while filling Form'
		
		global df
		df = df.append([logs])						
		driver.quit()
	return None    
automation()

if os.path.isfile('logs_user_case1.csv'):
    print("File already exists")
    with open('logs_user_case1.csv', 'a') as f:
        df.to_csv(f, header=False,index=False)
else:
    print("New file created")
    df.to_csv('logs_user_case1.csv',index=False)