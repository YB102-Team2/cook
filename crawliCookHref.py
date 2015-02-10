# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup 
from sets import Set
import os
import time

#要爬的網站(改)
url='https://icook.tw/categories/55?page=%d'    

#存放資料夾(改)
foldname='cookhref3'

#存放id
idSet = Set()

#抓出最後一頁頁數
res = requests.get(url%1)
res.encoding='utf8'
soup = BeautifulSoup(res.text)
lastpage = int(soup.select('li[class*="last"] a')[0]['href'].split('=')[1])

#末頁
pageEnd = lastpage
print 'All page = %d'%pageEnd


#若之前沒有抓檔紀錄從抓,有則接續著抓
if os.path.exists(foldname)==False:
      print 'Create fold %s'%foldname
      os.mkdir(foldname)
      pageStart=1
else:
    #從之前未做完的開始做
    nfile=os.listdir(foldname)
    if (len(nfile)!=0):
        for name in nfile:
            if name!=nfile[len(nfile)-1]:
                fo =open(foldname+'\\'+name, "r")
                #print name
                for line in fo.readlines():
                    idSet.add(line.strip())
                fo.close

        pageStart = int(nfile[len(nfile)-1].split('.')[0])
        print 'last.txt is '+nfile[len(nfile)-1]+' All set length is %d'%len(idSet)
    else:
        pageStart=1

#讀取全部ID(改)
fo =open('allId2.txt', "r")                
for line in fo.readlines():
    idSet.add(line.strip())
fo.close
print 'All set lengths are %d'%len(idSet)

#開始抓取
for i in range(pageStart,pageEnd+1):
    #若斷線重複嘗試
    try:
        res = requests.get(url%i)
    except requests.exceptions.ConnectionError as e:
        print 'ConnectionError on page %d'%i

        while 1:
            #連回就離開繼續
            print "Sleeping Start : %s" % time.ctime()
            time.sleep(30)
            print "Sleeping End : %s" % time.ctime()
            try:
                res = requests.get(url%i)
                break
            except requests.exceptions.ConnectionError as e:
                print 'ConnectionError on page %d'%i
            
    res.encoding='utf8'
    soup = BeautifulSoup(res.text)
    card = soup.select('div[class*="media-"]')
    
    #若被轉址
    if(len(card)==0):
        while 1:
            #連回就離開繼續
            print "Sleeping Start : %s" % time.ctime()
            time.sleep(30)
            print "Sleeping End : %s" % time.ctime()
            res = requests.get(url%i)
            soup = BeautifulSoup(res.text)
            card = soup.select('div[class*="media-"]')
            if(len(card)!=0):
                break

    #已1-10頁為一個檔案,已第1頁為檔名,開檔
    if((i-1)%10==0):
        #n記錄到第幾頁關檔                              
        n=i+9
        filename = foldname+'\\%05d.txt'%i
        cid_file = open(filename, 'w')
        print 'Create %05d'%i
    
    #抓id號
    for cd in card:
        #抓出id號碼
        href = cd.select('a[href]')[0]
        ids = href['href'].split('/')[2]
         
        if(ids not in idSet):
            idSet.add(ids)
            cid_file.write(ids+"\n")

    print 'Writes page %d'%i
            
    if(i==n or i==pageEnd-1):                              #關檔
        cid_file.close
        print 'Close %05d'%(n-9)


allfile = open('alls.txt', 'a')
allfile.write('\nSet numbers = %d'%len(idSet))
allfile.close


fIdin = open('allId3.txt','w')
for ids in idSet:
    fIdin.write(ids+'\n')
fIdin.close

print len(idSet)