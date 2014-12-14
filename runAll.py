__author__ = 'intuinno'


from processComments import *
from util import *
import os



startTime = datetime.now()

# makeCrossValidationDataset("data/comments_study.csv", "data/articles.csv")

# ComputeVocabulary("data/comments_study.csv","data/vocab.csv")
# Compute similarities requires that the vocab file already by computed
# vocabFilename, commentsFilename, articleFilename, articleRelevanceFilename
# ComputeCommentArticleRelevance("data/vocab.csv","data/comments_study.csv","data/articles.csv", "data/comment_study_article_relevance.csv")
# ComputeCommentConversationalRelevance("data/vocab.csv","data/comments_study.csv", "data/comment_study_comment_conversational_relevance.csv")
# #
# makeCommentsListConsideringNoPicksInArticle("data/comments_study.csv", "data/articles.csv", "data/trainInputComments.csv", "data/testInputComments.csv")
#
makeVWInputDataset( "data/trainInputComments.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv", "data/trainInput.vw")
#
makeVWInputDataset( "data/testInputComments.csv", "data/comment_study_article_relevance.csv", "data/comment_study_comment_conversational_relevance.csv", "data/testInput.vw")
#
cmd = 'vw -d data/trainInput.vw -f  model.vw --binary '
p = os.system(cmd)

cmd = 'vw -t data/testInput.vw -f  model.vw -p data/prediction.vw --binary '
p = os.system(cmd)

evaluatePrediction("data/comments_study.csv","data/prediction.vw","data/result.csv")



endTime = datetime.now()

print "start Time is " + str(startTime)
print "end Time is " + str(endTime)
print "Duration is " + str(endTime - startTime)
