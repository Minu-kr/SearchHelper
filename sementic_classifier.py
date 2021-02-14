import numpy as np
import pandas as pd
from konlpy.tag import Mecab
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model


def predict_label(token,model) :
    max_len = 80 #패딩의 길이

    encoded = tokenizer.texts_to_sequences([token]) # 정수로 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    label = 1 if score>0.5 else 0 # 예측결과를 labeling
    return label

def tokenized(new_sentence, stopwords, tokenizer,mecab):
    new_sentence = mecab.morphs(new_sentence) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    return new_sentence

def make_stopwords() :
    f = open('stopword.txt', 'r', encoding='utf8')
    stopwords_list = list(map(lambda s: s.strip(), f.readlines()))
    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한',
        '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들',
        '듯', '지', '임', '게']
    stopwords = stopwords + stopwords_list
    return stopwords

def set_tokenizer() :
    fit_data = np.load(file='token_fit_data.npy' , allow_pickle = True)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(fit_data)
    threshold = 2
    total_cnt = len(tokenizer.word_index) # 단어의 수
    rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if(value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    vocab_size = total_cnt - rare_cnt + 2
    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV')
    tokenizer.fit_on_texts(fit_data)
    return tokenizer

df = pd.read_csv('review3.csv', encoding='utf8') # 리뷰파일 로드
stopwords = make_stopwords() # 직접 지정한 불용어, 불용어 사전으로 불용어 리스트 만듦
tokenizer = set_tokenizer() # tokenizer를 모델에 맞게 set
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic") # 토큰화를 위한 mecab 생성(windows 환경 파일별도지정)
loaded_model = load_model('best_model.h5') # 감성분류 모델 로드

df['tokenized'] = df['리뷰'].map(lambda x: tokenized(x, stopwords, tokenizer,mecab)) # 리뷰 토큰화
df['label'] = df['tokenized'][df['평점']==3].map(lambda x: predict_label(x,loaded_model)) # 로드한 모델로 3점만 감성분류
df['label'][df['평점']>3] = 1 # 4~5점 : 긍정
df['label'][df['평점']<3] = 0 # 1~2점 : 부정
print(df.head())
