from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.patches import Circle
import matplotlib
import matplotlib.patches as patches
import cv2
import datetime

#%%
def ReadTrapsheet(filename):
    # read a trap sheet into a dictionary as numpy arrays
    d={}
    try:
        with open(filename) as f:
            reader = csv.DictReader(f)
                    
            for k in reader.fieldnames:
                d[k]=np.array([])
                
            for row in reader:
                for k in reader.fieldnames:
                    svalue = row[k]
                    try:
                        fvalue = float(svalue)
                        #print("float value: ", fvalue)
                        d[k] = np.append(d[k],fvalue)
                    except ValueError:
                        #print("Not a float", svalue)
                        d[k]=svalue
                    
        
    except:
        print('error.')
        
    return d
# %%        
def getRecentTrapsheet(sheetpath):
    try:
        p = Path(str(sheetpath))
        list_of_paths = p.glob('*Trapsheet*.csv'); 
        return max(list_of_paths, key=lambda p: p.stat().st_mtime) 
    except:
        return ''
    
# %%
        
def setSpine(ax,color):
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color(color)
    ax.spines['left'].set_color(color)
    ax.spines['right'].set_color(color)   

def addAoARect(ax,v1,v2,color,alpha):
    rect = patches.Rectangle((0,v1),1.2,v2-v1,linewidth=0,edgecolor='none',facecolor=color,alpha=alpha)    
    ax.add_patch(rect)    
    
def plotTrapsheet(ts, pinfo):


    theta_brc = -9.0;    
    if pinfo['aircraft']=='AV-8B':
        print('Harrier detected')
        theta_brc = 0.0;
    
    facecolor = '#404040'
    referencecolor = '#A6A6A6'  #glide slope and flight path references
    gridcolor = '#585858'
    spinecolor = gridcolor
    labelcolor = '#BFBFBF'
    dx = 20#-151;
    dy = 20#-6;

    num_aoa = 3
    feet = -6076.12
   # feet = -1
    
    theta = theta_brc*np.pi/180.;
    
    rotMatrix = np.array([[np.cos(theta), -np.sin(theta)], 
                         [np.sin(theta),  np.cos(theta)]])
    
    xy = np.array([ts['X']+dx, ts['Z']+dy])/1852.;
    xy = np.dot(rotMatrix,xy)
    
    
    #fig = plt.figure(facecolor="w")
    
    fig, axs = plt.subplots(3, 1, sharex=True,facecolor=facecolor,dpi=150)
    fig.set_size_inches(8, 6)
    matplotlib.use('Agg')
    plt.ioff() 
    #matplotlib.pyplot.ioff()
    # ========================================================================
    # %% Lineup
    ax=axs[1]
    #fig, ax = plt.subplots()
    
    #ax.set_xlim([0,1.2])
    ax.set_ylim([-401,801])
