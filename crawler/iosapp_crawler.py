# -*- coding: utf-8 -*-

import os
import sys
import urllib.request
import re
from time import sleep


def getAppName(html):  # 获取app名字
    # <h1 itemprop="name">QQ</h1>
    pat = '<h1 class="product-header__title">[\s\S]*<span class="badge badge--product-title">'
    string = str(re.compile(pat).findall(html))
    string = string.strip('\n').replace(' ', '').replace('\\n', '').replace('\xa0', ' ').replace('\\xa0', ' ')
    #print('string',string)
    name = ''
    if string != '[]':
        name = string.split('>')[1].split('<')[0]
    return name

def getApplogourl(html):  # 获取applogo url
    # <meta itemprop="image" content="http://is5.mzstatic.com/image/thumb/Purple128/v4/02/a6/41/02a64169-5f59-2895-2923-1a6db5fd730d/source/175x175bb.jpg"></meta>
    pat = '<section class="l-content-width section section--hero">[\s\S]*</picture>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    logourl = ''
    if string != '[]':
        logourl= string.split('img src="')[1].split('" style')[0]
    return logourl


def getcategoryleft(html):  # 获取分类结构的左半部分，暂时空缺
    # <span itemprop="applicationCategory">社交</span>
    pat='<a href="https://itunes.apple.com/cn/genre/id6005" class="link">[\s\S]*</a>'
    string=str(re.compile(pat).findall(html))
    #print('string',string)
    categoryleft = ''
    if string!='[]':
        categoryleft=string.split('>')[1].split('<')[0]
    return categoryleft


def getMinOsVersion(html):  # 获取app安装的最小os系统版本
    # <span itemprop="operatingSystem">需要 iOS 8.0 或更高版本。与 iPhone、iPad 和 iPod touch 兼容。</span></p>
    # app-requirements。。。
    pat = '兼容性</dt>[\s\S]*</div>'
    string = str(re.compile(pat).findall(html))
    string=string.strip('\n').replace(' ', '').replace('\\n', '').replace('\xa0',' ').replace('\\xa0',' ')
    #move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
    #string = string.translate(move)
    #string=''.join(string.split())
    #print('string',string)
    MinOsVersion = ''
    if string != '[]':
        MinOsVersion = string.split('需要')[1].split('或')[0]
        #MinOsVersion=MinOsVersion.replace('\xa0',' ')
    return MinOsVersion


def getMinOsVersiontext(html):  # 获取app安装的最小os系统版本的文本描述，同上
    pat = '兼容性</dt>[\s\S]*</div>'
    string = str(re.compile(pat).findall(html))
    string = string.strip('\n').replace(' ', '').replace('\\n', '').replace('\xa0', ' ').replace('\\xa0', ' ')
    # print('string',string)
    MinOsVersiontext = ''
    if string != '[]':
        MinOsVersiontext = string.split('class="ember-view">')[1].split('</div>')[0]
    return MinOsVersiontext


def getappurl(html):  # 获取app在应用商店的url，即本链接
    return html


def getappweb1(html):  # 获取app官网
    # <div class="app-links"><a rel="nofollow" target="_blank" href="https://support.qq.com/discuss/637_1.shtml" class="see-all">QQ 支持</a></div>
    pat = '<ul class="link-list link-list--small-bordered link-list--small-bordered-flush-end">[\s\S]*class="targeted-link link icon icon-after icon-external">'
    string = str(re.compile(pat).findall(html))
    string = string.split('<div more-text="更多"')[0]
    # print('string',string)
    appweb1 = ''
    if string != '[]':
        if string.find('网站') != -1:
            appweb1 = string.split('href="')[1].split('" class="see-all"')[0]
        else:
            appweb1 = string.split('href="')[1].split('" class="')[0]
    return appweb1


