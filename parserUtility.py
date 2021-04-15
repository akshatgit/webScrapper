from databaseUtility import *
from utility import *
from lxml import html
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import bs4

def apksupportTest(db, q):
    print("Came inside apksupportTest")

def apkdlTest(db, q):
    print("Came inside apkdlTest")

def Store360(db, q):
    test_query = "跟踪我丈夫的电话"    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = {'kw': '跟踪我丈夫的电话'}
    url = "http://zhushou.360.cn/search/index/"
    r = requests.get(url, params=payload, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    app_list =  = soup.find_all("li")
    # TODO: fetch data for all apps and check if there is more results. 



def tencent(db, q):
    test_query = "跟踪我丈夫的电话"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # TODO: 
    # Send Post request to https://android.myapp.com/myapp/searchAjax.htm?kw=跟踪我丈夫的电话&pns=&sid=
    # Reply is json request
    # Parse request and repeat till we get empty response. 


def amazon_app(db, q):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = {'q': 'track+husband+phone', 'i': 'mobile-apps', 'ref': 'nb_sb_noss'}
    r = requests.get('https://www.amazon.com/s', params=payload, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.find_all("div", attrs={"class": "a-size-base a-link-normal a-text-normal"})
    # TODO: 
    # Handle flagging as bot by amazon

#Failing. Use user-agent fix
def apksupport(db, q):
    print("Starting apksupport")
    numberOfTerms = 0
    while(q.empty() != True):
        time.sleep(1)
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        payload = {'q': word, 't': 'app'}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get('https://apk.support/search', params=payload, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Get App Names
        names_table = soup.find_all("div", attrs={"class": "it_column"})
        # Time
        currentTime = datetime.now()
        if(len(names_table) == 0):
            continue
        appIDList = ""
        first = 0
        # Create appDetailsTable in DB
        appDetailsTable = getTable(db, 'AppDetails')
        for name in names_table:
            # Developer Information
            developerPart = name.find_all("div", attrs={"class": "ss_tg"})
            developerPart = developerPart[0].find_all("a")
            developerTag = developerPart[0]['href']
            developerTag = developerTag[10:]
            developerName = developerPart[0].get_text()
            information = name.find_all("a")
            # Title
            titleTag = information[0].find_all("h3")
            title = titleTag[0].get_text()
            # Description
            descriptionTag = information[0].find_all("p")
            description = descriptionTag[0].get_text()
            # Stars
            starsTag = information[0].find_all("div", attrs = {"class" : "stars"})
            starsSpan = starsTag[0].find_all("span")
            stars = starsSpan[0]['title']
            starCount = stars[stars.rindex(' ')+1:]
            # AppID
            appID = information[0]['href']
            appID = appID[4 : ]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            # Image Source Link
            imageTag = information[0].find_all("div", attrs={"class" : "seo_img"})
            imageTag = imageTag[0].find_all("img")
            imageSource = imageTag[0]['data-original']

            # Insert Into AppDetails Table (one per app)
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, description=description, stars=stars, imageSource=imageSource, developerName=developerName, websiteName='apk.support', createdAt=currentTime))

        # Suggestion Addition
        suggestionList = soup.find_all("div", attrs={"class": "suggest"})
        suggestionList = suggestionList[0].find_all("li")
        suggestions = []
        suggestionsString = ""
        i = 0
        for suggestion in suggestionList:
            suggestionName = suggestion.get_text()
            if (i != 0):
                suggestionsString = suggestionsString + ","
            suggestionsString = suggestionsString + suggestionName
            i = 1
            suggestions.append(suggestionName)
            modifiedSuggestionName = commaSeparated(suggestionName)
            if(modifiedSuggestionName not in wordSet):
                wordSet.add(modifiedSuggestionName)
                q.put(modifiedSuggestionName)

        # Create appIdTable & suggestionTable in DB
        appIdTable = getTable(db, 'AppId')
        suggestionTable = getTable(db, 'AppSuggestions')        

        # Create entries for tables
        currentTime = datetime.now()
        appIdTableEntry = (word, appIDList, 'apk.support', currentTime)
        suggestionTableEntry = (word, suggestionsString, 'apk.support', currentTime)


        # Enter into appIdTable & suggestionTable (one per word)
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk.support', createdAt = currentTime))
        insertIntoSugesstionsTable(suggestionTable, dict(word=word, relatedSearchTerms= suggestionsString, websiteName = 'apk.support', createdAt = currentTime))

        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break

#Completed
def apkdl(db, q):
    print("Starting apkdl")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        payload = {'q': word}
        payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
        r = requests.get('https://apk-dl.com/search', params=payload_str)
        soup = BeautifulSoup(r.text, 'html.parser')
        names_table = soup.find_all("div", attrs={"class": "card no-rationale square-cover apps small"})
        if(len(names_table) == 0):
            continue
        appIDList = ""
        first = 0
        # Create appDetailsTable in DB
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        for name in names_table:
            appIDPart = name.find("a", attrs={"class": "card-click-target"})
            appID = appIDPart['href']
            imageLinkPart = name.find("img", attrs={"class": "cover-image lazy"})
            imageLink = imageLinkPart['data-original']
            titlePart = name.find("a", attrs={"class": "title"})
            title = titlePart.get_text()
            developerNamePart = name.find("a", attrs={"class": "subtitle"})
            developerName = developerNamePart.get_text()
            starsPart = name.find("div", attrs={"class" : "current-rating"})
            stars = starsPart['style']
            stars = stars.rsplit(' ', 1)[1]
            stars = stars[:-2]
            stars = int(stars)/10
            
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1

            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, stars=stars, imageSource=imageLink, developerName=developerName, websiteName='apk-dl.com', createdAt=currentTime))
            print('App Entered')
        
        appIdTable = getTable(db, 'AppId')
        appMainTableEntry = (word, appIDList, 'null', 'apk-dl.com')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk-dl.com', createdAt = currentTime))
        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break

