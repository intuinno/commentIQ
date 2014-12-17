__author__ = 'intuinno'

import csv
import os
from collections import Counter
import random


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

def makeVWInputDataset(commentFile, articleRelevanceFile, conversationalRelevanceFile, length_feature_file, grammarFeatureFile, grammarErrorCodeFile, vwInputfile):

    csvFile = open(commentFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    comments = {}

    commentCount = 0
    editorCommentCount = 0

    for row in csvReader:

        if row['editorsSelection'] == '1':
            if row['commentID'] not in comments:
                comments[row['commentID']] = {}
                comments[row['commentID']]['commentID'] = row['commentID']
                comments[row['commentID']]['editorsSelection'] = 1
                editorCommentCount += 1

        else:
            if row['commentID'] not in comments:
                comments[row['commentID']] = {}
                comments[row['commentID']]['commentID'] = row['commentID']
                comments[row['commentID']]['editorsSelection'] = -1
                commentCount += 1


    csvFile = open(articleRelevanceFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if row[0] in comments:
            comments[row[0]]['articleRelevance'] = row[13]

    csvFile = open(conversationalRelevanceFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if row[0] in comments:
             comments[row[0]]['conversationalRelevance'] = row[13]

    csvFile = open(length_feature_file, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if row['id'] in comments:
             comments[row['id']]['length'] = row['length']


    csvFile = open(grammarFeatureFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if row['commentID'] in comments:
             comments[row['commentID']]['spellingError'] = row['spellingError']
             comments[row['commentID']]['grammarError'] = row['grammarError']


    csvFile = open(grammarErrorCodeFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"', skipinitialspace=True, quoting=csv.QUOTE_NONE)

    for row in csvReader:
        if row['commentID'] in comments:
             comments[row['commentID']]['grammarErrorCode'] = row['spellingError']


    vwInputFileWriter =open(vwInputfile, 'w+')

    comments = comments.items()
    random.shuffle(comments)

    for (commentID, comment) in comments:
        row = str(comment['editorsSelection'])  + " '" + str(comment['commentID'])  + ' | ' + 'AR:'+ str(comment['articleRelevance'])


        if 'conversationalRelevance' in comment:
            row +=  ' CR:' + str( comment['conversationalRelevance'] )


        row += ' | ' + 'Length:' + str(comment['length'])
        # row.extend(['|',  'grammarError:' + str(comment['grammarError']) , 'spellingError:' + str(comment['spellingError'])])

        row += ' | ' +   str(comment['grammarErrorCode']) + '\n' # , 'spellingError:' + str(comment['spellingError'])])
        vwInputFileWriter.write(row)

    vwInputFileWriter.close()

    return comments

def howManyPickForAnArticle(commentFile, articleFile):
    # Read the articleFile
    csvFile = open(articleFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

	# Read each line and process it
    articleURLDictionary = {}
    count = 0
    for row in csvReader:
        articleURLDictionary[row['articleURL']] = Counter()
        articleURLDictionary[row['articleURL']]['id'] = row['articleID']
        articleURLDictionary[row['articleURL']]['selectionCount'] = 0
        articleURLDictionary[row['articleURL']]['commentCount'] = 0
        count += 1

    print "The Number of Article : " + str(count)


    # Read the commentFile
    csvFile = open(commentFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if row['editorsSelection'] == '1':
            articleURLDictionary[row['articleURL']]['selectionCount'] += 1

        articleURLDictionary[row['articleURL']]['commentCount'] += 1

    return articleURLDictionary

def writeHowManyPicksForAnArticle():

    articleURLDictionary = howManyPickForAnArticle("data/comments_study.csv", "data/articles.csv")

    if not os.path.isdir('result'):
        os.makedirs('result')


    with open('result/howManyPicksForAnArticle.csv','w+') as csvFile:

        fieldnames = ['id', 'commentCount', 'selectionCount']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, restval='0')
        writer.writeheader()

        for (articleID, article) in articleURLDictionary.items():
            print str(article['id']) + "\t NumSelection: " + str(article['selectionCount'])  + "\t NumComment: " + str(article['commentCount'])
            writer.writerow(article)

    return articleURLDictionary

def makeCommentsListConsideringNoPicksInArticle(commentFile, articleFile, trainFile, testFile):

    articleURLDictionary = howManyPickForAnArticle(commentFile, articleFile)

    selectedCommentsList = []
    notSelectedCommentsList = []

    csvFile = open(commentFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    for row in csvReader:
        if row['editorsSelection'] == '1':
            selectedCommentsList.append(row)
        else:
            if articleURLDictionary[row['articleURL']]['selectionCount'] > 0:
                notSelectedCommentsList.append(row)

    random.shuffle(selectedCommentsList)

    crossIndex = int(len(selectedCommentsList) * 0.8)

    trainSelectedCommentsList = selectedCommentsList[:crossIndex]
    testSelectedCommentsList = selectedCommentsList[crossIndex:]

    trainNotSelectedCommentsList = random.sample(notSelectedCommentsList, len(trainSelectedCommentsList))
    testNotSelectedCommentsList = random.sample(notSelectedCommentsList, len(testSelectedCommentsList))

    csvFile = open(trainFile, 'w+')
    csvWriter = csv.DictWriter(csvFile, fieldnames=csvReader.fieldnames)

    csvWriter.writeheader()

    for i in range(len(trainSelectedCommentsList)):
        csvWriter.writerow(trainSelectedCommentsList[i])
        csvWriter.writerow(trainNotSelectedCommentsList[i])

    csvFile = open(testFile, 'w+')
    csvWriter = csv.DictWriter(csvFile, fieldnames=csvReader.fieldnames)

    csvWriter.writeheader()

    for i in range(len(testSelectedCommentsList)):
	csvWriter.writerow(testSelectedCommentsList[i])
	csvWriter.writerow(testNotSelectedCommentsList[i])

def evaluatePrediction( commentFile, predictionFile, resultFile):

    csvFile = open(commentFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    comments = {}

    for row in csvReader:
        if row['commentID'] not in comments:
            comments[row['commentID']] = {}
        comments[row['commentID']]['commentID'] = row['commentID']

        if row['editorsSelection'] == '1':
            comments[row['commentID']]['editorsSelection'] = 1

        else:
            comments[row['commentID']]['editorsSelection'] = -1


    csvFile = open(predictionFile, 'Ur')
    csvReader = csv.reader(csvFile, delimiter=' ')

    with open(resultFile,'w+') as csvFile:

        fieldnames = ['id', 'editorsSelection', 'prediction']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, restval='0')
        writer.writeheader()

        truePositive = 0
        falsePositive = 0
        trueNegative = 0
        falseNegative = 0

        comment = {}

        for row in csvReader:
            comment['id'] = row[1]
            comment['editorsSelection'] = comments[row[1]]['editorsSelection']
            comment['prediction'] = row[0]
            writer.writerow(comment)

            if float(row[0]) == -1:
                if comment['editorsSelection'] == -1:
                    trueNegative += 1
                elif comment['editorsSelection'] == 1:
                    falseNegative += 1
                else:
                    print "You should not see me. There is something wrong in comments " + comments[row[1]]
            elif float(row[0]) == 1:
                if comment['editorsSelection'] == 1:
                    truePositive += 1
                elif comment['editorsSelection'] == -1:
                    falsePositive += 1
                else:
                    print "You should not see me. There is something wrong in comments " + comments[row[1]]
            else:
                    print "You should not see me. There is something wrong in comments " + comments[row[1]]


        print "True Positive: " + str(truePositive)
        print "False Positive: " + str(falsePositive)
        print "True Negative: " + str(trueNegative)
        print "False Negative: " + str(falseNegative)

        if (truePositive + falsePositive) == 0:
            print "something wrong"
        else:
            print "Precision: " + str( truePositive / (truePositive+ falsePositive+0.1))
        if (truePositive + falseNegative) == 0:
            print "something wrong"
        else:
            print "Recall: " + str(truePositive / (truePositive + falseNegative+0.1))

def makeCommentsFiles(commentFile):

    if not os.path.isdir('commentFiles'):
        os.makedirs('commentFiles')

    selectedCommentsList = []
    notSelectedCommentsList = []

    csvFile = open(commentFile, 'Ur')
    csvReader = csv.DictReader(csvFile, delimiter=',', quotechar='"')

    csvFile = open('commentFiles/comments.list', 'w+')
    listWriter = csv.writer(csvFile)

    cwd = os.getcwd()

    for row in csvReader:
        commentID = row['commentID']
        commentBody = row['commentBody']


        filename = cwd + '/commentFiles/' + commentID + '.comment'
        listWriter.writerow([filename])

        csvFile = open(filename, 'w+')
        csvFile.write(commentBody)