def getappweb2(html):  # 获取app支持网站
    # <div class="app-links"><a rel="nofollow" target="_blank" href="https://support.qq.com/discuss/637_1.shtml" class="see-all">QQ 支持</a></div>
    pat = '<ul class="link-list link-list--small-bordered link-list--small-bordered-flush-end">[\s\S]*class="targeted-link link icon icon-after icon-external">'
    string = str(re.compile(pat).findall(html))
    string = string.split('<div more-text="更多"')[0]
    # print('string',string)
    appweb2 = ''
    if string != '[]':
        if string.find('网站') != -1:
            appweb2 = string.split('网站')[1].split('href="')[1].split('" class="')[0]
        else:
            appweb2 = string.split('href="')[1].split('" class="')[0]
    return appweb2


def getInAppPurchasestext(html):  # 获取app内购项目
    # <div metrics-loc="Titledbox_热门 App 内购买项目"
    # <ol class="list">...
    pat = 'App 内购买项目</dt>[\s\S]*</button>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    result = ''
    InAppPurchasestext=''
    if string != '[]':
        #result = string.split('class="list-with-numbers__item__title">')[1].split('</span>')[0]
        #tempres=result.split('class="list-with-numbers__item__price small-hide medium-show-tablecell">')
        tempres = string.split('</li>')
        for ind in range(0,len(tempres)-1):
            tpres=tempres[ind]
            #print(tpres)
            iapitem=''
            iapprice=''
            iapitem=tpres.split('<span class="list-with-numbers__item__title">')[1].split('</span>')[0]
            iapprice=tpres.split('<span class="list-with-numbers__item__price small-hide medium-show-tablecell">')[1].split('</span>')[0]
            InAppPurchasestext=InAppPurchasestext+iapitem+"::"+iapprice+";"
    #print(InAppPurchasestext)
    return InAppPurchasestext


def getDeveloperName(html):  # 获取app开发者名字
    # <h2>开发者：Tencent Technology (Shenzhen) Company Limited</h2>
    pat = '<dd class="information-list__item__definition l-column medium-9 large-10">[\s\S]*</dd>'
    string = str(re.compile(pat).findall(html))
    string = string.strip('\n').replace(' ', '').replace('\\n', '').replace('\xa0', ' ').replace('\\xa0', ' ')
    # print('string',string)
    developerName = ''
    if string != '[]':
        developerName = string.split('>')[1].split('<')[0]
    return developerName


def getdeveloperid(html):  # 开发者唯一id，应从数据库重查询该developerid，暂时空缺
    # sql
    # print('string',string)
    developerid = ''
    return developerid


def getDeveloperStoreUrl(html):  # 获取app开发者在store内的url
    # <a href="https://itunes.apple.com/cn/developer/tencent-technology-shenzhen-company-limited/id292374531" class="view-more">查看此开发商提供的更多 App</a>
    # <div class="right">....
    pat = '<li class="t-subbody inline-list__item">[\s\S]*<li class="t-subbody inline-list__item inline-list__item--spaced">'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    DeveloperStoreUrl = ''
    if string != '[]':
        DeveloperStoreUrl = string.split('href="')[1].split('" class=')[0]
    return DeveloperStoreUrl


'''
href="https://itunes.apple.com/WebObjects/MZStore.woa/wa/appRatings?ratingSystem=appsApple">因含有以下内容而被评级为 12+：</a><ul class="list app-rating-reasons"><li>偶尔/轻微的成人/性暗示题材</li><li>偶尔/轻微的色情内容或裸露</li></ul></div><p><span class="app-requirements">兼容性
'''
def getcontentrating(html):  # 获取app的内容评级
    pat = '<span class="badge badge--product-title">[\s\S]*</span>'
    string = str(re.compile(pat).findall(html))
    #print('string',string)  #调试语句
    contentrating = ''
    if string != '[]':
        contentrating = string.split('>')[1].split('<')[0]
    return contentrating


def getcontentratingreason(html):  # 获取app内容评级的原因，同上
    # <ul class="list app-rating-reasons"><li>偶尔/轻微的成人/性暗示题材</li><li>偶尔/轻微的色情内容或裸露</li></ul></div><p><span class="app-requirements">兼容性：
    pat = '年龄分级</dt>[\s\S]*Copyright</dt>'
    string = str(re.compile(pat).findall(html))
    #print('string',string)
    contentratingreason = ''
    if string != '[]':
        ss = string.split('<dd class="information-list__item__definition l-column medium-9 ')
        #print(ss)
        for ind in range(2,len(ss)):
            temp=ss[ind].split('large-10">')[1].split('</dd>')[0]
            contentratingreason=contentratingreason+temp+';'
    return contentratingreason


