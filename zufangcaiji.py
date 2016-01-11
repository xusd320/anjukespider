# encoding: UTF-8
import urllib2
import re
import sqlite3
import time

   
#抓取html源码
def gethtml(url):
    page = urllib2.urlopen(url,timeout=120)
    html0 = page.read()
    html = html0.decode('utf8')
    return html


#正则匹配房源信息
def getdata(text1):    
    pattern1 = re.compile(u'<p class="tag">([1-3].)(\d.)<span>\|</span>.*<span>\|</span>.*<span>\|</span>(\d+\/\d+.)</p>\s*<address>\s*<a target="_blank"\s*href=".*">\s*(\S*)\s*</a>\s*［(.{2})-(\S*)\s.*］\s*</address>\s*<p class="bot-tag">\s*<span>.*</span><em></em>\s*</p>\s*</div>\s*<div class="zu-side">\s*<p><strong>(\d*)</strong>')
    housetuple = pattern1.findall(text1)
    return housetuple


#正则匹配判断尾页
def endpage(text2):
    pattern2 = re.compile(u'<i class="iNxt">')
    return pattern2.search(text2)


#读取板块数据
conn1 = sqlite3.connect('bankuaidata.db')
cursor=conn1.cursor()
cursor.execute("SELECT BANKUAI FROM BANKUAIDATA")


#创建存储数据库存储数据
conn2 = sqlite3.connect('housedata' + str(time.strftime("%Y%m%d%H%M%S")) + '.db')
conn2.execute('''CREATE TABLE HOUSEDATA
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                QUYU     TEXT,
                BANKUAI  TEXT,
                XIAOQU   TEXT,
                FANGXING TEXT,
                TING     TEXT,
                LOUCENG  TEXT,
                ZUJIN    INT);''')

s=0
for item in cursor.fetchall():
    for bk in item:
        for i in range(1,100):
            url='http://sh.zu.anjuke.com/fangyuan/' + str(bk)+ '/p' + str(i)
            html = gethtml(url)
            housedata = getdata(html)
            for house in housedata:
                conn2.execute("INSERT INTO HOUSEDATA (QUYU,BANKUAI,XIAOQU,FANGXING,TING,LOUCENG,ZUJIN) VALUES ('%s','%s','%s','%s','%s','%s','%d')" %(house[4],house[5],house[3],house[0],house[1],house[2],int(house[6])))
                conn2.commit()
                s=s+1
                print '已采集' + str(s) + '条房源'
            isendpage = endpage(html)
            if isendpage != None:
                break
       
conn2.close()

conn1.close()


