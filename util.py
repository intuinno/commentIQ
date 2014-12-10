__author__ = 'intuinno'

import csv
import os


def makeCrossValidationDataset(commentFile, articleFile):

    #Definition of constants
    constFoldNumber = 5

    #Open the output file based on the fold number

    if not os.path.isdir('crossData'):
        os.makedirs('crossData')

    trainWriterList = []
    testWriterList = []
    for i in range(constFoldNumber):
        testFileName = "crossData/articleTest" + str(i) +".csv"
        trainFileName = "crossData/articleTrain" + str(i) + ".csv"
        # output file will have have a final row that is the comment-article relevance
        testWriter = csv.writer(open(testFileName, "w+"),delimiter=",")
        trainWriter = csv.writer(open(trainFileName, "w+"),delimiter=",")

        trainWriterList.append( trainWriter )
        testWriterList.append(testWriter)

	# Read the articleFile
	csvFile = open(articleFile, 'Ur')
	csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

	# Read each line and process it
    articleURLDictionary = {}

    for row in csvReader:
        if csvReader.line_num == 1:
            for i in range(constFoldNumber):
                # print i
                trainWriterList[i].writerow(row)
                testWriterList[i].writerow(row)
        else:
            for i in range(constFoldNumber):
                if i == csvReader.line_num%constFoldNumber:
                    testWriterList[i].writerow(row)
                    articleURLDictionary[row[3]] = i

                else:
                    trainWriterList[i].writerow(row)


    trainWriterList = []
    testWriterList = []
    for i in range(constFoldNumber):
        testFileName = "crossData/commentTest" + str(i) +".csv"
        trainFileName = "crossData/commentTrain" + str(i) + ".csv"
        # output file will have have a final row that is the comment-article relevance
        testWriter = csv.writer(open(testFileName, "w+"),delimiter=",")
        trainWriter = csv.writer(open(trainFileName, "w+"),delimiter=",")

        trainWriterList.append( trainWriter )
        testWriterList.append(testWriter)

    # Read the commentFile
	csvFile = open(commentFile, 'Ur')
	csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if csvReader.line_num == 1:
            for i in range(constFoldNumber):
                # print i
                trainWriterList[i].writerow(row)
                testWriterList[i].writerow(row)
        else:
            for i in range(constFoldNumber):

                articleGroup = articleURLDictionary[row[10]]

                if i == articleGroup:
                    testWriterList[i].writerow(row)
                else:
                    trainWriterList[i].writerow(row)

def makeSmallDataset(commentFile, articleFile, numArticle):

    #Definition of constants
    constArticleNumber = numArticle

    #Make sure 'smallData' directory exists
    if not os.path.isdir('smallData'):
        os.makedirs('smallData')

    # Read the articleFile
    csvFile = open(articleFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    smallArticleFileName = "smallData/articles.csv"
    smallArticleWriter = csv.writer(open(smallArticleFileName, "w+"),delimiter=",")

	# Read each line and process it
    articleURLDictionary = {}
    count = 0
    for row in csvReader:
        if csvReader.line_num == 1:
            smallArticleWriter.writerow(row)
        elif count < constArticleNumber:
            smallArticleWriter.writerow(row)
            articleURLDictionary[row[3]] = True
            count += 1

    smallCommentFileName = "smallData/comments_study.csv"
    smallCommentWriter = csv.writer(open(smallCommentFileName, "w+"),delimiter=",")

    # Read the commentFile
    csvFile = open(commentFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if csvReader.line_num == 1:
            smallCommentWriter.writerow(row)
        elif row[10] in articleURLDictionary:
            smallCommentWriter.writerow(row)

def makeVWInputDataset(commentFile, articleRelevanceFile, conversationalRelevanceFile, vwInputfile):

    csvFile = open(commentFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    comments = {}

    for row in csvReader:
        if row['commentID'] not in comments:
            comments[row['commentID']] = {}
            comments[row['commentID']]['commentID'] = row['commentID']

            if row['editorsSelection'] == 1:
                comments[row['commentID']]['editorsSelection'] = 1
            else:
                comments[row['commentID']]['editorsSelection'] = -1


    csvFile = open(articleRelevanceFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        comments[row[0]]['articleRelevance'] = row[13]

    csvFile = open(conversationalRelevanceFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        comments[row[0]]['conversationalRelevance'] = row[13]

    vwInputFileName =vwInputfile
    vwInputFileWriter = csv.writer(open(vwInputFileName, "w+"),delimiter=" ")

    for (commentID, comment) in comments.items():
        row = [comment['editorsSelection'] ,"'" + str(comment['commentID']) ,  '|' , 'AR:'+ str(comment['articleRelevance']) ]

        if 'conversationalRelevance' in comment:
            row.append( 'CR:' + str( comment['conversationalRelevance'] ) )
        vwInputFileWriter.writerow(row)

    return comments





# def runExperiment(trainingCommentFile, trainingArticleFile, testCommentFile, testArticleFile, filePrefix='wsd_vw', quietVW=False):
#     trainFileVW = filePrefix + '.tr'
#     testFileVW  = filePrefix + '.te'
#     modelFileVW = filePrefix + '.model'
#
#     trainingCorpus = readWSDCorpus(trainingFile
#
#     ComputeVocabulary(trainingCommentFile,"smallData/vocab.csv")
# # Compute similarities requires that the vocab file already by computed
# # vocabFilename, commentsFilename, articleFilename, articleRelevanceFilename
#     ComputeCommentArticleRelevance("smallData/vocab.csv","smallData/comments_study.csv","smallData/articles.csv", "smallData/comment_study_article_relevance.csv")
#     ComputeCommentConversationalRelevance("smallData/vocab.csv","smallData/comments_study.csv", "smallData/comment_study_comment_conversational_relevance.csv")
#
#     testCorpus = None if testFile is None else readWSDCorpus(testFile)
#
#     print 'collecting translation table'
#     ttable = collectTranslationTable(trainingCorpus)
#
#     print 'generating classification data'
#     generateVWData(trainingCorpus, ttable, getFFeatures, getEFeatures, getPairFeatures, trainFileVW)
#     if testCorpus is not None:
#         generateVWData(testCorpus, ttable, getFFeatures, getEFeatures, getPairFeatures, testFileVW )
#
#     trainVW(trainFileVW, modelFileVW, quietVW)
#
#     train_pred = testVW(trainFileVW, modelFileVW, quietVW)
#     train_acc = evaluatePredictions(trainingCorpus, ttable, train_pred)
#
#     test_pred = None
#     test_acc = 0
#     if testCorpus is not None:
#         test_pred = testVW(testFileVW , modelFileVW, quietVW)
#         test_acc  = evaluatePredictions(testCorpus, ttable, test_pred)
#
#     return (train_acc, test_acc, test_pred)


# makeCrossValidationDataset("data/comments_study.csv", "data/articles.csv")
# makeSmallDataset("data/comments_study.csv", "data/articles.csv",10 )
