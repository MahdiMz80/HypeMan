#import csv
#import sys
#import pprint
import gspread
import json
import os 
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from oauth2client.service_account import ServiceAccountCredentials
#from datetime import datetime

def updateDatabase(path):
    
    if time.time() - getModificationTimeSeconds(path) > 3600:
        print('Updating from Google.')
        updateFromGoogle()
    else:
        print('Less than one hour since last refresh, skipping pull from google.')
    
def updateFromGoogle():
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('HypeManLSO-358d4493fc1d.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('HypeMan_LSO_Grades').sheet1
        list_of_hashes = sheet.get_all_records()    

        with open('data.txt', 'w') as outfile:            
            json.dump(list_of_hashes, outfile)        
    except:
        print('Exception thrown in updateFromGoogle')
        return
    
    print('Local HypeMan LSO grade database updated from Google Sheets.')    
    
def getModificationTimeSeconds(path):
    ct = time.time()
    try: 
        modification_time = os.path.getmtime(path) 
        #print("Last modification time since the epoch:", modification_time) 
    except OSError: 
        print("Path '%s' does not exists or is inaccessible" %path) 
        return ct-4000
  
    return modification_time
    
def printRow (row, place):
	#pp = pprint.PrettyPrinter()
	#pp.pprint(row)
	print(place + ': ' + row[1] + ' ' + row[3] + '/' + row[4] + '/' + row[5])
	return	

def isPilotQual(name):
    return False

def calculateGradeQual(curList, grade0):
    
    try:
        pt = float(curList[0]['finalscore'])
       # print('(QUAL) points ', pt, ' for ', curList[0]['pilot'])
        return pt
    except:
        return float(-1.0)    
    
def calculateGradeCivilian(curList, grade0):
    grade = grade0
    pt = float(-1.0)
    x = 0
    for i in curList:
        try:
            pt = float(i['finalscore'])
        except:
            x=0
            
        if pt >= 0.0:
            #print('(UNQUAL) highest score for ', i['pilot'], ' as ', pt)
            #grade['finalscore']=pt
            return pt
        else:
            #print('No finalscore for ', i['pilot'])
            return pt
           
            
def calculateGrade(curList, grade0):
    if isPilotQual(curList[0]['pilot']):
        return calculateGradeQual(curList,grade0)
    else:
        return calculateGradeCivilian(curList,grade0)

                
        
def calculatePilotRow(data, name, grade0):    
        
    boardRow = [];
    
    uniqueDates = []
    for i in reversed(data):
        grade = grade0
        if name == i['pilot']:
            if i['ServerDate'] not in uniqueDates:
                uniqueDates.append(i['ServerDate'])
    
    for i in uniqueDates:
        #print(i)
        curList = [];
        for j in data:
            if name == j['pilot'] and j['ServerDate'] == i:
                curList.append(j)
        
        boardRow.append(calculateGrade(curList,grade0))
        
            
#            if not haveDate:
#                curDate = i['ServerDate']
#                haveDate = True            
#                
#            if curDate == i['ServerDate']:
#                curList.append(i)
#                
#            else:
#                curDate = i['ServerDate']
#                grade = calculateGrade(curList, grade0)
#                boardRow.append(grade)
#                curList = [];
#                curList.append(i)       
                
    #print(boardRow)           
    return boardRow

lsoData = 'data.txt'
updateDatabase(lsoData)

with open('data.txt') as json_file:
    data = json.load(json_file)
 
grade0={}; grade0['color']='white'; grade0['score']=0.0; grade0['symbol']='x'; grade0['grade']='--'
    
pilots = []

pilotRows = []
# get the rows
for i in reversed(data):
    name = i['pilot']
    if name not in pilots:
        pilots.append(name)
        #print('Calculating for: ', name)
        pilotRow = calculatePilotRow(data, name, grade0)
        print(name,' score: ' , pilotRow)
        pilotRows.append(pilotRow)
        

maxLength = 0
for i in pilotRows:
    if len(i) > maxLength:
        maxLength = len(i)
    
table_vars = []    
for i in pilotRows:
    for k in i:
        print(k)
    for j in range(len(i),maxLength):
        print(j)
        
        

  
fig = plt.figure(dpi=100)
ax = fig.add_subplot(1,1,1)        
col_lables = ['Pilot', 'Qual','A','B','C','D','E']
table_vals = [['1', 'yes', 'None', 'False', 'False', 'no', '6.0'],['1', 'yes', 'None', 'False', 'False', 'no', '6.0']]
table_vals = [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]]
tab1 = ax.table(cellText=[table_vals], colLabels=col_lables)
#tab1.scale(1,4)
ax.axis('off')
plt.savefig('file.png')