#Completed
def apkpure(db, q):
    numberOfTerms = 0
    print("Starting apkpure")
    while(q.empty() != True):
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        checkMore = 1
        firstCheck = 1
        interval = 0
        appIDList = ""
        first = 0
        # Create appDetailsTable in DB
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        while(checkMore):
            if(firstCheck == 0):
                interval = interval + 15
            payload = {'q': word,  't': 'app', 'begin': interval}
            payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
            r = requests.get('https://apkpure.com/search-page', params=payload_str)
            soup = BeautifulSoup(r.text, 'html.parser')
            names_table = soup.find_all("dl", attrs={"class": "search-dl"})
            if(len(names_table) == 0):
                print("Skipping " + word)
                break
            for name in names_table:
                dtPart = name.find_all("dt")
                ddPart = name.find_all("dd")
                aPart = dtPart[0].find_all("a")
                appID = aPart[0]['href']
                imagePart = aPart[0].find_all("img")
                imageLink = imagePart[0]['src']
                titlePart = ddPart[0].find_all("p", attrs={"class": "search-title"})
                title = titlePart[0].find("a").get_text()
                starsPart = ddPart[0].find_all("span", attrs={"class": "score"})
                stars = starsPart[0]['title']
                stars = stars.rsplit(' ', 1)[1]
                pParts = ddPart[0].find_all("p")
                developerPart = pParts[1].find_all("a")
                developerName = developerPart[0].get_text()
                if first != 0:
                    appIDList = appIDList + ","
                appIDList = appIDList + appID
                first = 1
                
                insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, stars=stars, imageSource=imageLink, developerName=developerName, websiteName='apkpure.com', createdAt=currentTime))
            firstCheck = 0
            if(len(names_table) == 0):
                checkMore = 0
        appMainTableEntry = (word, appIDList, 'null', 'apkpure.com')
        appIdTable = getTable(db, 'AppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apkpure.com', createdAt = currentTime))
        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break

# Completed
def apkplz(db, q):
    print("Starting apkplz")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        payload = {'q': word}
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        r = requests.get('https://apkplz.net/search?', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        appList = soup.find_all("div", attrs={"class":"section row nop-sm"})
        appList = appList[0].find_all("div",attrs={"class":"row itemapp"})
        finalList = []
        appIDList = ""
        first = 0
        for app in appList:
            appDetails  = app.find_all("div",attrs={"class" : "col-md-12 col-sm-9 vcenter apptitle"}) 
            title = appDetails[0].find_all("a")
            title = title[0]['title']
            imageSource = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
            imageSource = imageSource[0].find_all("img")
            imageSource = imageSource[0]["data-original"]
            appID = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
            appID = appID[0].find_all("a")
            appID = appID[0]["href"]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            
            # Insert Into App Table
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, imageSource=imageSource, websiteName='apkplz.com', createdAt=currentTime))
            
        #Insert Into Main Table
        appIdTable = getTable(db, 'AppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apkplz.com', createdAt = currentTime))