#axes.set_ylim([ymin,ymax])

    ax.set_facecolor(facecolor)

    ax.plot(xy[0],feet*xy[1], 'g', linewidth=16, alpha=0.01)
    
    #ax.set_aspect('equal')
    
    if pinfo['aircraft']=='AV-8B':
        m = np.array(ax.get_xlim())
        m[0]=0        
        #m[1] = 500
        ax.plot(m,[0,0],referencecolor,linewidth=2,alpha=0.8)
        #print(m)                    
    else:    
        m = np.array(ax.get_xlim())
        m[0]=0        
        ax.plot(m,[0,0],referencecolor,linewidth=2,alpha=0.8)
        #print(m)                
                      
    ax.plot(xy[0],feet*xy[1], 'g', linewidth=16, alpha=0.1)
    ax.plot(xy[0],feet*xy[1], 'g', linewidth=10, alpha=0.1)
    ax.plot(xy[0],feet*xy[1], 'g', linewidth=6, alpha=0.15)
    ax.plot(xy[0],feet*xy[1], 'w-', linewidth=1, alpha=0.45)    
    
    #ax.set_xlim(m)
    ax.grid(linestyle='-', linewidth='0.5', color=gridcolor)   
    ax.tick_params(axis=u'both', which=u'both',length=0)
    setSpine(ax,'none')
    ax.spines['right'].set_color(spinecolor)
    ax.spines['left'].set_color(spinecolor)
    plt.setp(ax.get_xticklabels(), color=labelcolor)
    plt.setp(ax.get_yticklabels(), color=labelcolor)
   
    xpoint = 0.195
    xpointsize = 9
    mystr = 'Lineup'
    ax.text(xpoint,510,mystr,color=labelcolor,fontsize=xpointsize,alpha=0.5)
    
    # %% GLIDE SLOPE
    ax = axs[0]
    
    ax.set_ylim([-1,650])
       
    ax.set_facecolor(facecolor)
    
   # xgs = np.linspace(0,xy[-1],2)
    xgs = xy[0]
    zt = 6076.12*xgs*np.tan(3.5*np.pi/180.0);
    gx = 0
    gz = 40
    ax.plot(xy[0],ts['Alt'], 'g', linewidth=16, alpha=0.0)
    
    
    ax.plot(xgs+gx,zt+gz,referencecolor,linewidth=1.1,alpha=1)
    
    ax.plot(xy[0],ts['Alt']+60, 'g', linewidth=16, alpha=0.1)
    ax.plot(xy[0],ts['Alt']+60, 'g', linewidth=10, alpha=0.1)
    ax.plot(xy[0],ts['Alt']+60, 'g', linewidth=6, alpha=0.15)
    ax.plot(xy[0],ts['Alt']+60, 'w-', linewidth=1, alpha=0.45) 
    
    #ax.set_xlim(m)
    #ax.invert_xaxis()
    ax.grid(linestyle='-', linewidth='0.5', color=gridcolor) 
    ax.tick_params(axis=u'both', which=u'both',length=0)
    setSpine(ax,'none')
    ax.spines['right'].set_color(spinecolor) 
    ax.spines['left'].set_color(spinecolor)
    #major_ticks = np.arange(0, 101, 20)
    #minor_ticks = np.arange(0, 101, 5)

#ax.set_xticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
    #ax.set_yticks(major_ticks)
    #ax.set_yticks(minor_ticks, minor=True)

#    sh = carrier01.shape    
 #   ax.imshow(carrier01)
 
#    imagebox = OffsetImage(carrier01, zoom=0.02)
#    imagebox.image.axes = ax
#    p = Circle((0, 0), 10)
#    da = DrawingArea(10, 10, 0, 0)
#    da.add_artist(p)
#    xym = [0.6, 0]
#    ab = AnnotationBbox(da, xym,
#                        xybox=(1.02, xym[1]),
#                        xycoords='data',
#                        boxcoords=("axes fraction", "data"),
#                        box_alignment=(0., 0.5),
#                        arrowprops=dict(arrowstyle="->"))

    if pinfo['aircraft']=='AV-8B':
        # top down view
        carrier01 = plt.imread('boat03_2.png')
        ax.figure.figimage(carrier01, 940, 320, alpha=.75, zorder=1)
        
        # side view for the glideslope plot
        carrier02 = plt.imread('boat05_2.png')  
        ax.figure.figimage(carrier02, 930, 567, alpha=0.75, zorder=1)        
    else:
    
        carrier01 = plt.imread('boat03.png')  
    # ax.add_artist(ab)
        ax.figure.figimage(carrier01, 1000, 343, alpha=.45, zorder=1)
    
        carrier02 = plt.imread('boat05.png')  
        ax.figure.figimage(carrier02, 1000, 567, alpha=.45, zorder=1)
    
    plt.setp(ax.get_xticklabels(), color=labelcolor)
    plt.setp(ax.get_yticklabels(), color=labelcolor)
    
    mystr = 'Glide Slope'
    ax.text(xpoint,410,mystr,color=labelcolor,fontsize=xpointsize,alpha=0.5)
    
    #vv = ax.axes.xaxis.get_ticklabels()
    #for a in ax:
    # get all the labels of this axis
    
    #labels = [tick.get_text() for tick in ax.get_yticklabels()]
    #ax.set_yticklabels(labels[:-1])
    
    # remove the first and the last labels
    #labels[0] = labels[-1] = ""
    #labels[0]=""
    # set these new labels
    #ax.set_yticklabels(labels)
    
