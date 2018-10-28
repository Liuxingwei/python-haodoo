import http.client
import re

def main(url, file_name):
    conn = http.client.HTTPConnection('haodoo.net')
    conn.request('GET', url)
    response = conn.getresponse()
    content = response.read()
    try:
        content = content.decode('big5').encode('utf-8')
    except UnicodeDecodeError:
        pass
    finally:
        file = open(file_name, 'wb')
        file.write(content)
        # file.write(content)
        file.close()


# url = 'http://haodoo.net/?M=d&P=BV1342.epub'
# file_name = 'BV1342.epub'
#
# url = 'http://haodoo.net/?M=m&P=B241a:0'
# file_name = 'big5.html'

url = 'http://haodoo.net'
file_name = 'home.html'

a = []
a.append('abc')
a.append('abc')
a.append('xyz')
a.append('abc')
a.append('xyz')

main(url, file_name)