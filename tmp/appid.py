#
db = "/Users/akshatsinha/Documents/database.db"
import sqlite3
import yaml

def main():
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = "SELECT DISTINCT appID FROM AppDetails;"
    # query="SELECT name FROM sqlite_master WHERE type='table';"

    cur.execute(query)
    result = cur.fetchall()
    print(len(result))
    # print(type(result))
    print(result[0])
    stats = dict()
    for app in result:
        appid = app[0].split("/")[-1]
        if appid in stats:
            stats[appid]+=1
        else:
            stats[appid] = 1
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
    with open('./tmp/stats.yml', 'w') as outfile:
        yaml.dump(sorted_stats, outfile, sort_keys=False)    
    

if __name__ == '__main__':
    main()
    