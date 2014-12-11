__author__ = 'intuinno'


from processComments import *
from util import *
import os



startTime = datetime.now()

# makeCrossValidationDataset("data/comments_study.csv", "data/articles.csv")

ComputeVocabulary("data/comments_study.csv","data/vocab.csv")
# Compute similarities requires that the vocab file already by computed
# vocabFilename, commentsFilename, articleFilename, articleRelevanceFilename
ComputeCommentArticleRelevance("data/vocab.csv","data/comments_study.csv","data/articles.csv", "data/comment_study_article_relevance.csv")
ComputeCommentConversationalRelevance("data/vocab.csv","data/comments_study.csv", "data/comment_study_comment_conversational_relevance.csv")

print makeVWInputDataset("data/comments_study.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv","smallData/input.vw")


cmd = 'vw -d data/input.vw -f  model.vw -p data/prediction.vw --binary '


p = os.system(cmd)

endTime = datetime.now()

print "start Time is " + str(startTime)
print "end Time is " + str(endTime)
print "Duration is " + str(endTime - startTime)