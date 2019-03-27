import time
from selenium import webdriver
from bs4 import BeautifulSoup

def initialiseChromeDriver():
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://me.cleartrip.com/hotels/united-states/miami/")
    return driver

def clickSearchOnCleartrip(driver):
    button = driver.find_element_by_id('buttonHotelSearch')
    button.click()

def scrollToBotton(driver):
    for i in range(1, 2): # Iterating 100 times to scroll for the infinite scroll data content. Bad hack.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4) # Waiting for six seconds for the subsequent content to load

def scrollToTopAndGetPage(driver): # Scrolling to the top to start scraping
        driver.execute_script("window.scrollTo(0, 0);")
        return driver.page_source


def startScrapingContent(page):
    data = BeautifulSoup(page, "lxml")
    list_of_hotels = list()
    list_of_hotel_dictionary = list()
    for datum in data.find_all("li", {"class": "info"}):
        current_dictionary = dict()
        list_of_hotels.append(datum)
        small_element = datum.find("small",{"class":"areaName"})
        rate_element = datum.find("span", {"class":"taRating"})
        if(rate_element is not None and rate_element['title'] is not None):
            current_dictionary['rating'] = rate_element['title']
        else:
            current_dictionary['rating'] = 'Rating unavailable'
        hotel_name = small_element.text.replace("map", "")
        hotel_name = hotel_name.strip()
        current_dictionary['name'] = hotel_name
        list_of_hotel_dictionary.append(current_dictionary)
    print(list_of_hotel_dictionary)
    



driver = initialiseChromeDriver()
clickSearchOnCleartrip(driver)
time.sleep(10) # First time waiting for 20 seconds for the app to load.
scrollToBotton(driver)
page = scrollToTopAndGetPage(driver)
startScrapingContent(page)
