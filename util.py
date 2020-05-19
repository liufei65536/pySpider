'''
爬虫经常用到的函数，比如保存图片，建立数据库，打开浏览器等
'''
import os
from datetime import  date
import requests
from hashlib import md5


def save_b_file(url,stuffix='jpg'):
    '''
    保存二进制文件,主要是图片
    :param url: 文件url
    :param stuffix:文件后缀名
    :return: 成功返回none，否则提示错误。
    '''
    today = date.today().__format__('%Y-%m-%d')
    #创建文件夹，名为今日日期。
    if not os.path.exists(today):
        os.mkdir(today)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            suffix ='jpg'  #后缀名
            filepath = '{0}/{1}.{2}'.format(today,md5(response.content).hexdigest(),suffix)
            if not os.path.exists(filepath):
                with open(filepath,'wb') as f:
                    f.write(response.content)
            else:
                print('文件已存在\nfile has existed')
    except requests.ConnectionError:
        print('url连接错误\n connectionError')




if __name__ == '__main__':
    save_b_file('http://n.sinaimg.cn/default/1_img/upload/3933d981/700/w900h600/20200518/a767-itvqcca1685719.jpg')
