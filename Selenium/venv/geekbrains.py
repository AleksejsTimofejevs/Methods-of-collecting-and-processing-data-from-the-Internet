from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driverLocation = '/Users/a1/Desktop/Geek/Methods-of-collecting/Selenium/venv/chromedriver'
driver = webdriver.Chrome(driverLocation, options=chrome_options)

#assert 'GeekBrains' in driver.title

#html = driver.page_source

driver.get('https://geekbrains.ru/login')

elem = driver.find_element_by_id('user_email')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id('user_password')
elem.send_keys('Password172')

elem.send_keys(Keys.RETURN)

profile = driver.find_element_by_class_name('avatar')
driver.get(profile.get_attribute('href'))

edit_profile = driver.find_element_by_class_name('text-sm')
driver.get(edit_profile.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
select = Select(gender)
select.select_by_value('2')

driver.find_element_by_xpath('//@href')

#gender.submit()
#driver.back()
#driver.forward()
#driver.refresh()

#options = gender.find_elements_by_tag_name('option')
#for option in options:
#    if option.text == 'Женский':
#        option.click()

driver.quit()
