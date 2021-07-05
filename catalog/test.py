from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


gecko = "C:\Program Files\Selenium\geckodriver.exe"
driver = webdriver.Firefox(executable_path=gecko)

driver.get("https://delivery.metro-cc.ru/metro/search?keywords=%D0%BB%D1%83%D0%BA&sid=1")

enter_address(driver, "волоколамское шоссе 2")