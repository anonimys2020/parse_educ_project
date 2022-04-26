from os import system as cmd
# cmd('pip install selenium')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import urllib.request



s = Service("../chromedriver")
chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(service=s, options=chrome_options)

driver.get('https://gb.ru/login')

elem = driver.find_element(By.ID, 'user_email')
elem.send_keys('EMAIL')

elem = driver.find_element(By.ID, 'user_password')
elem.send_keys('PASSWORD')

elem.send_keys(Keys.ENTER)

driver.get('https://gb.ru/lessons/189774')

elem = driver.find_elements(By.CLASS_NAME, 'lesson-header_ended')
text = driver.find_elements(By.CLASS_NAME, 'lesson-header__title')
h2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[9]/gb__learning/div/header[1]/h2')

h2 = h2.get_attribute('innerHTML')
print(h2)

titles = ''
# for i in range(len(text)):
#     titles += text[i].get_attribute('innerHTML')
for i in text:
    titles += str(i.get_attribute('innerHTML') + '/')
# print(titles)

titles = titles.split('/')
print(titles)

links = []
for i in elem:
    i = i.get_attribute('href')
    i = i.split('/')
    i = i[-1]
    links += [f'https://gb.ru/api/v2/lessons/{i}/playlist']

json_str = []
for link in links:
    driver.get(link)
    text = driver.find_element(By.XPATH, '/html/body/pre')
    json_str += [text.get_attribute('innerHTML')]

for i in range(len(json_str)):
    json_str[i] = json.loads(json_str[i])
    json_str[i] = json_str[i]['playlist'][0]['sources'][0]['src']

print(json_str)
try:
    cmd(f'mkdir "/Volumes/Samsung USB/gb/{h2}"')
except:
    cmd('clear')
# cmd(f'cd "/Volumes/Samsung USB/gb/{h2}"')
for i in range(3, len(json_str)):
    print(f'Downloading file {titles[i]}.mp4 ...\nlink: {json_str[i]}')
    urllib.request.urlretrieve(json_str[i], f"/Volumes/Samsung USB/gb/{h2}/{titles[i]}.mp4")
    print(f'Done!')

print('ok')
driver.quit()