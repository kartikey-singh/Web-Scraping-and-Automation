import os
import sys
import time
import csv
import pandas as pd
from pprint import pprint
from random import randint
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime

logs = []
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")
logs.append(date)

def formFilling(driver,data):
	try:
		driver.find_element_by_xpath('//*[@id="reg_username_mobile"]').send_keys(data['Username'])
		logs.append("Username Entered Successfully")
	except:
		logs.append("Username NOT Entered Successfully")
	try:
		driver.find_element_by_xpath('//*[@id="reg_password_mobile"]').send_keys(data['Password'])
		logs.append("Password Entered Successfully")
	except:
		logs.append("Password NOT Entered Successfully")
	try:
		driver.find_element_by_xpath('//*[@id="reg_email_mobile"]').send_keys(data['Email'])
		logs.append("Email Entered Successfully")
	except:
		logs.append("Email NOT Entered Successfully")
	try: 
		if data['checked'] == 'NO':			
			driver.find_element_by_xpath('//*[@id="reg_email_splOffer_mobile"]').click()
		logs.append('Checking Successfully')	
	except:		
		logs.append('Checking Not Successfully')			
	try:
		driver.find_element_by_xpath('//*[@id="reg_state_mobile"]/option[' + data['State'] + ']').click()
		logs.append("State Clicked Successfully")	
	except:
		logs.append("State NOT Clicked Successfully")	
	try:
		driver.find_element_by_xpath('//*[@id="btn_register_' + data['Gender'] + '_mobile"]').click()
		logs.append("Submit Clicked Successfully")
	except:
		logs.append("Submit NOT Clicked Successfully")	
	return None		

def automation():
	try:
		headers = pd.read_excel('Database/header.xlsx')
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

		URL = 'https://www.rummycircle.com/#register'
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
			logs.append("Driver Loaded Successfully")
		except:
			logs.append("Driver NOT Loaded Successfully EXITING ....")
			return None
		try:
			datum = data.loc[i]
			logs.append(dict_headers)
			logs.append(datum)
			driver.get(URL)
			sleep_time = randint(3, 20)
			time.sleep(sleep_time)				
			formFilling(driver,datum)
		except:
			logs.append("Reached End of data.csv")
			return None
		time.sleep(5)	
		driver.quit()
	logs.append("Closing Script")
	return None    
automation()

print(logs)
df = pd.DataFrame(logs)
with open('logs_rummy.csv', 'a') as f:
    df.to_csv(f, header=False,index=False)