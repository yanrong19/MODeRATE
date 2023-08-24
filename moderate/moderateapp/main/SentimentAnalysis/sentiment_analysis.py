import pickle
import spacy
import string
import text2emotion as te

def RFR_AI_model_predict(comments): #input list of strings
    model = pickle.load(open('C:/Orbital/Orbital_Moderate/moderate/moderateapp/main/SentimentAnalysis/RFR_model.sav', 'rb')) 
    ratings = model.predict(comments)
    return ratings

def text_preprocessing(comments):
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

def RFR_avg_rating(comments):
    cleaned = text_preprocessing(comments)
    ratings = RFR_AI_model_predict(cleaned)
    average = sum(ratings)/len(ratings)
    return f'{average:.2f}'

def merge_dict(dict1, dict2):
    final_dict = {}
    for key in dict1.keys():
        if key in dict2.keys():
            final_value = dict1[key] + dict2[key]
        else:
            final_value = dict1[key]
        final_dict[key] = final_value
    for key in dict2.keys():
        if key not in final_dict.keys():
            final_dict[key] = dict2[key]
    return final_dict

def get_emotion_dict(comment):
    return te.get_emotion(comment)

def emotion_chart(comments):
    emotions_dict = {"Happy": 0.0, "Angry" : 0.0, "Surprise" : 0.0, "Sad" : 0.0, "Fear" : 0.0}
    for comment in comments:
        emotions_dict = merge_dict(emotions_dict, get_emotion_dict(comment))
    return list(emotions_dict.values())

def convert_emotion_chart_to_str(emotions):
    emo_string = ""
    for e in list(map(str, emotions)):
            emo_string += e + ","
    return emo_string[:-1]