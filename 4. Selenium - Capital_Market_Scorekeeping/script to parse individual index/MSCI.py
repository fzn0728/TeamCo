
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


def setup_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver  

def MSCI_find_hidden_link():
    '''
    Find the hidden link given by text indicator "page:", in case that they change the link
    '''
    url = 'https://www.msci.com/end-of-day-data-search'
    soup = BeautifulSoup(urlopen(url).read(),'lxml')
    sentence = soup.find("iframe", id = "_48_INSTANCE_2rBHjKjrfC0Q_iframe").text
    if "page:" in sentence:    
        msg, link = sentence.split("page:",1)
    else:
        raise NameError('The original content changed and auto link fetching has failed,'\
                        'please check the html file and find the hidden link manually.')
    return link[1:-2]
    

def MSCI_get_value_DM(url_table):
    '''
    Find 'tbody' first, and locate the 'tr' tag, then extract all text after 'td' tag.
    '''
    # Get soup
    soup = BeautifulSoup(urlopen(url_table).read(),'lxml')
    # Get data value
    data = []
    table = soup.find("tbody", id = "templateForm:tableResult0:tbody_element")
    rows = table.find_all('tr')
    for tr in rows:
        cols = tr.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values    
    df = pd.DataFrame([part for part in data])
    df.columns=['MSCI Index','Index Code','Last','Day','MTD','3MTD','YTD','1 Yr','3 Yr','5 Yr','10 Yr']
    df.to_csv('MSCI_DM.csv')
    return df

def MSCI_get_value_EM(url_table):
    driver = setup_driver()
    driver.get(url_table)
    time.sleep(5)
    # select = Select(driver.find_element_by_name('templateForm:_id56'))
    
    opt = driver.find_element_by_name('templateForm:_id56')
    # driver.find_element_by_class_name('aoc-ComboBox paragraphTextFont ').click()
    
    
    # opt.send_keys(Keys.RETURN)
    # opt.click()
    time.sleep(5)
    for option in opt.find_elements_by_tag_name('option'):
        if option.text == 'Emerging Markets (EM)':
            option.click()
    
    
    # select.select_by_value('1898').click()
    time.sleep(5)
    driver.find_element_by_id('templateForm:_id106').click()
    content = driver.page_source
    
    # Get soup
    soup = BeautifulSoup(content,'lxml')
    # Get data value
    data = []
    table = soup.find("tbody", id = "templateForm:tableResult0:tbody_element")
    rows = table.find_all('tr')
    for tr in rows:
        cols = tr.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values    
    df = pd.DataFrame([part for part in data])
    df.columns=['MSCI Index','Index Code','Last','Day','MTD','3MTD','YTD','1 Yr','3 Yr','5 Yr','10 Yr']
    df.to_csv('MSCI_DM.csv')
    return df
    
    

if __name__ == "__main__":
    # Get the hidden link
    ### link = find_hidden_link()
    url_table = 'https://www.msci.com/end-of-day-data-search'
    hidden_link_DM = 'https://app2.msci.com/webapp/indexperf/pages/IEIPerformanceRegional.jsf'
    hidden_link_EM = 'https://app2.msci.com/webapp/indexperf/pages/IEIPerformanceRegional.jsf'
    # Fetch html from url (jsf in this case)
    # Parse raw data from the table 
    # data_DM_df = MSCI_get_value_DM(hidden_link_DM)
    data_EM_df = MSCI_get_value_EM(hidden_link_EM)
    # Clean the format and change it into dataframe
    
    
