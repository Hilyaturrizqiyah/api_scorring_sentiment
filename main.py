from fastapi import FastAPI, status, HTTPException, Depends
import re
import pandas as pd
import uvicorn
from pydantic import BaseModel
import pickle
from scorring import score

app = FastAPI()

def str_to_lower(text):
    return text.lower()

def remove_punct(text):
    text = re.sub(r'[^a-zA-Z]', ' ', str(text))
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = re.sub(r'\s\s+', ' ', text)
    text = re.sub('([#])|([^a-zA-Z])', ' ', text)
    return text

def tokenization(text):
    # text = nltk.tokenize.word_tokenize(text)
    # return(text)
    text = re.split(r'\W+', text)
    return text

stopword = pd.read_csv('stopword.csv')
stopwords = [x for x in stopword['ada']]
def remove_stopword(text):
    text = [word for word in text if word not in stopwords]
    return text
## Opening a model from saved model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
## Opening vectorizer from saved model
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def preprocess(text: str):
    text = str_to_lower(text)
    text = remove_punct(text)
    text = tokenization(text)
    text = remove_stopword(text)
    text = ' '.join(text)
    return vectorizer.transform([text])

def predict(text: str):
    return model.predict(preprocess(text))

class RequestModel(BaseModel):
    tweet: str

class ResponseModel(BaseModel):
    tweet: str
    sentiment: str

class LabellingModel(BaseModel):
    text: str
    sentiment: list = [0]

# class LabellingModel(BaseModel):
#     text: str
#     sentiment: list = []

def scorring(text: str):
    text = score(text)
    return text

label_dict = {
    0: '1',
    1: '2',
    -1: '3',
    -2: '4',
    -3: '5',
    -4: '6',
}
# @app.get("/adverb", response_model=List[Adverb], tags=["adverb"])
# def get_categorie():
#     dataadv = conn.execute(adverb.select()).fetchall()
#     dfadv = pd.DataFrame(dataadv)
#     dfadv.columns = ["id", "adverb", "value"]
#     dfadv.to_csv('adverb.csv')
#     return {'message':'berhasil'}

@app.post("/predict", response_model=ResponseModel)
def predict(input: RequestModel):
    data = preprocess(input.tweet).toarray()
    sentiment = model.predict(data)
    response_model = ResponseModel(tweet=input.tweet, sentiment=label_dict[sentiment[0]])
    return response_model

@app.post("/score")
def scorring(input: RequestModel):
    # data = preprocess(input.tweet).toarray()
    sentimen = score(input.tweet)
    # response_model = LabellingModel(text=input.tweet, sentiment=sentimen)
    return sentimen

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)