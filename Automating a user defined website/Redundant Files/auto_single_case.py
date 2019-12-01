import os
import sys
import time
import csv
import pandas as pd
from pprint import pprint
from seleniumwire import webdriver
from datetime import datetime

logs = []
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")
logs.append(date)

def formFilling(driver,data):
	try:
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(data['Name'])
		logs.append("Name Entered Successfully")
	except:
		logs.append("Name NOT Entered Successfully")
	try:
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(data['Email'])
		logs.append("Email Entered Successfully")
	except:
		logs.append("Email NOT Entered Successfully")
	try:
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(data['Organization'])
		logs.append("Organisation Entered Successfully")
	except:
		logs.append("Organisation NOT Entered Successfully")
	try:
		attendance_xpath = '//*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[' + data['Days'] + ']/div/label'
		driver.find_element_by_xpath(attendance_xpath).click()
		logs.append("Attendance Day Clicked Successfully")	
	except:
		logs.append("Attendance Day NOT Clicked Successfully")	
	try:	
		if data['Dietary restrictions'] == 'xx':
			driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/label/div/div[1]/div[3]/div').click()
			driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/div/content/div/div/div[1]/input').send_keys('None Provided')
		else:    
			dietary_xpath = '//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label['+ data['Dietary restrictions'] +']'
			driver.find_element_by_xpath(dietary_xpath).click()
		logs.append("Dietary Restrictions Clicked Successfully")	
	except:
		logs.append("Dietary Restrictions NOT Clicked Successfully")		
	
	try:
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[6]/div/div[2]/div/div/label').click()
		logs.append("Pay $$ Clicked Successfully")
	except:
		logs.append("Pay $$ NOT Clicked Successfully")
	try:
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[3]/div[1]/div/div/content/span').click()
		logs.append("Submit Clicked Successfully")
	except:
		logs.append("Submit NOT Clicked Successfully")
	return None

def automation():
	try:
		headers = pd.read_excel('Database/header.xlsx')
		data = pd.read_csv('Database/data.csv')
		dietary_dict = {
		"None": "1",
		"Vegetarian": "2",
		"Vegan": "3",
		"Kosher": "4",
		"Gluten-free": "5",
		"Other": "xx"
		}
		data['Dietary restrictions'].replace(dietary_dict, inplace=True)
		days_dict = {
		"Day 1":"1",
		"Day 2":"2",
		"Day 3":"3"
		}
		data['Days'].replace(days_dict, inplace=True)
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

		#URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe0ySQZWZdcVCzBNBHSVcVBM3Pvyz6SM87o6qIe8uyNQtAvmw/viewform'
		URL = 'http://bantel.o18.click/c?o=504968&amp;m=1369&amp;a=23803'
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
			time.sleep(1)
			formFilling(driver,datum)
		except:
			logs.append("Reached End of data.csv")
			return None

		driver.quit()
	logs.append("Closing Script")
	return None    
automation()

# print(logs)
df = pd.DataFrame(logs)
with open('logs.csv', 'a') as f:
    df.to_csv(f, header=False,index=False)