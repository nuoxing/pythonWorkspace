import requests
import re

def test1():
    url = "http://www.baidu.com"
    response = requests.get(url,timeout=1)#返回的是一个response对象
    response.raise_for_status()
    s = response.text
    print(type(response))
    print(s)
    print(response.encoding)
    print(response.status_code)
    print(response.apparent_encoding)

def test2():
    requests.post()

test1()
