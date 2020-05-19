from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo
from config import *


#数据库MongoDB相关
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

#模拟浏览器
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KEYWORD = 'iPad'

#第一个页面
def search():
    try_times = 0
    try:
        url = 'https://search.jd.com/Search?keyword='+quote(KEYWORD)
        browser.get(url)
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        get_products()
        return total.text
    except TimeoutException:
        print('search()超时重试...')
        search()

#第page_number个页面
def next_page(page_number):
    """
    抓取索引页
    :param page: 页码
    :return:
    """
    print('正在爬取第',page_number,'页')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page_number)))
        get_products()
    except  Exception:
        print('next_page()出错重试')
        next_page(page_number)

#从页面中解析商品信息
def get_products():
    print("get_products")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList .gl-item').items()

    for item in items:
        product = {
            'image':item.find('.p-img').find('img').attr('src'),#因为不会CSS，看了好久才找到规律
            'price': item.find('.p-price').text(),
            'deal': item.find('.p-commit').text(),
            'title': item.find('.p-name').text()
        }
        #print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存到MongoDB成功',result)
    except Exception:
        print('存储到MongoDB失败',result)

if __name__ == '__main__':
    total =int (search())
    if total>10:
        total = 10
    for i in range(2,total+1):
        next_page(i)
