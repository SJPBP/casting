from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

driver.get("https://selenium-python.readthedocs.io/api.html")
driver.get("https://www.python.org/search/?q=pycon&submit=")
time.sleep(5)
driver.close()