def getinstallationsize(html):  # 获取app安装包size
    # <span class="label">大小： </span>244 MB</li><li class="language">
    pat = '<dd aria-label="259.3 MB" class="information-list__item__definition l-column medium-9 large-10">[\s\S]*</dd>'
    string = str(re.compile(pat).findall(html))
    temp = ''
    installationsize = 0
    if string != '[]':
        temp = string.split('large-10">')[1].split('B')[0]
        if temp[-1] == 'M':
            installationsize = temp.split('M')[0]
        elif temp[-1] == 'G':
            temp2 = temp.split('G')[0]
            installationsize = float(temp2) * 1000
    return installationsize


def getapplanguage(html):  # 获取app支持语言
    # <li class="language"><span class="label">语言: </span>简体中文</li><li><span class="label">开发商: </span>
    pat = '语言</dt>[\s\S]*</div>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    applanguage = ''
    if string != '[]':
        applanguage = string.split('class="ember-view">')[1].split('</div>')[0]
        applanguage = applanguage.strip('\n').replace(' ', '').replace('\\n', '').replace('<br>','').replace('<br/>','')
    return applanguage


def getDescriptiontext(html):  # 获取app描述文本
    # <div class="center-stack">
    pat = '>简介[\s\S]*</div>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    Descriptiontext = ''
    if string != '[]':
        Descriptiontext = string.split('class="ember-view">')[1].split('</div>')[0]
        Descriptiontext=Descriptiontext.strip('\n').replace(' ', '').replace('\\n', '').replace('<br>','').replace('<br/>','')
        #print('des: ',Descriptiontext)
    return Descriptiontext


def getrecentchangestext(html):  # 获取app更新文本
    # <div more-text="更多" metrics-loc="Titledbox_版本 7.2.0 中的新功能" class="product-review">
    pat = '<ul class="version-history__items">[\s\S]*</div>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    recentchangestext = ''
    if string != '[]':
        recentchangestext = string.split('class="ember-view">')[1].split('</div>')[0]
        recentchangestext=recentchangestext.strip('\n').replace(' ', '').replace('\\n', '').replace('<br>', '').replace('<br/>', '')
        #print('rec: ',recentchangestext)
    return recentchangestext


def getcomments(html):  # 获取评论，每个app只有三条，未处理
    pat = '<div class="we-modal__content__wrapper">[\s\S]*<section class="l-content-width section section--bordered">'
    string = str(re.compile(pat).findall(html))
    comments = string
    #if string != '[]':
        #comments = string.split('<h4>用户评论</h4>')[1].split('<div metrics-loc')[0]
    return comments

def dealcomments(comment):
    comms=comment.split('<div class="we-modal__content__wrapper">')
    result=[]
    for i in range(2,len(comms)):
        title=comms[i].split('class="we-customer-review__title we-truncate we-truncate--single-line ember-view">  ')[1].split('</h3>')[0]
        #print(comms[i])
        title=title.strip('\n').replace(' ','').replace('\\n','')
        rating=comms[i].split('<figure aria-label="')[1].split('（')[0]
        user=comms[i].split('class="we-customer-review__user we-truncate we-truncate--single-line ember-view">  ')[1].split('</div>')[0]
        user=user.strip('\n').replace(' ','').replace('\\n','')
        content=comms[i].split('class="we-customer-review__user we-truncate we-truncate--single-line ember-view">')[1].split('</div>')[2].split('</div>')[0]
        content=content.strip('\n').replace(' ','').replace('\\n','')
        data=(title,rating,user,content)
        #print('data: ',data)
        #print('data2: ',data[2])
        result.append(data)
    return result

