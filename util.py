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


                # # commentID,commentTitle,commentBody,approveDate,recommendationCount,display_name,location,commentQuestion,commentSequence,status,articleURL,editorsSelection,in_study
	# csvFile = open("data/comments_study.csv", 'Ur')
	# csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
	# comments  = {}
	# for row in csvReader:
	# 	if csvReader.line_num > 1:
	# 		comments[row[0]] = row
    #
	# # The number of documents is the number of comments
	# nDocuments = len(comments)
    #
    # csvFile = open("data/articles.csv", 'Ur')
	# csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
	# articles  = {}
	# for row in csvReader:
	# 	if csvReader.line_num > 1:
	# 		# key on the article URL
	# 		articles[row[3]] = row
    #
	# # output file will have have a final row that is the comment-article relevance
	# fileWriter = csv.writer(open("data/comment_study_article_relevance.csv", "w+"),delimiter=",")
	# # for each article and the comments on each
	# for (j, (commentID, comment)) in enumerate(comments.items()):
	# 	print "comment: " + str(j)
	# 	ct = CleanAndTokenize(comment[2].decode("utf8"))
	# 	ct = [w for w in ct if w not in stopword_list]
	# 	comment_stemmed_tokens = [porter.stem(t) for t in ct]
	# 	comment_stemmed_tokens_fd  = FreqDist(comment_stemmed_tokens)
    #


makeCrossValidationDataset("data/comments_study.csv", "data/articles.csv")