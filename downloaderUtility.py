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
import pandas as pd



def getTitleForAppID(dataframe, appID):
    df = dataframe.loc[dataframe['AppID'] == appID , 'Title']
    title = df.tolist()[0]
    for k in title.split("\n"):
        title = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    title = title.replace(' ','-').lower()
    return title

def downloadFromApkPlz(appID,outputDirectory):
    try:
        fileName = os.path.abspath(outputDirectory) + '/' + appID+ '.apk'
        if os.path.exists(fileName):
            print(appID + " is already downloaded at " + fileName)
            return True
        url1 = "https://apkplz.net/download-app/" + appID
        r1 = requests.get(url1)
        soup = BeautifulSoup(r1.text, 'lxml')
        #look for 'dllink' within all script tags, strip out the value of the variable using substrings
        download_url_untrimmed = re.search(r'dllink\s*=\s*(.*?);', str(soup.find_all('script')), flags=re.DOTALL).group(0)
        url2 = download_url_untrimmed.split("\"")[1]
        r = requests.get(url2)
        print("Sending request to " + url2)
        open(fileName,'wb').write(r.content)
        print("Downloaded " + fileName)
        return True
    except Exception as e:
        print(appID + " could not be downloaded from ApkPlz")
        return False

def downloadFromApkGk(appID,outputDirectory):
    try:
        #Avoid re-download of duplicates
        fileName = os.path.abspath(outputDirectory) + '/' + appID+ '.apk'
        if os.path.exists(fileName):
            print(appID + " is already downloaded at " + fileName)
            return True
        url1 = "https://apkgk.com/" + appID + "/download"
        r = requests.get(url1)
        soup = BeautifulSoup(r.text,'lxml')
        url2 = "https:"+str(soup.find("a",class_="btn btn-cus btn-down")["href"])
        r = requests.get(url2)
        print("Sending request to " + url2)
        open(fileName,'wb').write(r.content)
        print("Downloaded "+fileName)
        return True
    except Exception as e:
        print(appID + " could not be downloaded from ApkGk")
        return False

def downloadFromApkTada(appID, outputDirectory):
    try:
        fileName = os.path.abspath(outputDirectory) + '/' + appID+ '.apk'
        if os.path.exists(fileName):
            print(appID + " is already downloaded at " + fileName)
            return True
        #Download URL 1
        url1 = "https://apktada.com/download-apk/" + appID
        r1 = requests.get(url1)
        soup = BeautifulSoup(r1.text, 'lxml')
        #look for 'dllink' within all script tags, strip out the value of the variable using substrings
        download_url_untrimmed = re.search(r'dllink\s*=\s*(.*?);', str(soup.find_all('script')), flags=re.DOTALL).group(0)
        url2 = download_url_untrimmed.split("\"")[1]
        r = requests.get(url2)
        print("Sending request to " + url2)
        open(fileName,'wb').write(r.content)
        print("Downloaded " + fileName)
        return True
    except Exception as e:
        print(appID + " could not be downloaded from ApkTada")
        return False

def downloadByAppID(appID,outputDirectory):
    if not downloadFromApkPlz(appID,outputDirectory):
        if not downloadFromApkGk(appID,outputDirectory):
            downloadFromApkTada(appID,outputDirectory)

def getAppIDsFromCSV(fileName, column_name):
    df = pd.read_csv(fileName, usecols = [column_name])
    appIDs = [x for x in df[column_name].tolist() if str(x) != 'nan']
    return appIDs

