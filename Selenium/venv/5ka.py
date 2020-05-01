from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

driverLocation = '/Users/a1/Desktop/Geek/Methods-of-collecting/Selenium/venv/chromedriver'
driver = webdriver.Chrome(driverLocation, options=chrome_options)

driver.get('https://5ka.ru/special_offers/')


close = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='covid-close']"))
)

time.sleep(5)
actions = ActionChains(driver)
actions.move_to_element(close).click().perform()
page = 0
while page < 3:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'special-offers__more-btn'))
        )
        page +=1
        #button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
    except:
        print(page)
        break

time.sleep(1)
goods = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'sale-card'))
        )
pass
for good in goods:
    try:
        print(good.find_element_by_class_name('sale-card__title').text())
        #print('Цена по акции:', float(good
        #                              .find_element_by_class_name('sale-card__price--new')
        #                              .find_element_by_xpath('span[1]')
        #                              .text)/100)
    except:
        print('Парсинг окончен!')


driver.quit()