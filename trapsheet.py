from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
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


    trapfile = getRecentTrapsheet(trapfolder)
    p = Path(trapfile)
    ps = p.stem

    sh = 'SH_'
    perfect_Pass = "unicorn_"
    if sh in ps:
        if perfect_Pass in ps:
            print('SH Pass AND Unicorn in file name, THATS TITS YO!')
            ax.text(0.5, 0.75, ' *** SIERRA-HOTEL UNICORN PASS !! ***',
            verticalalignment='bottom', horizontalalignment='center',
            transform=ax.transAxes,
            color='darkblue', fontsize=22)
            #print('SIERRA HOTEL PASS!')
            ax.text(0.505, 0.755, ' *** SIERRA-HOTEL UNICORN PASS !! ***',
            verticalalignment='bottom', horizontalalignment='center',
            transform=ax.transAxes,
            color='lightblue', fontsize=22)
        else:
            print('SH Pass in file name so print that sucka!')
            ax.text(0.5, 0.75, 'SIERRA-HOTEL PASS',
            verticalalignment='bottom', horizontalalignment='center',
            transform=ax.transAxes,
            color='yellow', fontsize=15)
            #print('SIERRA HOTEL PASS!')
    else:
        print('no SH pass drawn')

    # %% GLIDE SLOPE
    ax = axs[0]

    ax.set_ylim([-1,650]) #Glideslope Reference scale from 0 to 650 feet

    ax.set_facecolor(facecolor)

    if pinfo['aircraft']=='AV-8B':#adam edit 2/14/21- added a check to see if Harrier or not for glideslop ref line adjustment
         # xgs = np.linspace(0,xy[-1],2)
        xgs = xy[0] #originally set to 0 2/14/21, doesn't seem to do anything when I change it
        zt = 6076.12*xgs*np.tan(3.5*np.pi/180.0); #original line:zt = 6076.12*xgs*np.tan(3.5*np.pi/180.0); 2/14/21 changed to 3.0*np
        gx = 0 #this must be a scaling thing... squished the graph when I changed to 100
        gz = 40
        ax.plot(xy[0],ts['Alt'], 'g', linewidth=16, alpha=0.0) #no idea what these lines do, don't see any changes
        ax.plot(xgs+gx,zt+gz+40,referencecolor,linewidth=1.1,alpha=1) #Glide Slope Reference line - 2/14/21 Added 55 to it to get the ref line to be more accurate
    else:
         # xgs = np.linspace(0,xy[-1],2)
        xgs = xy[0] #originally set to 0 2/14/21, doesn't seem to do anything when I change it
        zt = 6076.12*xgs*np.tan(3.5*np.pi/180.0);
        gx = 0 #this must be a scaling thing... squished the graph when I changed to 100
        gz = 40
        ax.plot(xy[0],ts['Alt'], 'g', linewidth=16, alpha=0.0) #no idea what these lines do, don't see any changes
        ax.plot(xgs+gx,zt+gz,referencecolor,linewidth=1.1,alpha=1) #Glide Slope Reference line -





    ax.plot(xy[0],ts['Alt']+60, 'g', linewidth=8, alpha=0.1) #"glow" effect arond the glideslope line
    ax.plot(xy[0],ts['Alt']+60, 'g', linewidth=5, alpha=0.1)  #"glow" effect arond the glideslope line
    ax.plot(xy[0],ts['Alt']+60, 'g', linewidth=3, alpha=0.15)  #"glow" effect arond the glideslope line
    ax.plot(xy[0],ts['Alt']+60, 'w-', linewidth=1, alpha=0.45)  #"glow" effect arond the glideslope line

    #ax.set_xlim(m)
    #ax.invert_xaxis()
    ax.grid(linestyle='-', linewidth='0.5', color=gridcolor) #Glideslope Grid
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



    #ax.set_ylabel("Angl")
    #ax.set_ylabel('SIERRA HOTEL PASS!',color=shcolor)

