#!/usr/bin/env python3

import http.client
import re
import os

def process(url, type=''):
    """
    主处理方法
    :param url:
    :return:
    """
    if url in links:
        return
    links.append(url)
    url_component = parse_url(url)
    if url_component['host'] != 'haodoo.net':
        return
    print(url)
    if  type == 'readonline':
        readonline_process(url, url_component)
    elif url_component['path'] != '':
        file_process(url, url_component)
    else:
        html_process(url, url_component)
    return

def readonline_process(url, url_component):
    """
    处理在线阅读的保存和解析
    :param url:
    :param url_component:
    :return:
    """

    body = get_body(url, url_component)
    path = './pages/' + url_component['query']
    save_file(body, path)
    content = parse_body(body)
    if content == '':
        return
    imgs_process(content)
    scripts_process(content)
    icons_process(content)
    styles_process(content)
    onlinereads_process(content)

    page_pattern = re.compile(':(\d*)&')
    page_match = page_pattern.findall(url_component['query'])
    if page_match and page_match[0] == '0':
        pages_pattern = re.compile('var\W*maxchapterid\W*=\W*(\d*)\W*;*', re.I)
        pages_match = pages_pattern.findall(content)
        if pages_match:
            pages = int(pages_match[0])
            for page in range(1, pages + 1):
                link = re.sub('\:0\&', ':' + str(page) + '&', url)
                link_component = parse_url(link)
                link_path = './pages/' + link_component['query']
                if os.path.exists(link_path):
                    print(link)
                    continue
                process(link, 'readonline')


def get_body(url, url_component):
    """
    获取内容
    :param url:
    :param url_component:
    :return:
    """
    conn = http.client.HTTPConnection(url_component['host'])
    conn.request('GET', url)
    response = conn.getresponse()
    body = response.read();
    conn.close()
    return body


def file_process(url, url_component):
    """
    处理可下载文件
    :param body:
    :param url_component:
    :return:
    """
    if url_component['path'] != '':
        path = './pages/' + url_component['path']
    else:
        path = './pages/' + url_component['query']
    if os.path.exists(path):
        return
    body = get_body(url, url_component)
    save_file(body, path)
    return


def html_process(url, url_component):
    """
    处理html文件
    :param body:
    :param url_component:
    :return:
    """
    body = get_body(url, url_component)
    path = './pages/' + url_component['query']
    save_file(body, path)
    content = parse_body(body)
    if content == '':
        return
    imgs_process(content)
    scripts_process(content)
    icons_process(content)
    styles_process(content)
    onlinereads_process(content)
    downloads_process(content)
    links_process(content)


def imgs_process(content):
    """
    处理图片
    :param content:
    :return:
    """
    imgs = get_imgs(content)
    if imgs:
        for img in imgs:
            img_url = generate_url(img)
            process(img_url)


def get_imgs(content):
    """
    获取所有图片路径列表
    :param content:
    :return:
    """
    img_pattern = re.compile('<img.*?src="?([^"\s]*)', re.IGNORECASE)
    imgs = img_pattern.findall(content)
    return imgs


def scripts_process(content):
    """
    处理脚本
    :param content:
    :return:
    """
    scripts = get_scripts(content)
    if scripts:
        for script in scripts:
            script_url = generate_url(script)
            process(script_url)


def get_scripts(content):
    """
    获取所有脚本列表
    :param content:
    :return:
    """
    script_pattern = re.compile('<script.*?src="?([^"\s]*)"?', re.IGNORECASE)
    scripts = script_pattern.findall(content)
    return scripts


def icons_process(content):
    """
    处理网站图标
    :param content:
    :return:
    """
    icons = get_icons(content)
    if icons:
        for icon in icons:
            icon_url = generate_url(icon)
            process(icon_url)


def get_icons(content):
    """
    获取网站图标列表
    :param content:
    :return:
    """
    icon_element_pattern = re.compile('(<link.*?rel="?.*?shortcut.*?"?.*?>)', re.IGNORECASE)
    icon_elements = icon_element_pattern.findall(content)
    icon_pattern = re.compile('href="?([^"\s]*)', re.IGNORECASE)
    icons = []
    if icon_elements:
        for icon_element in icon_elements:
            icon_match = icon_pattern.findall(icon_element)
            if icon_match:
                icons.append(icon_match[0])
    return icons


def styles_process(content):
    """
    处理样式表
    :param content:
    :return:
    """
    styles = get_styles(content)
    if styles:
        for style in styles:
            style_url = generate_url(style)
            process(style_url)


def get_styles(content):
    """
    获取样式表列表
    :param content:
    :return:
    """
    style_element_pattern = re.compile('(<link.*?rel="?.*?stylesheet.*?"?.*?>)', re.IGNORECASE)
    style_elements = style_element_pattern.findall(content)
    style_pattern = re.compile('href="?([^"\s]*)', re.IGNORECASE)
    styles = []
    if style_elements:
        for style_element in style_elements:
            style_match = style_pattern.findall(style_element)
            if style_match:
                styles.append(style_match[0])
    return styles


def onlinereads_process(content):
    """
    处理在线阅读
    :param content:
    :return:
    """
    onlinereads = get_onlinereads(content)
    if onlinereads:
        for onlineread in onlinereads:
            onlineread_url = 'http://haodoo.net/?M=u&P=' + onlineread[0] + ':0&L=' + onlineread[1]
            process(onlineread_url, 'readonline')


