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
    widget = driver.find_element_by_tag_name("iframe")
    driver.switch_to_frame(widget)
    button = driver.find_element_by_xpath('.//*[@id="introAgreeButton"]')
    button.click()

    # Finding the search box
    driver.switch_to_default_content()
    searchbox = driver.find_element_by_id("searchboxinput")
    location = "Dakar"
    searchbox.send_keys(location)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(2)
    cancelbut = driver.find_element_by_class_name("gsst_a")
    cancelbut.click()
    searchbox.send_keys("Hopitaux")
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)

    # Locating the results section
    entries = driver.find_elements_by_class_name("section-result")

    # Prepare the excel file using the Openpyxl
    wb = openpyxl.load_workbook("comapnies.xlsx")
    sheetname = wb.get_sheet_names()[0]
    sheet = wb[sheetname]
    sheet.title = "companies"
    return 0


if __name__ == "__main__":
    get_data()
