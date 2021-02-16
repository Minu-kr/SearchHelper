# 워드클라우드, review
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def plotword(img) :
    fig = plt.figure(figsize=(15, 15))
    plt.imshow(img, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def cloud(df) :
    list_positive = [x for x in df['리뷰'][df['label']==1]]
    list_negative = [x for x in df['리뷰'][df['label']==0]]

    review_positive = ' '.join(list_positive)
    review_negative = ' '.join(list_negative)
    f = open('negativestring.txt', 'w')
    f.write(review_negative)
    f.close()
    print(review_negative)
    mask = np.array(Image.open('shoes2.jpg'))
    wordcloud_positive = WordCloud(font_path='NanumGothic.ttf',
                          max_font_size=45,
                          background_color='white',
                          mask=mask,
                          max_words = 40,
                          colormap = 'autumn'
                         ).generate(review_positive)

    wordcloud_negative = WordCloud(font_path='NanumGothic.ttf',
                          max_font_size=45,
                          background_color='white',
                          mask=mask,
                          max_words = 40,
                          colormap = 'winter'
                         ).generate(review_negative)

    plotword(wordcloud_positive)
    plotword(wordcloud_negative)