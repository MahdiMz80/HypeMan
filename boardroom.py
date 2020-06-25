import gspread
import json
import os 
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties
import numpy as np
import statistics

import sys, getopt


from oauth2client.service_account import ServiceAccountCredentials
#from datetime import datetime
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
#if len(sys.argv)== 2:
#    print('Argument Number 2: ', str(sys.argv[1])) 


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
        pt = float(curList[0]['points'])
       # print('(QUAL) points ', pt, ' for ', curList[0]['pilot'])
        return pt
    except:
        return float(-1.0)    
    
def calculateGradeCivilian(curList, grade0):
    
    pt = float(-1.0)
    x = 0
    for i in curList:
        try:
            tmp = float(i['points'])
            if tmp > pt:
                pt = tmp
        except:
            x=0
          
    if pt >= 0.0:
        #print('(UNQUAL) highest score for ', i['pilot'], ' as ', pt)
        #grade['finalscore']=pt
        return pt
    else:
        #print('No finalscore for ', i['pilot'])
        return 0.0
           
            
def calculateGrade(curList, grade0):
    if isPilotQual(curList[0]['pilot']):
        return calculateGradeQual(curList,grade0)
    else:
        return calculateGradeCivilian(curList,grade0)

                
        
def calculatePilotRow(data, name, grade0):    
        
    boardRow = [];
    
    uniqueDates = []
    for i in reversed(data):
        #grade = grade0
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
    
airframe = ''

if len(sys.argv)== 2:
    print('Argument Number 2: ', str(sys.argv[1])) 

    if str(sys.argv[1]) == 'turkey':
        airframe = 'F-14B'
    elif str(sys.argv[1]) == 'hornet':    
        airframe = 'FA-18C_hornet'

print('size of data array: ' , str(len(data)))
count = 0
if airframe != '':
    data2 = []
    for i in data:
        # if i['airframe']
        if i['airframe'] == airframe:
            data2.append(i)
            # print('Deleting airframe: ', i['airframe'], ' was looking for: ' , airframe)
            # data.remove(i)
            count = count + 1

print('Number of rows removed: ', str(count))

data = data2
pilots = []


pilotRows = []
pilotDict = {}
# get the rows
for i in reversed(data):
    name = i['pilot']
    if name not in pilots:
        pilots.append(name)
        #print('Calculating for: ', name)
        pilotRow = calculatePilotRow(data, name, grade0)
        print(name,' score: ' , pilotRow)
        pilotRows.append(pilotRow)
        pilotDict[name]=pilotRow
        

maxLength = 0
for i in pilotRows:
    if len(i) > maxLength:
        maxLength = len(i)
    
   
if maxLength < 17:
    maxLength = 17
    
fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_ticks([])
frame1.axes.get_yaxis().set_ticks([])

tb = Table(ax, bbox=[0, 0, 1, 1])

tb.auto_set_font_size(False)


n_cols = maxLength+2
n_rows = len(pilots)+1
width, height = 100 / n_cols, 100.0 / n_rows
anchor='⚓'
goldstar = '⭐'
goldstar = '★'
#unicorn='✈️'
blankcell='#1A392A'

#colors=['red','orange','orange','yellow','lightgreen']  #078a21
#colors=['#a00000','#835C3B','#d17a00','#b6c700','#0bab35','#057718','#057718']
colors=['#a00000','#d17a00','#d17a00','#b6c700','#0bab35','#057718','#057718']
        
redcolor = '#a00000'
browncolor = '#835C3B'
orangecolor = '#d17a00'
yellowcolor = '#b6c700'
greencolor = '#0bab35'

minDate = data[-1]['ServerDate']
maxDate = data[0]['ServerDate']
textcolor = '#FFFFF0'
edgecolor = '#708090'
cell = tb.add_cell(0,0,4*width,height,text='Callsign',loc='center',facecolor=blankcell) #edgecolor='none'
cell.get_text().set_color(textcolor)
cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
cell.set_edgecolor(edgecolor)
#cell.set_fontsize(24)
cell = tb.add_cell(0,1,width,height,text='',loc='center',facecolor=blankcell) #edgecolor='none'
cell.get_text().set_color(textcolor)
cell.set_edgecolor(edgecolor)
cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))
cell.set_edgecolor(edgecolor)
#cell.set_fontsize(24)
titlestr = ' JOINT OPS WING'
count = 0
for col_idx in range(2,maxLength+2):
    
    text = ''
    
    if count < len(titlestr):
        text = titlestr[count]
        count = count + 1
    cell = tb.add_cell(0, col_idx, width, height,
                    text=text,
                    loc='center',
                    facecolor=blankcell)    
    cell.set_edgecolor(edgecolor)
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
    cell.set_edgecolor(edgecolor)    

#cell.set_text_props(family='')


titlestr = 'JOW Greenie Board ' + minDate + ' to ' + maxDate

minRows = len(pilots)

if minRows < 12: 
    minRows = 12
    
#for p_idx in range(0,len(pilots)):
for p_idx in range(0,minRows):
    row_idx = p_idx+1
   
    rd = []
    name = ''
    scoreText = ''
    
    if p_idx < len(pilots):
        name = pilots[p_idx]
        rd = pilotDict[name]
        avg = statistics.mean(rd)
        scoreText = round(avg,1)
        if name.lower() == 'eese':
            name = "SippyCup"    

            
    cell = tb.add_cell(row_idx,0,4*width,height,text=name,loc='center',facecolor=blankcell,edgecolor='blue') #edgecolor='none'    
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size="7.5"))
    cell.set_edgecolor(edgecolor)
#    name = pilots[p_idx];

    
    cell = tb.add_cell(row_idx,1,width,height,text=scoreText,loc='center',facecolor=blankcell)
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size="7.4"))
    cell.set_edgecolor(edgecolor)
    col_idx = 2
        
    for g in rd:
        
        text = ''
        
        if g == 0:             
            color=redcolor  
        elif g == 1:
            color=browncolor
        elif g== 1.5:
            color=browncolor
        elif g == 2:
            color=orangecolor
        elif g == 2.5:
            color=orangecolor
        elif g == 3:
            color = yellowcolor
        elif g == 4:
            color = greencolor 
        elif g == 5:
            text = anchor
            color = greencolor
        else:
            color = blankcell
                    
            # elif g >= 5.0:
           #     text = anchor
           #     color = colors[6]  
               
                    
        cell = tb.add_cell(row_idx,col_idx,width,height,text=text,loc='center',facecolor=color) #edgecolor='none'  
        cell.get_text().set_color('#333412')
       # cell.auto_set_font_size()
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size="14"))
        cell.set_edgecolor(edgecolor)    
        col_idx = col_idx + 1
                
        
    color = blankcell
    text=''
    
    # add the remaining cells to the end
    for f in range(col_idx,maxLength+2):
        cell = tb.add_cell(row_idx,f,width,height,text=text,loc='center',facecolor=color) #edgecolor='none'            
        cell.set_edgecolor(edgecolor)
        
#tb.set_fontsize(7)    
ax.add_table(tb)
ax.set_axis_off()
ax.axis('off')
plt.box(False)
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
#plt.title(titlestr,color='w')

plt.savefig('board.png',transparent=False,bbox_inches='tight', pad_inches=0)