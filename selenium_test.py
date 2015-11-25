from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(chrome_options = chrome_options)
browser.get('https://www.ask.com')
elem = browser.find_element_by_name("q")
elem.send_keys("cheap credit cards")
elem.send_keys(Keys.RETURN)
win1 = browser.window_handles[0]
browser.save_screenshot('credit')

ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').skey_up(Keys.CONTROL).perform()
win2 = browser.window_handles[1]
browser.switch_to_window(win2)
browser.get("http://www.ask.com")
elem = browser.find_element_by_name("q")
elem.send_keys("useful blogging tools")
elem.send_keys(Keys.RETURN)


ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
win3 = browser.window_handles[2]
browser.switch_to_window(win3)
browser.get("http://www.ask.com")
elem = browser.find_element_by_name("q")
elem.send_keys("best boba place")
elem.send_keys(Keys.RETURN)


ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
win3 = browser.window_handles[2]
browser.switch_to_window(win3)
browser.get("http://www.ask.com")
elem = browser.find_element_by_name("q")
elem.send_keys("best place to buy old cars")
elem.send_keys(Keys.RETURN)
