# -*- coding: utf-8 -*-



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
import time
import string
import openpyxl
import os


def get_data():
    print("Hello World")
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 5)
    
    # Opening Google maps
    driver.get("https://www.google.com/maps")
    time.sleep(3)
    
    # Closing the google consent form
    #widget = driver.find_element_by_tag_name("iframe")
    #driver.switch_to_frame(widget)
    #div_button = driver.find_element_by_class_name("VfPpkd-dgl2Hf-ppHlrf-sM5MNb")
    button_xpath='//button[contains(@aria-label,"Accepter l\'utilisation de cookies")]'
    button = driver.find_element_by_xpath(button_xpath)
    button.click()

    # Finding the search box
    #driver.switch_to_default_content()
    searchinput_xpath='//input[@id="searchboxinput"]'
    searchbox = driver.find_element_by_xpath(searchinput_xpath)
    location = "Dakar"
    searchbox.send_keys(location)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(2)
    cancelsearch_xpath='//a[@class="gsst_a"]'
    cancelbut = driver.find_element_by_xpath(cancelsearch_xpath)
    cancelbut.click()
    searchbox.send_keys("Hopitaux") # or search hôpitaux dakar instead
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    
    # Locating the results section
    results_div='//div[@class="MVVflb-haAclf V0h1Ob-haAclf-d6wfac MVVflb-haAclf-uxVfW-hSRGPd"]'
    entries = driver.find_elements_by_xpath(results_div)
    
    #suggestion
    #list all the hospitals found with the google search and store their info
    #then search hospital by hospital and directly go through the reviews and the ratings
    

    # Prepare the excel file using the Openpyxl
    wb = openpyxl.load_workbook("comapnies.xlsx")
    sheetname = wb.get_sheet_names()[0]
    sheet = wb[sheetname]
    sheet.title = "companies"
    return 0


if __name__ == "__main__":
    get_data()