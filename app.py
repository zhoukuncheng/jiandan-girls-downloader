import requests
import os
import re
from gevent import monkey

monkey.patch_all()


def open_url(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.26 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.content


def get_page(url):
    html = open_url(url).decode('utf-8')
    pattern = r'<span class="current-comment-page">\[(\d{4})\]</span>'  # 正则表达式寻找页面地址

    page = int(re.findall(pattern, html)[0])
    return page


def find_imgs(page_url):
    pattern = r'<img src="(.*?\.jpg)"'
    html = open_url(page_url).decode('utf-8')
    img_addrs = re.findall(pattern, html)
    return img_addrs


def save_imgs(img_addrs, page_num, folder):
    os.mkdir(str(page_num))
    os.chdir(str(page_num))
    for i in img_addrs:
        pattern = r'sinaimg.cn/mw600/(.*?).jpg'
        filename = i.split('/')[-1]
        image = open_url(i)
        with open(filename, 'wb') as f:
            f.write(image)
            f.close()


def download_imgs(folder='jiandan', pages=10):
    os.mkdir(folder)  # 新建文件夹
    os.chdir(folder)  # 跳转到文件夹
    folder_top = os.getcwd()  # 获取当前工作目录
    url = 'http://jandan.net/ooxx/'
    page_num = get_page(url)  # 获取网页最新的地址
    for i in range(pages):
        page_num -= i  # 递减下载几个网页
        page_url = url + 'page-' + str(page_num) + '#comments'  # 组合网页地址
        img_addrs = find_imgs(page_url)  # 获取图片地址
        save_imgs(img_addrs, page_num, folder)  # 保存图片
        os.chdir(folder_top)


if __name__ == '__main__':
    folder = input("Please enter a folder(default is 'jiandan'): ")
    pages = input("How many pages do you wan to download(default is 10): ")
    download_imgs(str(folder), int(pages))
