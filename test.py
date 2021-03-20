def tencent(db, q):
    test_query = "跟踪我丈夫的电话"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # TODO: 
    # Send Post request to https://android.myapp.com/myapp/searchAjax.htm?kw=跟踪我丈夫的电话&pns=&sid=
    # Reply is json request
    # Parse request and repeat till we get empty response. 
    # Hardcoded query for testing. Need to fetch query seeds from DB