def downloadApksFromCSV(fileName):
    df = pd.read_csv(fileName, usecols = ['AppID','Title'])
    appIDs = df.AppID
    count = 0
    for appID in appIDs:
        try:
            fileName = os.getcwd() + '\\APKs\\benign\\'+ appID + '.apk'
            if os.path.exists(fileName):
                continue
            url1 = "https://apkplz.net/download-app/" + appID
            r1 = requests.get(url1)
            soup = BeautifulSoup(r1.text, 'lxml')
            #look for 'dllink' within all script tags, strip out the value of the variable using substrings
            download_url_untrimmed = re.search(r'dllink\s*=\s*(.*?);', str(soup.find_all('script')), flags=re.DOTALL).group(0)
            url2 = download_url_untrimmed.split("\"")[1]
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded " + fileName)
            count += 1
            if count == 700:
                break
        except Exception as e:
            fileName = os.getcwd() + '\\APKs\\benign\\'+ "errors.txt"
            errorMessage = "\n" + appID + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID+ " could not be downloaded")
            continue




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
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            url1 = "https://apkpure.com" + appID + "/download?from=details"
            r1 = requests.get(url1, headers = headers)
            soup = BeautifulSoup(r1.text, 'html.parser')
            url2 = soup.find(id="download_link")["href"]
            r = requests.get(url2)
            open(fileName,'wb').write(r.content)
            print("Downloaded " + fileName)
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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

def downloadTencent(db,table):
    count = 0
    for row in db[table]:
        try:
            downloadUrl = str(row["appURL"])
            appID = str(row["appID"])
            fileName = os.getcwd() + '\\APKs\\tencent\\'+ appID + '.apk'
            #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            if os.path.exists(fileName):
                print(appID + " already downloaded. Skipping..")
                count += 1
                continue
            r = requests.get(downloadUrl, stream = True)
            with open(fileName, 'wb' ) as f:
                for chunk in r.iter_content( chunk_size = 1024 ):
                    if chunk: # filter out keep-alive new chunks
                        f.write( chunk )
            # open(fileName,'wb').write(r.content)
            # open(fileName).close()
            print("Downloaded "+fileName)
            count += 1
            if count == 500:
                break
        except Exception as e:
            fileName = os.getcwd() + '\\APKs\\tencent\\'+ "errors.txt"
            errorMessage = "\n" + appID + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appID + " could not be downloaded")
            continue

def downloadStore360(db,table):
    count = 0
    for row in db[table]:
        try:
            downloadUrl = str(row["downloadURL"])
            appName = str(row["appName"])
            fileName = os.getcwd() + '\\APKs\\Store360\\'+ appName + '.apk'
            #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            if os.path.exists(fileName):
                print(appName + " already downloaded. Skipping..")
                count += 1
                continue
            r = requests.get(downloadUrl, stream = True)
            with open(fileName, 'wb' ) as f:
                for chunk in r.iter_content( chunk_size = 1024 ):
                    if chunk: # filter out keep-alive new chunks
                        f.write( chunk )
            # open(fileName,'wb').write(r.content)
            # open(fileName).close()
            print("Downloaded "+fileName)
            count += 1
            if count == 500:
                break
        except Exception as e:
            fileName = os.getcwd() + '\\APKs\\Store360\\'+ "errors.txt"
            errorMessage = "\n" + appName + " could not download" + format(e)
            open(fileName,'a').write(errorMessage)
            open(fileName).close()
            print(appName + " could not be downloaded")
            continue

if __name__ == '__main__':
    # path = os.getcwd() + '\\DB\\'
    # db = databaseStartUp("sqlite:///" + path + "apkpure.db")
    # downloadApkpure(db,"appDetails")

    # db = databaseStartUp("sqlite:///" + path + "apkplz.db")
    # downloadApkplz(db,"appDetails")

    # db=databaseStartUp("sqlite:///" + path + "apktada.db")
    # downloadApktada(db,"appDetails")

    # db=databaseStartUp("sqlite:///" + path + "apkfab.db")
    # downloadApkfab(db,"appDetails")

    # db=databaseStartUp("sqlite:///" + path + "apkgk_database.db")
    # downloadApkgk(db,"appDetails")

    # db = databaseStartUp("sqlite:///" + "cn_database.db")
    # downloadTencent(db, "appDetailsChinese")

    # db = databaseStartUp("sqlite:///" + "cn_database2.db")
    # downloadStore360(db, "appDetailsChinese")

    #downloadApksFromCSV('Apk_list.csv')
    for appID in getAppIDsFromCSV("/Users/adil/Documents/IPV/Labled apps/250_en_sample.csv","appId"):
        downloadByAppID(appID,"/Users/adil/Documents/IPV/APKs/testcorpus")