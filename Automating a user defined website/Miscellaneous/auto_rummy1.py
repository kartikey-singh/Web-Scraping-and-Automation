import os
import sys
import time
import csv
import pandas as pd
from random import randint
from pprint import pprint
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime

logs = {}
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")
logs['Timestamp']  = date

Columns = ['Timestamp','Headers','Data','Status']
df = pd.DataFrame(columns = Columns)

def formFilling(driver,data):	
	driver.find_element_by_xpath('//*[@id="reg_username_mobile"]').send_keys(data['Username'])		

	driver.find_element_by_xpath('//*[@id="reg_password_mobile"]').send_keys(data['Password'])
	
	driver.find_element_by_xpath('//*[@id="reg_email_mobile"]').send_keys(data['Email'])
	
	if data['checked'] == 'NO':			
		driver.find_element_by_xpath('//*[@id="reg_email_splOffer_mobile"]').click()

	driver.find_element_by_xpath('//*[@id="reg_state_mobile"]/option[' + data['State'] + ']').click()

	driver.find_element_by_xpath('//*[@id="btn_register_' + data['Gender'] + '_mobile"]').click()
	return None		

def automation():
	try:
		headers = pd.read_excel('Database/header1.xlsx')
		data = pd.read_csv('Database/data_rummy.csv')
		state_dict = {
		"Andaman and Nicobar Islands": "1",
		"Andhra Pradesh": "2",
		"Assam": "3",
		"Bihar": "4",
		"Chandigarh": "5",
		"Chhattisgarh": "6",
		"Dadra and Nagar Haveli": "7",
		"Daman and Diu": "8",
		"Delhi": "9",
		"Goa": "10",
		"Gujarat": "11",
		"Haryana": "12",
		"Himachal Pradesh": "13",
		"Jammu and Kashmir": "14",
		"Jharkhand": "15",
		"Karnataka": "16",
		"Kerala": "17",
		"Lakshadweep": "18",
		"Madhya Pradesh": "19",
		"Maharashtra": "20",
		"Manipur": "21",
		"Meghalaya": "22",
		"Mizoram": "23",
		"Nagaland": "24",
		"Odisha": "25",
		"Pondicherry": "26",
		"Punjab": "27",
		"Rajasthan": "28",
		"Sikkim": "29",
		"Tamil Nadu": "30",
		"Telangana": "31",
		"Tripura": "32",
		"Uttar Pradesh": "33",
		"Uttarakhand": "34",
		"West Bengal": "35"
		}
		data['State'].replace(state_dict, inplace=True)		
	except:
		logs['Status'] = 'Failed'
		return None

	for i in range(0,headers.shape[0]):
		dict_headers = {}
		header = headers.loc[i]
		if header['Referrer'] != 'NONE':
			dict_headers['Referer'] = header['Referrer']
		dict_headers[header['Option']] = header['IP']
		dict_headers['User-Agent'] = header['USERAGENT']

		URL = 'https://www.rummycircle.com/#register'
		try:						
			user_agent = "user-agent="+header['USERAGENT']
			chrome_options = webdriver.ChromeOptions()			
			chrome_options.add_argument(user_agent) 	
			driver = webdriver.Chrome(			
				chrome_options=chrome_options,
				executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')
			
			driver._client.set_header_overrides(headers=dict_headers)			
		except:
			logs['Status'] = 'Failed'
			return None
		try:
			datum = data.loc[i]
			logs['Headers'] = str(dict_headers)
			logs['Data'] = str(datum)
			driver.get(URL)
			sleep_time = randint(3, 20)
			time.sleep(sleep_time)
			try:		
				formFilling(driver,datum)
				logs['Status'] = 'Successful'
			except:
				logs['Status'] = 'Failed'
			print(logs)	
			global df
			df = df.append([logs])	
		except:
			print("Reached End of data.csv")
			return None
		time.sleep(5)	
		driver.quit()
	print("Closing Script ...")
	return None    
automation()


if os.path.isfile('logs_rummy.csv'):
    print("File already exists")
    with open('logs_rummy.csv', 'a') as f:
        df.to_csv(f, header=False,index=False)
else:
    print("New file created")
    df.to_csv('logs_rummy.csv',index=False)

