import json
from bs4 import BeautifulSoup
import requests
import time
import re
import os

'''
TODO
- scrape multiple pages 
- store html file from the links 
- handle if atHome.de tries to block python script'''

# returns a list for apartment, usage to get to new website where we find infomation about particular apartment
def get_apartment_links(apartment_links):
    links = []
    for i in apartment_links:
        text = str(i)
        res =  re.search(r'html', text)
        if res is not None:
            links.append("https://www.athome.de/"+i.attrs['href'])
    return links  


# getting content of all apartments we have links to
def get_content_of_apartment(link_to_apartments):
    store_content = []
    for link_to_apartment in link_to_apartments:
        get_apartment_information = requests.get(link_to_apartment)
        soup = BeautifulSoup(get_apartment_information.text, 'lxml')
        # get content of characteristics block
        res = soup.find_all('li', {'class': 'feature-bloc-content-specification-content'})
        # print all characteristics from particular apartment
        store_characteristics = []
        for r in res:
            key = r.find('div', {'class': 'feature-bloc-content-specification-content-name'}).text
            value = r.find('div', {'class': 'feature-bloc-content-specification-content-response'}).text
            key = key.replace(" ", "_")
            value = value.replace(" ", "_")
            store_characteristics.append(key +" "+value)
        # store location 
        location = soup.find('div', {'class': 'block-localisation-address'})
        store_characteristics.append("Location "+ location.text.replace(" ", "_"))
        store_content.append(store_characteristics)
    return store_content



def store_output(target_path, target_file, data):
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise

    # File will be written in UTF-8: target_path, target_file)+".json", 'w', encoding="utf-8"
    # ensure_ascii = False -> "Sale_price": "1,000,000_€
    #  nothing gives: "Sale_price": "1,000,000_\u20ac
    with open(os.path.join(target_path, target_file)+".json", 'w', encoding = "utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii = False)



def make_dic(keys, values):
    data = {}
    for i in range(len(keys)):
        data[keys[i]] = values[i]
    return data


def main(apartment_no, page):
	# Pretending to be the browser
	header = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


	# Query String Parameters
	payload = {
	    'tr': 'buy',
	    'q': 'd5f74ae0',
	    'loc': 'L4-berlin',
	    'ptypes': 'flat',
	    'pages': ""
	}

	payload['pages'] = str(page)
	response = requests.get("https://www.athome.de/en/srp/?", headers=header, params=payload)
	# Test
	print(response.url)
	# -------
	soup = BeautifulSoup(response.text, 'lxml')
	apartment_links = soup.find_all('a')
	link_to_apartments = get_apartment_links(apartment_links)
	contents = get_content_of_apartment(link_to_apartments)



	# each apartment information is stored in a separate json file
	# inlcude cases if key is not present
	for content in contents:
	    # for one apartment
	    keys = []
	    values = []
	    # making dynamic key value pair, preprocesssing step
	    for e in content:
	        key, value = e.split()
	        keys.append(key)
	        values.append(value)
	    
	    
	    data = make_dic(keys, values)
	    store_output('./apartment_data', f'apartment{apartment_no}', data)
	    apartment_no += 1
	    print(f'apartment_no: {apartment_no}')
	    

	# after 30 apartments wait for 10 seconds and go on with process
	if(apartment_no % 30 == 0):
		time.sleep(10)
	# wait for 2 seconds    
	time.sleep(2)
	return apartment_no


sites = 43
page = 1 
apartment_no = 1
if __name__ == '__main__':
	print("Start scraping...")
	for _ in range(sites):
		apartment_no = main(apartment_no, page)
		apartment_no += 1
		page = page + 1
	print("Scraping finished.")



