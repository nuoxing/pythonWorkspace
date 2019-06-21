import io
import sys
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

fp = urllib.request.urlopen('http://www.baidu.com')
print(fp.geturl())
mybytes = fp.read()
# note that Python3 does not read the html code as string
# but as html code bytearray, convert to string with
mystr = mybytes.decode("utf-8")

fp.close()

print(mystr)
f = open("F:/baidu.txt","w",encoding='utf-8');
f.write(mystr)
f.close()