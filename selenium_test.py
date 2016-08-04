from pytesseract import image_to_string
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
import os

os.chdir('C:/')

kw = []


def find_green_pixels(filename):
    im = Image.open(filename)
    pix = im.load()
    x_max = im.size[0]
    y_max = im.size[1]
    for i in range(x_max):
        for j in range(y_max):
            if pix[i,j] == (89, 148, 107): # (239, 196, 57) yellow
                green_pixel = 1
                return green_pixel


def invert_green_pixels(im):
    pix = im.load()
    x_max = im.size[0]
    y_max = im.size[1]
    green_pix_x = list()
    green_pix_y = list()
    for i in range(x_max):
        for j in range(y_max):
            if pix[i,j] == (89, 148, 107):
                green_pix_x.append(i)
                green_pix_y.append(j)

    green_x = sorted(list(set(green_pix_x)))
    green_y = sorted(list(set(green_pix_y)))
    green_begin_x = [green_x[0]]
    green_end_x = []
    for i in range(len(green_x)-1):
        diff = green_x[i+1] - green_x[i]
        if diff != 1:
            green_begin_x.append(green_x[i+1])
            green_end_x.append(green_x[i])
    green_end_x.append(green_x[-1])
    green_begin_y = [green_y[0]]
    green_end_y = []
    for i in range(len(green_y)-1):
        diff = green_y[i+1] - green_y[i]
        if diff != 1:
            green_begin_y.append(green_y[i+1])
            green_end_y.append(green_y[i])
    green_end_y.append(green_y[-1])
    for k in range(len(green_begin_y)):
        for i in range(green_begin_x[0], green_end_x[0] + 1):
            for j in range(green_begin_y[k], green_end_y[k] + 1):
                if pix[i, j] == (89, 148, 107): #(239, 196, 57)
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
    driver.get("http://www.com")
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
        if find_green_pixels('%s.png' % string):
            im = Image.open('%s.png' % string)
            im2 = invert_green_pixels(im)
            im2.save('%s_ch.png' % string)
            ads_in_pic.append(1)
        else:
            # print 'no Ads!'
            ads_in_pic.append(0)
    # print ads_in_pic

    all_dict = {}
    advertiser_urls = []
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
                    raw_url = re.split(' ', lines[i])[1]
                    clean_url = tidy_url(raw_url)
                    count_dot = clean_url.count(".")
                    count_slash = clean_url.count("/")
                    if count_dot != 2:
                        continue

                    try:
                        clean_url = clean_url[0:clean_url.index('/')]
                    except:
                        pass

                    if clean_url not in advertiser_urls:
                        advertiser_urls.append(clean_url)
                        if p == 1:
                            rank = str(len(advertiser_urls)) + ' top'
                            final_desc =  str(len(advertiser_urls)) + ' (top) : ' + clean_url
                        else:
                            rank = str(len(advertiser_urls)) + ' bottom'
                            final_desc =  str(len(advertiser_urls)) + ' (bottom) : ' + clean_url
                        if clean_url not in all_dict.keys():
                            all_dict[clean_url] = rank
                        #print final_desc
    output_df = pd.DataFrame(all_dict, index=[keyword])
    print output_df
    return output_df


results = pd.DataFrame()
for q in range(len(kw)):
    print kw[q]
    output = find_ad_urls(kw[q])
    results = results.append(output)

results.to_csv('results.csv')
