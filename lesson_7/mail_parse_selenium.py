from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time
from pprint import pprint

client=MongoClient('localhost', 27017)
db=client['letters_from_mail']
mail=db.mail

driver=webdriver.Chrome('/Users/kirillvolkov/PycharmProjects/lesson_6_selenium/chromedriver')
driver.get('https://mail.ru/')
assert "Mail.ru" in driver.title

elem=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'mailbox:login')))
elem.send_keys('study.ai_172@mail.ru') #imperium.armanov@mail.ru
elem.send_keys(Keys.RETURN)

elem=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'mailbox:password')))
elem.send_keys('NewPassword172') #Password445
elem.send_keys(Keys.RETURN)

assert "Mail.ru" in driver.title

#скролим до конца пока все письма не откроются
actions=ActionChains(driver)
actions.send_keys(Keys.ARROW_DOWN)

#выходим из цикла при задержке выполнения операции
timeout = 20   # [seconds]
timeout_start = time.time()

while time.time() < (timeout_start + timeout):
    actions.perform()

letters=driver.find_elements_by_xpath('//div[@class="layout__main-frame"]//a')
links=[]
for letter in letters:
    letter_link = letter.get_attribute('href')
    links.append(letter_link)

while True:
    try:
        for link in links:
            time.sleep(1)
            driver.get(link)
            time.sleep(3)
            sender_p=driver.find_element_by_xpath('//div[@class="letter__author"]/span')
            sender=sender_p.get_attribute('title')
            date=driver.find_element_by_class_name('letter__date').text
            topic=driver.find_element_by_class_name('thread__subject').text
            text= driver.find_element_by_class_name('letter-body').text.strip()

            mail_info= {}
            mail_info['sender'] = sender
            mail_info['date'] = date
            mail_info['topic'] = topic
            mail_info['text_block'] = text
            mail.update_one(mail_info, {'$set': mail_info}, upsert=True)
            driver.back()
    except:
        break

objects=mail.find()
for obj in objects:
     pprint(obj)

driver.quit()