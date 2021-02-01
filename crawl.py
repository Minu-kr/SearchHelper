from bs4 import BeautifulSoup
import requests as req
import re

p = re.compile('reviewItems_text__.*')

url = req.get('https://search.shopping.naver.com/gate.nhn?id=24302992388')
soup = BeautifulSoup(url.content, 'html.parser')
s = soup.find('script').string.split("'")[1]


true_url = req.get('https://search.shopping.naver.com/'+s)
soup2 = BeautifulSoup(true_url.content, 'html.parser') #여기에 html담
result = str(soup2.find_all(class_=p))

real_result=re.sub('<.+?>', '', result, 0).strip()

print(real_result)
