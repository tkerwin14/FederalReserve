# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 12:46:06 2019

@author: tessk
"""

import requests 
from bs4 import BeautifulSoup
import os


def pullYearPage(yearStr): 
    '''
    Parameters: 
    yearStr - string - a 4 character string of the year you want to pull
    Returns a BeautifulSoup object with the page from the Fed Board pulled.
    '''
    #Create the urL:
    baseUrl = "https://www.federalreserve.gov/monetarypolicy/fomchistorical" 
    url = baseUrl + yearStr + ".htm" 
    #Try to get the page:
    res = requests.get(url)
    #Convert HTML into bs
    if (res.status_code == 200): 
        return BeautifulSoup(res.text, features="lxml")
    else: 
        return None


def findTranscriptUrls(bs): 
    '''
    Parameters: 
    bs - BeautifulSoup - the beautiful soup object of the page year
    Returns a list of the meeting transcript urls for that year
    '''
    #Get all the links:
    aLinks = bs.find_all("a")
    aHref = [x.get('href') for x in aLinks]
    aHref = [x for x in aHref if x != None]
    #Subset to the files: 
    fileUrl = "/monetarypolicy/files/"
    aHref = [x for x in aHref if x.startswith(fileUrl)]
    aHref = [x for x in aHref if x[-11:] == "meeting.pdf"]
    assert len(aHref) >= 8
    return aHref

def savePDF(pdfName): 
    '''
    Parameters: 
    pdfName - string - the name of the pdf you want to pull
    Returns a boolean depending on whether we could download the PDF.
    '''
    #Creates an output directory if necessary: 
    if os.path.isdir("./files/") == False:
        os.mkdir("./files/")
    #Tries to fetch URL: 
    baseUrl = "https://www.federalreserve.gov"
    url = baseUrl + pdfName
    response = requests.get(url)
    #If success, download the contents and return true, otherwise false
    fileName = pdfName.split("/")[-1]
    if (response.status_code == 200):
        with open(os.path.join("./files/", fileName), "wb") as f:
            f.write(response.content)
        return True
    else: 
        return False 

def pullYears(startYear, endYear): 
    '''
    Parameters: 
    startYear - int - the year you want to start the pull
    endYear - int - the year you want to end the pull
    Returns the list of pdf names along with a boolean about whether the file
    was sucessfully download.
    '''
    unfound = []
    years = range(startYear, endYear + 1)
    for year in years: 
        yearbs = pullYearPage(str(year))
        pdfUrls = findTranscriptUrls(yearbs)
        saveUrl = [savePDF(url) for url in pdfUrls]
        unfoundUrls = [{"fileName": pdfUrls[i], "saved": saveUrl[i]} for i in range(0, len(pdfUrls))]
        unfound.extend(unfoundUrls)
    return unfound
    

pdfLst = pullYears(1990, 2012)
