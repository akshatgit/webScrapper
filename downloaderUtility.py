from databaseUtility import *
from utility import *
from lxml import html
from datetime import datetime
import wget
import requests
import re
from bs4 import BeautifulSoup
import bs4
import os

def downloadApkpure(db,table):
    #table = getTable(db,appDetails)
    for row in db[table]:
        try:
            appID = str(row["appID"])
            #Get just app ID from DB version of app ID
            appID_pos = appID.rfind("/")
            appID_trimmed = appID[appID_pos+1:]
            fileName = os.getcwd() + '\\APKs\\apkpure\\'+ appID_trimmed + '.apk'
            if os.path.exists(fileName):
                continue
            url1 = "https://apkpure.com" + appID + "/download?from=details"
            r1 = requests.get(url1)
            soup = BeautifulSoup(r1.text, 'html.parser')
            url2 = soup.find(id="download_link")["href"]
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded " + fileName)
        except Exception:
            fileName = os.getcwd() + '\\APKs\\apkpure\\'+ "errors.txt"
            errorMessage = "\n" + appID_trimmed + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID_trimmed+ " could not be downloaded")
            continue


def downloadApkplz(db,table):
    for row in db[table]:
        try:
            appID = str(row["appID"])
        #fetch just the appID
            appID_pos = appID.rfind("/")
            appID_trimmed = appID[appID_pos+1:]
            fileName = os.getcwd() + '\\APKs\\apkplz\\'+ appID_trimmed + '.apk'
            if os.path.exists(fileName):
                continue
            #Download URL 1
            url1 = "https://apkplz.net/download-app/" + appID_trimmed
            r1 = requests.get(url1)
            soup = BeautifulSoup(r1.text, 'lxml')
            #look for 'dllink' within all script tags, strip out the value of the variable using substrings
            download_url_untrimmed = re.search(r'dllink\s*=\s*(.*?);', str(soup.find_all('script')), flags=re.DOTALL).group(0)
            url2 = download_url_untrimmed.split("\"")[1]
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded " + fileName)
        except Exception:
            fileName = os.getcwd() + '\\APKs\\apkplz\\'+ "errors.txt"
            errorMessage = "\n" + appID_trimmed + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID_trimmed+ " could not be downloaded")
            continue


def downloadApktada(db,table):
    for row in db[table]:
        try:
            appID = str(row["appID"])
            #fetch just the appID
            appID_pos = appID.rfind("/")
            appID_trimmed = appID[appID_pos+1:]
            #Avoid re-download of duplicates
            fileName = os.getcwd() + '\\APKs\\apktada\\'+ appID_trimmed + '.apk'
            if os.path.exists(fileName):
                continue
            #Download URL 1
            url1 = "https://apktada.com/download-apk/" + appID_trimmed
            r1 = requests.get(url1)
            soup = BeautifulSoup(r1.text, 'lxml')
            #look for 'dllink' within all script tags, strip out the value of the variable using substrings
            download_url_untrimmed = re.search(r'dllink\s*=\s*(.*?);', str(soup.find_all('script')), flags=re.DOTALL).group(0)
            url2 = download_url_untrimmed.split("\"")[1]
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded " + fileName)
        except Exception:
            fileName = os.getcwd() + '\\APKs\\apktada\\'+ "errors.txt"
            errorMessage = "\n" + appID_trimmed + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID_trimmed+ " could not be downloaded")
            continue

def downloadApkfab(db,table):
    for row in db[table]:
        try:
            appID = str(row["appID"])
            #fetch just the appID
            appID_pos = appID.rfind("/")
            appID_trimmed = appID[appID_pos+1:]
            #Avoid re-download of duplicates
            fileName = os.getcwd() + '\\APKs\\apkfab\\'+ appID_trimmed + '.apk'
            if os.path.exists(fileName):
                continue
            #Download URL 1
            url1 = appID + "/download"
            r1 = requests.get(url1)
            soup = BeautifulSoup(r1.text, 'lxml')
            url2 = soup.find('iframe')["src"]
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded " + fileName)
        except Exception:
            fileName = os.getcwd() + '\\APKs\\apkfab\\'+ "errors.txt"
            errorMessage = "\n" + appID_trimmed + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID_trimmed+ " could not be downloaded")
            continue


def downloadApkgk(db,table):
    for row in db[table]:
        try:
            appID = str(row["appID"])
            appID_trimmed = appID[1:]
            #Avoid re-download of duplicates
            fileName = os.getcwd() + '\\APKs\\apkgk\\'+ appID_trimmed + '.apk'
            if os.path.exists(fileName):
                continue
            url1 = "https://apkgk.com/" + appID_trimmed + "/download"
            r = requests.get(url1)
            soup = BeautifulSoup(r.text,'lxml')
            url2 = "https:"+str(soup.find("a",class_="btn btn-cus btn-down")["href"])
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded "+fileName)
        except Exception as e:
            fileName = os.getcwd() + '\\APKs\\apkgk\\'+ "errors.txt"
            errorMessage = "\n" + appID_trimmed + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID_trimmed+ " could not be downloaded")
            continue


if __name__ == '__main__':
    path = os.getcwd() + '\\DB\\'
    db = databaseStartUp("sqlite:///" + path + "apkpure.db")
    downloadApkpure(db,"appDetails")

    db = databaseStartUp("sqlite:///" + path + "apkplz.db")
    downloadApkplz(db,"appDetails")

    db=databaseStartUp("sqlite:///" + path + "apktada.db")
    downloadApktada(db,"appDetails")

    db=databaseStartUp("sqlite:///" + path + "apkfab.db")
    downloadApkfab(db,"appDetails")

    db=databaseStartUp("sqlite:///" + path + "apkgk_database.db")
    downloadApkgk(db,"appDetails")