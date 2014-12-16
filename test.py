__author__ = 'intuinno'
from processComments import *
from util import *
import os



# Computes the length of comments
# ComputeCommentLength("data/comments_study.csv", "data/comments_length_feature.csv")
# howManyPickForAnArticle("data/comments_study.csv", "data/articles.csv")
# evaluatePrediction("smallData/comments_study.csv","smallData/prediction.vw","smallData/result.csv")

# makeVWInputDataset(500, "data/comments_study.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv", "data/input.vw")

# makeCommentsListConsideringNoPicksInArticle("data/comments_study.csv", "data/articles.csv", "data/trainInputComments.csv", "data/testInputComments.csv")
#
# makeVWInputDataset( "data/trainInputComments.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv", "data/inputTrain.vw")
#
# makeVWInputDataset( "data/testInputComments.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv", "data/inputTest.vw")

#
# cmd = 'vw -d data/trainInput.vw -f  model.vw --binary '
# p = os.system(cmd)
#
# cmd = 'vw -t data/testInput.vw -i  model.vw -p data/prediction.vw --binary '
# p = os.system(cmd)
#
# evaluatePrediction("data/comments_study.csv","data/prediction.vw","data/result.csv")

makeCommentsFiles("smallData/comments_study.csv")
