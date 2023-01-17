from nltk.tokenize import word_tokenize
import pandas as pd
from config import conn
from models import adverb, verb, adjectives
from schemas import Adverb, Verb, Adjectives
from typing import List
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming(text: str):
    # Find the root word
    # stemming of words
    factory = StemmerFactory()
    stem = factory.create_stemmer()
    stemmed = [stem.stem(word) for word in text]
    return stemmed

def score(tweet: str):
    dataadv = conn.execute('SELECT * FROM adverb').fetchall()
    adverb1 = pd.DataFrame(dataadv)
    adverb1.to_csv('adverb.csv')  

    datav = conn.execute('SELECT * FROM verb').fetchall()
    verb1 = pd.DataFrame(datav)
    verb1.to_csv("verb.csv")

    dataadj = conn.execute('SELECT * FROM adjectives').fetchall()
    df = pd.DataFrame(dataadj)
    df.to_csv("adjectives.csv")

    # POS_tweets = tweet
    # adverb1=pd.read_csv("adverb.csv")
    # verb1=pd.read_csv("verb.csv")
    
    ''' Verb and adverb are dictionaries having values for verbs and adverbs'''
    verb={};adverb={}
    l=adverb1['value'].values
    j=0
    for i in adverb1['adverb'].values:
        adverb[i]=l[j]
        j+=1
    l=verb1['value'].values
    j=0
    for i in verb1['verb'].values:
        verb[i]=l[j]
        j+=1
    
    ''' Add the adjectives in the dictionary'''
    
    Adjectives={}
    # df=pd.read_csv("adjectives.csv")
    for i in range(len(df)) : 
        Adjectives[df.loc[i, "word"]]= [df.loc[i, "happiness"],df.loc[i, "anger"],df.loc[i, "sadness"],df.loc[i, "fear"],df.loc[i, "disgust"]] 

    ''' Assign Scores to each tweet'''
    FINAL={};FINAL1={'Tweets':[],'Happiness':[],'Sadness':[],'Fear':[],'Disgust':[],'Anger':[],'Sentiment':[]}
    # for tweet in POS_tweets:
    sum_adverb=0;sum_verb=0
    score_list=[]
    words = word_tokenize(tweet)
    stem = stemming(words)
    score_list = []
    f_stem = 0

    for i in words:
        if (i in adverb):
            sum_adverb += adverb[i]
        # elif (stem[f_stem] in adverb):
        #     sum_adverb += adverb[stem[f_stem]]
        elif (i in verb):
            sum_verb += verb[i]
        # elif (stem[f_stem] in verb):
        #     sum_verb += verb[stem[f_stem]]
        else:
            if (i in Adjectives) or (stem[f_stem] in Adjectives):
                if i in Adjectives:
                    ADJ = Adjectives[i]
                elif (stem[f_stem] in Adjectives):
                    ADJ = Adjectives[stem[f_stem]]
                else:
                    pass
                    # Calculate Score
                c = sum_adverb + sum_verb
                if (c) < 0:
                    for j in range(len(ADJ)):
                        ADJ[j] = 5.0-ADJ[j]
                elif (c >= 0.5):
                    for j in range(len(ADJ)):
                        ADJ[j] = c*ADJ[j]
                else:
                    for j in range(len(ADJ)):
                        ADJ[j] = 0.5*ADJ[j]
                score_list.append(ADJ)
        f_stem += 1
    total_adj = len(score_list)

    s = [0.0 for i in range(5)]
    emo = ''
    if (total_adj != 0):
        for i in score_list:
            s[0] += i[0] #Happiness
            s[1] += i[1] #Anger
            s[2] += i[2] #Sadness
            s[3] += i[3] #Fear
            s[4] += i[4] #Disgust
        for i in range(len(s)):
            s[i] = "{0:.6f}".format(s[i]/total_adj)
            s[i] = float(s[i])
        emotion = 0.0
        for i in range(len(s)):
            if (s[i] > emotion):
                emotion = max(emotion, s[i])
                if i == 0:
                    emo = '2'
                elif i == 1:
                    emo = '4'
                elif i == 2:
                    emo = '3'
                elif i == 3:
                    emo = '5'
                elif i == 4:
                    emo = '6'

    else:
        s = [0.2000 for i in range(5)]
        emo = '1'

    s.append(emo)

    # FINAL[tweet] = s
    FINAL1['Tweets'].append(tweet)
    FINAL1['Happiness'].append(s[0])
    FINAL1['Anger'].append(s[1])
    FINAL1['Fear'].append(s[3])
    FINAL1['Sadness'].append(s[2])
    FINAL1['Disgust'].append(s[4])
    FINAL1['Sentiment'].append(s[5])

    # FINAL1['Sentiment'].append(s[5])
    # DB = pd.DataFrame(FINAL1,columns=['Happiness','Anger','Fear','Sadness','Disgust','Sentiment'])
    return FINAL1
    # print(FINAL1)