# DCS Weather Select

DCS Weather Select is a windows bat file that pops up a file selection dialog to select a DCS mission.  The weather inside that DCS mission is then updated to reflect the real world METAR data from a real weather reporting station. 
It's a slight modification of the version from havoc-company.com available here:  http://www.havoc-company.com/forum/viewtopic.php?f=30&t=1336.

## Getting Started

You will need to have a working version of Python installed.  I recommend the Anaconda Python distribution available here: https://www.anaconda.com/   install it under your "user" not for the "system" or else you will need to elevate
the command prompt to administrator every time you want to install python packages.

### Activating the Python Environment
By default python is not added to your path by default, keep it that way.  Each time you want to call "python" you will need to call this *activate.bat*.  By default Anaconda python is installed in C:\Users\%YOUR USERNAME%\Anaconda3\.

You will need to edit *weather_select_caucasus.bat* to match the path to the version of activate.bat and as an argument to activate.bat pass the path to the Anaconda3 folder.  For example, on my system I installed Anaconda to D:\Anaconda3.  My
weather_select_caucasus.bat contains this line:

```
call D:\Anaconda3\Scripts\activate.bat D:\Anaconda3
```

Yours may look something like:

```
call C:\Users\Stainer\Anaconda3\Scripts\activate.bat C:\Users\Stainer\Anaconda3
```
### Setting the Weather Stations
The weather stations to use are hard coded inside weather_select_caucasus.bat.  There is a primary, and a secondary weather station.  If the METAR is not available from the primary station the secondary is used.  For example:

```
SET PRIMARY_AIRPORT=URSS 
SET BACKUP_AIRPORT=UGSB
```

### Checkwx.com API key
You will need an API key from www.checkwx.com.  Sign up for a free account and you will be given an API key and modify *dcs_weather2.py* with this private API key.  For example:

```
s_api_key_checkwx = 'abc51c1c56692025b39bb41c5d '
```

# Frequency Asked Questions
- [Once every 5 years there may be a hurricane?](#once-every-5-years-there-may-be-a-hurricane)
- [What if we fly the DCS F-16 and can't handle any wind?](#what-if-we-fly-the-DCS-F-16-and-cant-handle-any-wind?)
- [What if this causes the boat to steer into land and beach itself?](#what-if-this-causes-the-boat-to-steer-into-land-and-beach-itself)
- [The weather generated wasn't perfect and made it slightly harder to team kill and strafe the runway on our casual training flights](#The-weather-generated-wasnt-perfect-and-made-it-slightly-harder-to-team-kill-and-strafe-the-runway-on-our-casual-training-flights)

## Once every 5 years there may be a hurricane?
Yes.  Because it's based on real weather every 5-10 years there may be hurricane strength winds that ruin your day.  Deal with it or just manually change the weather back to something to your liking.

## What if we fly the DCS F-16 and can't handle any wind?
Apparently the F-16 as a modern all-weather multirole combat fighter cannot operate in anything stiffer than a gentle summer breeze.  Direct all complaints to Eagle Dynamics.

## What if this causes the boat to steer into land and beach itself?
The US Navy has extensive experience performing aircraft recover operations with their large blue water Navy in very shallow litoral waters a couple of miles from land, follow the procedures outlined in NATOPS.

## The weather generated wasn't perfect and made it slightly harder to team kill and strafe the runway on our casual training flights?
Yes, the struggle is real.  

# Common METAR Weather Stations
URSS Sochi - https://www.checkwx.com/weather/URSS/metar
UGSB Batumi - https://www.checkwx.com/weather/UGSB/metar
