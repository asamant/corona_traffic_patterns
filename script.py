#!/usr/bin/env python3

''' Logic for visualizing the effect of COVID-19 on city traffic:

1. Create a list of cities with the worst known traffic. Online sources
2. Open the Google Maps website
3. Enable the traffic viewing option
4. Set the traffic type as "Live"
5. Iterate over the list of cities, entering the city names one by one in the search box
6. Take screenshot of the active browser page, save in an image file per city
7. Set the traffic type as "Typical, at 7:30 PM on Mondays"
8. Repeat step 6 till all cities' screenshots are captured

'''

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

try:
    # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver
    # Needs chromedriver in the same dir (if not added to PATH)
    driver = webdriver.Chrome(executable_path='./chromedriver')
except:
    print("""Could not find the chromedriver executable. Please check if it is added to the PATH variable or if it isin the current script's directory.
    Or get it from: https://sites.google.com/a/chromium.org/chromedriver/downloads""")
    sys.exit()

driver.fullscreen_window()

# access the Google Maps page
driver.get('http://maps.google.com')
time.sleep(5)

# Test
search_box = driver.find_element_by_name('q')
search_box.send_keys('New York' + Keys.ENTER)
# search_box.submit()

time.sleep(3)

# Clear search button
clear_search_button = driver.find_element_by_class_name('sbcb_a')
click_action = ActionChains(driver)
click_action.click(clear_search_button)
click_action.perform()

time.sleep(5)

driver.quit()
