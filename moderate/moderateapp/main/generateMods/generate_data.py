import pandas as pd
import sys
import os
PATH = 'C:/Orbital/Orbital_Moderate/moderate/moderateapp/main'
sys.path.insert(0, PATH)
from WebScraping.scrapeReddit import scrape_posts, nus_sub
from SentimentAnalysis.sentiment_analysis import *

# load csv and create empty df
csv_path = 'https://github.com/ZhiQi12/Orbital-/blob/master/moderate/moderateapp/main/generateMods/moderate_mods.csv?raw=true'
mods = pd.read_csv(csv_path)
df = pd.DataFrame(columns = ["id", "code","rating","comment1","comment2","comment3","searched","emotions"])

# main function to load the entire csv file
def update(df, mods):
    counter = 1
    for i in range(len(mods["code"])):
        mod = mods["code"][i]
        tpl = scrape_posts(mod, nus_sub, 3)
        if tpl != ([], []):
            try:
                comment1 = tpl[1][0]
            except:
                comment1 = ""
            try:
                comment2 = tpl[1][1]
            except:
                comment2 = ""
            try:
                comment3 = tpl[1][2]
            except:
                comment3 = ""

            df = df.append({'id':counter,'code':mod, 'rating':RFR_avg_rating(tpl[0]), 'comment1':comment1,
                    'comment2':comment2, 'comment3':comment3, 'searched':mods["searched"][i],
                    'emotions':convert_emotion_chart_to_str(emotion_chart(tpl[0]))}, ignore_index=True)
            counter +=1
        else:
            pass
        
    return df
    
# save df into csv file
if __name__=='__main__':
    updated_df = update(df, mods)
    updated_df.to_csv("moderate_mods.csv", index=False)
    #print(os.getcwd())


