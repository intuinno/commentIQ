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
# # #
# makeCommentsListConsideringNoPicksInArticle("data/comments_study.csv", "data/articles.csv", "data/trainInputComments.csv", "data/testInputComments.csv")
# ComputeCommentLength("data/comments_study.csv", "data/comments_length_feature.csv")

makeVWInputDataset( "resultBackup/trainInputComments.csv", "resultBackup/comment_study_article_relevance.csv", "resultBackup/comment_study_comment_conversational_relevance.csv","featureFileList.txt","data/trainInput.vw")
#
makeVWInputDataset( "resultBackup/testInputComments.csv", "resultBackup/comment_study_article_relevance.csv", "resultBackup/comment_study_comment_conversational_relevance.csv", "featureFileList.txt","data/testInput.vw")
cmd = 'vw  data/trainInput.vw -f L1_model.vw --binary  -l 0.01 -c -k  --passes 100 --l1 0.0000001 '
p = os.system(cmd)

cmd = '../vowpal_wabbit/utl/vw-varinfo   -f L1_model.vw --binary  -l 0.01 -c -k  --passes 100 --l1 0.0000001 data/trainInput.vw > varinfo.txt'
p = os.system(cmd)

cmd = 'vw data/trainInput.vw -f model.vw --binary  -l 0.01 -c -k  --passes 100  --feature_mask L1_model.vw'
p = os.system(cmd)

cmd = '../vowpal_wabbit/utl/vw-varinfo   -f model.vw --binary  -l 0.01 -c -k  --passes 100 --feature_mask L1_model.vw data/trainInput.vw > varinfoMask.txt'
p = os.system(cmd)

cmd = 'vw -t data/testInput.vw -i  model.vw -p data/prediction.vw --binary'

p = os.system(cmd)
evaluatePrediction("data/comments_study.csv","data/prediction.vw","data/result.csv")


makeGatherplotInput( "resultBackup/trainInputComments.csv", "resultBackup/comment_study_article_relevance.csv", "resultBackup/comment_study_comment_conversational_relevance.csv","data/result.csv","featureFileList.txt", "data/gatherplotFeatures.csv")


endTime = datetime.now()

print "start Time is " + str(startTime)
print "end Time is " + str(endTime)
print "Duration is " + str(endTime - startTime)
