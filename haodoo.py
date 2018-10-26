#!/usr/bin/env python3

import selenium.webdriver
import re
import os
import http.client


def parse_url(url):
    """
    解析url，获取其中的「协议」、「主机名」、「路径」、「查询串」信息
    :param url: url
    :return: component: map {'protocal': protocal, 'host': host, 'path': path, 'query': query}
    """
    pattern = re.compile('^((?P<protocal>http)://)?((?P<host>[^/]*)/?)?((?P<path>[^?^#]*)/?)?(?P<query>\?[^#]*)?')
    match = pattern.search(url)
    protocal = match.group('protocal')
    host = match.group('host')
    path = match.group('path')
    query = match.group('query')

    component = {
        'protocal': protocal or '',
        'host': host or '',
        'path': path or '',
        'query': query or ''
    }
    return component


def get_file_type(path):
    """
    获取文件类型
    :param path:
    :return:
    """
    pattern = re.compile('([^.]*$)')
    match = pattern.search(path)
    return match and match.group(1)


def process(url):
    """
    处理html文件
    :param url:
    :return:
    """
    urlComponent = parse_url(url)
    if urlComponent['host'] and urlComponent['host'] != 'haodoo.net':
        return
    if urlComponent['path']:
        fileType = get_file_type(urlComponent['path'])
        if 'png' == fileType or 'jpg' == fileType or 'jpeg' == fileType or 'png' == fileType or 'js' == fileType:
            image_and_js_process(url)
        elif 'css' == fileType:
            css_process(url)
    elif urlComponent['query']:
        "此处处理是不完善的，仅适用于好读网站"
        html_process(url)
    return


def image_and_js_process(url):
    """
    处理图片和js文件
    :param url:
    :return:
    """
    urlComponent = parse_url(url)
    filePath = './pages/' + urlComponent['path']
    if os._exists(filePath):
        return
    path_process(filePath)
    conn = http.client.HTTPConnection(urlComponent['host'])
    conn.request('GET', url)
    response = conn.getresponse()
    file = open(filePath, 'wb')
    file.write(response.read())
    file.close()
    return


def path_process(filePath):
    
    return


def css_process(url):
    """
    处理css文件
    :param url:
    :return:
    """
    return


def html_process(url):
    """
    处理html文件
    :param url:
    :return:
    """
    urlComponent = parse_url(url);
    # filePath = './pages/' + urlComponent['query']
    # if os._exists(filePath):
    #     return
    chrome.get(url)
    # content = chrome.page_source
    # file = open(filePath, 'w')
    # file.write(content)
    # file.close()

    imgs = chrome.find_elements_by_css_selector('img')
    for img in imgs:
        process(img.get_attribute('src'))
    scripts = chrome.find_elements_by_xpath("//script[@src]")
    for script in scripts:
        process(script.get_attribute('src'))

    return


opts = selenium.webdriver.ChromeOptions()

opts.headless = True

chrome = selenium.webdriver.Chrome(options = opts)

url = 'http://haodoo.net/?M=hd&P=welcome'

process(url)

chrome.close()
