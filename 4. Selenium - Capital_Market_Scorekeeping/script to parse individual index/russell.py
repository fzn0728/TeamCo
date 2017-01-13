

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def setup_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver    


def open_russell(url):
    driver.get(url)
    login = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lazy"))).click()  
    time.sleep(5)
    driver.switch_to_window(driver.window_handles[-1])
    # Page 1
    driver.find_element_by_xpath("//input[@name='FundCode'][@value='irs3']").click()
    driver.find_element_by_xpath("//input[@name='FundCode'][@value='iru2']").click()
    driver.find_element_by_xpath("//input[@name='FundCode'][@value='irus']").click()
    driver.find_element_by_css_selector("a[href='javascript:submitForm(document.forms[0].action);']").submit()
    # Page 2
    time.sleep(5)
    driver.find_element_by_xpath("//input[@id='rdoStdRtrn'][@value='standard']").click()
    driver.find_element_by_css_selector("a[href='javascript:submitForm(document.forms[0].action);']").submit()
    # Page 3
    time.sleep(5)
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='1_day']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='Last_3_mo']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='1_year']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='3_years']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='5_years']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='10_years']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='MTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='QTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='YTD']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='MTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='QTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='YTD']").click()
    # Select date on Page 3
    time.sleep(5)
    # driver.find_element_by_xpath("//select[@name='d_startDate']/option[@value='12']").submit()
    # Click Next on Page 3
    driver.find_element_by_css_selector("a[href='javascript:validateForm(document.forms[0].action);']").click() 
    return driver

if __name__ == "__main__":
    # Set up the driver
    driver = setup_driver()

    # Open the website
    url = "http://www.ftserussell.com/tools-analytics/russell-index-performance-calculator"
    driver = open_russell(url)

    # Get the text content of current website
    time.sleep(5)
    content = driver.page_source
    soup =  BeautifulSoup(content,"lxml")
    table = soup.find_all('tr', attrs={'bgcolor':'#FFFFFF'})
    data = []
    for t_ in table:
        rows = t_.find_all('td')
        rows = [ele.text.strip() for ele in rows]
        data.append([ele for ele in rows if ele]) # Get rid of empty values 
    df = pd.DataFrame([part for part in data])
