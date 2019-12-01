import os
import sys
import time
import psutil
import urllib.request
import pandas as pd
from selenium import webdriver
from seleniumwire import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

for proc in psutil.process_iter():
	# check whether the process name matches
	if proc.name() == "browsermob-proxy":
		proc.kill()

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
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/label
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[3]/div/label
	driver.find_element_by_xpath(attendance_xpath).click()
	
	# DIETARY RESTRICTION
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[1]
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[2]
	# Other Option
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div
	# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/div/content/div/div/div[1]/input
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
	headers = pd.read_excel('header.xlsx')
	for i in range(0,headers.shape[0]):
		dict = {}
		header = headers.loc[i]
		dict['Referer'] = header['Referrer']
		dict[header['Option']] = header['IP']
		dict['User-Agent'] = header['USERAGENT']
		dict['existing_proxy_port_to_use'] = "8090"
		print(dict)
		
		URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe0ySQZWZdcVCzBNBHSVcVBM3Pvyz6SM87o6qIe8uyNQtAvmw/viewform'
		data = pd.read_csv('data.csv')
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

		for j in range(0,data.shape[0]):

			server = Server(path="./browsermob-proxy/bin/browsermob-proxy", options=dict)
			server.start()
			time.sleep(1)
			proxy = server.create_proxy()
			time.sleep(1)

			profile = webdriver.FirefoxProfile()
			selenium_proxy = proxy.selenium_proxy()
			profile.set_proxy(selenium_proxy)
			driver = webdriver.Firefox(firefox_profile=profile, proxy=server,
				executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/geckodriver')
			proxy.new_har("google")


			datum = data.loc[j]
			driver.get(URL)
			time.sleep(1)
			formFilling(driver,datum)
			driver.quit()


			server.stop()	
	return None    

automation()

# print (proxy.har) # returns a HAR JSON blob
