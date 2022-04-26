from os import system as cmd
# cmd('pip install selenium')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import urllib.request


class Parse:
    def __init__(self, email=str, password=str, url=str, path='/Volumes/Samsung USB/gb', service="./chromedriver"):
        self.url = url
        self.path = path

        self.s = Service(service)
        self.chrome_options = Options()
        self.chrome_options.add_argument("start-maximized")

        self.driver = webdriver.Chrome(service=self.s, options=self.chrome_options)

        self.driver.get('https://gb.ru/login')

        self.elem = self.driver.find_element(By.ID, 'user_email')
        self.elem.send_keys(email)

        self.elem = self.driver.find_element(By.ID, 'user_password')
        self.elem.send_keys(password)

        self.elem.send_keys(Keys.ENTER)

        self.driver.get(self.url)

        self.elem = self.driver.find_elements(By.CLASS_NAME, 'lesson-header_ended')
        self.text = self.driver.find_elements(By.CLASS_NAME, 'lesson-header__title')
        self.h2 = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[9]/gb__learning/div/header[1]/h2')

        self.h2 = self.h2.get_attribute('innerHTML')

        self.titles = ''
        for self.i in self.text:
            self.titles += str(self.i.get_attribute('innerHTML')) + '/'
        self.titles = self.titles.split('/')

        self.titles.pop(-1) # последняя строка - "/" получается пустая сторка, из-за этого удаляем


        self.links = []
        self.homework_url = []

        for self.i in self.elem:
            self.i = self.i.get_attribute('href')
            self.i = self.i.split('/')
            self.i = self.i[-1]
            self.links += [f'https://gb.ru/api/v2/lessons/{self.i}/playlist']
            self.homework_url += [f'https://gb.ru/lessons/{self.i}/homework']

        self.json_str = []
        for link in self.links:
            self.driver.get(link)
            self.text = self.driver.find_element(By.XPATH, '/html/body/pre')
            self.json_str += [self.text.get_attribute('innerHTML')]
        self.json = self.json_str

        for self.i in range(len(self.json_str)):
            self.json_str[self.i] = json.loads(self.json_str[self.i])
            self.json_str[self.i] = self.json_str[self.i]['playlist'][0]['sources'][0]['src']

        print(self.homework_url)

        self.homeworks = []
        self.homework_str = ''
        for self.i in self.homework_url:
            self.driver.get(self.i)
            self.homework = []
            self.homework = self.driver.find_element(By.CLASS_NAME, 'task-block-teacher')
            self.homework = self.homework.get_attribute('innerHTML')
            for self.j in range(len(self.homework)):
                self.homework_str += str(self.homework[self.j])
            self.homeworks += [self.homework_str]
        # print(len(self.homeworks), self.homeworks[0], '\n', self.homeworks[1])

        try:
            cmd(f'mkdir "{self.path}/{self.h2}"')
        except:
            pass

    def get_all(self):
        for self.i in range(len(self.json_str)):
            print(f'Downloading file {self.path}/{self.h2}/{self.titles[self.i]}.mp4\nlink: {self.json_str[self.i]}')
            try:
                cmd(f'mkdir "{self.path}/{self.h2}/Lesson {self.i + 1}"')
            except:
                pass
            with open(f'{self.path}/{self.h2}/Lesson {self.i + 1}/data.json', 'a') as file:
                file.write(self.json[self.i])
            file.close()
            with open(f'{self.path}/{self.h2}/Lesson {self.i + 1}/homework.html', 'a') as html:
                html.write(self.homeworks[self.i])
            html.close()
            urllib.request.urlretrieve(self.json_str[self.i], f"{self.path}/{self.h2}/Lesson {self.i + 1}/{self.titles[self.i]}.mp4")
            print(f'Done!')

        print('ok')

        self.driver.quit()

    def get_homeworks(self):
        for self.i in range(len(self.json_str)):
            try:
                cmd(f'mkdir "{self.path}/{self.h2}/Lesson {self.i + 1}"')
            except:
                pass
            with open(f'{self.path}/{self.h2}/Lesson {self.i + 1}/homework.html', 'a') as html:
                html.write(self.homeworks[self.i])
            html.close()
            print(f'Done!')

        print('ok')

        self.driver.quit()

    def get_json(self):
        for self.i in range(len(self.json_str)):
            try:
                cmd(f'mkdir "{self.path}/{self.h2}/Lesson {self.i + 1}"')
            except:
                pass
            with open(f'{self.path}/{self.h2}/Lesson {self.i + 1}/data.json', 'a') as file:
                file.write(self.json[self.i])
            file.close()
            print(f'Done!')

        print('ok')

        self.driver.quit()

    def get_videos(self):
        for self.i in range(len(self.json_str)):
            print(f'Downloading file {self.path}/{self.h2}/{self.titles[self.i]}.mp4\nlink: {self.json_str[self.i]}')
            try:
                cmd(f'mkdir "{self.path}/{self.h2}/Lesson {self.i + 1}"')
            except:
                pass
            urllib.request.urlretrieve(self.json_str[self.i], f"{self.path}/{self.h2}/Lesson {self.i + 1}/{self.titles[self.i]}.mp4")
            print(f'Done!')

        print('ok')

        self.driver.quit()