def get_onlinereads(content):
    """
    获取在线阅读列表
    :param content:
    :return:
    """
    onlinereads = []
    onlineread_element_pattern = re.compile('''(readonline\(['"][^'"\s]*['"].*?['"][^'"\s]*['"]\))''', re.I)
    onlineread_elements = onlineread_element_pattern.findall(content)
    if onlineread_elements:
        for onlineread_element in onlineread_elements:
            onlineread_pattern = re.compile('''['"]([^'"\s]*)['"]''')
            onlineread = onlineread_pattern.findall(onlineread_element)
            if onlineread:
                onlinereads.append(onlineread)
    return onlinereads


def downloads_process(content):
    """
    处理下载文件
    :param content:
    :return:
    """
    book_path = './books'

    download_link_pattern = re.compile('''(onClick\W*=\W*['"]Download)''', re.IGNORECASE)
    download_link_match = download_link_pattern.search(content)
    if not download_link_match:
        return

    include_files_pattern = re.compile(
        '\<\!--------------------- START INCLUDE FILES ---------------------\>(.*?)\<\!-- SiteSearch Google --\>',
        re.DOTALL)
    include_files_match = include_files_pattern.findall(content)
    if not include_files_match:
        return
    include_file_string = include_files_match[0]

    category_pattern = re.compile('''((\&lt;)|<)a\W*href="\?M=hd.*?"((\&gt;)|>)(?P<category>.*?)((\&lt;)|<)''', re.I)
    category_match = category_pattern.search(include_file_string)
    if category_match and category_match.groups('category'):
        category = re.sub(' .*', '', category_match.group('category'))

    book_path += '/' + category

    title_pattern = re.compile('SetTitle\("(.*?)"\)', re.I)
    title_match = title_pattern.findall(include_file_string)
    title = title_match[0]
    book_path += '/' + title
    file_list = re.split('<font color="CC0000">', include_file_string, flags=re.DOTALL)
    for i in range(1, len(file_list)):
        file_string = file_list[i]
        fileTitlePattern = re.compile('^.*?</font>(.*?)<input', re.I)
        file_title_match = fileTitlePattern.findall(file_string)
        file_title = file_title_match[0]
        if len(file_list) > 1:
            file_path = book_path + '/' + file_title
        else:
            file_path = book_path
        downloads_pattern = re.compile('"(Download.*?)"', re.IGNORECASE)
        downloads_match = downloads_pattern.findall(file_string)
        for download in downloads_match:
            download_info_pattern = re.compile('Download(.*?)\(\'(.*)\'\)', re.IGNORECASE)
            download_info_match = download_info_pattern.search(download)
            download_file_name = download_info_match.group(2) + '.' + download_info_match.group(1).lower()
            download_link = 'http://haodoo.net/?M=d&P=' + download_file_name
            download_file_path = file_path + '/' + download_file_name
            print(download_file_path)
            if os.path.exists(download_file_path):
                continue
            body = get_body(download_link, parse_url(download_link))
            save_file(body, download_file_path)
        continue
    return


def links_process(content):
    """
    处理链接
    :param content:
    :return:
    """
    links = get_links(content)
    if links:
        for link in links:
            link_url = generate_url(link)
            process(link_url)


def get_links(content):
    """
    获取链接列表
    :param content:
    :return:
    """
    link_pattern = re.compile('<a.*?href="?([^"\s]*)')
    links = link_pattern.findall(content)
    return links


def generate_url(url):
    """
    补足url
    :param url:
    :return:
    """
    url_pattern = re.compile('^https?://', re.IGNORECASE)
    url_match = url_pattern.search(url)
    if not url_match:
        root_pattern = re.compile('^/')
        root_match = root_pattern.search(url)
        path_limit = ''
        if not root_match:
            path_limit = '/'
        url = 'http://haodoo.net' + path_limit + url
    return url


def parse_body(body):
    """
    尝试解析body
    :param body:
    :return:
    """
    try:
        content = body.decode('utf-8')
    except UnicodeDecodeError:
        content = body.decode('big5')
    except RuntimeError:
        content = ''
    finally:
        return content


def save_file(body, path):
    """
    保存文件
    :param body:
    :param path:
    :return:
    """
    if os.path.exists(path):
        return
    try:
        body = body.decode('big5').encode('utf-8')
    except UnicodeDecodeError:
        pass
    finally:
        make_dir(path)
        file = open(path, 'wb')
        file.write(body)
        file.close()

def parse_url(url):
    """
    解析url，获取其中的「协议」、「主机名」、「路径」、「查询串」信息
    :param url: url
    :return: component: map {'protocal': protocal, 'host': host, 'path': path, 'query': query}
    """
    pattern = re.compile('^((?P<protocal>https?)://)?((?P<host>[^/]*)/?)?((?P<path>[^?^#]*)/?)?(?P<query>\?[^#]*)?')
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


def make_dir(path):
    """
    逐层创建文件夹
    :param path:
    :return:
    """
    path_parts = path.split('/')
    target_path = ''
    for i in range(0, len(path_parts) - 1):
        if path_parts[i] == '':
            continue
        target_path += path_parts[i] + '/'
        if not os.path.exists(target_path):
            os.mkdir(target_path)


make_dir('./one/two/three/four/')

links = []
url = 'http://haodoo.net/?M=hd&P=welcome'
process(url)