def getotherapps(html):  # otherapp字段
    # <ul role="presentation" class="list"><li><a href="https://itunes.apple.com/cn/app/%E5%BE%AE%E5%8D%9A/id350962117?mt=8" class="name"><span>
    pat = ' 更多来自此开发人员的 App[\s\S]*<section class="l-content-width section">'
    string = str(re.compile(pat).findall(html))
    #print('string',string)
    otherapps = ''
    if string != '[]':
        ss = string.split('</a>')
        for ind in range(1,len(ss)-1):
            tpapp=ss[ind].split('single-line">')[1].split('</h3>')[0]
            #print(tpapp)
            otherapps=otherapps+tpapp+";"
        #print(otherapps)
    return otherapps


def getNumdownloads(html):  # 下载次数，appstore无此数据
    '''
    pat='<i itemprop="interactionCount"[\s\S]*</i>'
    string=str(re.compile(pat).findall(html))
    Numdownloads=''
    if string!='[]':
        Numdownloads=string.split('>')[1].split('<')[0]
        '''
    Numdownloads = ''
    return Numdownloads


def getstarratingall(html):  # 所有版本评分
    # <div>所有版本:</div>
    pat = '<li class="inline-list__item">[\s\S]*（满分 5 分）'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    starratingall = 0
    temp=''
    if string != '[]':
        temp = string.split('figure aria-label="')[1].split('（')[0]
        starratingall=float(temp)
    return starratingall


def getratingcountall(html):  # 所有版本评分份数
    # <div>所有版本:</div>
    pat = '<h4 class="we-customer-ratings__count t-subbody small-hide medium-show">[\s\S]*</h4>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    ratingcountall = 0
    temp=''
    temp0=-1
    if string != '[]':
        temp = string.split('">')[1].split(' 个评分')[0]
        #print(temp)
        #print(temp[-1])
        if temp[-1] == 'K':
            temp = float(temp.split('K')[0])*1000
            temp0 = int(temp)
        else:
            temp0 =int(temp)
        #ratingcountall=int(temp)
        ratingcountall = temp0
    return ratingcountall


def getstarratingcurrent(html):  # 当前版本评分
    # <div>当前版本:</div>
    pat = '<div>当前版本:</div>[\s\S]*份评分</span>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    starratingcurrent = 0
    temp=''
    if string != '[]':
        temp = string.split('aria-label=')[1].split('星,')[0].split("'")[1]
        starratingcurrent=float(temp)
    return starratingcurrent


def getratingcountcurrent(html):  # 当前版本评分份数
    # <div>当前版本:</div>
    pat = '<div>当前版本:</div>[\s\S]*份评分</span>'
    string = str(re.compile(pat).findall(html))
    # print('string',string)
    ratingcountcurrent = 0
    temp=''
    if string != '[]':
        temp = string.split('星,')[1].split('份评分')[0]
        ratingcountcurrent=int(temp)
    return ratingcountcurrent


def getVersionname(html):  # 版本名字
    # <span itemprop="softwareVersion">7.2.0</span></li><li><span class="label">
    pat = ' <p class="l-column small-6 medium-12 whats-new__latest__version">[\s\S]*</p>'
    string = str(re.compile(pat).findall(html))
    Versionname = ''
    if string != '[]':
        Versionname = string.split('>')[1].split('<')[0]
    return Versionname


def getuploaddate(html):  # app更新时间
    # <span itemprop="datePublished" content="2011-06-23 03:33:55 Etc/GMT">2017年09月19日</span></li><li><span class="label">版本
    pat = '<ul class="version-history__items">[\s\S]*</time>'
    string = str(re.compile(pat).findall(html))
    uploaddate = ''
    if string != '[]':
        #uyear = string.split('年')[0].split('>')[-1]
        #umonth = string.split('月')[0].split('年')[-1]
        #uday = string.split('日')[0].split('月')[-1]
        #uploaddate = uyear + umonth + uday
        uploaddate = string.split('class="version-history__item__release-date">')[1].split('</time>')[0]
    return uploaddate


