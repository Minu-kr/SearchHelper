from django.shortcuts import render
import requests as req
import json
import key, crawl
# Create your views here.

def search(request) :
    if request.method == "POST" :
        keyword = request.POST.get("keyword")

        X_Naver_Client_Id = getattr(key, 'X_Naver_Client_Id')
        X_Naver_Client_Secret = getattr(key, 'X_Naver_Client_Secret')

        url ="https://openapi.naver.com/v1/search/shop.json?query={0}&display=10&start=1&sort=sim".format(keyword)
        headers = {
            "X-Naver-Client-Id": X_Naver_Client_Id,
            "X-Naver-Client-Secret":  X_Naver_Client_Secret,
            "User-Agent" : "curl/7.49.1",
            "Accept" : "*/*"
        }

        response=req.get(url= url, headers=headers)
        msg=response.json()
        CrawlURL=msg['items'][0]['link']
        #mallName=msg['items'][0]['mallName']
        #crawl.crawl(CrawlURL, mallName)
        return render(request, 'search.html', {"msg" : msg})

def main(request) :
    if request.method == "GET" :
      return render(request, 'main.html')