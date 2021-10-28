import bs4
import csv
import time
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
        auction_results.append(entry)


    #write to CSV
    with open('BAT_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        datawriter = csv.DictWriter(csvfile, fieldnames=[*auction_results[0]])
        datawriter.writeheader()
        for data in auction_results:
            datawriter.writerow(data)


def data_enrichment(input):
    re_pattern_date = '(\d+\/\d+\/\d+)'
    re_pattern_price = ' (\$\d+,?\d+) '
    re_pattern_model_yr = ' ?([12]\d{3}) '
    re_pattern_sold = '(Sold)'
    if match := re.search(re_pattern_model_yr, input['title'], re.IGNORECASE):
        input['model year'] = match.group(1)
    if 'Porsche' in input['title'] and '911' in input['title']:
        Trim_Enrichment_911(input)
    if match := re.search(re_pattern_price, input['subtitle'], re.IGNORECASE):
        input['final price'] = match.group(1)
    if match := re.search(re_pattern_date, input['subtitle'], re.IGNORECASE):
        input['auction end date'] = match.group(1) 
    if match := re.search(re_pattern_sold, input['subtitle'], re.IGNORECASE):
        input['sold'] = True
    else:
        input['sold'] = False
    return input
    
    
def Trim_Enrichment_911(input):
    re_pattern_911_models = '911 (\w* ?[GTSarg4R ]{0,7})'
    if match := re.search(re_pattern_911_models, input['title'], re.IGNORECASE):
        input['model trim'] = match.group(1).strip()
    return input


if __name__ == '__main__':
    main()