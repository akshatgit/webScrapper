import csv
import yaml
from queue import Queue
from google.cloud import translate_v2 as translate

def commaSeparated(term):
    result = ""
    if len(term.split(' ')) > 1:
        count = len(term.split(' '))
        i = 0
        for word in term.split(' '):
            if i > 0:
                result = result + "+"
            result = result + word
            i = i + 1
        return result
    else:
        return term

def readTermsAndCreateQueue():
    termsList = []
    finalTermsList = []
    with open('android_terms.csv','rt')as f:
        data = csv.reader(f)
        lineNumber = 0
        for row in data:
                if lineNumber >= 1:
                    key = row[2]
                    terms = row[3]
                    i = 0
                    for term in terms.split('"'):
                        if i%2 == 0:
                            i = i+1
                            continue
                        else:
                            i = i+1
                            termsList.append(term)
                else:
                    lineNumber = lineNumber + 1
    for term in termsList:
        result = commaSeparated(term)
        finalTermsList.append(result)
    # print("Number of elements being searched for " + str(len(finalTermsList)))
    q = Queue()
    wordSet = set()
    for term in finalTermsList:
        if(term != ""):
            wordSet.add(term)
    for word in wordSet:
        q.put(word)
    # print("Queue size is initially " + str(q.qsize()))
    return q

def formatForGoogleSearch(word):
    returnWord = ""
    for char in word:
        if char == '+':
            returnWord = returnWord + ' '
        else:
            returnWord = returnWord + char
    return returnWord

def extractForApkTadaWebPageViaGoogle(dataRow):
    colonIndex = dataRow.find(':')
    if colonIndex != -1:
        attributeName = dataRow[:colonIndex]
        value = dataRow[colonIndex + 2:]
        # print(attributeName + "->" + value)
    else:
        spaceIndex = dataRow.find(' ')
        attributeName = 'Stars'
        value = dataRow[spaceIndex + 1 : spaceIndex + 5]
        # print(attributeName + "->" + value)
    return attributeName, value

def tr(query):  
    translate_client = translate.Client()
    result_simplified = translate_client.translate(query, target_language='zh-CN') # to translate to simplified chinese
    
    return result_simplified

def chinese_list():
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

    print(len(terms_list))
    count = 0
    for i in terms_list:
        cn_list[i] = tr(i)
        count += 1
        print(count, cn_list[i])
    
    with open('./cn/terms.yml', 'w') as outfile:
        yaml.dump(cn_list, outfile, sort_keys=False)    
    
    
chinese_list()