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

def makeSmallDataset(commentFile, articleFile):

    #Definition of constants
    constArticleNumber = 5

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




# makeCrossValidationDataset("data/comments_study.csv", "data/articles.csv")
makeSmallDataset("data/comments_study.csv", "data/articles.csv")