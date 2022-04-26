from check import *
import config

a = Parse(email=config.email, password=config.password, url='https://gb.ru/lessons/217494')
b = Parse.get_homeworks(a)