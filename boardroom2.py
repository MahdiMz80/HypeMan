import gspread
import json
import os 
import time
from datetime import datetime
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
  
    if not os.path.isfile(path) or time.time() - getModificationTimeSeconds(path) > 3600:
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

def calculateGradeCivilian(curList):    
    
    gradeCell = {}
    gradeCell['score'] = -1
    gradeCell['icon'] = ''
    gradeCell['bg'] = '#FFFFFF'
    
    
    pt = float(-1.0)    
    for i in curList:
        if i['case'] == 3 and not '3' in gradeCell['icon']:
            gradeCell['icon'] += '3'
         
        if i['case'] == 2 and not '2' in gradeCell['icon']:
            gradeCell['icon'] += '2'
         
        
         
        try:
            tmp = float(i['points'])
            if tmp > pt:
                pt = tmp
                
            if tmp == 5 and not '5' in gradeCell['icon']:
                gradeCell['icon']+= '5'
        except:
            pt=0
    
    gradeCell['bg'] = colorFromPoints(pt)
    gradeCell['score'] = pt
    
  #  if not gradeCell['score']:
  #      print('what')
    return gradeCell
    
def colorFromPoints(g):

    bluegraycolor = '#708286'
    glossgraycolor = '#5F615E'							  
    redcolor = '#ED1B24'
    browncolor = '#835C3B'
    orangecolor = '#d17a00'
    yellowcolor = '#b6c700'
    greencolor = '#0bab35'
    bluecolor = '#01A2EA'
    blankcell='#FFFFFF'
    blackcolor = '#000000'
    color = 'blankcell'
    
    if g == -1:             
        color=blankcell
    elif g == 0:
        color=blackcolor
    elif g == 1:
        color=redcolor
    elif g == 2.0:                
        color=browncolor
    elif g == 2.5:                
        color=bluecolor            
    elif g == 3.0:
        color = yellowcolor
    elif g == 4.0:
        color = greencolor 
    elif g == 4.50:
        color = greencolor							  
    elif g == 5:                
        color = greencolor
    elif g == 5.5:
        color = bluegraycolor						 
    else:
        color = blankcell
        
    return color
      
    
def calculateGradeTailhooker(curList):
    
    # loop through their grades and find their FIRST wire
    
    gradeCell = {}
    gradeCell['score'] = 1
    gradeCell['icon'] = ''
    gradeCell['bg'] = '#FFFFFF'
    
    pts = []
    
    count = 0
    for i in curList:
        count = count + 1
        #print(' Calculate grade iteration: ', count)
        
        # skip WOFDS
        if 'WOFD' in i['grade']:
            continue
        
        if not i['wire']:
            #print('Empty.')
            pts.append(i['points'])
        else:
            #print('not empty')
            
            if not i['finalscore']:
                gradeCell['score'] = i['points']
            else:
                gradeCell['score'] = i['finalscore']
                
            pts.append(i['points'])
            gradeCell['bg'] = colorFromPoints(min(pts))            
            
            if i['case'] == 3:
                gradeCell['icon']+='3'                
            return gradeCell
    
    
    if len(pts) == 0:
        gradeCell['score'] = 1
        pts.append(1)
    else:
        gradeCell['score'] = statistics.mean(pts)
        
    gradeCell['bg'] = colorFromPoints(min(pts)) 
        
    return gradeCell   
    
def calculateGrade(curList, ruleset):
    if ruleset == 'best':
        return calculateGradeCivilian(curList)                       

    if ruleset == 'first':        
        return calculateGradeTailhooker(curList)    

        
                

def calculatePilotRow(data, name, ruleset):    
        
    #print(name)
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
        
        ithPilotGrade = calculateGrade(curList,ruleset)
        
        boardRow.append(ithPilotGrade)
        
            
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

def CalculateAverageScore(pilotRow):
    
    score = 0.0
    for i in pilotRow:
        score = score + i['score']
    
    finalscore = score/len(pilotRow)
    #print(finalscore)
    return finalscore
        
