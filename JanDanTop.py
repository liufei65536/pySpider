#煎蛋热榜图
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import os
from hashlib import md5
from datetime import date
import requests


def save_image(item):

    today = date.today().__format__('%Y-%m-%d')
    if not os.path.exists(today):
        os.mkdir(today)
    try:
        url = 'http:'+item
        response = requests.get(url)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(today, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')



#开浏览器
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

url = 'http://jandan.net/top-ooxx'
browser.get(url)

def get_image():
    html = browser.page_source
    doc = pq(html)
    items = doc('.commentlist').find('li').items()
    #print(items)
    for item in items:
       # print(item)
        image = item.find('p').find('a').attr('href')
        yield image



if __name__ == '__main__':
    print(date.today())
    items = get_image()
    for item in items:
        save_image(item)
    browser.close()

