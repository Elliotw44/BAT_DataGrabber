import bs4
import csv
import time
import requests
from multiprocessing import Pool
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InsecureCertificateException, NoSuchElementException

def main():
    result_url = input("Input the BaT Result URL:")
    web_driver = webdriver.Firefox()
    web_driver.get(result_url)
    load_more = True
    #Find all the URLs we want to parse
    while load_more:
        try:
            #click the load more button if it exists
            elem = web_driver.find_element(By.CSS_SELECTOR, 'div.auctions-footer:nth-child(4) > button:nth-child(1)')
            elem.click()
            time.sleep(1)
        except NoSuchElementException:
            load_more = False
    
    #we've loaded all the results now load it into bs4
    soup = bs4.BeautifulSoup(web_driver.page_source, 'html.parser')
    raw_results = soup.find_all("div", class_="block")

    #format results into dictionary
    auction_results = []
    for item in raw_results:
        if len(item.contents) < 7:
            continue
        entry = {}
        entry['url'] = item.contents[1].attrs['href']
        entry['title'] =item.contents[3].text
        entry['subtitle'] = item.contents[5].text

        entry = data_enrichment(entry)
        if len(entry) < 6:
            continue  #not an auction result
        auction_results.append(entry)


    #Parse all Auction URLs using ThreadPool
    pool = Pool(13)
    final_records = pool.map(auction_page_enrichment, auction_results)
    pool.close()
    pool.join()


    #write to CSV
    with open('BAT_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        datawriter = csv.DictWriter(csvfile, fieldnames=[*final_records[0]])
        datawriter.writeheader()
        for data in final_records:
            datawriter.writerow(data)

#parse out model yr, auction date, price, sold
def data_enrichment(input):
    re_pattern_date = '(\d+\/\d+\/\d+)'
    re_pattern_price = ' (\$\d+,?\d+) '
    re_pattern_model_yr = ' ?([12]\d{3}) '
    re_pattern_sold = '(Sold)'
    if match := re.search(re_pattern_model_yr, input['title'], re.IGNORECASE):
        input['model year'] = match.group(1)
    if 'Porsche' in input['title'] and ('911' in input['title'] or 'GT3' in input['title'] or 'GT2' in input['title']):
        trim_enrichment_911(input)
    if match := re.search(re_pattern_price, input['subtitle'], re.IGNORECASE):
        input['final price'] = match.group(1)
    if match := re.search(re_pattern_date, input['subtitle'], re.IGNORECASE):
        input['auction end date'] = match.group(1) 
    if match := re.search(re_pattern_sold, input['subtitle'], re.IGNORECASE):
        input['sold'] = True
    else:
        input['sold'] = False
    return input
    
#parse out 911 trim information    
def trim_enrichment_911(input):
    re_pattern_911_models = '911 (\w* ?[GTSarg4R ]{0,7})'
    re_pattern_GT_models = '(GT[2|3] ?[RST]{0,2})'
    if match := re.search(re_pattern_GT_models, input['title'], re.IGNORECASE):
        input['model trim'] = match.group(1).strip()
    elif match := re.search(re_pattern_911_models, input['title'], re.IGNORECASE):
        input['model trim'] = match.group(1).strip()
    return input

#parse out transmission and mileage information
def auction_page_enrichment(input):
    re_pattern_manual = 'Speed Manual'
    re_pattern_miles = '[0-9k] Miles'
    mileage_set = False
    auction_url = input['url']
    auction_page = requests.get(auction_url)
    auction_soup = bs4.BeautifulSoup(auction_page.content, 'html.parser')
    raw_results = auction_soup.find_all('li', class_="listings-essentials-item")
    input['transmission'] = "Automatic"
    for listing_es in raw_results:
        listing_content = listing_es.text
        if match := re.search(re_pattern_manual, listing_content, re.IGNORECASE):
            input['transmission'] = "Manual"
        if  mileage_set == False and re.search(re_pattern_miles, listing_content, re.IGNORECASE):
            input['miles'] = listing_content
            mileage_set = True
    return input



if __name__ == '__main__':
    main()