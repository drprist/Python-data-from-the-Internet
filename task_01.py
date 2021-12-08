from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(
    executable_path='./chromedriver.exe',
    options=chrome_options
)

login = "study.ai_172"
pwd = "NextPassword172#"
host = "https://account.mail.ru/login/"

driver.get(host)

login_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
login_field.send_keys(login)
login_field.submit()

password_field = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, 'password')))
password_field.send_keys(pwd)
password_field.submit()

driver.implicitly_wait(10)

url_set = set()
last_letter = 0

while True:
    data = driver.find_element(By.CLASS_NAME, 'letter-list')
    letters = data.find_elements(By.CSS_SELECTOR, 'a')
    if letters[-1] == last_letter:
        break
    for i in letters:
        link = i.get_attribute('href')
        if link and 'e.mail.ru' in link:
            url_set.add(link)

    last_letter = letters[-1]
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
    time.sleep(1)

emails = []
for a in url_set:
    driver.get(a)
    letters_dict = {}

    elem = driver.find_element(By.CLASS_NAME, 'letter__author')
    letters_dict['author'] = elem.find_element(By.CLASS_NAME, 'letter-contact').text
    letters_dict['date'] = elem.find_element(By.CLASS_NAME, 'letter__date').text
    letters_dict['link'] = a
    letters_dict['thread'] = driver.find_element(By.CLASS_NAME, 'thread__subject').text
    letters_dict['text'] = driver.find_element(By.CLASS_NAME, 'letter__body').text
    emails.append(letters_dict)

client = MongoClient('127.0.0.1', 27017)
db = client['emails']
collection = db.mailru

for a in emails:
    try:
        collection.update_one({'link': a['link']}, {'$set': a}, upsert=True)
    except DuplicateKeyError as e:
        print(e)

print('FINISH')
