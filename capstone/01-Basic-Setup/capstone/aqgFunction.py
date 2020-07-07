access_key='AKIAQPXCCTPJBHJDWJES'
secret_access_key='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'
import boto3
import os
client=boto3.client('s3',aws_access_key_id=access_key,
                    aws_secret_access_key=secret_access_key)
s3 = boto3.resource(
    's3',
   
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key
)
upload_file_bucket='chinu-dummy-bucket'


import spacy
from capstone.clause import *
from capstone.nonClause import *
from capstone.aqgFunction import *
from capstone.identification import *
from capstone.questionValidation import *
from capstone.nlpNER import nerTagger
from flask import current_app
import secrets

class AutomaticQuestionGenerator():
    filename=secrets.token_hex(8)
    # AQG Parsing & Generate a question
    def aqgParse(self, sentence):

        #nlp = spacy.load("en")
        nlp = spacy.load('en_core_web_md')

        singleSentences = sentence.split(".")
        questionsList = []
        if len(singleSentences) != 0:
            for i in range(len(singleSentences)):
                segmentSets = singleSentences[i].split(",")

                ner = nerTagger(nlp, singleSentences[i])

                if (len(segmentSets)) != 0:
                    for j in range(len(segmentSets)):
                        try:
                            questionsList += howmuch_2(segmentSets, j, ner)
                        except Exception:
                            pass

                        if clause_identify(segmentSets[j]) == 1:
                            try:
                                questionsList += whom_1(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += whom_2(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += whom_3(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += whose(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += what_to_do(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += who(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += howmuch_1(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += howmuch_3(segmentSets, j, ner)
                            except Exception:
                                pass


                            else:
                                try:
                                    s = subjectphrase_search(segmentSets, j)
                                except Exception:
                                    pass

                                if len(s) != 0:
                                    segmentSets[j] = s + segmentSets[j]
                                    try:
                                        questionsList += whom_1(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += whom_2(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += whom_3(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += whose(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += what_to_do(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += who(segmentSets, j, ner)
                                    except Exception:
                                        pass

                                    else:
                                        try:
                                            questionsList += what_whom1(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += what_whom2(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += whose(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += howmany(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += howmuch_1(segmentSets, j, ner)
                                        except Exception:
                                            pass

                questionsList.append('\n')
        return questionsList



    def DisNormal(self, str):
        print("\n")
        print("------X------")
        print("Start  output:\n")

        count = 0
        out = ""

        for i in range(len(str)):
            count = count + 1
            print("Q-0%d: %s" % (count, str[i]))

        print("")
        print("End  OutPut")
        print("-----X-----\n\n")


    # AQG Display the Generated Question
    def display(self, str):
        print("\n")
        print("------X------")
        print("Start  output:\n")

        count = 0
        out = ""
        for i in range(len(str)):
            if (len(str[i]) >= 3):
                if (hNvalidation(str[i]) == 1):
                    if ((str[i][0] == 'W' and str[i][1] == 'h') or (str[i][0] == 'H' and str[i][1] == 'o') or (
                            str[i][0] == 'H' and str[i][1] == 'a')):
                        WH = str[i].split(',')
                        if (len(WH) == 1):
                            str[i] = str[i][:-1]
                            str[i] = str[i][:-1]
                            str[i] = str[i][:-1]
                            str[i] = str[i] + "?"
                            count = count + 1

                            if (count < 10):
                                print("Q-0%d: %s" % (count, str[i]))
                                out += "Q-0" + count.__str__() + ": " + str[i] + "\n"

                            else:
                                print("Q-%d: %s" % (count, str[i]))
                                out += "Q-" + count.__str__() + ": " + str[i] + "\n"

        print("")
        print("End  OutPut")
        print("-----X-----\n\n")
        print("ssssssssssssssssssssssssssssssssssss")
        file=self.filename+r'.txt'
        s3.Object('chinu-dummy-bucket', file).put(Body=out)
        return 0
    

