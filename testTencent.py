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
import xml.etree.ElementTree as ET
from databaseUtility import *

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


def tencentTest(db):
    #translated_query_terms = [tr_cn(term).get("translatedText") for term in get_query_terms()]
    #test_query = "track my husband's phone"
    #print(tr_cn(test_query).get("translatedText"))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # TODO: 
    # Hardcoded query for testing. Need to fetch query seeds from DB
    print("Sending request to Tencent")
    numberOfTerms = 0
    #time.sleep(1)
    #hardcoded payload
    #For tencent, the pns parameter is incremented by 10 in each call to return all requests for a particular query.
    #the parameter value is base64 encoded before sending the request
    #The loop terminates when no further results are obtained (try/except statement)
    appDetailsTable = getTable(db, 'appDetailsChinese')
    appIdTable = getTable(db, 'AppId')
    for term in get_query_terms():
        for count in range(0,1000,10):
            count_bytes = str(count).encode('ascii')
            print(tr_cn(term).get("translatedText"))
            payload = {'kw':tr_cn(term).get("translatedText"),'pns':base64.b64encode(count_bytes).decode('ascii'),'sid':''}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get('https://android.myapp.com/myapp/searchAjax.htm', params=payload, headers=headers)
            response = r.json()
            #In the test script, only pkgName is printed to test the number of results returned.
            #TODO: Add all appdetails to DB
            currentTime = datetime.now()
            try:
                for item in response["obj"]["items"]:
                    print(item["pkgName"])
                    appID = item["pkgName"]
                    fileSize = item["appDetail"]["fileSize"]
                    apkHash = item["appDetail"]["apkMd5"]
                    downloadURL = item["appDetail"]["apkUrl"]
                    title = item["appDetail"]["appName"]
                    desc = item["appDetail"]["description"]
                    developerName = item["appDetail"]["authorName"]
                    version = item["appDetail"]["versionName"]
                    category = version = item["appDetail"]["categoryName"]
                    averageRating = item["appDetail"]["averageRating"]
                    imageLink = item["appDetail"]["iconUrl"]
                    #savedetailsinDB
                    insertIntoAppDetailsTable(appDetailsTable, dict(pkgName=appID,appID=appID, App_Name=title, appURL=downloadURL,desc=desc,file_size=fileSize,author_name=developerName,rating=averageRating,category=category,hash=apkHash, imageSource=imageLink, developerName=developerName, websiteName='android.myapp.com', createdAt=currentTime,version=version,other=str(item)))
                    #download APK
                    #path = 'F:/Grad School/CS 839 Topics in Security and Privacy/Project/Code/webScrapper/APKs/' + appID +'.apk'
                    #wget.download(downloadURL,path)
                    #appMainTableEntry = (word, appIDList, 'null', 'apkpure.com')
                    #insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apkpure.com', createdAt = currentTime))
                    #numberOfTerms = numberOfTerms + 1
                    # if(numberOfTerms == 5000):
                    #     break
            except TypeError:
                print("All results returned for query!")
                break
        #Add entries to database
            # currentTime = datetime.now()
            # if(len(names_table) == 0):
            #     continue
            # appIDList = ""
            # first = 0
            # TODO: Create appDetailsTable in DB
            # TODO: Make fresh DB for Chinese app stores
            # TODO: Add chinese description to "other" column and add english translation in a separate column
            # TODO: Add function for China360
            # Create appDetailsTable in DB
        
db = databaseStartUp("sqlite:///cn_database.db")
tencentTest(db)
    

        # Suggestion Addition
        # suggestionList = soup.find_all("div", attrs={"class": "suggest"})
        # suggestionList = suggestionList[0].find_all("li")
        # suggestions = []
        # suggestionsString = ""
        # i = 0
        # for suggestion in suggestionList:
        #     suggestionName = suggestion.get_text()
        #     if (i != 0):
        #         suggestionsString = suggestionsString + ","
        #     suggestionsString = suggestionsString + suggestionName
        #     i = 1
        #     suggestions.append(suggestionName)
        #     modifiedSuggestionName = commaSeparated(suggestionName)
        #     if(modifiedSuggestionName not in wordSet):
        #         wordSet.add(modifiedSuggestionName)
        #         q.put(modifiedSuggestionName)

        # Create appIdTable & suggestionTable in DB
        # appIdTable = getTable(db, 'AppId')
        # suggestionTable = getTable(db, 'AppSuggestions')        

        # # Create entries for tables
        # currentTime = datetime.now()
        # appIdTableEntry = (word, appIDList, 'apk.support', currentTime)
        # suggestionTableEntry = (word, suggestionsString, 'apk.support', currentTime)


        # # Enter into appIdTable & suggestionTable (one per word)
        # insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk.support', createdAt = currentTime))
        # insertIntoSugesstionsTable(suggestionTable, dict(word=word, relatedSearchTerms= suggestionsString, websiteName = 'apk.support', createdAt = currentTime))

        # numberOfTerms = numberOfTerms + 1
        # if(numberOfTerms == 5000):
        #     break

