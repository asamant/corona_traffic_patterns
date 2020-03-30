#!/usr/bin/env python3

''' Logic for visualizing the effect of COVID-19 on city traffic:

1. Create a list of cities with the worst known traffic. Online sources
2. Open the Google Maps website
3. Enable the traffic viewing option
4. Set the traffic type as "Live"
5. Iterate over the list of cities, entering the city names one by one in the search box
6. Take a screenshot of the active browser page, save in an image file per city
7. Set the traffic type as "Typical, at 7:30 PM on Mondays"
8. Repeat step 6 till all cities' screenshots are captured

'''

import os
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Enable traffic
def enable_traffic_updates(driver):

    # open the side bar first
    xpath_hamburger_butt = """//*[@id="omnibox-singlebox"]/div[1]/div[1]/button"""
    driver.find_element_by_xpath(xpath_hamburger_butt).click()
    time.sleep(2)

    # then click on the traffic button to enable traffic viz
    xpath_traffic_button = """//*[@id="settings"]/div/div[2]/div/ul[2]/li[2]/button"""
    driver.find_element_by_xpath(xpath_traffic_button).click()

# Take screenshots for cities
def generate_city_screenshot(city, driver, screenshot_filename):

        # search for city and navigate there
        search_box = driver.find_element_by_name('q')
        search_box.send_keys(city + Keys.ENTER)
        time.sleep(3)

        # Clear search button
        clear_search_button = driver.find_element_by_class_name('sbcb_a')
        clear_search_button.click()
        time.sleep(2)

        # take screenshot
        driver.save_screenshot(screenshot_filename)
        time.sleep(2)


def switch_to_typical_traffic(driver):

    # click on the "Live/Typical traffic" dropdown menu button
    traffice_dropdown_xpath = "/html/body/jsl/div[3]/div[9]/div[23]/div[1]/div[1]/div[3]/div/div/div/span/span[1]/div/div/div/div[1]"
    traffic_dropdown = driver.find_element_by_xpath(traffice_dropdown_xpath)
    traffic_dropdown.click()
    time.sleep(2)

    # switch to "Typical traffic" from "Live traffic". assumes that traffic is enabled already, and "Live traffic" is already selected
    ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
    time.sleep(2)

    # horrible hack - click on slider and keep moving until we hit 6:30-ish PM
    traffic_time_slider = driver.find_element_by_class_name("widget-layer-slider-thumb")
    traffic_time_slider.click()
    traffic_time_width = driver.find_element_by_class_name("widget-layer-slider-enabled")
    width_regex = re.compile('width: ([0-9]+)%')

    current_slider_pos = 15

    # 76% on slider = approximately 6:30 PM. Peak traffic time
    while (current_slider_pos < 76):
        style_string = traffic_time_width.get_attribute("style")
        matchObj = width_regex.match(style_string)
        if matchObj:
            current_slider_pos = int(matchObj.group(1)) # get current slider position
        ActionChains(driver).send_keys(Keys.RIGHT).perform() # move slider to the right

    time.sleep(2) # not needed per se


def main(cities):
    try:
        # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver
        # Needs chromedriver in the same dir (if not added to PATH)
        driver = webdriver.Chrome(executable_path='./chromedriver')
    except:
        print("""Could not find the chromedriver executable. Please check if it is added to the PATH variable or if it isin the current script's directory.
        Or get it from: https://sites.google.com/a/chromium.org/chromedriver/downloads""")
        sys.exit()

    driver.fullscreen_window()

    # store screenshots in a new directory
    cwd = os.getcwd()
    screenshot_path = os.path.join(cwd, 'Screenshots')
    if not os.path.exists(screenshot_path):
        os.mkdir(screenshot_path)

    # access the Google Maps page
    driver.get('http://maps.google.com')
    time.sleep(3)

    # assumes these updates are "Live traffic" updates by default
    enable_traffic_updates(driver)
    time.sleep(2)

    for city in cities:
        city_name = city[:].replace(" ", "-") # copy to a new string first
        screenshot_filename = screenshot_path + '/' + city_name + '-corona.png'
        generate_city_screenshot(city, driver, screenshot_filename)

    # to compare with the previous screenshots
    switch_to_typical_traffic(driver)

    for city in cities:
        city_name = city[:].replace(" ", "-") # copy to a new string first
        screenshot_filename = screenshot_path + '/' + city_name + '-typical.png'
        generate_city_screenshot(city, driver, screenshot_filename)

    driver.quit()

if __name__== "__main__":

    # city list
    # https://www.worldatlas.com/articles/cities-with-the-worst-traffic-in-the-world.html
    default_city_list = ["New York", "Beijing", "Tainan", "Rio de Janeiro", "Istanbul", "Bucharest", "Jakarta", "Bangkok", "Mexico City", "Mumbai", "Bangalore"]

    num_args = len(sys.argv)

    if num_args == 1:
        main(default_city_list)
    elif num_args == 2:
        city_list = []
        with open(sys.argv[1], 'r') as file:
            inp = file.read().replace(',','\n').rstrip()
            city_list = inp.split('\n')
        
        if (len(city_list) == 0):
            print("There was an error parsing the input file. Please make it comma- or newline-separated")
        else:
            main(city_list)
    else:
        print("""Incorrect usage of this script.
        Either pass no argument, or only one argument - a file consisting of city names""")
