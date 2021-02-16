from django.shortcuts import render
import requests as req
import json
import key, crawl, sementic_classifier, makewordcloud
# Create your views here.

def search(request) :
    if request.method == "POST" :
        keyword = request.POST.get("keyword")
        print(keyword)
        url = "http://www.enuri.com/search.jsp?nosearchkeyword=&issearchpage=&searchkind=&es=&c=&ismodelno=false&hyphen_2=false&from=list&owd=&keyword={0}".format(keyword)
        makewordcloud.cloud(sementic_classifier.test(crawl.crawl(url)))
        return render(request, 'search.html')

def main(request) :
    if request.method == "GET" :
      return render(request, 'main.html')