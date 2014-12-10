__author__ = 'intuinno'


from processComments import *
from util import *
import os



startTime = datetime.now()

makeCrossValidationDataset("data/comments_study.csv", "data/articles.csv")

ComputeVocabulary("smallData/comments_study.csv","smallData/vocab.csv")
# Compute similarities requires that the vocab file already by computed
# vocabFilename, commentsFilename, articleFilename, articleRelevanceFilename
ComputeCommentArticleRelevance("smallData/vocab.csv","smallData/comments_study.csv","smallData/articles.csv", "smallData/comment_study_article_relevance.csv")
ComputeCommentConversationalRelevance("smallData/vocab.csv","smallData/comments_study.csv", "smallData/comment_study_comment_conversational_relevance.csv")

print makeVWInputDataset("smallData/comments_study.csv", "smallData/comment_study_article_relevance.csv", "smallData/comment_study_comment_conversational_relevance.csv")


cmd = 'vw -d smallData/vwInputFile -f prediction.vw'


p = os.system(cmd)

endTime = datetime.now()

print "start Time is " + str(startTime)
print "end Time is " + str(endTime)
print "Duration is " + str(endTime - startTime)