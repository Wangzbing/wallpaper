#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime
import sys
import json
import random
import requests
from os import path
from PIL import Image
from bs4 import BeautifulSoup
import win32gui, win32con, win32api


def _getUrl(url,i,cat):
    url= url % (i,cat)
    dat=json.loads(requests.get(url).text)
    ever =dat['data']
    arr=[]
    for each in ever:
        var = each['src']['rawSrc']
        arr.append(var)
    result =random.choice(arr)
    return  result
    print(result)
    print(u'已为您检索到图片共%s张' % str(len(each)))
def _downloadImg(url):
    # Download Images
    basePath = 'D:\\temp\\img'
    if(os.path.isfile(basePath)):
        basePath = os.path.dirname(basePath)
    baseFolder = basePath + '\\Download\\'
    if(not path.exists(baseFolder)):
        os.makedirs(baseFolder)
    print(baseFolder)
    now_time = datetime.datetime.now().strftime('%m%d%H%M%S')
    print(now_time)
    jpgFile = baseFolder +now_time+ '.jpg'
    bmpFile = baseFolder +now_time+ '.bmp'
    response = requests.get(url)
    print(u'正在将文件写入到%s' % baseFolder)
    with open(jpgFile, 'wb') as file:
        file.write(response.content)
    img = Image.open(jpgFile)
    img.save(bmpFile, 'BMP')
    os.remove(jpgFile)

    # Update WallPaper
    print(u'正在设置图片:%s为桌面壁纸...' % now_time+'.jpg')
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmpFile, 1 + 2)
    print('成功应用图片')

if __name__ == '__main__':
    sysUri=sys.path[0]
    exe='\\picTest.exe'
    print(sys.path[0])
    #判断注册表中是否有该shell,没有及添加shell指令，有就继续执行该shell

    # Query Images
    searchURL = 'https://infinity-api.infinitynewtab.com/get-wallpaper?page=%d&source=%s'
    # searchURL = 'https://unsplash.com/napi/search?client_id=%s&query=%s&page=1'
    # client_id = 'fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7'
    categories = ['InfinityLandscape', 'Infinity', 'Unsplash', 'Startup+Stock+Photos']
    categorie = random.choice(categories)
    print(categorie)
    baseURL = searchURL % (0, categorie)
    response = requests.get(baseURL)
    print('正在从infinity上搜索图片...')
    # Parse Images
    data = json.loads(response.text)
    # images
    ever = data['data']
    index = data['totalPages']
    count = 0
    indexs = []
    while (count < index):
        indexs.append(count)
        count = count + 1;
        indexs.append(count)
        print(count)
    print(indexs)
    i = random.choice(indexs)
    result=_getUrl(searchURL,i,categorie)
    _downloadImg(result)
