from django.test import TestCase
from unittest import mock
from unittest.mock import MagicMock
import time
import sys
import praw
import scrapeReddit
PATH = 'C:/Orbital/Orbital_Moderate/moderate/moderateapp/main'
sys.path.insert(0, PATH)
from WebScraping.scrapeReddit import *
from SentimentAnalysis.sentiment_analysis import *

# Create your tests here.
class MyTestCase(TestCase):

    def setUp(self):
        self.mod = "Mock mod"
        self.banned_words = ["banned"]
        # Mock Comment 1
        self.mock_comment1 = MagicMock()
        self.mock_comment1.body = "This comment has a banned word so there should only be 1 score"
        self.mock_comment1.created_utc = 1641006000  # 1/1/2022
        self.mock_comment1.score = 3

        # Mock Comment 2
        self.mock_comment2 = MagicMock()
        self.mock_comment2.body = '''
        as a working professional, actually I'd argue for a non CS major looking to do SWE, CS2103 may help but in my opinion,
        there are actually more fundamental modules that's more important in actual practice (assuming the student already done CS2030/2040 or variants thereof)
        - for instance, CS2105 - networking knowledge is criminally underrated for a SWE - students don't know that don't know
        networking and/or operating systems will actually hit their limit fast as a technical person. don't get me wrong - the SWE course
        is great for getting exposure to projects, but there are actually more critical modules even as a SWE. the tendency however, is for students not to
        appreciate these content while they are learning it
        '''
        self.mock_comment2.created_utc = 1651374000  #1/5/2022
        self.mock_comment2.score = 9

        # Mock Comment 3
        self.mock_comment3 = MagicMock()
        self.mock_comment3.body = '''
        Taking CS2030 and CS2040 this semester. I would say CS2040 helped me tremendously in passing OAs for SWE internships whereas CS2030 has been.
        Just my personal opinion though
        '''
        self.mock_comment3.created_utc = 1654052400  #1/6/2022
        self.mock_comment3.score = 12

        # Mock Comment 4
        self.mock_comment4 = MagicMock()
        self.mock_comment4.body = "This is the comment of mock comment 4"
        self.mock_comment4.created_utc = 1420052400  #1/1/2015
        self.mock_comment4.score = 0

        # Mock Comment 5
        self.mock_comment5 = MagicMock()
        self.mock_comment5.body = '''hello! i took this mod last sem and ur feelings are justified bc this mod was truly death for me. For some background, 
        I'm hopeless in math/data stuff lol, and DAO is all abt that so u can imagine....I tried to contribute most to the weekly group assignments, 
        and my group usually gets full marks/close to full marks. So those saved my final grade. For the project I wrote most of the report, excel analysis was
        done by my groupmates simply bc idk how to. If you really want to get a good grade (not S/U), I suggest going over topic by topic and redoing the questions
        in the lectures, group assignments, past year papers. Then consult on qns udk/don't understand. For finals I probably got 30% of the paper correct. Rest I 
        couldn't answer/half answered. In the end my final grade was C and I S/Ued it. So don't give up, this too shall pass haha
        '''
        self.mock_comment5.created_utc = 1654052400  #1/6/2022
        self.mock_comment5.score = 10

        #Mock Post 1
        self.mock_post1 = MagicMock()
        mock_commentsList1 = MagicMock(return_value=[self.mock_comment1, self.mock_comment2, self.mock_comment3, self.mock_comment4, self.mock_comment5], spec=praw.models.comment_forest.CommentForest)
        self.mock_post1.comments = mock_commentsList1
        self.mock_post1.comments.list.return_value = [self.mock_comment1, self.mock_comment2, self.mock_comment3, self.mock_comment4, self.mock_comment5]
        self.mock_post1.score = 5
        self.mock_post1.title = "Title for Mock Reddit Post 1 with Mock mod"
        self.mock_post1.selftext = "Selftext for Mock Reddit Post 1. This post has mock comment1,2,3,4,5."
        self.mock_post1.num_comments = len(self.mock_post1.comments.list.return_value)
        self.mock_post1.created_utc = 1654052400  #1/6/2022

        # Mock Post 2
        self.mock_post2 = MagicMock()
        mock_commentsList2 = MagicMock(return_value=[self.mock_comment3], spec=praw.models.comment_forest.CommentForest)
        self.mock_post2.comments = mock_commentsList2
        self.mock_post2.comments.list.return_value = [self.mock_comment3]
        self.mock_post2.score = 12      
        self.mock_post2.title = "Title for Mock Reddit Post 2"
        self.mock_post2.selftext = "Selftext for Mock Reddit Post 2. This post only has mock comment3"
        self.mock_post2.num_comments = len(self.mock_post2.comments.list.return_value)
        self.mock_post2.created_utc = 1641006000  # 1/1/2022
        pass

        self.comment = """
        I’m having so much trouble understanding the contents. 
        I spend so long just trying to understand 1 lecture cause 
        I keep repeating certain parts or spending hours watching YouTube 
        explanations, to the point where when I do finally somewhat get 
        what’s going on, I’m behind by 2 lectures already."
        """
        self.stopWords = "I am is are the a in"
    
    def tearDown(self):
        pass

    def test_read_bannedwordsCSV(self):
        print("test_read_bannedwordsCSV")
        self.assertTrue(len(scrapeReddit.read_bannedwordsCSV()) == 2)
        self.assertTrue(type(scrapeReddit.read_bannedwordsCSV()) == tuple)

    def test_filterPost(self):
        print("test_filterPost")
        
        self.assertTrue(scrapeReddit.filterPost(self.mock_post1, self.banned_words, self.mod))
        self.assertFalse(scrapeReddit.filterPost(self.mock_post2, self.banned_words, self.mod))  # False as mock_post2 does not have mod name inside its title 

    def test_filterComment(self):
        print("test_filterComment")

        self.assertFalse(scrapeReddit.filterComment(self.mock_comment1, self.banned_words))  #False = banned words found
        self.assertTrue(scrapeReddit.filterComment(self.mock_comment2, self.banned_words))
        self.assertTrue(scrapeReddit.filterComment(self.mock_comment3, self.banned_words))


    def test_check_date(self):
        print("test_check_date")
        mock_post1 = MagicMock()
        mock_post1.created_utc = time.time() - 86400 # 1 day b4 today

        mock_post2 = MagicMock()
        mock_post2.created_utc = 1420052400  #1/1/2015

        self.assertEqual(scrapeReddit.check_date(self.mock_post1), 1)
        self.assertEqual(scrapeReddit.check_date(self.mock_post2), 0)
        self.assertEqual(scrapeReddit.check_date(mock_post1), 1)
        self.assertEqual(scrapeReddit.check_date(mock_post2), -1)
        
    
    @mock.patch('WebScraping.scrapeReddit.praw.Reddit', spec=praw.models.reddit.subreddit.Subreddit)
    def test_create_subreddit(self, mock_subreddit):
        print("test_create_subreddit")
        self.assertTrue(isinstance(mock_subreddit, praw.models.reddit.subreddit.Subreddit))

    def test_getComments(self):
        print("test_getComments")
        self.assertTrue(isinstance(scrapeReddit.getComments(self.mock_post1,self.banned_words), dict))
        self.assertTrue(isinstance(scrapeReddit.getComments(self.mock_post2,self.banned_words), dict))
        self.assertEqual(scrapeReddit.getComments(self.mock_post1, self.banned_words)["Score"], [6,4,0,7])
        self.assertEqual(scrapeReddit.getComments(self.mock_post2, self.banned_words)["Score"], [4])

    @mock.patch('WebScraping.scrapeReddit.praw.Reddit', spec=praw.models.reddit.subreddit.Subreddit)
    def test_scrape_posts(self, mock_subreddit):

        mock_subreddit.search.return_value = [self.mock_post1, self.mock_post2]   # Mock subreddit has 2 mock posts created in SetUp function above
        outcome = scrapeReddit.scrape_posts(self.mod, mock_subreddit, 3)
        self.assertTrue(isinstance(outcome, tuple))
        self.assertEqual(len(outcome), 2)   # 2 lists in the tuple 
        self.assertEqual(type(outcome[0]), list) 


    def test_unit_sentiment_analysis(self):
        #text preprocessing
        cleaned1 = text_preprocessing([self.comment])[0]
        cleaned2 = text_preprocessing([self.stopWords])[0]

        self.assertGreater(len(cleaned1), 0) #ensure non-stopwords remain
        self.assertEqual(len(cleaned2), 0) #ensure all stopwords removed

        #model prediction
        rating1 = RFR_AI_model_predict([self.comment])[0]
        rating2 = RFR_AI_model_predict([self.stopWords])[0]
        self.assertTrue(1 <= rating1 <= 10) #check rating falls within range 0 - 10
        self.assertTrue(1 <= rating2 <= 10) #check rating falls within range 0 - 10

    def test_integration_sentiment_analysis(self):
        avg_rating = RFR_avg_rating([self.comment]) #integrate text-preprocessing and model prediction
        self.assertTrue(1 <= float(avg_rating) <= 10) #check rating falls within range 0 - 10

    def test_unit_emotion(self):
        dict1 = {"a": 1, "b": 0}
        dict2 = {"a": 2, "b": 3}
        self.assertEqual(merge_dict(dict1, dict2), {"a":3, "b":3}) #ensure merging done correctly

        self.assertEqual(list(get_emotion_dict(self.comment).keys()), ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']) #ensure all emotions present in comment

    def test_integration_emotion(self):
        emotions = emotion_chart([self.comment]) #integrate merge_dict and get_emotion_dict

        self.assertEqual(sum(emotions), 1) #ensure total breakdown equals to number of entry
        self.assertEqual(len(emotions), 5) #ensure 5 values, each for one emotion

        self.assertTrue(type(convert_emotion_chart_to_str(emotions)) is str) #ensure final output in a string

    def test_system_testing_scraping_sentiment(self):
        pass


