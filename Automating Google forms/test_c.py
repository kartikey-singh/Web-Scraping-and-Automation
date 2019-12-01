import os
import sys
import time
import csv
import pandas as pd
from pprint import pprint
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime

URL = 'https://www.rummycircle.com/#register'
desired_capabilities = {
    "acceptInsecureCerts": True
}
# user_agent = "user-agent="+header['USERAGENT']
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(user_agent) 
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--allow-insecure-localhost')
# chrome_options.add_argument('--disable-web-security')
# chrome_options.add_argument('--ignore-urlfetcher-cert-requests')
# chrome_options.add_argument('--no-proxy-server')
driver = webdriver.Chrome(
	# desired_capabilities=desired_capabilities,
	chrome_options=chrome_options,
	executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')
# driver._client.set_header_overrides(headers=dict_headers)		
driver.get(URL)
		