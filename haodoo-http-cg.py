#!/usr/bin/env python3
import http.client
import re
import os


def main():
    homepage()


def homepage():
    body = get_body(homepage_url)
    content = parse_body(body)

    return


def get_body(url):
    """
    获取内容
    :param url:
    :return:
    """
    url_component = parse_url(url)
    conn = http.client.HTTPConnection(url_component['host'])
    conn.request('GET', url)
    response = conn.getresponse()
    body = response.read();
    conn.close()
    return body


def parse_body(body):
    """
    尝试解析body
    :param body:
    :return:
    """
    content = ''
    try:
        content = body.decode('utf-8')
    except UnicodeDecodeError:
        content = body.decode('big5')
    except RuntimeError:
        content = ''
    finally:
        return content


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


homepage_url = 'http://haodoo.net/?M=hd&P=welcome'
category_list = []
column_list = []
page_list = []
link_list = []

main()