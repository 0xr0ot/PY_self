#!usr/bin/env python3
# -*- coding: utf-8 -*-


import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from config import *
import pymongo


driver = webdriver.Chrome(drv_path)
wait = WebDriverWait(driver, 10)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def search():
    try:
        driver.get(url)
        inputs = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="q"]')))
        submits = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        inputs.send_keys(find_text)
        submits.click()
        totals = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()##
        return totals.text
    except TimeoutException:
        return search()


def next_page(page_num):
    print('Openning page', page_num)
    try:
        inputs = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                            '#mainsrp-pager > div > div > div > div.form > input')))
        submits = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                            '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        inputs.clear()
        inputs.send_keys(page_num)
        submits.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 
                   '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_num)))
        get_products()##
    except TimeoutException:
        return next_page(page_num)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = driver.page_source
    doc = pq(html)
    its = doc('#mainsrp-itemlist .items .item').items()
    for it in its:
        product = {
            'image': it.find('.img').attr('src'),
            'price': it.find('.price').text(),
            'deal': it.find('.deal-cnt').text()[:-3],
            'title': it.find('.title').text(),
            'shop': it.find('.shop').text(),
            'location': it.find('.location').text()
            }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('Save to mongo successfully!', result)
    except Exception:
        print('Save failed!', result)


def main():
    totals = search()
    total = int(re.findall('(\d+)', totals)[0])
    for i in range(2, total + 1):
        next_page(i)
    driver.close()


if __name__ == '__main__':
    main()
