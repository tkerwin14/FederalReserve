'''
Program: fed_pdf.py
Author: Tess Kerwin
Date Created: 11/7/2017
Purpose:
'''


import slate
import pandas as pd
import re
import os

def separateOutSections(pdfName):
    '''
    Parameters: pdfName - string of pdf url
    Opens the PDF, pulls the text, breaks it out by speaker,
    returns a dataframe with the variables:
    speakerTalk - content
    speakerType - male (MR), female (MS), or chairman (CH)
    transcriptName - transcript pulled from
    '''
    #Open the PDF
    with open(pdfName) as f:
        pages = slate.PDF(f)
    #Create one long string:
    allTxt = " ".join(pages)
    #Get list of all matches for speakers:
    allMatches = createMatchList(allTxt)
    #Break out the sections:
    sections = []
    for i in range(0, len(allMatches)-1):
        speakerObj = {}
        speakerSection = allTxt[allMatches[i]:allMatches[i+1]]
        speakerType = speakerSection[0:2]
        speakerObj["speakerTalk"] = speakerSection
        speakerObj["speakerType"] = speakerType
        sections.append(speakerObj)
    #Put into pandas df:
    sectionDf = pd.DataFrame(sections)
    sectionDf['transcriptName'] = pdfName
    return sectionDf

def createMatchList(allTxt):
    '''
    Parameters - allTxt - string
    Returns a list of the matches for speakers (defined as MR, MS, and CHAIRMAN).
    '''
    #Find the matches for MR, MS, and CHAIRMAN
    mrMatch = [m.start() for m in re.finditer(r"\bMR\b", allTxt)]
    msMatch = [m.start() for m in re.finditer(r"\bMS\b", allTxt)]
    chairMatch = [m.start() for m in re.finditer(r"\bCHAIRMAN\b", allTxt)]
    #Create a version with all matches:
    #Note: you can do OR, but easier to debug matching by doing separately
    allMatches = mrMatch
    allMatches.extend(msMatch)
    allMatches.extend(chairMatch)
    allMatches.sort()
    #The last one will be the last txt in doc
    allMatches.append(len(allTxt)-1)
    return allMatches

def getAllMeetings():
    '''
    Gets all the files from the PDF location, gets a dataframe of content
    for each PDF, and then returns the appended dataframe.
    '''
    allPdfs = os.listdir("./files/")[1:]
    print(allPdfs)
    df = pd.DataFrame()
    for pdf in allPdfs:
        pdfPath = os.path.join("./files/", pdf)
        pdfMeeting = separateOutSections(pdfPath)
        df = df.append(pdfMeeting)
    return df

df = getAllMeetings()
