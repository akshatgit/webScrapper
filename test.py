import requests
import json
import time
import base64

def tencentTest():
    test_query = "跟踪我丈夫的电话"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # TODO: 
    # Send Post request to https://android.myapp.com/myapp/searchAjax.htm?kw=跟踪我丈夫的电话&pns=&sid=
    # Reply is json request
    # Parse request and repeat till we get empty response. 
    # Hardcoded query for testing. Need to fetch query seeds from DB
    print("Sending request to Tencent")
    numberOfTerms = 0
    time.sleep(1)
    #hardcoded payload
    for count in range(0,1000,10):
        count_bytes = str(count).encode('ascii')
        payload = {'kw':'跟踪我丈夫的电话','pns':base64.b64encode(count_bytes).decode('ascii'),'sid':''}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get('https://android.myapp.com/myapp/searchAjax.htm', params=payload, headers=headers)
        response = r.json()
        try:
            for item in response["obj"]["items"]:
                print(item["pkgName"])
        except:
            print("All results returned for query!")
            break
tencentTest()
    #soup = BeautifulSoup(r.text, 'html.parser')
    # Get App Names

#     names_table = soup.find_all("div", attrs={"class": "it_column"})
#     # Time
#     currentTime = datetime.now()
#     if(len(names_table) == 0):
#         continue
#     appIDList = ""
#     first = 0
#         # Create appDetailsTable in DB
#         appDetailsTable = getTable(db, 'AppDetails')
#         for name in names_table:
#             # Developer Information
#             developerPart = name.find_all("div", attrs={"class": "ss_tg"})
#             developerPart = developerPart[0].find_all("a")
#             developerTag = developerPart[0]['href']
#             developerTag = developerTag[10:]
#             developerName = developerPart[0].get_text()
#             information = name.find_all("a")
#             # Title
#             titleTag = information[0].find_all("h3")
#             title = titleTag[0].get_text()
#             # Description
#             descriptionTag = information[0].find_all("p")
#             description = descriptionTag[0].get_text()
#             # Stars
#             starsTag = information[0].find_all("div", attrs = {"class" : "stars"})
#             starsSpan = starsTag[0].find_all("span")
#             stars = starsSpan[0]['title']
#             starCount = stars[stars.rindex(' ')+1:]
#             # AppID
#             appID = information[0]['href']
#             appID = appID[4 : ]
#             if first != 0:
#                 appIDList = appIDList + ","
#             appIDList = appIDList + appID
#             first = 1
#             # Image Source Link
#             imageTag = information[0].find_all("div", attrs={"class" : "seo_img"})
#             imageTag = imageTag[0].find_all("img")
#             imageSource = imageTag[0]['data-original']

#             # Insert Into AppDetails Table (one per app)
#             insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, description=description, stars=stars, imageSource=imageSource, developerName=developerName, websiteName='apk.support', createdAt=currentTime))

#         # Suggestion Addition
#         suggestionList = soup.find_all("div", attrs={"class": "suggest"})
#         suggestionList = suggestionList[0].find_all("li")
#         suggestions = []
#         suggestionsString = ""
#         i = 0
#         for suggestion in suggestionList:
#             suggestionName = suggestion.get_text()
#             if (i != 0):
#                 suggestionsString = suggestionsString + ","
#             suggestionsString = suggestionsString + suggestionName
#             i = 1
#             suggestions.append(suggestionName)
#             modifiedSuggestionName = commaSeparated(suggestionName)
#             if(modifiedSuggestionName not in wordSet):
#                 wordSet.add(modifiedSuggestionName)
#                 q.put(modifiedSuggestionName)

#         # Create appIdTable & suggestionTable in DB
#         appIdTable = getTable(db, 'AppId')
#         suggestionTable = getTable(db, 'AppSuggestions')        

#         # Create entries for tables
#         currentTime = datetime.now()
#         appIdTableEntry = (word, appIDList, 'apk.support', currentTime)
#         suggestionTableEntry = (word, suggestionsString, 'apk.support', currentTime)


#         # Enter into appIdTable & suggestionTable (one per word)
#         insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk.support', createdAt = currentTime))
#         insertIntoSugesstionsTable(suggestionTable, dict(word=word, relatedSearchTerms= suggestionsString, websiteName = 'apk.support', createdAt = currentTime))

