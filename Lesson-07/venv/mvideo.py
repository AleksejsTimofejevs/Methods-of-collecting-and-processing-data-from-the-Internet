from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time
import json

client = MongoClient('localhost', 27017)
db = client['mvideo']

def insert_product(hit):
    db.mvideo.update_one({"productId": hit['productId']},
                                     {'$set': hit},
                                      upsert=True
                                      )

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

driverLocation = '/Users/a1/Desktop/Geek/Methods-of-collecting/Lesson-07/venv/chromedriver'
driver = webdriver.Chrome(driverLocation, options=chrome_options)

driver.get('https://www.mvideo.ru/')

time.sleep(5)

page = 0
while True:
    try:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='wrapper']//div[10]//a[@class='sel-product-tile-title']"))
        )
        try:
            for prod in products:
                product_info = prod.get_attribute('data-product-info')
                product_info = product_info.replace('\n\t\t\t\t\t', '')
                dict = json.loads(product_info)
                insert_product(dict)
                print(dict, type(dict))
        except:
            print('ошибка')

        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='wrapper']//div[10]//a[@class='next-btn sel-hits-button-next']"))
        )

        page +=1
        actions = ActionChains(driver)
        actions.move_to_element(button).click().perform()
    except:
        break

driver.quit()