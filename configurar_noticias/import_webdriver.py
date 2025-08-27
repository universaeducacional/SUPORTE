from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")  # ou qualquer outro argumento que queira

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")