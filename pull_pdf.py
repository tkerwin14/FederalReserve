'''
Program: pull_pdf.py
Author: Tess Kerwin
Date Created: 11/8/2017
Purpose: 
'''

import requests
import os
from datetime import date
from datetime import timedelta
import pdb

baseUrl = "https://www.federalreserve.gov/monetarypolicy/files"

#The dates to start the testing for pdfs: 
startDates = [{"mnth": 1, "day": 26}, {"mnth": 3, "day": 18}, 
              {"mnth": 4, "day": 29}, {"mnth": 6, "day": 24}, 
              {"mnth": 8, "day": 5},  {"mnth": 9, "day": 16}, 
              {"mnth": 10, "day": 28}, {"mnth": 12, "day": 16}]



def savePDF(pdfName): 
    '''
    Parameters - pdfName - string 
    Returns a boolean depending on whether we could download the PDF
    '''
    #Tries to fetch URL: 
    url = os.path.join(baseUrl, pdfName)
    response = requests.get(url)
    #If success, download the contents and return true, otherwise false
    if (response.status_code == 200):
        with open(os.path.join("./files/", pdfName), "wb") as f:
            f.write(response.content)
        return True
    else: 
        return False 
    
def checkDays(startDt, plus, num): 
    '''
    Parameters: startDt - date object - date we want to start testing
                plus - boolean - whether we should go forward or backward
                num - int - the number of days to go forward/backward
    Tests out the days for the FOMC meeting by trying to download the PDF, continues 
    until it either finds it or number of days runs out, returns a boolean for the 
    whether we were successful. 
    '''
    dt = startDt
    foundDownload = False
    cnt = 0
    while (~foundDownload) & (cnt < num): 
        dateCheck = str(dt.year) + str(dt.month).zfill(2) + str(dt.day).zfill(2)
        meetingPdf = "FOMC" + dateCheck + "meeting.pdf"
        foundDownload = savePDF(meetingPdf)
        dt = dt + timedelta(days=1) if plus else dt - timedelta(days=1)
        cnt = cnt + 1
    return foundDownload
        

def pullYear(year): 
    '''
    Parameters:  year - string 
    Loops through all the startdates, tries to download the pdfs for each, 
    returns a list of any dates that were not successfully downloaded
    '''
    unfound = [] 
    for dt in startDates: 
        dtCheck = date(year, dt["mnth"], dt["day"])
        foundDownload = checkDays(dtCheck, True, 15)
        #A bit clunky, but then check the days going backward
        if (foundDownload == False): 
            foundDownloadNeg = checkDays(dtCheck, False, 15)
            if (foundDownloadNeg == False): 
                unfound.append(dtCheck)
    return unfound


def pullDates(dtLst): 
    '''
    Parameters - dtLst - the list of dates you want to check
    Same as pullYear except we have a specific date with attached year in mind.
    '''
    unfound = []
    for dt in dtLst:
        foundDownload = checkDays(dt, True, 30)
        if (foundDownload == False): 
            foundDownloadNeg = checkDays(dt, False, 30)
            if (foundDownloadNeg == False):
                unfound.append(dt)
    return unfound


def pullYears(): 
    '''
    Loops through all years, pulls the PDFs in each one, returns a list of
    any problem dates.
    '''
    unfound = []
    years = range(1990, 2012)
    for year in years: 
        unFoundYear = pullYear(year)
        unfound.extend(unFoundYear)
    return unfound
    
firstPull = pullYears()
secondPull = pullDates(firstPull)
assert len(secondPull) == 0
            
