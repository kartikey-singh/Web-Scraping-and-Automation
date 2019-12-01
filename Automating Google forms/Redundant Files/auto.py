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
	for i in range(0,headers.shape[0]):
		dict = {}
		header = headers.loc[i]
		dict['Referer'] = header['Referrer']
		dict[header['Option']] = header['IP']
		dict['User-Agent'] = header['USERAGENT']
		dict['existing_proxy_port_to_use'] = "8090"
		print(dict)
		
		# URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe0ySQZWZdcVCzBNBHSVcVBM3Pvyz6SM87o6qIe8uyNQtAvmw/viewform'
		URL = 'http://bantel.o18.click/c?o=504968&amp;m=1369&amp;a=23803'
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

		server = Server(path="./browsermob-proxy/bin/browsermob-proxy", options=dict)
		server.start()
		time.sleep(1)
		proxy = server.create_proxy()
		time.sleep(1)

		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy)) #Configure chrome options
		driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')

		# profile = webdriver.FirefoxProfile()
		# selenium_proxy = proxy.selenium_proxy()
		# profile.set_proxy(selenium_proxy)
		# driver = webdriver.Firefox(firefox_profile=profile, proxy=server,
		# 	executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/geckodriver')
		proxy.new_har("google")

		for j in range(0,data.shape[0]):
			datum = data.loc[j]
			print(datum)
			driver.get(URL)
			time.sleep(1)
			formFilling(driver,datum)

		# print (proxy.har) # returns a HAR JSON blob		
		driver.quit()
		server.stop()	
	return None    

automation()


