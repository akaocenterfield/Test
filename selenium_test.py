from pytesseract import image_to_string
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import os

os.chdir('C:/')

kw = ["flower online", "buy flowers online", "deliver flowers", "online flower delivery"]


def find_yellow_pixels(filename):
    im = Image.open(filename)
    pix = im.load()
    x_max = im.size[0]
    y_max = im.size[1]
    for i in range(x_max):
        for j in range(y_max):
            if pix[i, j] == (239, 196, 57):
                yellow_pixel = 1
                return yellow_pixel


def filter_yellow_pixels(im):
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

    for k in range(len(yellow_begin_y)):
        for i in range(yellow_begin_x[0], yellow_end_x[0] + 1):
            for j in range(yellow_begin_y[k], yellow_end_y[k] + 1):
                if pix[i, j] == (239, 196, 57):
                    pix[i, j] = (255, 255, 255)
                elif pix[i, j][0] > 240 & pix[i, j][1] > 240 & pix[i, j][1] < 200:
                    pix[i, j] = (255, 255, 255)
                else:
                    pix[i, j] = (255 - pix[i, j][0], 255 - pix[i, j][1], 255 - pix[i, j][2])
    return im


def tidy_url(url):
    clean_url = url.replace('vv', 'w').replace('|', 'l').replace('.coml', '.com/').\
        replace('.corn', '.com').replace('\xef\xac\x82', 'fl')
    return clean_url


def find_ad_urls(keyword):

    driver = webdriver.Chrome()
    driver.get("http://ask.com")
    elem = driver.find_element_by_name("q")
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    driver.set_window_size(1350, 900)
    driver.execute_script("document.body.style.zoom='300%'")
    time.sleep(1)
    total_height = driver.execute_script('return document.body.scrollHeight')
    window_height = driver.execute_script('return document.documentElement.clientHeight')

    n = 0
    for num in range(0, total_height, window_height - 85):
        driver.execute_script('window.scrollTo(0,%d)' % num)
        time.sleep(1)
        #print num
        n += 1
        string = keyword + str(n)
        driver.save_screenshot('%s.png' % string)
    driver.close()

    ads_in_pic = []
    for i in range(n):
        string = keyword + str(i+1)
        if find_yellow_pixels('%s.png' % string):
            im = Image.open('%s.png' % string)
            im2 = filter_yellow_pixels(im)
            im2.save('%s_ch.png' % string)
            ads_in_pic.append(1)
        else:
            #print 'no Ads!'
            ads_in_pic.append(0)
    #print ads_in_pic

    all_dict = {}
    ad_urls = []
    p = 1
    for j in range(n):
        p = p * ads_in_pic[j]
        if ads_in_pic[j] == 1:
            string = keyword + str(j+1)
            im3 = Image.open('%s_ch.png' % string)
            im3.load()
            im3.split()
            parsed_text = image_to_string(im3)
            lines = re.split('\n', parsed_text)
            #print lines
            for i in range(0, len(lines)):
                if "Ad" in lines[i][0:4]:
                    sss = re.split(' ', lines[i])[1]
                    clean_url = tidy_url(sss)
                    if clean_url not in ad_urls:
                        ad_urls.append(clean_url)
                        if p == 1:
                            rank = str(len(ad_urls)) + ' top'
                            final_desc =  str(len(ad_urls)) + ' (top) : ' + clean_url
                        else:
                            rank = str(len(ad_urls)) + ' bottom'
                            final_desc =  str(len(ad_urls)) + ' (bottom) : ' + clean_url
                        if clean_url not in all_dict.keys():
                            all_dict[clean_url] = rank
                        #print final_desc
    print all_dict


for q in range(len(kw)):
    print kw[q]
    find_ad_urls(kw[q])
