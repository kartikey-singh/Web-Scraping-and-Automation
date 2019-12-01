import os
import sys
import time
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from seleniumwire import webdriver
from datetime import datetime

logs = []
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")
logs.append(date)

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

# URL = 'https://goo.gl/forms/IVYWrdBKmVAtg3ru2'
# URL = 'https://7b21cb92-8c0f-4b55-9798-b7c57e6819a9.htmlpasta.com/'
URL = 'https://docs.google.com/forms/d/e/1FAIpQLScZd1fMogV2dNYiMHu-rDDxmLdjwYEr-hZ9b6Q2npFxndT6qg/viewform'

def formFilling(driver,data):
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')
	input_list = soup.find_all('input')
	columns = data.shape[0]
	if len(input_list) < columns:
		logs.append('Incomaptible Form')
		return None

	for i in range(0,columns):
		# try:
		driver.find_element_by_xpath(xpath_soup(input_list[i])).send_keys(data.iloc[i])
		# except:
		# 	logs.append('Could not be done')

	tags = ['span','div','button','submit']	
	flag = 0
	for tag in tags:
		submits = soup.find_all(tag,string = 'Submit')
		
		if len(submits) > 0:
			for submit in submits:
				driver.find_element_by_xpath(xpath_soup(submit)).click()				
			flag = 1
	time.sleep(4)
	submits = soup.find_all('input',{'type':'submit'})		
	print(submits)
	for submit in submits:
		flag = 1
		driver.find_element_by_xpath(xpath_soup(submit)).click()
	
	if flag == 0:
		logs.append('Oops cannot find any Submit Button')	
		return None	
	return None

def automation():
	try:
		headers = pd.read_excel('Database/header.xlsx')
		data = pd.read_csv('Database/data3.csv')
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
		# try:				
		user_agent = "user-agent="+header['USERAGENT']
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument(user_agent) 
		driver = webdriver.Chrome(
			chrome_options=chrome_options,
			executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')
	
		driver._client.set_header_overrides(headers=dict_headers)
		logs.append("Driver Loaded Successfully")
		# except:
		# 	logs.append("Driver NOT Loaded Successfully EXITING ....")
		# 	return None
		# try:
		datum = data.loc[i]
		logs.append(dict_headers)
		logs.append(datum)
		driver.get(URL)
		time.sleep(1)
		formFilling(driver,datum)
		# except:
		# 	logs.append("Reached End of data.csv")
		# 	return None

		driver.quit()
		time.sleep(3)
	logs.append("Closing Script")
	return None    
automation()

# print(logs)
df = pd.DataFrame(logs)
with open('logs.csv', 'a') as f:
    df.to_csv(f, header=False,index=False)