def plotSquadron(pilotRows, options):
    #print('PlotSquadron')
    maxLength = 0
    for i in pilotRows:
        if len(i) > maxLength:
            maxLength = len(i)
    if maxLength < options['maxRows']:
        maxLength = options['maxRows']

    fig = plt.figure(figsize=(6, 3), dpi=250)
    ax = fig.add_subplot(1,1,1)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])
    
    tb = Table(ax, bbox=[0, 0, 1, 1])
    #tb.scale(0.25, 1)     
    tb.auto_set_font_size(False)
    n_cols = maxLength+2
    n_rows = len(pilots)+1
    width, height = 100 / n_cols, 100.0 / n_rows
    #height = height/10
    shithot ='🎖️'	  
    anchor='⚓'
    goldstar = '⭐'
    goldstar = '★'
    case3 = '•'
    case3= '◉'
    case2 = '⊙'
    case2 = '○'
    #case2 = '○'
    #case2 = '∘'
    #unicorn='✈️'
    blankcell='#FFFFFF'
     #colors=['red','orange','orange','yellow','lightgreen']  #078a21
    #colors=['#a00000','#835C3B','#d17a00','#b6c700','#0bab35','#057718','#057718']
    colors=['#a00000','#d17a00','#d17a00','#b6c700','#0bab35','#057718','#057718']
            
    # redcolor = '#a00000'
    # browncolor = '#835C3B'
    # orangecolor = '#d17a00'
    # yellowcolor = '#b6c700'
    # greencolor = '#0bab35'
    # bluecolor = '#01A2EA'
    
    try:
        minDate = data[-1]['ServerDate']
        maxDate = data[0]['ServerDate']
    except:
        minDate =''
        maxDate = ''
        
    textcolor = '#000000'
    edgecolor = '#708090'
    cell = tb.add_cell(0,0,10*width,height,text='Callsign',loc='center',facecolor=blankcell) #edgecolor='none'
    cell.get_text().set_color(textcolor)    
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
    cell.set_edgecolor(edgecolor)
    cell.set_linewidth(0.5)
    #cell.set_fontsize(24)
    cell = tb.add_cell(0,1,width,height,text='',loc='center',facecolor=blankcell) #edgecolor='none'
    cell.get_text().set_color(textcolor)
    cell.set_edgecolor(edgecolor)
    cell.set_linewidth(0.5)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))
    cell.set_edgecolor(edgecolor)
    #cell.set_fontsize(24)
    titlestr = ' '+options['squadron']
    count = 0
    for col_idx in range(2,options['maxCols']+2):
        
        text = ''
        
        if count < len(titlestr):
            text = titlestr[count]
            count = count + 1
        cell = tb.add_cell(0, col_idx, width, height,
                        text=text.upper(),
                        loc='center',
                        facecolor=blankcell)
        cell.set_linewidth(0.5)                        
        cell.set_edgecolor(edgecolor)
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
        cell.set_edgecolor(edgecolor)    

    #cell.set_text_props(family='')


    #titlestr = 'JOW Greenie Board ' + minDate + ' to ' + maxDate

    minRows = len(pilots)

    if minRows < options['maxRows']: 
        minRows = options['maxRows']
        
    #for p_idx in range(0,len(pilots)):
    for p_idx in range(0,minRows):
        row_idx = p_idx+1
       
        rd = []
        name = ''
        scoreText = ''
        
        if p_idx < len(pilots):
            name = pilots[p_idx]            
            rd = pilotRows[name]
