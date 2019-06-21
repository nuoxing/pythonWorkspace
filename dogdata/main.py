from  urllib import request
import urllib
from lxml import etree
import csv
import time
import data2db
import uuid

#根据url获取数据
def gethtml(url):
    time.sleep(1)
    req = request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    with request.urlopen(req) as f:
        print('Status:', f.status, f.reason)
        html = f.read().decode('utf-8')
        return html
    pass

#获取每种宠物的访问的url,返回list list中是一个字典map {"imgurl":"","doginfourl":""}
def getdogurlList(html):
    reslist = []
    html = etree.HTML(html)
    resdivs = html.xpath('//div[@class="pet_list"]/div')
    for div in resdivs:
        resmap = {}
        doginfourl = div.xpath("./a/@href")[0]
        imgurl = div.xpath('./a/img/@src')[0]
        resmap['doginfourl'] = doginfourl
        resmap['imgurl'] = imgurl
        reslist.append(resmap)
    return reslist
    pass

#基本信息,返回map
def getdogdetailinfo(html):
    html = etree.HTML(html)
    #获取小狗的名称
    #dogname = html.xpath('//div[@class="spec-r"]//h1/a')[0].text
    #print("dogname",dogname)
    #获取小狗的简介
    dogintroducelist = html.xpath('//div[@class="spec-r"]/div[@class="smain"]/p//text()')
    dogintroducestr = "".join(str(s) for s in dogintroducelist)
    print(dogintroducestr)
    #详细特征
    lilist = html.xpath('//ul[@class="sinfolist sinfo1"]/li')

    name = lilist[0].xpath("./span")[0].text
    life = lilist[0].xpath("./span")[1].text
    hair = lilist[0].xpath("./span")[2].text
    alias = lilist[1].xpath("./span")[0].text
    height = lilist[1].xpath("./span")[1].text
    oripro = lilist[1].xpath("./span")[2].text
    price = lilist[2].xpath("./span")[0].text
    fun = lilist[2].xpath("./span")[1].text
    shape = lilist[2].xpath("./span")[2].text
    print(name,life,hair,alias,height,oripro,price,fun,shape)

    reslist = []
    reslist.append(name)
    reslist.append(life)
    reslist.append(hair)
    reslist.append(alias)
    reslist.append(height)
    reslist.append(oripro)
    reslist.append(price)
    reslist.append(fun)
    reslist.append(shape)
    return reslist


#获取形态特征
def getfeatureInfo(html):
    reslist = []
    html = etree.HTML(html)
    divs = html.xpath('//div[@class="spec-r"]//div[@class="sxp"]')
    for div in divs:
        divstr = (etree.tostring(div,encoding="utf-8", pretty_print=True, method="html"))
       # divstr = div.text
        divstr = divstr.decode("utf-8")
        reslist.append(divstr)
    return reslist
    pass

#下载图片
def downloadImg(url):
    filename  = url.split('/')[-1]
    print('filename=',filename)
    path = 'E:/ipetproject/image/'+filename
   # urllib.request.urlretrieve(url,path)
    return path

def main():
    url = "http://www.ichong123.com/gougou"
    html_ = gethtml(url)
   # print(html_)
    reslist = getdogurlList(html_)
    print(len(reslist))
    for tempmap in reslist:
        #下载图片
        path = downloadImg(tempmap['imgurl'])
        dogdetailinfohtml = gethtml(tempmap["doginfourl"])
        #
        infolist_ = getfeatureInfo(dogdetailinfohtml)
        infolist = getdogdetailinfo(dogdetailinfohtml)
        infolist.append(path)
        infolist.extend(infolist_)

        #datatocsv(infolist)
        datatomysqldb(infolist)
        #return
    pass

def datatocsv(reslist):
    try:
        with open('E:/items.csv', 'a+', encoding='utf-8', newline='') as f:  # 设置newline，否则两行之间会空一行
            csvwriter = csv.writer(f)
            csvwriter.writerow(reslist)
    except Exception as e:
        print(e.__cause__)
        pass

def datatomysqldb(res):
   # for res in reslist:
        id = uuid.uuid1()
        sql = "insert into tb_pet_detailed_info" \
              "(id,varietyname,life,hair,aliias,height,placeorigin,price,fun,shape,picpath,feature,temperament,feedpoint,environment,createtime,updatetime) " \
              "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',NOW(),NOW())" % (id,res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8],res[9],res[10],res[11],res[12],res[13])
        print("sql=",sql)
        dbhandler = data2db.DbHandler()
        dbhandler.insert(sql)
        pass





main()

