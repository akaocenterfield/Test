from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(chrome_options = chrome_options)
browser.get('https://www.google.com')
elem = browser.find_element_by_name("q")
elem.send_keys("cheapest fee credit cards")
elem.send_keys(Keys.RETURN)
win1 = browser.window_handles[0]
browser.save_screenshot('credit')



kw = ['lakers tickets', 
      'auto repair shop',
      'best dog insurance']



for ii in range(0, len(kw)):
    ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
    win = browser.window_handles[ii + 1]
    browser.switch_to_window(win)
    browser.get("http://www.google.com")
    elem = browser.find_element_by_name("q")
    elem.send_keys(kw[ii])
    elem.send_keys(Keys.RETURN)

