from browsermobproxy import Server
import psutil
import time

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == "browsermob-proxy":
        proc.kill()

dict = {'Referer': 'https://google.com',
    	'X-Forwarded-For': '47.29.76.109',
    	'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'}
server = Server(path="./browsermob-proxy/bin/browsermob-proxy", options=dict)

server.start()
time.sleep(1)
proxy = server.create_proxy()
time.sleep(1)
from selenium import webdriver
profile = webdriver.FirefoxProfile()
selenium_proxy = proxy.selenium_proxy()
profile.set_proxy(selenium_proxy)
driver = webdriver.Firefox(firefox_profile=profile, proxy=server,
	executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/geckodriver')


proxy.new_har("google")
driver.get("https://en.wikipedia.org/wiki/X-Forwarded-For")
print (proxy.har) # returns a HAR JSON blob

server.stop()
driver.quit()