#            avg = statistics.mean(rd)
            avg = CalculateAverageScore(rd)
            scoreText = round(avg,1)
                
        cell = tb.add_cell(row_idx,0,10*width,height,text=name,loc='center',facecolor=blankcell,edgecolor='blue') #edgecolor='none'    
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size="7"))
        cell.set_edgecolor(edgecolor)
        cell.set_linewidth(0.5)
    #    name = pilots[p_idx];

        
        cell = tb.add_cell(row_idx,1,width,height,text=scoreText,loc='center',facecolor=blankcell)
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(size="6.0"))
        cell.set_edgecolor(edgecolor)
        cell.set_linewidth(0.5)
        col_idx = 2
            
        for ij in rd:
            
            color = ij['bg']
            
            if not color:
                color = blankcell
                
            text = ''      
            
            if '3' in ij['icon']:
                text = case3
            elif '2' in ij['icon']:
                text = case2
                        
            cell = tb.add_cell(row_idx,col_idx,width,height,text=text,loc='center',facecolor=color) #edgecolor='none'  
            cell.get_text().set_color('#333412')
            cell.set_linewidth(0.5)
           # cell.auto_set_font_size()
            cell.set_text_props(fontproperties=FontProperties(weight='bold',size="10"))
            cell.set_edgecolor(edgecolor)    
            col_idx = col_idx + 1
                    
            
        color = blankcell
        text=''
        
        # add the remaining cells to the end
        for f in range(col_idx,options['maxCols']+2):
            cell = tb.add_cell(row_idx,f,width,height,text=text,loc='center',facecolor=color) #edgecolor='none' 
            cell.set_linewidth(0.5)            
            cell.set_edgecolor(edgecolor)
     
    #
    #tb.set_fontsize(7)    
    ax.add_table(tb)
    ax.set_axis_off()
    ax.axis('off')
    plt.box(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    #plt.title(titlestr,color='w')

    plt.savefig('board.png',transparent=False,bbox_inches='tight', pad_inches=0)
    
def plotDefaultBoard(pilotRows, options):
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
    shithot ='🎖️'		  
    anchor='⚓'
    goldstar = '⭐'
    goldstar = '★'
    case3 = '•'
    case3= '◉'
    case2 = '⊙'
    case2 = '○'
    #case2 = '○'
    #case2 = '∘'
    #unicorn='✈️'
    blankcell='#1A392A'
    

    #colors=['red','orange','orange','yellow','lightgreen']  #078a21
    #colors=['#a00000','#835C3B','#d17a00','#b6c700','#0bab35','#057718','#057718']
    colors=['#a00000','#d17a00','#d17a00','#b6c700','#0bab35','#057718','#057718', '#708286','#5F615E']
            
    redcolor = '#a00000'
    bluegraycolor = '#708286'
    glossgraycolor = '#5F615E'						  
    browncolor = '#835C3B'
    orangecolor = '#d17a00'
    yellowcolor = '#b6c700'
    greencolor = '#0bab35'

   # try:
   #     minDate = data[-1]['ServerDate']
   #     maxDate = data[0]['ServerDate']
   # except:
   #     minDate =''
   #     maxDate = ''
        
    textcolor = '#FFFFF0'
    edgecolor = '#708090'
    cell = tb.add_cell(0,0,5*width,height,text='Callsign',loc='center',facecolor=blankcell) #edgecolor='none'
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
    
    currentMonth = datetime.now().month
    titlestr = ' JOINT OPS WING' #+ str(currentMonth) + '/' + str(datetime.now().year)
    
    print(titlestr)
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


#    titlestr = 'JOW Greenie Board ' + minDate + ' to ' + maxDate

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
            rd = pilotRows[name]
            #avg = statistics.mean(rd)
            avg = CalculateAverageScore(rd)
            scoreText = round(avg,1)
            if name.lower() == 'eese':
                name = "SippyCup"    

                
        cell = tb.add_cell(row_idx,0,5*width,height,text=name,loc='center',facecolor=blankcell,edgecolor='blue') #edgecolor='none'    
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
            color = g['bg']            
            text = ''      
            
            if '5.5' in g['icon']:
                text = shithot
            elif '3' in g['icon'] and '5' in g['icon']:
                text = goldstar
            elif '3' in g['icon']:
                text = case3            
            elif '5' in g['icon']:
                text = anchor   
            elif '2' in g['icon']:
                text = case2
                        
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

# set defaults
airframe = ''
squadron = ''
ruleset = 'best'

#print('Length of argv: ' , len(sys.argv));
if len(sys.argv) >= 2:
    if str(sys.argv[1]) == 'turkey':
        airframe = ['F-14B', 'F-14A-135-GR']
    elif str(sys.argv[1]) == 'hornet':
        airframe = 'FA-18C_hornet'
    elif str(sys.argv[1]) == 'scooter':
        airframe = 'A-4E-C'
    elif str(sys.argv[1]) == 'harrier':
        airframe = 'AV8BNA'
    elif str(sys.argv[1]) == 'goshawk':
        airframe = 'T-45'				 
    print('Aircraft: ', airframe)
if len(sys.argv) >= 3:
    ruleset = str(sys.argv[2])

if len(sys.argv) >= 4:
    squadron = str(sys.argv[3]);
    print('Squadron: ', squadron)

print('Ruleset: ', ruleset)
lsoData = 'data.txt'

updateDatabase(lsoData)

with open('data.txt') as json_file:
    data = json.load(json_file)
 


# go through and  keep only a specified airframe    
data2 = data
print('... size of data array: ' , str(len(data)))
count = 0

if airframe != '':
    data2 = []
    print('Keeping only grades for airframe: ', airframe)    
    for i in data:
        # if i['airframe']
        #if i['airframe'] == airframe:
        if i['airframe'] in airframe:
            data2.append(i)
            # print('Deleting airframe: ', i['airframe'], ' was looking for: ' , airframe)
            # data.remove(i)
            count = count + 1

print('Number of rows kept: ', str(count))

data = data2
print('size of data array: ' , str(len(data)))
count = 0
if squadron != '':
    data2 = []
    print('Searching for squadron: ' , squadron)
    for i in data:    
        name = i['pilot']
        #print('Name: ' , name)
        name = name.replace('-', '')
        name = name.replace('_', '')
        name = name.replace('[', '')
        name = name.replace(']', '')
        name = name.replace('|', '')
        name = name.replace('\\', '')
        name = name.replace('/', '')
        name = name.replace('@', '')    
        name = name.lower()
        
        index = name.find(squadron)
        
        if index != -1:
            data2.append(i)
            count = count + 1;
            #print('Keeping in squadron: ' , name)
          #  name = name.replace(squadron,'')

# if the squadron was empty just keep the original data
data = data2

data2 = []
print('Skipping WOFDs')
for i in data:
    if not'WOFD' in i['grade']:
        data2.append(i)

data = data2
print('Number remaining: ', str(len(data)))
pilots = []          
pilotRows = {}
pilotDict = {}
# get the rows as they will appear in our Greenie Board

# set the default grade
#grade0={}; grade0['color']='white'; grade0['score']=0.0; grade0['symbol']='x'; grade0['grade']='--'

# if squadron is empty then lets trim the landings not in the current month
data2 = []
if squadron == '':
    currentMonth = datetime.now().month
    print('skipping landings not in current month')
    for i in data: 
        #print(i)
        idate = i['ServerDate'].split('/')
        imonth = int(idate[1])
        
        if imonth == currentMonth:
            data2.append(i)
            
    data = data2
       
    
for i in reversed(data):
    name = i['pilot']
    if name not in pilots:
        pilots.append(name)        
        pilotRow = calculatePilotRow(data, name, ruleset)
        #print(name,' score: ' , pilotRow)
        pilotRows[name] = (pilotRow)
       # pilotDict[name]=pilotRow
        

options = {}

if squadron == '':
    plotDefaultBoard(pilotRows, options)
else:
    options['airframe'] = airframe
    options['squadron'] = squadron
    options['ruleset'] = ruleset
    options['maxRows']=10
    options['maxCols']=17
    plotSquadron(pilotRows, options)

print('done')    