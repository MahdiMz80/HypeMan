import csv
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

import random
from time import sleep

# add a random delay to every upload entry.  The goal here is to prevent too many requests from happening at once
# and to prevent the case of two requests happening at exactly the same time, such as during a formation landing
# luvit/lua seem to be able to handle the rapid fire of UDP data coming from DCS, but the google sheets API
# limits the number of queries it will accept
sleep(random.uniform(1.0, 30))

if len(sys.argv) == 2:
	
	line = sys.argv[1]	

	result = [x.strip() for x in line.split(',')]
	
	# now = datetime.now() # current date and time
	# result.append(now.strftime("%d/%m/%Y"))
	# result.append(now.strftime("%H:%M:%S"))
	# print(list(result))
	
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('JOWFlightTrack-ceda2c0174a7.json', scope)
	client = gspread.authorize(creds)

	sheet = client.open('JowFlightStats').sheet1
	#list_of_hashes = sheet.get_all_records()


	print('Adding Flight Log Entry... ', end = '')

	row = result
	index = 2
	sheet.insert_row(row, index)
	print('Done!')