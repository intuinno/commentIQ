__author__ = 'intuinno'
from processComments import *
from util import *
import os



# howManyPickForAnArticle("data/comments_study.csv", "data/articles.csv")
# evaluatePrediction("smallData/comments_study.csv","smallData/prediction.vw","smallData/result.csv")

# makeVWInputDataset(500, "data/comments_study.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv", "data/input.vw")

makeCommentsListConsideringNoPicksInArticle("data/comments_study.csv", "data/articles.csv")