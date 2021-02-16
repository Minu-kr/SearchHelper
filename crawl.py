import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import json
from IPython.display import display
from time import sleep
import makewordcloud
import matplotlib.pyplot as plt
import time
import re
content = []
point = []
model_no=[]
result=[]
def crawl(url):
    #chrome 드라이버로 model_no가 들어있는 html 태그를 전부 찾음
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    driver.implicitly_wait(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ori_result = soup.find_all('li', class_='prodItem wide ')

    #리뷰가 없는 상품은 리스트에서 제외
    for i in ori_result :
        if(i.find('em', class_="kbnum")!=None) :
            result.append(i)

    driver.close()

    for i in range(len(result)) :
        #modelno에 따라 API get 요청 후 Json 데이터 응답
        model_no.append(result[i]['ingimodelno'])
        review_url = "http://www.enuri.com/view/zum/ajax/detailBoard_ajax.jsp?modelno={0}&pageno=1&pagesize={1}".format(model_no[i], "10000")
        data = requests.get(review_url)
        json_data = json.loads(data.text)
        review_count = int(json_data['reviewCount'])
        #리뷰 Json => List로 저장
        for j in range(review_count):
            content.append(json_data['reviewBody'][j]['content'])
            point.append(json_data['reviewBody'][j]['point'])
        #누적 리뷰수가 5000이 넘으면 리뷰요청 중지
        if (len(point) > 5000):
            break;
    #리뷰 List => DataFrame으로 저장
    df = pd.DataFrame([x for x in zip(point, content)])
    df.columns = ["평점", "리뷰"]
    df['리뷰'] = df['리뷰'].map(extract)
    display(df.tail(5))
    return df

#리뷰의 필요없는 특수문자 제거
def extract(text) :
    subtract_text = re.sub('amp|gt|lt|apos|[-=+,#/\?:^$.@*\"※~&%ㆍ!;』\\‘|\(\)\[\]\<\>`\'…》]', "", text)
    return subtract_text

# wordcloud = WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate(text)
# plt.figure(figsize=(22,22)) #이미지 사이즈 지정
# plt.imshow(wordcloud, interpolation='lanczos') #이미지의 부드럽기 정도
# plt.axis('off') #x y 축 숫자 제거
# plt.show()
# plt.savefig()