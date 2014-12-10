__author__ = 'intuinno'
from processComments import *

# ComputeVocabulary("smallData/comments_study.csv", "smallData/vocab.csv")

# Compute similarities requires that the vocab file already by computed
#ComputeCommentArticleRelevance()
#ComputeCommentConversationalRelevance()

ComputeVocabulary("smallData/comments_study.csv","smallData/vocab.csv")
# startTime = datetime.now()
#
# # Compute similarities requires that the vocab file already by computed
# ComputeCommentArticleRelevance()
# ComputeCommentConversationalRelevance()
#
# endTime = datetime.now()
#
# print "start Time is " + str(startTime)
# print "end Time is " + str(endTime)
# print "Duration is " + str(endTime - startTime)