#    xticks = ax.xaxis.get_major_ticks()
#    xticks[0].label1.set_visible(False)
#    xticks[-1].label1.set_visible(False)
        
    # %% Angle of Attack
    ax = axs[2]
    
   # ax.set_ylim([4,11])
    ax.xaxis.label.set_color(labelcolor)
   # ax.set_title('Angle of Attack',color=labelcolor)
    plt.setp(ax.get_xticklabels(), color=labelcolor)
    plt.setp(ax.get_yticklabels(), color=labelcolor)
    ax.set_xlabel("Distance (Nautical Miles)")
    # ax.set_ylabel("Angl")
    # ax.set_ylabel('AoA',color=labelcolor)
    
#    ax.get_xaxis().set_visible(False)
#    ax.get_yaxis().set_visible(False)
    #lm = ax.get_ylim() 
    #print(lm)
    #if np.abs(np.diff(lm)) < 3.5:
    
    maxvalue = np.max(ts['AoA'][:-num_aoa])
    minvalue = np.min(ts['AoA'][:-num_aoa])
    
    
    if maxvalue < 10 and minvalue > 6:
        maxvalue = 10.01
        minvalue = 5.99
    
    if maxvalue > 10 and minvalue > 6:
        minvalue = 3.99
    #if minvalue > 5.01:
    #    minvalue = 5.01
        
    print('Max value: ',maxvalue)
    print('Min value: ',minvalue)    
    ax.set_ylim([minvalue,maxvalue])
    
        
        
    ax.set_facecolor(facecolor)
   
    stralph = 'α'
    stralph = 'AoA'
    #ax.text(1.1535,10.4,stralph,color='g',fontsize=22,alpha=0.3)    
    ax.text(xpoint,10.2,stralph,color=labelcolor,fontsize=xpointsize,alpha=0.5)
    
    
    # 6.3 6.9 7.4 8.1 8.8 9.3 9.8
    
#    addAoARect(ax,5.6,6.3,'red',0.1) 
#    addAoARect(ax,6.3,6.9,'red',0.2)
#    addAoARect(ax,6.9,7.4,'orange',0.2)
#    addAoARect(ax,7.4,8.8,'green',0.4)
#    addAoARect(ax,8.8,9.3,'orange',0.2)
#    addAoARect(ax,9.3,9.9,'red',0.2)
#    addAoARect(ax,9.9,10.5,'red',0.1)    
    #addAoARect(ax,8.1,8.8,'orange',0.2)
#    rect = patches.Rectangle((0,6.3),1.2,6.9-6.3,linewidth=0,edgecolor='none',facecolor='red',alpha=0.1)    
#    ax.add_patch(rect)
#    rect = patches.Rectangle((0,6.9),1.2,2.4,linewidth=0,edgecolor='none',facecolor='red',alpha=0.1)
#    ax.add_patch(rect)
    
    lm = ax.get_xlim() 
    
    xmax = lm[1]
    
    if xmax < 0.7:
        xmax = 0.7
        
    if xmax > 1.2:
        xmax = 1.2
   
    ax.plot([0,xmax],[8.8,8.8],'g-',linewidth=1.2,alpha=0.8,linestyle='--')
    ax.plot([0,xmax],[7.4,7.4],'g-',linewidth=1.2,alpha=0.8,linestyle='--')    
    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'g-', linewidth=16, alpha=0.1) 
    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'g-', linewidth=10, alpha=0.1) 
    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'g-', linewidth=6, alpha=0.15) 
    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'w-', linewidth=1, alpha=0.45) 
    ax.grid(linestyle='-', linewidth='0.5', color=gridcolor) 
    # plt.gca().invert_yaxis()
