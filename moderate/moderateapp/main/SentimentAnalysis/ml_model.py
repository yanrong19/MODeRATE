import spacy
import string
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle

dataset = pd.read_csv('https://github.com/ZhiQi12/Orbital-/blob/master/moderate/moderateapp/main/SentimentAnalysis/Comments%20Review%20-%20Sheet1.csv?raw=true')[["Comment","Emotion","Rating"]]

class Model: 
    def __init__(self,trained_model):
        self.trained_model = trained_model

def text_preprocess(comments):
    cleaned = []
    nlp = spacy.load("en_core_web_sm")
    for message in comments:
        str = ""
        doc = nlp(message)
        for token in doc:
            if not token.is_stop and not (token.text in string.punctuation) and token.text!= "\n":
                str += token.lemma_.lower() + " "
        cleaned.append(str[0:len(str)-1])
    return cleaned

def create_model():
    RFR = Pipeline([
        ('count vectorizer', CountVectorizer()),
        ('chi2score', SelectKBest(chi2,k=50)),
        ('tf_transformer', TfidfTransformer()),
        ('regressor', RandomForestRegressor())
    ])
    return RFR

def main():
    
    RFR = create_model()
    model1 = RFR.fit(text_preprocess(dataset["Comment"]), dataset["Rating"])
    modelObj = Model(model1)

    pickle.dump(modelObj.trained_model, open("RFR_model.sav", 'wb'))

if __name__=='__main__':
    main()