#    ax.get_xaxis().set_visible(False)
#    ax.get_yaxis().set_visible(False)
    #lm = ax.get_ylim()
    #print(lm)
    #if np.abs(np.diff(lm)) < 3.5:

    maxvalue = np.max(ts['AoA'][:-num_aoa])
    minvalue = np.min(ts['AoA'][:-num_aoa])


    # 6.3 6.9 7.4 8.1 8.8 9.3 9.8

#    addAoARect(ax,5.6,6.3,'red',0.1)
#    addAoARect(ax,6.3,6.9,'red',0.2)
#    addAoARect(ax,6.9,7.4,'orange',0.2)
#    addAoARect(ax,7.4,8.8,'green',0.4)
#    addAoARect(ax,8.8,9.3,'orange',0.2)
#    addAoARect(ax,9.3,9.9,'red',0.2)
#    addAoARect(ax,9.9,10.5,'red',0.1)
    #addAoARect(ax,8.1,8.8,'orange',0.2)
#    rect = patches.Rectangle((0,6.3),1.2,6.9-6.3,linewidth=0,edgecolor='none',facecolor='green',alpha=0.1)
#    ax.add_patch(rect)
#    rect = patches.Rectangle((0,6.9),1.2,2.4,linewidth=0,edgecolor='none',facecolor='red',alpha=0.1)
#    ax.add_patch(rect)

    hornet_aoa = 'FA-18C_hornet'
    hawk_aoa = 'T-45'
    tomcatA_aoa = 'F-14A-135-GR'
    tomcatB_aoa = 'F-14B'
    harrier_aoa = 'AV8BNA'
    skyhawk_aoa = 'A-4E-C'


    if hornet_aoa in ps:    # 7.4 on speed min, 8.1 on speed, 8.8 onspeed max
        print('AOA line displayed for Hornet')

        if maxvalue < 10 and minvalue > 6:
            print('AOA Hornet * maxvalue < 10 and minvalue > 6 *')
            maxvalue = 10.01
            minvalue = 5.99

        if maxvalue > 10 and minvalue > 6:
            print('AOA Hornet ** maxvalue > 10 and minvalue > 6 **')
            minvalue = 3.99
        #if minvalue > 5.01:
        #    minvalue = 5.01

        print('Hornet Max value: ',maxvalue)
        print('Hornet Min value: ',minvalue)
        ax.set_ylim([minvalue,maxvalue])
        ax.set_facecolor(facecolor)

        stralph = 'a'
        stralph = 'AoA'
        #ax.text(1.1535,10.4,stralph,color='g',fontsize=22,alpha=0.3)
        ax.text(xpoint,10.2,stralph,color=labelcolor,fontsize=xpointsize,alpha=0.5)

        lm = ax.get_xlim()
        xmax = lm[1]

        if xmax < 0.7:
            #print('HORNET ** xmax < 0.7:')
            xmax = 0.7

        if xmax > 1.2:
            #print('TOMCAT ** xmax > 1.2:')
            xmax = 1.2

        ax.plot([0,xmax],[8.8,8.8],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
        ax.plot([0,xmax],[7.4,7.4],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
    elif hawk_aoa in ps: # 6.75 onspeed min, 7.00 onspeed, 7.25 onspeed max
        print('AOA line displayed for Goshawk')

        if maxvalue < 8.5 and minvalue > 6:
            print('AOA Goshawk * maxvalue < 10 and minvalue > 5 *')
            maxvalue = 8.51
            minvalue = 6.01

        if maxvalue > 10 and minvalue > 4:
            print('AOA Goshawk ** maxvalue > 10 and minvalue > 4 **')
            minvalue = 3.99
        #if minvalue > 5.01:
        #    minvalue = 5.01

        print('Goshawk Max value: ',maxvalue)
        print('Goshawk Min value: ',minvalue)
        ax.set_ylim([minvalue,maxvalue])
        ax.set_facecolor(facecolor)

        stralph = 'a'
        stralph = 'AoA'
        #ax.text(1.1535,10.4,stralph,color='g',fontsize=22,alpha=0.3)
        ax.text(xpoint,10.2,stralph,color=labelcolor,fontsize=xpointsize,alpha=0.5)

        lm = ax.get_xlim()
        xmax = lm[1]

        if xmax < 0.8:
            #print('Goshawk ** xmax < 0.7:')
            xmax = 0.8

        if xmax > 1.2:
            #print('Goshawk ** xmax > 1.2:')
            xmax = 1.2

        ax.plot([0,xmax],[7.25,7.25],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
        ax.plot([0,xmax],[6.75,6.75],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
    elif tomcatA_aoa or tomcatB_aoa in ps: # 9.5 onspeed min, 10.0 onspeed, 10.5 onspeed max - 2/14/21 Decided to try increading Tomcat 0.5
        print('AOA line displayed for Tomcat')

        if maxvalue < 12.0 and minvalue > 8.0:
            print('AOA Tomcat * maxvalue < 17.5 and minvalue > 12.5 *')
            maxvalue = 12.01
            minvalue = 7.99

        if maxvalue > 12.0 and minvalue > 8.0:
            print('AOA Tomcat ** maxvalue > 17.5 and minvalue > 12.5 **')
            minvalue = 5.99
        #if minvalue > 5.01:
        #    minvalue = 5.01

        print('Tomcat Max value: ',maxvalue)
        print('Tomcat Min value: ',minvalue)
        ax.set_ylim([minvalue,maxvalue]) #Added 2/1/21 - This will create the Y-axis max and min limits, I added 1.5 to show a little extra area above and below the red reference lines
        ax.set_facecolor(facecolor)

        stralph = 'a'
        stralph = 'AoA'
        #ax.text(1.1535,10.4,stralph,color='g',fontsize=22,alpha=0.3)
        ax.text(xpoint,10.2,stralph,color=labelcolor,fontsize=xpointsize,alpha=0.5)

        lm = ax.get_xlim() #Mathplot x-axis limits... barking up the wrong tree when trying to reprint the AOA reference lines... leave this as is.
        xmax = lm[1]

        if xmax < 0.7:
            #print('TOMCAT ** xmax < 0.7:')
            xmax = 0.7

        if xmax > 1.2:
            #print('TOMCAT ** xmax > 1.2:')
            xmax = 1.2

        ax.plot([0,xmax],[10.818,10.818],'g-',linewidth=1.2,alpha=0.8,linestyle='--') # Based on aoa to degree conversion degrees=.918*aoa-3.411
        ax.plot([0,xmax],[9.9,9.9],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
    elif harrier_aoa in ps: # 10 is onspeed min,  11 is onspeed, 12 is onspeed max
        if maxvalue < 13 and minvalue > 9:
            print('AOA * maxvalue < 17.5 and minvalue > 12.5 *')
            maxvalue = 13.01
            minvalue = 8.99

        if maxvalue > 13 and minvalue > 9:
            print('AOA ** maxvalue > 17.5 and minvalue > 12.5 **')
            minvalue = 6.99

        if maxvalue > 14 and minvalue < 8: #added 2/14/21 - This keeps the plot reference lines under control with wild AOA values seen with Harrier
            print('AOA ** maxvalue > 17.5 and minvalue > 12.5 **')
            maxvalue = 15.0
            minvalue = 7.0

        #if minvalue > 5.01:
        #    minvalue = 5.01

        print('Harrier Max value: ',maxvalue)
        print('Harrier Min value: ',minvalue)
        ax.set_ylim([minvalue,maxvalue])
        ax.set_facecolor(facecolor)

        stralph = 'a'
        stralph = 'AoA'
        #ax.text(1.1535,10.4,stralph,color='g',fontsize=22,alpha=0.3)
        ax.text(xpoint,10.2,stralph,color=labelcolor,fontsize=xpointsize,alpha=0.5)

        lm = ax.get_xlim() #Mathplot x-axis limits... barking up the wrong tree when trying to reprint the AOA reference lines... leave this as is.
        xmax = lm[1]

        if xmax < 0.7:
            xmax = 10.7
            print(' xmax = 10.7')
        if xmax > 1.2:
            xmax = 1.2
            print(' xmax = 1.2')

        print('AOA line displayed for skyhawk')
        ax.plot([0,xmax],[12.0,12.0],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
        ax.plot([0,xmax],[10.0,10.0],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
    elif skyhawk_aoa in ps: # 8.5 onspeed min, 8.75 onspeed, 9.0 onspeed max
        if maxvalue < 10.75 and minvalue > 6.75:
            print('AOA * maxvalue < 17.5 and minvalue > 12.5 *')
            maxvalue = 10.76
            minvalue = 6.74

        if maxvalue > 10.75 and minvalue > 6.75:
            print('AOA ** maxvalue > 17.5 and minvalue > 12.5 **')
            minvalue = 4.74
        #if minvalue > 5.01:
        #    minvalue = 5.01

        print('skyhawk Max value: ',maxvalue)
        print('skyhawk Min value: ',minvalue)
        ax.set_ylim([minvalue,maxvalue])
        ax.set_facecolor(facecolor)

        stralph = 'a'
        stralph = 'AoA'
        #ax.text(1.1535,10.4,stralph,color='g',fontsize=22,alpha=0.3)
        ax.text(xpoint,10.2,stralph,color=labelcolor,fontsize=xpointsize,alpha=0.5)

        lm = ax.get_xlim() #Mathplot x-axis limits... barking up the wrong tree when trying to reprint the AOA reference lines... leave this as is.
        xmax = lm[1]

        if xmax < 0.7:
            xmax = 0.7

        if xmax > 1.2:
            xmax = 1.2

        print('AOA line displayed for Skyhawk')
        ax.plot([0,xmax],[9.0,9.0],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
        ax.plot([0,xmax],[8.5,8.5],'g-',linewidth=1.2,alpha=0.8,linestyle='--') #g-
    else:
        print('no SH pass drawn')


    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'g-', linewidth=8, alpha=0.1)
    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'g-', linewidth=5, alpha=0.1)
    ax.plot(xy[0][:-num_aoa],ts['AoA'][:-num_aoa], 'g-', linewidth=3, alpha=0.15)
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

    lm = ax.get_xlim() #Mathplot x-axis limits... barking up the wrong tree when trying to reprint the AOA reference lines... leave this as is.
    xmax = lm[1]
    ax.set_xlim([0.001,xmax])
    ax.invert_xaxis()


    plt.show()

    titlestr = ''
    callsign = pinfo['callsign']
    titlestr = callsign;
    titlestr+=' '
    unicorn = 'unicorn_'
    if unicorn in ps:
        print('unicorn in file name so change the grade to _OK_')
        #print('SIERRA HOTEL PASS!')
        titlestr+='_OK_'
        titlestr+=' '
        titlestr+='5.0'
    else:
        print('no unicorn pass drawn')
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
    #titlestr+='\n'
    #titlestr+=' TESTING 1...2...3!'

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
    scooter = 'A-4E-C'
    goshawk = 'T-45'
	
    if hornet in ps:
        print('contains hornet')
        ps = ps.replace(hornet,'')
        pinfo['aircraft']='F/A-18C'
    elif goshawk in ps:
        print('contains goshawk')
        ps = ps.replace(goshawk,'')
        pinfo['aircraft']='T-45C'
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
    elif scooter in ps:
        print('contains scooter')
        ps = ps.replace(scooter,'')
        pinfo['aircraft']='A-4'
	
    else:
        print('unknown aircraft.')

    print(ps)



    pinfo['callsign']=ps[0:-1]
    return pinfo
def getCallsign(input):
    print('Getting callsign from: ', input)

# %%

# %%

#%%
trapfolder = 'C:/python_code/bm/trapsheets'
trapfolder = 'C:/FlightSimDocs/JOW/stats/SLModStats/LSO'
trapfolder = 'C:/HypeMan/trapsheets'
trapfolder = 'C:/Users/DCSAdmin/Saved Games/DCS.openbeta_server'
trapfolder = 'C:/Users/jow/Saved Games/DCS.openbeta_server'
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