# Completed    
def apktada(db, q):
    print("Starting apktada")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        # word = 'apps+to+find+cheaters'
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        payload = {'q': word}
        r = requests.get('https://apktada.com/search?', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        appList = soup.find_all("div", attrs={"class":"section row nop-sm"})
        appList = appList[0].find_all("div",attrs={"class":"row itemapp"})
        appIDList = ""
        appDetailsTable = getTable(db, 'AppDetails')
        if len(appList) == 0:
            print('GO TO GOOGLE')
            appIDList = googleQueryParser(appDetailsTable, 'apktada.com', word)
        else:
            finalList = []
            first = 0
            currentTime = datetime.now()
            for app in appList:
                appDetails  = app.find_all("div",attrs={"class" : "col-md-12 col-sm-9 vcenter apptitle"}) 
                title = appDetails[0].find_all("a")
                title = title[0]['title']
                imageSource = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
                imageSource = imageSource[0].find_all("img")
                imageSource = imageSource[0]["data-original"]
                appID = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
                appID = appID[0].find_all("a")
                appID = appID[0]["href"]
                if first != 0:
                    appIDList = appIDList + ","
                appIDList = appIDList + appID
                first = 1
                
                # Insert Into App Table
                insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, imageSource=imageSource, websiteName='apktada.com', createdAt=currentTime))

        #Insert Into Main Table
        appIdTable = getTable(db, 'AppId')
        currentTime = datetime.now()
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apktada.com', createdAt = currentTime))
        # break

# Completed
def allfreeapk(db, q):
    print("Starting allfreeapk")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        payload = {'q': word}
        r = requests.get('https://m.allfreeapk.com/search.html?', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        appList = soup.find_all("div", attrs={"class":"list"})
        appList = appList[0].find_all("li")
        finalList = []
        appIDList = ""
        first = 0
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        for app in appList:
            appDetails  = app.find_all("div",attrs={"class":"l"}) 
            title =  app.find_all("div",attrs={"class":"r"}) 
            title = title[0].find_all("a")
            title = title[0].get_text()
            imageSource = appDetails[0].find_all("img")
            imageSource = imageSource[0]["data-original"]
            appID = appDetails[0].find_all("a")
            appID = appID[0]["href"]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            
            # Insert Into App Table
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, imageSource=imageSource, websiteName='m.allfreeapk.com', createdAt=currentTime))

        #Insert Into Main Table
        appIdTable = getTable(db, 'AppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'm.allfreeapk.com', createdAt = currentTime))

# Completed
def apkfab(db, q):
    print("Starting apkfab")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        payload = {'q': word}
        r = requests.get('https://apkfab.com/search', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        appList = soup.find_all("div", attrs={"class":'list'})
        finalList = []
        appIDList = ""
        first = 0
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        for app in appList:
            title = app.find_all("div",attrs={"class":"title"})
            if(len(title)  < 1):
                continue
            title = title[0].get_text()
            rating = app.find_all("span", attrs={"class":"rating"})
            starCount = rating[0].get_text()
            imageSource = app.find_all("img")
            imageSource  = imageSource[0]['data-src']
            appID = app.find_all("a")
            appID = appID[0]['href']
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            
            # Insert Into App Table
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, stars= starCount, imageSource=imageSource, websiteName='apkfab.com', createdAt=currentTime))
            
        #Insert Into Main Table
        appIdTable = getTable(db, 'AppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apkfab.com', createdAt = currentTime))

