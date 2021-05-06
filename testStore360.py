import requests
import json
import wget
import time
import base64
from utility import *
from databaseUtility import *
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
import bs4
import os
import math
import xml.etree.ElementTree as ET
from databaseUtility import *
import pandas as pd

def get_query_terms():
    terms_list = []
    cn_list = {}
    with open('android_terms.csv','rt')as f:
        data = csv.reader(f)
        lineNumber = 0;
        for row in data:
                if lineNumber >= 1:
                    key = row[2];
                    terms = row[3];
                    i = 0;
                    for term in terms.split('"'):
                        if i%2 == 0:
                            i = i+1;
                            continue
                        else:
                            i = i+1;
                            terms_list.append(term)
                else:
                    lineNumber = lineNumber + 1;
    return terms_list


def testStore360(db):
    appDetailsTable = getTable(db, 'appDetailsChinese')
    appIdTable = getTable(db, 'AppId')
    for term in get_query_terms():
        print("Sending request to Store360")
        print(tr_cn(term).get("translatedText"))
        payload = {'kw':tr_cn(term).get("translatedText")}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get('http://zhushou.360.cn/search/index', params=payload, headers=headers)
        soup = BeautifulSoup(r.text,'html.parser')
        try:
            for number in soup.find_all('span'):
                if number.parent.name == 'h2' and number.contents[0].isnumeric() == True:
                    #print(number)
                    numberOfResults = number.contents[0]
            numberOfPages = math.ceil(int(numberOfResults)/15.0)
            #print(numberOfPages)
            for page in range(numberOfPages):
                payload = {'kw':tr_cn(term).get("translatedText"),'page':page}
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                r = requests.get('http://zhushou.360.cn/search/index', params=payload, headers=headers)
                soup = BeautifulSoup(r.text,'html.parser')
                for app in soup.find_all('a'):
                    if app.parent.name == 'h3':
                        detailsUrl = "http://zhushou.360.cn" + str(app["href"])
                        app_data = getDetailsfromUrl(detailsUrl)
                        print(app_data)
                        #cannot fetch APP ID from Store 360 site. Need to update it later during APK parsing.
                        insertIntoAppDetailsTableStore360(appDetailsTable, dict(term = term, translatedTerm = tr_cn(term).get("translatedText"), appName=app_data["App_name"], rating=app_data["rating"],downloadURL=app_data["downloadURL"],version=app_data["version"],authorName=app_data["authorName"],publishDate=app_data["publishDate"], websiteName='zhushou.360.cn'))
        except Exception as e:
            continue

def getDetailsfromUrl(detailsUrl):
    try:
        id_start_pos = detailsUrl.rfind("/")
        id_end_pos = detailsUrl.rfind("?")
        id = detailsUrl[id_start_pos+1:id_end_pos]
        r = requests.get(detailsUrl)
        soup = BeautifulSoup(r.text, 'html.parser')
        appName_end_pos = str(soup.find(id='app-name').contents[0]).rfind("</span")
        appName_start_pos = str(soup.find(id='app-name').contents[0]).rfind(">",0,appName_end_pos)
        appName = str(soup.find(id='app-name').contents[0])[appName_start_pos+1:appName_end_pos]
        for element in soup.find_all('span',class_ = "s-1 js-votepanel"):
            rating = element.contents[0]
        downloadUrl = "https://app.api.sj.360.cn/url/download/id/" + id + "/from/web_detail"
        baseInfo = soup.find_all("div",class_ = "base-info")
        soup = BeautifulSoup(str(baseInfo), 'html.parser')
        metadata = list()
        for element in soup.find_all('td'):
            metadata.append(element.contents[1])
        authorName = metadata[0]
        publishDate = metadata[1]
        version = metadata[2]
        osVersion = metadata[3]
        #print("Rating: " + rating + "\nAuthor Name: " + authorName + "\nPublish Date: " + publishDate + "\nVersion: " + version + "\nOS Version: " + osVersion + "\nDownload URL: " + downloadUrl)
        #insertIntoAppDetailsTable(appDetailsTable, dict(pkgName=appID,appID=appID, App_Name=title, appURL=downloadURL,desc=desc,file_size=fileSize,author_name=developerName,rating=averageRating,category=category,hash=apkHash, imageSource=imageLink, developerName=developerName, websiteName='android.myapp.com', createdAt=currentTime,version=version,other=str(item)))
        appDetails = {"App_name":appName, "rating":rating, "authorName":authorName, "publishDate" : publishDate, "version":version, "downloadURL":downloadUrl}
        return appDetails
    except Exception as e:
        appDetails = {"App_name":'', "rating":'', "authorName":'', "publishDate" : '', "version":'', "downloadURL":''}
        return appDetails

#getDetailsfromUrl("http://zhushou.360.cn/detail/index/soft_id/513870?recrefer=SE_D_%E9%97%B4%E8%B0%8D%E5%BA%94%E7%94%A8")
db = databaseStartUp("sqlite:///cn_database2.db")
testStore360(db)
    #In the test script, only pkgName is printed to test the number of results returned.
    #TODO: Add all appdetails to DB

        #savedetailsinDB
        #insertIntoAppDetailsTable(appDetailsTable, dict(pkgName=appID,appID=appID, App_Name=title, appURL=downloadURL,desc=desc,file_size=fileSize,author_name=developerName,rating=averageRating,category=category,hash=apkHash, imageSource=imageLink, developerName=developerName, websiteName='android.myapp.com', createdAt=currentTime,version=version,other=str(item)))