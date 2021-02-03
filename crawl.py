import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import json
from IPython.display import display
#import wordcloud
import csv
import matplotlib.pyplot as plt

content = []
point = []
def crawl(url):
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    driver.implicitly_wait(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find('li', class_='prodItem wide')
    modelno = result['ingimodelno']

    driver.close()

    review_url = "http://www.enuri.com/view/zum/ajax/detailBoard_ajax.jsp?modelno={0}&pageno=1&pagesize={1}".format(modelno, "10000")

    data = requests.get(review_url)
    json_data = json.loads(data.text)

    review_count = int(json_data['reviewCount'])

    for i in range(review_count):
        content.append(json_data['reviewBody'][i]['content'])
        point.append(json_data['reviewBody'][i]['point'])

    df = pd.DataFrame([x for x in zip(point,content)])
    df.columns = ["평점", "리뷰"]

    df.평점 = [int(x) for x in df.평점]
    df["긍정리뷰"]=df['평점']>3

    display(df[df["긍정리뷰"]==False])
    #df.to_csv('review.csv')

keyword="나이키+에어맥스"
url="http://www.enuri.com/search.jsp?nosearchkeyword=&issearchpage=&searchkind=&es=&c=&ismodelno=false&hyphen_2=false&from=list&owd=&keyword={0}".format(keyword)
crawl(url)

# wordcloud = WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate(text)
# plt.figure(figsize=(22,22)) #이미지 사이즈 지정
# plt.imshow(wordcloud, interpolation='lanczos') #이미지의 부드럽기 정도
# plt.axis('off') #x y 축 숫자 제거
# plt.show()
# plt.savefig()