#         numberOfTerms = numberOfTerms + 1
#         if(numberOfTerms == 5000):
#             break


# def tencent(db, q):
#     test_query = "跟踪我丈夫的电话"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#     # TODO: 
#     # Send Post request to https://android.myapp.com/myapp/searchAjax.htm?kw=跟踪我丈夫的电话&pns=&sid=
#     # Reply is json request
#     # Parse request and repeat till we get empty response. 
#     # Hardcoded query for testing. Need to fetch query seeds from DB
#     print("Sending request to Tencent")
#     numberOfTerms = 0
#     while(q.empty() != True):
#         time.sleep(1)
#         word = q.get()
#         print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
#         payload = {'q': word, 't': 'app'}
#         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         r = requests.get('https://android.myapp.com/myapp/searchAjax.htm', params=payload, headers=headers)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         # Get App Names
#         names_table = soup.find_all("div", attrs={"class": "it_column"})
#         # Time
#         currentTime = datetime.now()
#         if(len(names_table) == 0):
#             continue
#         appIDList = ""
#         first = 0
#         # Create appDetailsTable in DB
#         appDetailsTable = getTable(db, 'AppDetails')
#         for name in names_table:
#             # Developer Information
#             developerPart = name.find_all("div", attrs={"class": "ss_tg"})
#             developerPart = developerPart[0].find_all("a")
#             developerTag = developerPart[0]['href']
#             developerTag = developerTag[10:]
#             developerName = developerPart[0].get_text()
#             information = name.find_all("a")
#             # Title
#             titleTag = information[0].find_all("h3")
#             title = titleTag[0].get_text()
#             # Description
#             descriptionTag = information[0].find_all("p")
#             description = descriptionTag[0].get_text()
#             # Stars
#             starsTag = information[0].find_all("div", attrs = {"class" : "stars"})
#             starsSpan = starsTag[0].find_all("span")
#             stars = starsSpan[0]['title']
#             starCount = stars[stars.rindex(' ')+1:]
#             # AppID
#             appID = information[0]['href']
#             appID = appID[4 : ]
#             if first != 0:
#                 appIDList = appIDList + ","
#             appIDList = appIDList + appID
#             first = 1
#             # Image Source Link
#             imageTag = information[0].find_all("div", attrs={"class" : "seo_img"})
#             imageTag = imageTag[0].find_all("img")
#             imageSource = imageTag[0]['data-original']

#             # Insert Into AppDetails Table (one per app)
#             insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, description=description, stars=stars, imageSource=imageSource, developerName=developerName, websiteName='apk.support', createdAt=currentTime))

#         # Suggestion Addition
#         suggestionList = soup.find_all("div", attrs={"class": "suggest"})
#         suggestionList = suggestionList[0].find_all("li")
#         suggestions = []
#         suggestionsString = ""
#         i = 0
#         for suggestion in suggestionList:
#             suggestionName = suggestion.get_text()
#             if (i != 0):
#                 suggestionsString = suggestionsString + ","
#             suggestionsString = suggestionsString + suggestionName
#             i = 1
#             suggestions.append(suggestionName)
#             modifiedSuggestionName = commaSeparated(suggestionName)
#             if(modifiedSuggestionName not in wordSet):
#                 wordSet.add(modifiedSuggestionName)
#                 q.put(modifiedSuggestionName)

#         # Create appIdTable & suggestionTable in DB
#         appIdTable = getTable(db, 'AppId')
#         suggestionTable = getTable(db, 'AppSuggestions')        

#         # Create entries for tables
#         currentTime = datetime.now()
#         appIdTableEntry = (word, appIDList, 'apk.support', currentTime)
#         suggestionTableEntry = (word, suggestionsString, 'apk.support', currentTime)


#         # Enter into appIdTable & suggestionTable (one per word)
#         insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk.support', createdAt = currentTime))
#         insertIntoSugesstionsTable(suggestionTable, dict(word=word, relatedSearchTerms= suggestionsString, websiteName = 'apk.support', createdAt = currentTime))

#         numberOfTerms = numberOfTerms + 1
#         if(numberOfTerms == 5000):
#             break