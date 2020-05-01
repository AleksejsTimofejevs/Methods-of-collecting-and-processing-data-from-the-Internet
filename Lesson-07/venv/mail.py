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

client = MongoClient('localhost', 27017)
db = client['mailru']

def insert_product(mail):
    db.mailru.update_one({"link": mail['link']},
                                     {'$set': mail},
                                      upsert=True
                                      )

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

driverLocation = '/Users/a1/Desktop/Geek/Methods-of-collecting/Lesson-07/venv/chromedriver'
driver = webdriver.Chrome(driverLocation, options=chrome_options)

driver.get('https://mail.ru/')

elem = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'mailbox:login'))
)

elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)

elem = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'mailbox:password'))
)
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)
time.sleep(2)

unique_mails = []

while len(unique_mails) <40:
    try:
        mails = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "llc_normal"))
        )

        try:
            unique_mails_on_page = []
            for mail in mails:
                mail_info = mail.get_attribute('href')
                unique_mails_on_page.append(mail_info)
            print(unique_mails_on_page)
        except:
            print('ошибка')

        if len(unique_mails) != len(list(set(unique_mails + unique_mails_on_page))):
            unique_mails = list(set(unique_mails + unique_mails_on_page))
        else:
            break

        actions = ActionChains(driver)
        actions.move_to_element(mails[-1])
        actions.perform()
        time.sleep(4)
    except:
        break

for uniq_m in unique_mails:
    driver.get(uniq_m)
    title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "h2"))
        )
    body = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "letter__body"))
    )
    mail_from = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='letter__author']/span"))
    )
    date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "// div[ @class ='letter__author'] / div[@ class ='letter__date']"))
    )

    insert_product({
        'link': uniq_m,
        'title': title.text,
        'body': body.text,
        'from': mail_from.get_attribute('title'),
        'date': date.text
    })

    pass

driver.quit()