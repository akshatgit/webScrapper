import requests
import time
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
from databaseUtility import *
from parserUtility import *
from utility import *
import json
import sqlite3
from sqlite3 import Error
from queue import Queue 
import sys
import dataset
import argparse
import traceback

db = databaseStartUp()
termsQueue = readTermsAndCreateQueue()

def countArgumentsPassed(args):
    count = 0
    if args.all:
        count = count + 1
    if args.website:
        count = count + 1
    if args.websites:
        count = count + 1
    if args.statistics:
        count = count + 1
    if args.supportedWebsites:
        count = count + 1
    if args.google:
        count = count + 1
    if args.random:
        count = count + 1
    if args.analyze:
        count = count + 1
    return count

dispatcher = {
    'amazon': amazon_app,
    'apksupport': apksupport,
    'apkdl': apkdl,
    'apkpure': apkpure,
    'apkplz': apkplz,
    'apktada': apktada,
    'allfreeapk': allfreeapk,
    'apkfab': apkfab,
    'malavida': malavida,
    'apkgk': apkgk 
}

def runAllSupportedWebsites():
    print("Started processing for all supported websites")
    # apksupport(db, termsQueue)
    # apkdl(db, termsQueue)
    # apkpure(db, termsQueue)
    # apkplz(db, termsQueue)
    # apktada(db, termsQueue)
    # allfreeapk(db, termsQueue)
    # apkfab(db, termsQueue)
    # malavida(db, termsQueue)
    # apkgk(db, termsQueue)
    for k, v in dispatcher.items():
        dispatcher[v](db, termsQueue)
    print("Finished Processing for all supported websites")

def runSingleWebsite(website):
    print("Came inside single website")
    try:
        dispatcher[website](db, termsQueue)
    except Exception as e:
        print('Exception caused ->' + str(e))
        print("Invalid website name passed into function ->" + website)
        traceback.print_exc()

def runWebsiteList(websites):
    print("Came inside run website list")
    websiteList = websites.split(",")
    for website in websiteList:
        runSingleWebsite(website)

def getStatistics():
    getStats(db)

def listSupportedWebsites():
    print("===The following websites are currently supported!===")
    print("=====================================================")
    for k, v in dispatcher.items():
        print(k)
    print("=====================================================")
    print("Please enter these keys to run the appropriate parser")

def randomAppsPerWebsite():
    print("===The following random apps are returned per website!===")
    getRandomApps(db)

def analyzeApps():
    print("===Analyzing Apps===")
    analyzeAppsInDB(db)

# Driver function for g flag which was made for testing
def google():
    print('TESTING PURPOSE. WILL BE REMOVED')
    appDetailsTable = getTable(db, 'AppDetails')
    # appIDList = googleQueryParser(appDetailsTable, 'apktada.com', 'track+my+phone+apps')
    # apktada(db, termsQueue)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="run for all websites", action="store_true")
    parser.add_argument("-w","--website", help="run for one particular website")
    parser.add_argument("-ws", "--websites", help="run for list of webistes")
    parser.add_argument("-s", "--statistics", help="get statistics", action="store_true")
    parser.add_argument("-sw", "--supportedWebsites", help="list supported websites", action="store_true")
    parser.add_argument("-g", "--google", help="google search", action="store_true")
    parser.add_argument("-r", "--random", help="get 20 random results per website", action="store_true")
    parser.add_argument("-z", "--analyze", help="get number of apps common across websites", action="store_true")
    args = parser.parse_args()
    count = countArgumentsPassed(args)
    if count > 1:
        print("Please choose one of the flags available (-a, -w, -ws, -s, -sw). Run script with '-h' flag to see how to run it")
        sys.exit(0)
    elif count == 1:
        if args.all:
            print("Run for all websites from main")
            runAllSupportedWebsites()
        elif args.website:
            print("Running from main with " + args.website)
            runSingleWebsite(args.website)
        elif args.websites:
            print("Running from main with list of websites " + args.websites)
            runWebsiteList(args.websites)
        elif args.statistics:
            print("Calling statistics")
            getStatistics()
        elif args.supportedWebsites:
            print("Listing supported websites")
            listSupportedWebsites()
        elif args.google:
            print("Google Search!")
            google()
        elif args.random:
            print("Getting 20 random apps per website")
            randomAppsPerWebsite()
        elif args.analyze:
            print("Analyzing")
            analyzeApps()
    elif count == 0:
        print("No args passed. Defaulting to all websites")
        runAllSupportedWebsites()
    sys.exit(0)