def getCopyrighttext(html):  # 版权声明
    # <li class="copyright">Copyright © 2009 - 2017 Tencent Inc. All Rights Reserved</li></ul><div class="app-rating">
    pat = 'Copyright</dt>[\s\S]*</div>'
    string = str(re.compile(pat).findall(html))
    Copyrighttext = ''
    if string != '[]':
        Copyrighttext = string.split('">')[1].split('</dd>')[0]
    return Copyrighttext


def getAppstoreid(html):  # 获取app在应用商店内的id，appurl的id部分
    string = html
    # print('string',string)
    Appstoreid = ''
    if string != '[]':
        Appstoreid = string.split('?mt')[0].split('id')[-1]
    return Appstoreid

'''
get all categaries link
ios: 25 个 主分类
'''
def getallcategaries(url):
    #url = 'https://itunes.apple.com/cn/genre/ios-%E5%9B%BE%E4%B9%A6/id6018?mt=8'
    print(url)
    html1 = str(urllib.request.urlopen(url).read().decode('utf-8'))
    # <div id="selectedcontent" class="grid3-column">
    pat2 = '<div id="genre-nav" class="nav">[\s\S]* <div class="upsell-placard">'
    temp = str(re.compile(pat2).findall(html1))
    # print(temp)
    # allLink=str(re.compile(pat2).findall(html1)).strip('\n').replace(' ','').replace('\\n','').replace('\\t','')
    allLink = temp.split('<li><a href="')
    # print(allLink)
    allLinks = []
    for i in range(1, len(allLink)):
        allLinks.append(allLink[i].split('" class=')[0])
    allLinks = list(set(allLinks))
    allLinks.sort()
    for i in allLinks:
        print(i)
    print(len(allLinks))
    return allLinks


'''
主分类入库
'''
def dealallcategaries(allcats,cur,db):
    ind=0
    for cat in allcats:
        #insert into crawlcats(caturl,add_date) values('testurl',now())
        ind=ind+1
        print("cat "+str(ind)+" : "+cat)
        try:
            insertsql = "insert into crawlcats(caturl,add_date) values('%s',now())"
            data = (cat)
            cur.execute(insertsql % data)
            db.commit()  # 不执行不能插入数据
            print('cat成功')
        except Exception as e:
            # print(str(e))
            print('cat失败')
            # db.rollback()
    return


'''
def getallapp(url): 由一个分类的url，获得该分类下的appurl
'''
def getallapp(url):
    # url = 'https://itunes.apple.com/cn/genre/ios-%E5%9B%BE%E4%B9%A6/id6018?mt=8'
    # print(url)
    html1 = str(urllib.request.urlopen(url).read().decode('utf-8'))
    # <div id="selectedcontent" class="grid3-column">
    pat2 = '<div id="selectedcontent"[\s\S]*<div id="genre-nav" class="nav">'
    temp = str(re.compile(pat2).findall(html1))
    # print(temp)
    # allLink=str(re.compile(pat2).findall(html1)).strip('\n').replace(' ','').replace('\\n','').replace('\\t','')
    allLink = temp.split('<li><a href="')
    # print(allLink)
    allLinks = []
    for i in range(1, len(allLink)):
        allLinks.append(allLink[i].split('">')[0])
    allLinks = list(set(allLinks))
    # print(allLinks[10])
    return allLinks

'''
allapps url入库
'''
def dealallappurls(allapp,cur,db):
    for app in allapp:
        # insert into crawlcats(caturl,add_date) values('testurl',now())
        try:
            insertsql = "insert into crawlapps(appurl,add_date) values('%s',now())"
            data = (app)
            cur.execute(insertsql % data)
            db.commit()  # 不执行不能插入数据
            #print('appurl成功')
        except Exception as e:
            # print(str(e))
            print('appurl失败')
            # db.rollback()
    return


