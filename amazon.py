from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv

url = "https://www.amazon.com/s?k=laptops&crid=1KD2UI5H92ZD8&sprefix=laptop%2Caps%2C312&ref=nb_sb_noss_1"

driver = webdriver.Chrome('chromedriver')
driver.get(url)
delay = 3

try:
    main_div = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results sg-row']")))
    inner_html = main_div.get_attribute('innerHTML')
    soup = BeautifulSoup(inner_html, 'html.parser')
    all_div = soup.find_all('div')

    #arrays
    myDiv = []
    name = []
    price = []
    url_image = []

    for script in all_div:
        if script.has_attr('data-index'):
            try:
                name_span = script.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
                price_span = script.find("span", {"class": "a-price-whole"})
                image_div = script.find("div", {"class": "a-section aok-relative s-image-fixed-height"})

                if name_span is not None and price_span is not None:
                    image = image_div.find('img')
                    if price_span is None:
                        price.append("None")
                    else:
                        price.append(price_span.get_text())


                    name.append(name_span.get_text())
                    url_image.append(image['src'])
                    
            except:
                pass


    print("Total items scrap: "+str(len(name)))
    df = pd.DataFrame({'name': name, 'price': price, 'image': url_image})
    df.to_csv('output.csv', mode='a', index=False, header= True)
    print("Data scrap successfully")
    

except TimeoutException:
    print("Loading taking to much time")
