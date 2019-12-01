import urllib.request
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import sys
import os

# driver = webdriver.Firefox()
driver = webdriver.Chrome(executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver')
driver.header_overrides = {
    'Referer': 'https://google.com',
    'X-Forwarded-For': '47.29.76.109',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
}
driver.get ('https://docs.google.com/forms/d/e/1FAIpQLSe0ySQZWZdcVCzBNBHSVcVBM3Pvyz6SM87o6qIe8uyNQtAvmw/viewform')
# NAME
driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input').send_keys('NAME')
# EMAIL
driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input').send_keys('EMAIL@mail.com')
# ORGANISATION
driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]/input').send_keys('ORG')
# ATTENDANCE DAY 

# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div/label
# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/label
# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[3]/div/label
driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/label').click()
# DIETARY RESTRICTION
# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[1]
# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[2]
# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[5]



# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div
# //*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/div/content/div/div/div[1]/input


driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/label[5]').click()

# driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[5]/div/div[2]/div/content/div/div/div/content/div/div/div[1]/input').send_keys('FOOD')
# PAY $$ ON ARRIVAL
driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[2]/div[6]/div/div[2]/div/div/label').click()
# SUBMIT
driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[3]/div[1]/div/div/content/span').click()
time.sleep(3)