# Completed
def malavida(db, q):
    print("Starting malavida")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        word = word.replace('+','-')
        r = requests.get('https://www.malavida.com/en/s/'+word)
        soup = BeautifulSoup(r.text, 'html.parser')
        appDetails = soup.find_all("section", attrs={"class":'app-list'})
        appList = soup.find_all("section", attrs={"class":'app-download'})
        counter = 0
        finalList = []
        appIDList = ""
        first = 0
        notFound = soup.find_all("section", attrs={"class":'not-found'})
        if(len(notFound)>0):
            continue
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        for app in appList:
            appSrc = app.find_all("div", attrs={"class":"title"})
            appDesc = app.find_all("p")
            imageSource = app.find_all('img')
            imageSource = imageSource[0]['src']
            appLink = appSrc[0].find_all("a")
            appID = appLink[0]['href']
            title = appLink[0].get_text()
            description = appDesc[0].get_text()
            counter = counter+1
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            
            # Insert Into App Table
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, imageSource=imageSource, description= description, websiteName='malavida.com', createdAt=currentTime))
            counter=counter+1

        #Insert Into Main Table
        appIdTable = getTable(db, 'AppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'malavida.com', createdAt = currentTime))

# Completed
def apkgk(db, q):
    print("Starting apkgk")
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        time.sleep(1)
        payload = {'keyword': word}
        r = requests.get('https://apkgk.com/search/', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        appId = soup.find_all("ul", attrs={"class":'topic-wrap'})
        if(len(appId) == 0):
            print("Skipping " + word)
            continue
        appId = appId[0].find_all("a")
        names_table = soup.find_all('div', attrs={"class":'topic-bg'})
        if(len(names_table) == 0):
            print("Skipping " + word)
            continue
        finalList = []
        appIDList = ""
        first = 0
        counter = 0
        appDetailsTable = getTable(db, 'AppDetails')
        currentTime = datetime.now()
        for name in names_table:
            appName = name.find_all("div", attrs={"class": "topic-tip-name"})
            appDesc = name.find_all("div", attrs={"class": "topic-tip-description"})
            appSrcMain  = name.find_all("div", attrs={"class": "c-lz-load"})
            imageTag = appSrcMain[0].find_all("img")
            imageSource = imageTag[0]['data-src']
            
            appID = appId[counter]['href']
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            if (len(appDesc) > 0):
                description = appDesc[0].get_text()
            else:
                description = "NULL"
            title = appName[0].get_text()
            
            # Insert Into App Table
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, imageSource=imageSource, description= description, websiteName='apkgk.com', createdAt=currentTime))
            counter=counter+1

        #Insert Into Main Table
        appIdTable = getTable(db, 'AppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apkgk.com', createdAt = currentTime))

def googleQueryParser(appDetailsTable, websiteName, word):
    print("Inside google search with website name as " + websiteName)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'referer': 'https://www.google.com/',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'pragma': 'no-cache',
    }
    googleWord = "site:" + websiteName + '+' + word
    url = f"https://www.google.com/search?&q={googleWord}&sourceid=chrome&ie=UTF-8"
    time.sleep(2)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup)
    searchResults = soup.find_all('div', attrs={"class":'rc'})
    appIDList = ""
    first = 0
    for result in searchResults:
        searchURL = result.find('a')['href']
        if searchURL.find(websiteName) != -1 and searchURL.find('/app/') != -1:
            time.sleep(1)
            innerR = requests.get(searchURL)
            siteSoup = BeautifulSoup(innerR.text, 'html.parser')
            icon = siteSoup.find('img', attrs={"class":'section media'})
            if hasattr(icon, 'src'):
                imageSource = icon['src']
                title = siteSoup.find('h1').get_text()
                appID = ''
                stars = ''
                supplementaryData = ''
                otherData = siteSoup.find('ul', attrs={"class":'list-unstyled'})
                for data in otherData:
                    if type(data) is not bs4.element.NavigableString:
                        attributeName, value = extractForApkTadaWebPageViaGoogle(data.get_text())
                        if attributeName == 'Package Name':
                            appID = value
                        elif attributeName == 'Stars':
                            stars = value
                        else:
                            supplementaryData = supplementaryData + attributeName + ': ' + value + ', '
                supplementaryData = supplementaryData[:-2]
                if first != 0:
                    appIDList = appIDList + ","
                appIDList = appIDList + appID
                first = 1
                print('Extracted App')
                currentTime = datetime.now()
                insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, imageSource=imageSource, websiteName='apktada.com', referrer='google.com', createdAt=currentTime, stars=stars, otherData=supplementaryData))
    print('FROM GOOGLE ' + str(len(appIDList)))
    return appIDList