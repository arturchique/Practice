from time import sleep

from bs4 import BeautifulSoup
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PerekrestokParser:
    @staticmethod
    def parse_perekrestok(page, address, _json):
        gecko = "C:\Program Files\Selenium\geckodriver.exe"
        driver = webdriver.Firefox(executable_path=gecko)
        # Жду пока прогрузится страница
        driver.implicitly_wait(20)
        driver.get(page)

        cards = driver.find_elements_by_class_name("xf-product")
        # Объекты BS для комфортного парсинга
        soups = []
        for card in cards[:15]:
            soup = BeautifulSoup(card.get_attribute('innerHTML'))
            soups.append(soup)
        driver.quit()

        json_output = {}
        for card in soups:
            try:
                name = card.find('a', class_='xf-product-title__link').text.strip('\n ')
                price = card.find('span', class_='xf-price__rouble').text + card.find('span',
                                                                                      class_='xf-price__penny js-price-penny').text.strip(
                    '\xa0\u200a')
                json_output[name] = price + " ₽"
            except AttributeError:
                pass
        _json["Перекрёсток"] = json_output


class UtkonosParser:
    @staticmethod
    def parse_utkonos(page, _json):
        soup = BeautifulSoup(page.text)
        json_output = {}
        cards = soup.find_all('div', class_='goods_pos_bottom')
        for card in cards:
            try:
                name = card.find('a', class_='goods_caption').text
                price = card.find('div', class_='goods_price-item current').text
                json_output[name] = price
            except AttributeError:
                pass
        _json["Утконос"] = json_output


class LavkaParser:
    @staticmethod
    def parse_lavka(page, address, _json):
        gecko = "C:\Program Files\Selenium\geckodriver.exe"
        driver = webdriver.Firefox(executable_path=gecko)
        # Жду пока прогрузится страница
        driver.implicitly_wait(20)
        driver.get(page)
        # Выбираем адресс доставки
        LavkaParser.enter_address(driver, address)
        driver.implicitly_wait(5)
        cards = driver.find_elements_by_class_name("DesktopSubcategory_item")
        # Объекты BS для комфортного парсинга
        soups = []
        for card in cards[:15]:
            soup = BeautifulSoup(card.get_attribute('innerHTML'))
            soups.append(soup)
        driver.quit()
        # Парсинг и заполнение json файла
        json_output = {}
        for card in soups:
            try:
                name = card.find('div', class_='DesktopProductItem_name').text + " " + card.find('div',class_='DesktopProductItem_weight').text
                price = card.find('div', class_='DesktopProductItem_resultPrice').text
                json_output[name] = price
            except AttributeError:
                pass
        _json["Яндекс.Лавка"] = json_output

    @staticmethod
    def enter_address(driver: webdriver.Firefox, address: str):
        driver.find_element_by_css_selector("div.RestaurantPageLocationMapWithButton_button").click()

        driver.implicitly_wait(1)
        address_input = driver.find_element_by_css_selector("input.AppAddressInput_addressInput")
        address_input.send_keys(f"{address}", Keys.ENTER)

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.DesktopLocationModal_ok"))).click()


class MetroParser:
    @staticmethod
    def parse_metro(page, address, _json):
        gecko = "C:\Program Files\Selenium\geckodriver.exe"
        driver = webdriver.Firefox(executable_path=gecko)
        driver.get(page)

        MetroParser.enter_address(driver, address)

        cards = driver.find_elements_by_css_selector("a.product__link")
        soups = []
        for card in cards[:15]:
            soup = BeautifulSoup(card.get_attribute('innerHTML'))
            soups.append(soup)
        driver.quit()
        json_output = {}
        for card in soups:
            try:
                name = card.find('p', class_='product__title').text
                price = card.find('div', class_='product__price').text.replace(u"\n", u"")
                json_output[name] = price
            except AttributeError:
                pass
        _json["Metro"] = json_output

    @staticmethod
    def enter_address(driver: webdriver.Firefox, address: str):
        driver.find_element_by_css_selector("button.Button_1FB7o").click()
        sleep(5)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.search_select_1NNnP"))).click()
        address_input = driver.find_element_by_css_selector("input.search_select_1NNnP")
        address_input.send_keys(f"{address}")
        sleep(2)
        address_input.send_keys(Keys.ENTER)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.map__FNDx"))).click()


