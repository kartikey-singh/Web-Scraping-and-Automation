import logging
from pprint import pprint
from seleniumwire import webdriver 

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    chrome_options=chrome_options,
    executable_path='/home/kartikey/Desktop/Files/Freelance-WebScraping-Selenium/chromedriver',
)

driver._client.set_header_overrides(
    headers={
        "User-Agent": "Mozilla/5.0 (test)",
        "Accept": "text/html, foo/bar",
        "Accept-Language": "en,de;q=0.7,fr;q=0.3",
        'New-Header1': 'Some Value',
    })

driver.get("https://www.google.com")

for request in driver.requests:
    if request.response:
        print(request.path, request.response.status_code)
        pprint(dict(request.headers))