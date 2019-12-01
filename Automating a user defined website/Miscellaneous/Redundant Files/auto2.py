import os
import sys
import time
import pandas as pd
from pprint import pprint
from seleniumwire import webdriver

def formFilling(driver,data):
	# NAME
	driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(data['Name'])
	# EMAIL
	driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(data['Email'])
	# ORGANISATION
	driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(data['Organization'])
	# ATTENDANCE DAY 
	attendance_xpath = '//*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[' + data['Days'] + ']/div/label'
	# Working Examples:
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div/label
	driver.find_element_by_xpath(attendance_xpath).click()
	# DIETARY RESTRICTION
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[1]
	if data['Dietary restrictions'] == 'xx':
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/label/div/div[1]/div[3]/div').click()
		# Input Field
		driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/div/content/div/div/div[1]/input').send_keys('None Provided')
	else:    
		dietary_xpath = '//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label['+ data['Dietary restrictions'] +']'
		driver.find_element_by_xpath(dietary_xpath).click()
	# PAY $$ ON ARRIVAL
	driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[6]/div/div[2]/div/div/label').click()
	# SUBMIT
	driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[3]/div[1]/div/div/content/span').click()
	return None

def automation():
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

	for i in range(0,headers.shape[0]):
		dict_headers = {}
		header = headers.loc[i]
		dict_headers['Referer'] = header['Referrer']
		dict_headers[header['Option']] = header['IP']
		dict_headers['User-Agent'] = header['USERAGENT']

		URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe0ySQZWZdcVCzBNBHSVcVBM3Pvyz6SM87o6qIe8uyNQtAvmw/viewform'
		# URL = 'http://bantel.o18.click/c?o=504968&amp;m=1369&amp;a=23803'

		user_agent = "user-agent="+header['USERAGENT']
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument(user_agent) 
		driver = webdriver.Chrome(
			chrome_options=chrome_options,
			executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')
	
		driver._client.set_header_overrides(headers=dict_headers)

		try:
			datum = data.loc[i]
			print(dict_headers)
			print(datum)
			driver.get(URL)
			time.sleep(1)
			formFilling(driver,datum)
		except:
			print("Reached End of data.csv")
			return None

		# for request in driver.requests:
		#     if request.response:
		#         print(request.path, request.response.status_code)
		#         pprint(dict(request.headers))
		driver.quit()
	return None    
automation()