def getAllInfo(url):  # 由appurl获取app所有信息
    print('当前url：', url)
    html1 = str(urllib.request.urlopen(url).read().decode('utf-8'))
    name = getAppName(html1)
    print('名称:', name)
    if name == '':
        return

    appid = ''
    print('appid：', appid)

    categoryleft = str(getcategoryleft(html1))
    print('categoryleft：', categoryleft)

    Versionname = str(getVersionname(html1))
    print('版本名称:', Versionname)

    packagename = ''
    print('packagename:', packagename)

    appstorename = 'appstore'
    print('appstorename:', appstorename)

    MinOsVersion = str(getMinOsVersion(html1))
    print('MinOsVersion：', MinOsVersion)

    MinOsVersiontext = str(getMinOsVersiontext(html1))
    print('MinOsVersiontext：', MinOsVersiontext)

    appurl = str(getappurl(url))
    print('appurl：', appurl)

    appweb1 = str(getappweb1(html1))
    print('app官网:', appweb1)

    appweb2 = str(getappweb2(html1))
    print('app支持:', appweb2)

    pernum = ''
    print('权限数:', pernum)

    pertext = ''
    print('权限文本:', pertext)

    Specdescribe = ''
    print('特殊描述:', Specdescribe)

    Descriptiontext = str(getDescriptiontext(html1))
    # print('描述文本：',Descriptiontext)

    Screenpic = ''
    print('Screenpic:', Screenpic)

    currencytype = 'RMB'
    print('currencytype:', currencytype)

    appprice = 'FREE'
    print('appprice:', appprice)

    InAppPurchasestext = str(getInAppPurchasestext(html1))
    print('InAppPurchasestext：', InAppPurchasestext)

    HaveInAppPurchases = 'N'
    if InAppPurchasestext != '':
        HaveInAppPurchases = 'Y'
    print('HaveInAppPurchases:', HaveInAppPurchases)

    developerName = str(getDeveloperName(html1))
    print('开发者名字：', developerName)

    # developerid=str(getdeveloperid(html1))
    # print('开发者唯一id：',developerid)

    DeveloperStoreUrl = str(getDeveloperStoreUrl(html1))
    print('开发者storeurl：', DeveloperStoreUrl)

    contentrating = str(getcontentrating(html1))
    print('内容分级：', contentrating)

    contentratingreason = str(getcontentratingreason(html1))
    print('内容分级原因：', contentratingreason)

    installationsize = str(getinstallationsize(html1))
    print('安装包大小:', installationsize)

    applanguage = str(getapplanguage(html1))
    print('应用支持语言:', applanguage)

    Numdownloads = str(getNumdownloads(html1))
    print('下载次数:', Numdownloads)

    recentchangestext = str(getrecentchangestext(html1))
    # print('更新变化文本',recentchangestext)

    uploaddate = str(getuploaddate(html1))
    print('更新时间:', uploaddate)

    Copyrighttext = str(getCopyrighttext(html1))
    print('版权声明:', Copyrighttext)

    Appstoreid = str(getAppstoreid(url))
    print('应用商店内id：', Appstoreid)

    starratingall = str(getstarratingall(html1))
    print('所有版本评分:', starratingall)
    ratingcountall = str(getratingcountall(html1))
    print('所有版本评分份数:', ratingcountall)

    starratingcurrent = str(getstarratingcurrent(html1))
    print('当前版本评分:', starratingcurrent)
    ratingcountcurrent = str(getratingcountcurrent(html1))
    print('当前版本评分份数:', ratingcountcurrent)

    commentcount = ''
    print('评论数', commentcount)

    otherapps = str(getotherapps(html1))
    print('推荐相关应用:', otherapps)

    comments = str(getcomments(html1))
    #print('用户评论:',comments)

    mycomments=dealcomments(comments)
    #print('mycomments: ',mycomments)

testurl="https://itunes.apple.com/cn/app/qq/id444934666?mt=8"
getAllInfo(testurl)

'''
#def mainwork():
if __name__ == '__main__':
    #db = pymysql.connect(host="localhost", user="root", password="Wbp1994!test", db="appnet1", port=3306, charset='utf8')
    db = pymysql.connect(host="localhost", user="root", password="mwq199502", db="appnet5", port=3306, charset='utf8')
    cur = db.cursor()

    #完成basework,一次
    #basework(cur,db)

    mainwork(cur,db)

    print("Good Game!")

    cur.close()
    db.close()
'''
