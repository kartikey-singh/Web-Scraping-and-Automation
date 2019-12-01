import requests
url = 'https://httpbin.org/headers'
# Get a copy of the default headers that requests would use
headers = requests.utils.default_headers()
# Update the headers with your custom ones
# You don't have to worry about case-sensitivity with
# the dictionary keys, because default_headers uses a custom
# CaseInsensitiveDict implementation within requests' source code.
headers.update({
	'Referer': 'https://google.com',
    'X-Forwarded-For': '47.29.76.109',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'	        
})
response = requests.get(url, headers=headers)
print(response.text)