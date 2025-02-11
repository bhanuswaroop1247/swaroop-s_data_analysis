# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:18:31 2025

@author: 91984
"""
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from textblob import TextBlob

#Reading the CSV file
df=pd.read_csv('chatgpt1.csv')

#Creating the function to detect language
x=df['Text'][0]
lan=detect(x)

def det(x):
    try:
        lang=detect(x)
    except:
        lang= 'Other'
    return lang

df['Lang']=df['Text'].apply(det)

df=df.loc[df['Lang'] == 'en']
df=df.reset_index(drop=True)

#Cleaning Some text
df['Text']=df['Text'].str.replace('amp','')
#df['Text']=df['Text'].str.replace('http','')
#df['Text']=df['Text'].str.replace('t.co','')

#Developing a sentiment function

def get_sentiment(text):
    sentiment=TextBlob(text).sentiment.polarity
    if sentiment>0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'
    
df['sentiment']=df['Text'].apply(get_sentiment)

#Generating the wordcloud

comment_words=''
stopwords=set(STOPWORDS)

for val in df.Text:
    val=str(val)
    tokens = val.split()
    comment_words = comment_words + " ".join(tokens)+ " "

wordcloud= WordCloud(width=900,height=500,background_color= 'black'
                     ,stopwords=stopwords,min_font_size=10).generate(comment_words)    

plt.figure(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout()
plt.show()


import seaborn as sns
sns.set_style('whitegrid')
plt.figure(figure=(10,5))
sns.countplot(x='sentiment',data=df)
plt.xlabelr('Sentiment')
plt.ylabel('Count of Sentiment')
plt.Title('Sentiment Distribution')
plt.show()
























































