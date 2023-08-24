## Level of Achievement: Apollo 11

![19e71a7ecb804111963590d0ee72f9d7 (1)](https://user-images.githubusercontent.com/74350301/175823931-8ac2c789-9121-4f13-8b4e-f4668dad3ae4.png)
# MODeRATE

MODeRATE is a web app which generates sentimental scores for NUS modules based on reviews scraped from Reddit. 

## Problem Statement
During ModReg, a NUS student may have a hard time deciding which modules to bid for in their upcoming semester of study. They may try to go to the NUS subReddit to search for reviews about the modules. In doing so, they may have a hard time finding out the general sentiment of the module given the numerous posts and comments that they would have to read through and compare. Such a process is also very time-consuming, inefficient and can be confusing for the student.

## Objective
To provide an efficient and effortless way for students to better understand the general sentiment of a module.

## Description 

MODeRATE is a web application that helps to determine the sentiment rating of a (NUS) module with the help of an artificial intelligent(AI) model. MODeRATE is made up of 2 components: web scraping and sentimental analysis. Web scraping involves extracting data from a website. Sentimental analysis involves the use of algorithms and AI models to classify text and determine whether a given input has a positive, negative or neutral sentiment associated with it. 

In this project, data such as text reviews, number of upvotes and date posted are scraped from the NUS subReddit. They are then passed through and analysed by our custom made AI model (using random forest regressor) trained on Reddit posts and submissions. The algrotihm filters out irrelevent comments based on certain criterias such as length of the post and nature of the post (a question or statement). The model then produces a sentiment score for each relevant review parsed into it. Factors such as date of post, number of upvotes, etc. help refine the sentiment score to account for relevance and credibility of the scraped posts. Additionally, to allow students to have an even better understanding of the general sentiment of the module, MODeRATE also generates the most relevant comments for users to view. An emotion chart is also provided for students to view the emotions associated with the module through the scraped posts.

With MODeRATE, NUS students can have a better gauge on the general sentiment of the module before they decide to bid during ModReg. It also allows the faculty to check on how well the module is doing over the semesters as our algorithm updates based on real-time data.

## Prototype
Link to the working prototype:
<br>
https://moderate-app.herokuapp.com/

## Features

### Custom AI Model
* Transformers such as CountVectorizer and TFIDFTransformer.
* Random Forest Regressor AI Model.
* Trained on Reddit submissions dataset.
* More accurate analysis than a pre-trained model.

### Sentiment Rating
* Gives a score out of ten (Quantifiable).
* Easy to compare across different modules.

### Top 3 comments
* Display the top 3 most relevant comments about the module.
* Relevance determined by number of upvotes and date posted.
* Acts as references for the user to better understand what others are saying about the module.

### Emotion Chart
* A pie chart used to display the emotions associated with the reviews about the modules.
* Displays for users to understand the breakdown of emotions from all the scraped reviews.
	
### View Metrics
* Sorts and displays the top 3 highest-rated and most-searched module in MODeRATE.
* To show user which modules are the most popular in MODeRATE.

### Database Update Scheduling
* Goes through all module codes stored in the database and re-performs web scraping and sentiment analysis.
* Updates the database of its rating, comments and emotions.
* Helps increase reliability of the rating by performing regular updates.

## Design

### Webscrapping
The primary function of the web scraping component is used to extract relevant data from websites to be parsed into our artificial intelligent(AI) model for text analysis. The Python PRAW library, which is an exclusive web scraping tool for Reddit, was used. A few other web scraping tools and libraries such as Selenium and BeautifulSoup were also considered. However, PRAW yielded the best results in terms of time complexity.

#### Websites for Data Source
A small-scale survey was conducted to determine which websites students would go to to find reviews for modules. Namely, two particular websites were mentioned: NUSMODs and the NUS subReddit.

* NUSMODs
A significant portion of the module reviews were quite outdated (>3 years). Several students mentioned how such reviews were unreliable as many changes would have been made to the module by the time they were taking it. Hence, NUSMODs was not included as a data source for web scraping in this project.

* NUS subReddit
Module reviews shown are rather recent (<2 years). New posts are made more frequently as compared to NUSMODs, hence the module reviews are more reliable. Some students pointed out an issue which is that some reviews show high degree of bias, seen by the use of certain high-intensity word phrases to describe the module. While some students prefer objective reviews, having a biased comment is also a way to show the general sentiment surrounding the module. Hence, the NUS subReddit was chosen to be a data source for web scraping in this project.

#### Data scraped
* Text comment - Primary component to use for sentiment analysis by the AI model. Short comments usually do not provide very constructive reviews about the modules. Hence, upon further testing, a minimum length of 8 words must be present in a text body for it to be considered relevant and be scrapped.

* Number of upvotes - A factor used to determine the relevance of a comment. A high number of upvotes can be used to indicate that a particular review resonated well with other users, hence its reliability.

* Date of post - Another factor used to determine the relevance of a comment. A newer post can indicate a 'fresher' and hence, a more reliable review as opposed to an older post. This is based on the assumption that fewer changes can happen to a module in a smaller span of time. However, it is still possible for a drastic change to occur over a single semester of study.

#### Banned Words
Helps to filter out irrelevant texts. Posts and comments containing these words/patterns are usually found to be irrelevant. Refer to list of banned words: 
<br>
https://raw.githubusercontent.com/ZhiQi12/Orbital-/master/WebScraping/banned_words.csv

### Relevance Scoring System
The relevance scoring system(RSS) acts as an extension from the web scraping component of this project. After the above data have been scraped from Reddit, a score will be given to a post to help determine its relevance. Refer to the scoring system below:

|Length (words)|Number of Upvotes (Comment)|Date of Post|
| :--: | :--: | :---: |
|<table> <tr><th>Criteria</th><th>Score</th></tr><tr><td>x < 8 </td><td>-</td></tr><tr><td>8<= x <50 </td><td>0</td></tr><tr><td>50<= x <100 </td><td>1</td></tr><tr><td>100<= x <150 </td><td>2</td></tr><tr><td>150<= x <200 </td><td>3</td></tr><tr><td>x >=200 </td><td>4</td></tr> </table>| <table> <tr><th>Criteria</th><th>Score</th></tr><tr><td>0</td><td>0</td></tr><tr><td>x <= 3</td><td>1</td></tr><tr><td>post_upvote > 10 & x > 0.8 * post_upvote</td><td>1</td></tr><tr><td>post_upvote > 10 & x > 0.9 * post_upvote</td><td>2</td></tr><tr><td>post_upvote < 10 & x > 3</td><td>2</th></tr><tr><td> 20 <= x < 50</td><td>2</td></tr><tr><td>x >= 50</td><td>3</td></tr> </table>| <table> <tr><th>Criteria</th><th>Score</th></tr><tr><td>x >= 3 years</td><td>-</td></tr><tr><td> 5 months <= x < 3 years </td><td>0</td></tr><tr><td> x < 4 months </td><td>1</td></tr> </table>|

### Artificial Intelligence Model (Sentiment Analysis)
The primary function of the AI model was to recognise patterns in a text to determine the sentiment associated with it in the context of a module review. The method used here was the Bag-of-Words(BoW) approach to help convert texts from our dataset into numerical form used for anaysis.

#### Custom Dataset
To ensure the AI model provides the most accurate predictions, we created our very own custom dataset using reviews on the NUS subReddit and provided our own rating to the comments. The comments were scrapped manually from the NUS subReddit. The ratings ranged from 1 to 10 which was given based on factors such as the intensity of choice of words, nature of comment, length of comment, etc.

Refer to the custom dataset:
<br>
https://docs.google.com/spreadsheets/d/1b2lHf4xYJ8It8KscUmsg0Pj9CIuiWi9cyLKumfxGK4w/edit?usp=sharing

#### Transformers
* Count Vectorizer - Helps to convert a text into tokens (a basic unit such as a word/character/subword which gives useful semantic meaning) used for processing.
* Select-K-Best - Keeps the k best features while removing the least useful features from the model.
* TFID Vectorizer - A common term weighting scheme that gives a feature a higher weight the greater the number of times it appears in a document but also a lower weight the greater the number of times it appears across documents.

#### Machine Learning Alogrithm
Several machine learning algorithms were tested for their accuracy to determine which model was best suited for sentiment analysis in this case study. The testing involves training a model using their respective transformers and ML algorithm on our custom dataset before testing on a series of test cases. The accuracy is given based on how far apart the model prediction rating is from our proposed rating.

Refer to the test cases and tested model results: 
<br>
https://docs.google.com/spreadsheets/d/1wbAVXMZ6UNz-A0g9hnvzZnsTtUklKzeyohDvMoLqd8Q/edit#gid=0

#### Model Selection
#### Creating the Model
The random forest regressor algorithm was chosen after testing.
<br>
* Loading the Dataset
```
import pandas as pd

dataset = pd.read_csv("Comments Review - Sheet1.csv")[["Comment","Emotion","Rating"]]
```

* Training the Model
```
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestRegressor

RFR = Pipeline([
    ('count vectorizer', CountVectorizer()),
    ('chi2score', SelectKBest(chi2,k=50)),
    ('tf_transformer', TfidfTransformer()),
    ('regressor', RandomForestRegressor())
])

model = RFR.fit(dataset["Comment"], dataset["Rating"])
```
* Saving and Loading the Model
```
import pickle

pickle.dump(model, open("RFR_model.sav", 'wb')) # Saving

PATH = "-path to saved model"
RFR_model = pickle.load(open(PATH, 'rb')) # Loading
```

### Database Design

#### Database Objects and their Attributes
|Module|Issue|
| :--: | :--: |
| Code | Code |
| Rating | Message |
| Comment1 |  |
| Comment2 |  |
| Comment3 |  |
| No. of Times Searched |  |
| Emotions |  |

#### Database Update Scheduling
Extracts all existing module codes from the database. For each module code, perform one round of web scraping and sentiment analysis. After which, update the database of the new ratings, comments and emotions.

This ensures that users view the most recent (and thus most reliable) rating for that module.

#### Flow Chart for Integrated System
<img width="3190" alt="flowchart" src="https://user-images.githubusercontent.com/74350301/175825096-75fdf0ea-309a-4070-844b-d1236cca35a7.png">

## Solution Evaluation
Usability testing with potential users was done to evaluate and improve on the suitability of the solution. Two different testings were done. The first testing involves a Powerpoint mockup to showcase the basic front-end and back-end designs. The second testing involves a clickable wireframe where potential users can interact with the application in the wireframe. Feedback was gathered after each round of testing with potential users.

### Powerpoint Mockup (Low-fidelity)
A simple Powerpoint was created to showcase ideas for basic front-end and back-end designs. The Powerpoint was displayed for potential users to view, understand and give feedback on the suitability of our solution.
#### Front End
<a href="url"><img src="https://user-images.githubusercontent.com/74350301/180607095-16260f0d-39cd-4649-8bc5-d07130f714d5.png" height="300" width="600" ></a>

#### Back End
<a href="url"><img src="https://user-images.githubusercontent.com/74350301/180607131-0bfea55f-4315-4bd9-a472-413914f87a28.png" height="300" width="600" ></a>
<br>

Link to mockup: https://docs.google.com/presentation/d/1frL-iCQV-CSvXogfe4_3n_1mIEyMA_NnTAAqyynRGxg/edit?usp=sharing

### Clickable Wireframe (High-fidelity)
This is an interactive process where users are able to click on buttons and navigate around the app in the wireframe. This allows potential users to have a better sense of the features of the final prototype.
Link to wireframe: https://www.figma.com/proto/gjBlJgyJ4v2ZEEZJQcWDWW/MODeRATE-Wireframe?node-id=2%3A2&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=2%3A2

## Deployment

### Django
Django is the primary platform used to create the web application. The application is first deployed onto localhost for initial testing and improvements. Django makes use of SQLite and its own database system to store objects created in the application itself.

### Heroku
Heroku, a cloud platform which manages app deployments with Git, is used to host the web app. After creating a Heroku application, it was linked to this github repository. A Procfile was created which specifies the commands executed by the web app on the Heroku platofrm. The information of the modules (rating, comments, emotions) is stored in Heroku Postgres, which is a managed SQL database service provided directly by Heroku. PGadmin, a management tool for Postgres databases, is then used to access and update the Heroku database. This is done by importing the csv file, updated from re-performing web scraping and sentiment analysis, into the database. 

## Testing
Testing was done to ensure correctness of our solution.

### Unit and Integration Testing
Testing was carried out for the two main components of our solution: web scraping and sentiment analysis. Each component was broken down into smaller basic functions to carry out unit testing. After which, integration testing was done by integrating the smaller basic functions to ensure each component works as intended. Finally, both components were integrated for the final testing.

All unit and integration testing were done using the in-built Django unittest library.

### System and User Testing
Once both components have been correctly integrated, system testing was done to check for potential errors of the system in each stage of deployment (Django and Heroku).

Finally, potential users were gathered to test the system to check for final bugs and errors.

Link to developer and user testing log: 
<br>
https://docs.google.com/spreadsheets/d/1PvtfJL-JlSUcfA14KmbrmRp8Sz-f-ZiZcPWhs7-_Tiw/edit?usp=sharing

## Getting Started

### Dependencies

* Python 3.9+
* Google Chrome

### Libraries

* PRAW
* pandas
* NLTK
* scikit-learn
* Django
* pickle
* spaCy / en_core_web_sm

### Installing
* Create and activate virtual environment

* Install Python Dependencies
```
pip install -r requirements.txt
```
```
python -m spacy download en_core_web_sm
```

### Changing path for files and other 
* Navigate to folder moderate -> moderateapp -> main -> generateMods -> generatedata.py, change the file path for line 4 such that it references the folder containing *WebScraping* & *SentimentAnalysis* folder (under main folder).
* Navigate to folder moderate -> moderateapp -> main -> generateMods -> getAllMods.py, change the file path for line 7 such that it references the folder containing *WebScraping* & *SentimentAnalysis* folder (under main folder).
* Navigate the folder moderate -> moderateapp -> main -> SentimentAnalysis -> ml_model.py and run the file. 
* Navigate to folder moderate -> moderateapp -> main -> SentimentAnalysis -> sentiment_analysis.py, change the file path for line 7 such that it references the  RFR.sav file.
* Navigate to folder moderate -> moderateapp -> test.py, change the file path for line 4 such that it references the folder containing *WebScraping* & *SentimentAnalysis* folder (under main folder).

### Operating on Django
* To run the web application using Django, navigate to the folder with *manage.py* file in command prompt and run:
```
python manage.py runserver
```
copy the URL provided in the command prompt:
```
http://127.0.0.1:8000/
```
paste it in a Google Chrome browser and press enter. The web application should now be running.

* To view the database storing the modules and issues:
1) Create an admin by navigating to the folder with *manage.py* file in command prompt and run:
```
python manage.py createsuperuser
```
2) Enter your desired username and press enter.
3) Enter your email address and press enter. This field can be left blank.
4) Enter your desired password and press enter.
5) Admin user is now created. With the web app running, enter the following URL:
```
http://127.0.0.1:8000/admin/
```	
6) Input the corresponding username and password. Press enter.
7) Database is now accessible.

## How To Use
1) Upon starting up the web application in a Google Chrome browser, you should be directed to the homepage. 
2) In the homepage, instructions are given on how to use MODeRATE.
3) Using the sidebar, click on *Find* which will navigate you to the search function.
4) Input the desired module code and press enter/click the submit button.
5) MODeRATE will display the sentiment rating, top 3 comments and emotion chart for the user to view.
6) If there is an issue, click the *Report Problem* button at the bottom right of the screen.
	* Enter the problem into the text box and click *Submit*.
	* From there, you can return to the homepage by clicking on the *Return to Home* button.
7) To use the View Metrics feature, click on *View* using the sidebar which will navigate you to the viewing menu.
8) Click on *Highest-Rated Mods* or *Most-Searched Mods* to view the respective metrics.
9) After done using the app, CTRL-BREAK in command prompt to close it.
<br>
For a visual guide on how to use the app, check out this video:
<br>
https://www.youtube.com/watch?v=IpdVr33PcLE
<br>

## Authors

Contributor names

* Chew Zhi Qi 
* Foo Yan Rong
