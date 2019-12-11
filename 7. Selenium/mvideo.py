from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from pprint import pprint
import time

client=MongoClient('localhost', 27017)
mongo_base=client['best_sellers']
items_for_sale=mongo_base.items_for_sale

chrome_options=Options()
chrome_options.add_argument('start-maximized')

driver=webdriver.Chrome('/Users/kirillvolkov/PycharmProjects/lesson_6_selenium/chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru/')

assert "М.Видео" in driver.title

try:
    slider_m= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'accessories-new')))

    while True:
        try:
            arrow=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.accessories-new .sel-hits-button-next')))
            arrow.click()

            if 'disabled' in arrow.get_attribute('class'):
                break
            time.sleep(1)
        except:
            break

    items=slider_m.find_elements_by_class_name('gallery-list-item')

    for item in items:
        product_data = json.loads(item.find_element_by_xpath('//a[@data-product-info]').get_attribute("data-product-info"))
        items_for_sale.insert_one(product_data)

        driver.quit()
except:
    driver.quit()

