import bs4
import csv
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def main():
    result_url = 'https://bringatrailer.com/porsche/911-gt3/?q=gt3/'
    web_driver = webdriver.Firefox()
    result_page = web_driver.get(result_url)
    load_more = True
    #Find all the URLs we want to parse
    while load_more:
        try:
            #click the load more button if it exists
            elem = web_driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[8]/div[3]/div[4]/button")
            elem.click()
            time.sleep(1)
        except NoSuchElementException:
            load_more = False
    
    #we've loaded all the results now load it into bs4
    soup = bs4.BeautifulSoup(web_driver.page_source, 'html.parser')
    auc_results = soup.find_all("div", class_="filter-group")
    #pull out json list of all reuslts
    string_json_results = auc_results[0].attrs['data-list']
    result_dict = json.loads(string_json_results)['items']
    final_dict = ETL_flatten(result_dict)

    #write to CSV
    with open('BAT_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        datawriter = csv.DictWriter(csvfile, fieldnames=[*final_dict[0]])
        datawriter.writeheader()
        for data in final_dict:
            datawriter.writerow(data)


def ETL_flatten(dict):
    for data in dict:
        data['images'] = data['images']['small']['url']
    return dict
        

if __name__ == '__main__':
    main()