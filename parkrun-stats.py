# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 20:39:05 2018

@author: bryan
"""

import pandas as pd
import numpy as np

def convertTimes(serParkrunnerTimeSplit):
    runnerTimesinSecs = []
    numRunners = len(serParkrunnerTimeSplit)
    for i in range(0,numRunners):
        if str(serParkrunnerTimeSplit[i]) == 'nan':
            mins = 0
            secs = 0
        else:
            if len(serParkrunnerTimeSplit[i]) == 2:
                hours = 0
                mins = serParkrunnerTimeSplit[i][0]
                secs = serParkrunnerTimeSplit[i][1]
            else:
                tmpval = float(serParkrunnerTimeSplit[i][0])
                if tmpval < 2:
                    hours = serParkrunnerTimeSplit[i][0]
                    mins = serParkrunnerTimeSplit[i][1]
                    secs = serParkrunnerTimeSplit[i][2]
                else:
                    hours = 0
                    mins = serParkrunnerTimeSplit[i][0]
                    secs = serParkrunnerTimeSplit[i][1]
                    
        runnerTimesinSecs.append(float(hours)*60*60+float(mins)*60+float(secs))
    return runnerTimesinSecs

def parseRunnersNames(serParkrunnerNameSplit):
    lsFirstNames = []
    lsLastNames = []
    lsAthleteCode = []    

    numRunners = len(serParkrunnerNameSplit)
    
    for i in range(0,numRunners):
        if len(serParkrunnerNameSplit[i]) <= 3:
            # first name, last name and athlete code
            print(serParkrunnerNameSplit[i][0])
            lsFirstNames.append(serParkrunnerNameSplit[i][0])
            if lsFirstNames[i] == 'Unknown' :
                lsLastNames.append('Unknown')
                lsAthleteCode.append('0')
                continue
            
            lsLastNames.append(serParkrunnerNameSplit[i][1])
            tmpStr= str.split(serParkrunnerNameSplit[i][2],'=')
            tmpStr = tmpStr[1:]
            lsAthleteCode.append(tmpStr[0][0:-1])
        else:
            foundLastName = False
            tmpFirstName = ''
            tmpLastName = ''
            for j in range(0,len(serParkrunnerNameSplit[i])-1):
                if serParkrunnerNameSplit[i][j].isupper() :
                    if foundLastName == False :
                        tmpLastName = serParkrunnerNameSplit[i][j]
                        foundLastName = True
                    else :
                        tmpLastName = tmpLastName + ' ' + serParkrunnerNameSplit[i][j]
    
                else:
                    if j == 0 :
                        tmpFirstName =  serParkrunnerNameSplit[i][j]
                    else :
                        tmpFirstName = tmpFirstName + ' ' + serParkrunnerNameSplit[i][j]
            tmpStr= str.split(serParkrunnerNameSplit[i][len(serParkrunnerNameSplit[i])-1],'=')
            tmpStr = tmpStr[1:]
            lsAthleteCode.append(tmpStr[0][0:-1])
            lsLastNames.append(tmpLastName)
            lsFirstNames.append(tmpFirstName)    
    
    return lsFirstNames, lsLastNames , lsAthleteCode


event = [334,335,336]
numEvents = len(event)
dfOut = pd.DataFrame()
dfOutV = pd.DataFrame()
for eventNum in range(0,numEvents):
    filename = 'c:\\temp\\cc-'+ str(event[eventNum]) + '.csv'
    filenameV = 'c:\\temp\\cc-'+ str(event[eventNum]) + '-v.csv'

    dfIn = pd.read_csv(filename)
    dfIn['eventNum']= event[eventNum]
    dfInV = pd.read_csv(filenameV,header= None)
    dfInV = dfInV.T
    dfInV['eventNum']= event[eventNum]
    dfOut = dfOut.append(dfIn)
    dfOutV = dfOutV.append(dfInV)


dfOut.reset_index(inplace=True,drop=True)
dfOutV.reset_index(inplace=True,drop=True)
serParkrunnerNameSplit = dfOut['parkrunner ? (#)'].str.split(' ')

lsFirstNames, lsLastNames, lsAthleteCode = parseRunnersNames(serParkrunnerNameSplit)

serParkrunnerTimeSplit = dfOut['Time ? (#)'].str.split(':')        
lsrunnertimesinseconds = convertTimes(serParkrunnerTimeSplit)                
                
                
                
                