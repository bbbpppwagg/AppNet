import os
import sys
import socket
import urllib.request
import re
import pymysql
import time
import basetools.iosappus

timeout=20
socket.setdefaulttimeout(timeout)
sleep_time=1
maxTryNum=6

if __name__ == '__main__':
    #db = pymysql.connect(host="localhost", user="root", password="Wbp1994!test", db="appnet2", port=3306, charset='utf8')
    #db = pymysql.connect(host="118.89.140.156", user="root", password="Wbp1994!test", db="appnet1", port=3306,charset='utf8')
    #db = pymysql.connect(host="localhost", user="root", password="mwq199502", db="appnet5", port=3306, charset='utf8')
    #cur = db.cursor()

    #starturl = 'https://itunes.apple.com/us/genre/ios-books/id6018?mt=8'
    starturl='https://itunes.apple.com/us/genre/ios-business/id6000?mt=8'
    #starturl='https://itunes.apple.com/us/genre/ios/id36?mt=8'
    resp=basetools.iosappus.openlink(starturl)

    #完成basework,一次
    #basetools.iosappus.basework(starturl,cur,db)

    '''
    querysql="select * from crawlcats"
    cur.execute(querysql)
    results = cur.fetchall()
    print(results)
    '''

    print("Good Game!")

    #cur.close()
    #db.close()