#    ax.tick_params(axis='x', colors='red')
#    ax.tick_params(axis='y', colors='red')
    ax.tick_params(axis=u'both', which=u'both',length=0)
    setSpine(ax,'none')
    ax.spines['right'].set_color(spinecolor) 
    ax.spines['left'].set_color(spinecolor)
    ax.spines['bottom'].set_color(spinecolor)
    #ax.grid(which='minor', alpha=0.2)
    #ax.grid(which='major', alpha=0.5)
    
    
    ax.set_xlim([0.001,xmax]) 
    ax.invert_xaxis()
    plt.show()    
    
    titlestr = ''
    callsign = pinfo['callsign']
    titlestr = callsign;
    titlestr+=' '
    titlestr+=ts['Grade']
    titlestr+=' '
    titlestr+=str(ts['Points'][-1])
    titlestr+='PT'
    titlestr+='\n'
    titlestr+=str(ts['Details'])
    titlestr+='\n'
    titlestr+=pinfo['aircraft']
    titlestr+=' '
    titlestr +=pinfo['time']
    #tstr.join([str(ts['Grade'][-1]), ' ', str(ts['Points'][-1]) , ' points'])
    
    fig.suptitle(titlestr, fontsize=14,color=labelcolor)
    #fig.title(ts['Details'], fontsize=10)
    fig.savefig('trapsheet.png', facecolor=facecolor)    
    

#    img = cv2.imread('test2png.png')
#    crop_img = img[0:-1-25, 85:-1]
    
  #  cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
 #   cv2.imwrite('file.png',crop_img)
def parseFilename(vinput):
    
    pinfo ={}
    p = Path(vinput)
    last_modified = p.stat().st_mtime
    mod_timestamp = datetime.datetime.fromtimestamp(last_modified)
    
   
    #modificationTime = time.ctime ( fileStatsObj [ last_modified ] )
#    print("Last Modified Time : ", modificationTime )
    timestampStr = mod_timestamp.strftime("%b %d %Y, %H:%M:%S")
    pinfo['time']=timestampStr
    print(timestampStr)
    ps = p.stem
    print(ps)
    ps=ps.replace('AIRBOSS-','')
    ind = ps.find('-')
    print(ps)
    ps = ps[ind+1:-1]
    print(ps)
    ind = ps.rfind('-')
    ps = ps[0:ind]
    
    hornet = 'FA-18C_hornet'
    tomcatB = 'F-14B'
    harrier = 'AV8BNA'
    tomcatA = 'F-14A-135-GR'
    if hornet in ps:
        print('contains hornet')
        ps = ps.replace(hornet,'')
        pinfo['aircraft']='F/A-18C'
    elif tomcatA in ps:
        print('contains tomcat')
        ps = ps.replace(tomcatA,'')
        pinfo['aircraft']='F-14A-135-GR'
    elif tomcatB in ps:
        print('contains tomcat')
        ps = ps.replace(tomcatB,'')
        pinfo['aircraft']='F-14B'
    elif harrier in ps:
        print('contains av8bna')
        ps = ps.replace(harrier, '')
        pinfo['aircraft']='AV-8B'
    else:
        print('unknown aircraft.')

    print(ps)
    
    pinfo['callsign']=ps[0:-1]
    print(pinfo['callsign'])
    return pinfo
    
#%%
trapfolder = 'C:/python_code/bm/trapsheets'
trapfolder = 'C:/FlightSimDocs/JOW/stats/SLModStats/LSO'
trapfolder = 'C:/HypeMan/trapsheets'
trapfolder = 'C:/Users/DCSAdmin/Saved Games/DCS.openbeta_server'
trapfolder = 'C:/Users/jow/Saved Games/DCS.openbeta_server'
trapfolder = 'C:/HypeMan/'
#trapfolder = 'C:/temp'
p = Path(str(trapfolder))


#print('Latest path: ', latest_path)

trapfile = getRecentTrapsheet(trapfolder)

if trapfile == '':
    print('No trap file found')
    quit()
    
print('Final file is:', trapfile)

#trapfile = '../trapsheets/AIRBOSS-CVN74_Trapsheet-PyCo00_F-14B-0008.csv'
#trapfile = '../trapsheets/AIRBOSS-CVN74_Trapsheet-Vexx_FA-18C_hornet-0191.csv'
#trapfile = '../trapsheets/AIRBOSS-CVN74_Trapsheet-DG_441_FA-18C_hornet-0042.csv'

pinfo = parseFilename(trapfile)

ts = ReadTrapsheet(trapfile)
plotTrapsheet(ts, pinfo)

# %% this is a cell here
print('Grade: ', ts['Grade'], ' Points: ', ts['Points'][-1], ' Details: ', ts['Details'])