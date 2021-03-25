from requests.api import head
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request as req
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time 
import re
import requests
import os
from collections import defaultdict
import certifi
import urllib3


def make_driver():
    CHROME_BIN = '/opt/google/chrome/chrome'
    CHROME_DRIVER = '/opt/chrome/chromedriver'

    options = Options()
    options.binary_location = CHROME_BIN
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--lang=ja-JP')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options,executable_path=CHROME_DRIVER)
    driver.implicitly_wait(10)
    return driver

def kw_in_title(file):
    with open(file) as f:
        kw_in_lists = [s.strip() for s in f.readlines()]
    kw_in_list = ' OR '.join(kw_in_lists)
    return kw_in_list

def kw_out_title(file):
    with open(file) as f:
        kw_out_lists = [s.strip() for s in f.readlines()]
    kw_out_list = ' -'.join(kw_out_lists)
    return kw_out_list

def search(driver, kw):
    # kw = input('検索：')
    input_element = driver.find_element_by_name('q')
    input_element.clear()
    input_element.send_keys(kw)
    input_element.send_keys(Keys.RETURN)
    time.sleep(2)

def re_pattern(except_file_main,except_file_sub):
    with open(except_file_main) as f:
        pattern_main_lists = [s.strip() for s in f.readlines()]
    with open(except_file_sub) as f:
        pattern_sub_lists = [s.strip() for s in f.readlines()]
    pattern_lists = pattern_main_lists + pattern_sub_lists
    pattern_list = '|'.join(pattern_lists)
    pattern = re.compile(pattern_list)
    return pattern  

def get_title(url):
    print('途中１-タイトル開始')
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    # headers = {"User-Agent": "~~~~~"}
    # os.environ['CURL_CA_BUNDLE'] = ''
    # ssl_path = '/usr/local/lib/python3.8/dist-packages/certifi/cacert.pem'
    ssl_path = certifi.where()
    url_info = requests.get(url,verify=ssl_path,headers=headers,timeout=10)
    print('non timeout')
    # print(url_info.raise_for_status())
    url_html = BeautifulSoup(url_info.content, "html.parser")
    print('途中１-スクレイピング実行')
    title = url_html.find('title')
    ogp_img = url_html.find('meta',property="og:image").get('content')
    return title.text,ogp_img

def macth_search(dictionary, domain_name):
    flag=False
    for key in dictionary.keys():
        if domain_name in key :
            flag = True
            break
    return flag
# url_info = requests.get(url, verify=ssl_path ,headers=headers)
# url_info = requests.get(url, verify=ssl_path , headers=headers)
def next_page(driver):
    next_button = driver.find_element_by_id("pnnext")
    next_button.click()

def re_pattern_title(file):
    with open(file) as f:
        pattern_lists = [s.strip() for s in f.readlines()]
    pattern_list = '|'.join(pattern_lists)
    title_pattern = re.compile(pattern_list)
    return title_pattern

def adress_list(driver,in_keyword,out_keyword,url_pattern,title_in_pattern,title_out_pattern):
    sign = False
    class_name = "yuRUbf"
    class_elems = driver.find_elements_by_class_name(class_name)

    for elem in class_elems:
        a_tag = elem.find_element_by_tag_name("a")
        url = a_tag.get_attribute("href")
        if '.pdf' in url:
            print('pdf除去')
            continue
        domain_name = urlparse(url).netloc
        print('途中１-ドメイン取得')
        if not bool(url_pattern.search(url)):
            try:
                title,ogp_img = get_title(url)
            except AttributeError:
                print('attributeerror')
                continue
            except requests.exceptions.SSLError:
                print('sslerror')
                continue
            print('途中１-タイトル取得')
            if (len(title) > 255) or (len(url) > 200) or (len(ogp_img) > 200) or (not ogp_img):
                continue
            flag_in = macth_search(in_keyword,domain_name)
            flag_out = macth_search(out_keyword,domain_name)
            if flag_in or flag_out:
                continue
            if len(in_keyword)+len(out_keyword) >= 20:
                sign = True
                break
            if bool(title_in_pattern.search(title)):
                in_keyword[url].append(title)
                in_keyword[url].append(ogp_img)
            elif not bool(title_out_pattern.search(title)):
                out_keyword[url].append(title)
                out_keyword[url].append(ogp_img)
        else:
            continue
    return in_keyword,out_keyword,sign

def get_url(driver,except_file_main,except_file_sub,contain_title,except_title):
    url_pattern = re_pattern(except_file_main,except_file_sub)
    title_in_pattern = re_pattern_title(contain_title)
    title_out_pattern = re_pattern_title(except_title)
    print('途中１-パターン作成')
    in_keyword = defaultdict(list)
    out_keyword = defaultdict(list)
    start_time = time.time()
    print('ループ開始')
    page = 0
    while True:
        in_keyword,out_keyword,sign = adress_list(driver,in_keyword,out_keyword,url_pattern,title_in_pattern,title_out_pattern)
        if sign:
            break
        page += 1
        if page == 9:
            break
        next_page(driver)  
        print('途中１-ネクストページ')
        if time.time() - start_time > 300:
            print('timeout')
            break
    print('ループ完了')
    return in_keyword,out_keyword