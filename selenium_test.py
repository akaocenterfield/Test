from pytesseract import image_to_string
from PIL import Image
from selenium import webdriver
import time
import re
import os

os.chdir('C:/Users/akao/Desktop')

keyword = "dog care"

driver = webdriver.Chrome()
driver.get("http://google.com")
elem = driver.find_element_by_name("q")
elem.send_keys(keyword)
time.sleep(1)
driver.set_window_size(1100, 900)
driver.execute_script("document.body.style.zoom='200%'")
total_height = driver.execute_script('return document.body.scrollHeight')
window_height = driver.execute_script('return document.documentElement.clientHeight')

n = 0
for num in range(0, total_height, window_height):
    driver.execute_script('window.scrollTo(0,%d)' % num)
    n += 1
    string = keyword + str(n)
    driver.save_screenshot('%s.png' % string)

driver.close()


def find_yellow_pixels(im):
    pix = im.load()
    x_max = im.size[0]
    y_max = im.size[1]
    yellow_pix_x = list()
    yellow_pix_y = list()
    for i in range(x_max):
        for j in range(y_max):
            if pix[i,j] == (239, 196, 57):
                yellow_pix_x.append(i)
                yellow_pix_y.append(j)

    yellow_x = sorted(list(set(yellow_pix_x)))
    yellow_y = sorted(list(set(yellow_pix_y)))
    yellow_begin_x = [yellow_x[0]]
    yellow_end_x = []
    for i in range(len(yellow_x)-1):
        diff = yellow_x[i+1] - yellow_x[i]
        if diff != 1:
            yellow_begin_x.append(yellow_x[i+1])
            yellow_end_x.append(yellow_x[i])
    yellow_end_x.append(yellow_x[-1])

    yellow_begin_y = [yellow_y[0]]
    yellow_end_y = []
    for i in range(len(yellow_y)-1):
        diff = yellow_y[i+1] - yellow_y[i]
        if diff != 1:
            yellow_begin_y.append(yellow_y[i+1])
            yellow_end_y.append(yellow_y[i])
    yellow_end_y.append(yellow_y[-1])

    #print yellow_begin_x
    #print yellow_end_x
    #print yellow_begin_y
    #print yellow_end_y
    for k in range(len(yellow_begin_y)):
        for i in range(yellow_begin_x[0], yellow_end_x[0] + 1):
            for j in range(yellow_begin_y[k], yellow_end_y[k] + 1):
                if pix[i,j] == (239, 196, 57) :
                    pix[i,j] = (255, 255, 255)
                elif pix[i,j][0] > 240 & pix[i,j][1] > 240 & pix[i,j][1] < 200 :
                    pix[i,j] = (255, 255, 255)
                else:
                    pix[i,j] = (255 - pix[i,j][0], 255 - pix[i,j][1], 255 - pix[i,j][2])
    return im

ad_urls = list()
for i in range(n):
    string = keyword + str(i+1)
    im = Image.open('%s.png' % string)
    try:
        im = find_yellow_pixels(im)
    except:
        print 'no Ads!'

    im.save('%s_ch.png' % string)
    im2 = Image.open('%s_ch.png' % string)
    im2.load()
    im2.split()
    parsed_text = image_to_string(im2)
    lines = re.split('\n', parsed_text)
    #print lines

    for i in range(0, len(lines)):
        if lines[i][0:4] == ":Ad:":
            sss = lines[i][5:]

            final = sss.replace('|', 'l').replace('.coml', '.com/').replace('.corn', '.com')
            if final not in ad_urls:
                ad_urls.append(final)
                final_desc =  'No.' + str(len(ad_urls)) + ' ad url : ' + final
                print final_desc
