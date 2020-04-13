# dcs_weather2.py - originally by the Havoc company.  Slight modification
# to disable setting the mission to the real clock time of the server
#

import os
import re
import sys
import json
import time
import zipfile
import datetime
import requests
import random as rd
# you might need to run this in a command line window if this module is not installed
# pip install requests

# real time / weather update script for dcs world (tested under 1.5/2.5)
# created by havoc-company.com
s_version_info = " V1.3.2 2019.MAR.27_23:00"

# usage
# dcs_weather.py <path and file name of mission.miz> <primary_airport code> <backup_airport code> <time control>
# eg
# dcs_weather.py D:\DCS_Missions\Weapons_Training_v2.11.2.miz UGSB UGSS real
# dcs_weather.py D:\DCS_Missions\Weapons_Training_v2.11.2.miz UGSB UGSS rand
# ^ update and use random time of day
# dcs_weather.py D:\DCS_Missions\Weapons_Training_v2.11.2.miz KLAS KLAS 6
# ^ no backup airport and use preset #6 autumn evening
# time control - dawn = 0 1 2 3  dusk = 4 5 6 7
# use real time in mission <time control> = real
# https://www.world-airport-codes.com/ get ICAO code for airport you want to use
# https://www.world-airport-codes.com/alphabetical/country-name/g.html#georgia
# EGAA = int, URSS = sochi, URKK = Krasnador, UGTB = tibilsi, UGKS = kobuleti, UGGS = Sukhumi, UGSB = Batumi
# EGAC = city, OMDW = Al Maktoum, OMSJ = Sharjah, OOKB = khasab, OIKB = Bandar, OISS = Shiraz


class G:  # Globals class ...... to store all the data we need to mess with (populate with some defaults)

    # you need to register with www.checkwx.com create an account, then request an api key (takes 24hrs or less)
    # once activated your key will appear in your API dashboard www.checkwx.com/apikey
    #  enter your key below between the quotes

    
    s_api_key_checkwx = 'checkwx private api key goes here '

    filename_checkwx = 'data.checkwx.json'
    filename_avwx = 'data.avwx.json'

    b_debug_load = False  # these 2 value are for debug testing only leave them to False
    b_debug_checkwx = False

    b_daws_mission = False  # depreciated DAWS has been abandoned

    b_update_weather = True  # Set this to False if you do NOT want to use METAR weather

    s_cloud_base_min = '450'
    s_cloud_base_max = '5000'
    s_cloud_thickness_min = '200'
    s_cloud_thickness_max = '2000'
    s_fog_visibility_min = '1800'  # use this to limit how much fog visibility will effect things
    s_fog_visibility_max = '4200'  # was 6000
    s_fog_thickness_min = '0'
    s_fog_thickness_max = '1000'
    s_sand_visibility_min = '1600'
    s_sand_visibility_max = '2999'

    s_temperature = '8'

    s_cloud_base_m = '5000'
    s_cloud_thickness_m = '380'
    s_cloud_density = '0'  # no clouds by default
    s_iprecptns = '0'
    s_qnh = '760'

    s_wind_speed_8k = '15'
    s_wind_dir_8k = '0'
    s_wind_speed_2k = '10'
    s_wind_dir_2k = '0'
    s_wind_speed_gnd = '0'
    s_wind_dir_gnd = '180'

    s_turbulence = '20'

    s_fog_enable = 'false'  # fog off by default
    s_fog_visibility_m = '0'
    s_fog_thickness_m = '0'
    s_fog_density = '0'

    b_sand_storm = False
    s_sand_enable = 'false'
    s_sand_density_m = '0'

    s_primary_airport = ''
    s_backup_airport = ''
    s_mission_miz = ''                 # full name inc path
    s_mission_miz_filename = ''         # just filename
    s_mission_miz_path = ''            # path to miz file

    s_year = ''
    s_month = ''
    s_day = ''
    s_hour = ''
    s_mins = ''
    s_seconds = ''
    s_start_time = ''
    i_rand_template = 1
    # presets used if time is too late in day and dark eg autumn / winter, first block is Caucaus second Persian Gulf
    l_dates = [['2019', '03', '06', '7', '30'], ['2019', '06', '03', '5', '50'], ['2019', '09', '28', '7', '45'],
               ['2019', '12', '26', '8', '30'], ['2019', '03', '06', '14', '0'], ['2019', '06', '03', '16', '0'],
               ['2019', '09', '28', '14', '0'], ['2019', '12', '26', '13', '0'],

               ['2019', '03', '08', '6', '10'], ['2019', '06', '03', '5', '0'], ['2019', '09', '28', '5', '0'],
               ['2019', '12', '26', '6', '30'], ['2019', '03', '08', '12', '0'], ['2019', '06', '03', '13', '0'],
               ['2019', '09', '28', '12', '0'], ['2019', '12', '26', '12', '0']

               ]
    b_change_time = False  # set to to False if you do NOT want to update time
    b_qnh_update = True  # set this to True if you want to have the QNH set by METAR data
    b_adjust_for_daylight_savings = False  # this controls if u want to add one hour to account for clock going forward
    i_time_index = 0
    b_json_save = True  # this is for saving then loading the json data to/from file useful for debug or over ride
    json_weather = False


# TODO better less shite command line parsing (but this is test version to see if any problems)
# parse commandline stuff eg airport code / time
if len(sys.argv) < 5:
    print("Not enough arguments need more input")
    print("usage example")
    print('dcs_weather.py "D:\DCS_Missions\Weapons_Training_v2.11.2.miz" UGSB UGGS real')
    exit(1)
elif len(sys.argv) == 3:
    G.s_backup_airport = str(sys.argv[2])  # set backup to primary
elif len(sys.argv) == 4:
    G.s_primary_airport = str(sys.argv[2])
    G.s_backup_airport = str(sys.argv[3])
elif len(sys.argv) == 5:
    G.s_primary_airport = str(sys.argv[2])
    G.s_backup_airport = str(sys.argv[3])
    G.b_change_time = False
    if str(sys.argv[4]) == 'real':
        G.i_time_index = 99
    elif str(sys.argv[4]) == 'rand':
        G.i_time_index = 100
    else:
        G.i_time_index = int(sys.argv[4])
#  TODO maybe add check for number before setting this

# deal with filename and paths
G.s_mission_miz = sys.argv[1]
G.s_mission_miz_path, G.s_mission_miz_filename = os.path.split(sys.argv[1])
G.s_mission_miz_path = G.s_mission_miz_path + '\\'


def change_mission_data_item(l_mission, s_item, i_new_value, s_tab='\t\t'):  # used to change single unique item value
    i_mission_size = len(l_mission)
    i_count = 0
    s_new_item = s_tab + s_item + str(i_new_value) + ","

    while i_count < i_mission_size:
        if s_item in l_mission[i_count]:
            l_mission[i_count] = s_new_item
            break
        i_count += 1


# used to change single unique item value between 2 boundries
def change_mission_data_item_v2(l_mission, s_item, i_new_value, i_start_pos, i_end_pos, s_tab='\t\t'):
    s_new_item = s_tab + s_item + str(i_new_value) + ","

    while i_start_pos < i_end_pos:
        if s_item in l_mission[i_start_pos]:
            l_mission[i_start_pos] = s_new_item
            break
        i_start_pos += 1


def change_newline_chars_in_file(s_filename):  # used to deal with extra chars being written to file (0x0D)
    with open(s_filename, "rb") as input_file:
        content = input_file.read()
    content = content.replace(b"\x0D", b"\x0A")
    with open(s_filename, "wb") as output_file:
        output_file.write(content)


def check_weather_limits():
    # created this to make sure values fall within the acceptable range that can be configured in the DCS editor
    # dcs has a hard base limit of 300m, think we should be above it as people bitch about it
    s_base_tmp = G.s_cloud_base_m

    if int(G.s_cloud_base_m) <= int(G.s_cloud_base_min):  # going for ?
        i_diff = abs(int(s_base_tmp) - int(G.s_cloud_base_min))
        G.s_cloud_base_m = G.s_cloud_base_min
        G.s_cloud_thickness_m = str(int(G.s_cloud_thickness_m) + int(i_diff))

    if int(G.s_cloud_thickness_m) <= int(G.s_cloud_thickness_min):
        G.s_cloud_thickness_m = '200'
    if G.s_fog_enable == 'true':
        if int(G.s_fog_visibility_m) >= int(G.s_fog_visibility_max):  # make sure its not out of bounds for DCS
            G.s_fog_visibility_m = G.s_fog_visibility_max
        if int(G.s_fog_visibility_m) <= int(G.s_fog_visibility_min):
            G.s_fog_visibility_m = G.s_fog_visibility_min
    else:
        G.s_fog_visibility_m = '0'

    if G.s_sand_enable == 'true':
        if int(G.s_sand_density_m) >= int(G.s_sand_visibility_max):  # make sure its not out of bounds for DCS
            G.s_sand_density_m = G.s_sand_visibility_max
        if int(G.s_sand_density_m) <= int(G.s_sand_visibility_min):
            G.s_sand_density_m = G.s_sand_visibility_min
    else:
        G.s_sand_density_m = '0'

    if int(G.s_cloud_density) >= 9 or G.s_fog_enable == 'true' and int(G.s_cloud_base_m) <= 2000:
        G.s_cloud_base_m = '2000'


def convert_feet_to_meters(f_feet):  # cos we get data in feet
    # 1 foot = 0.3048 meters
    f_meters = float(f_feet) * 0.3048
    return str(int(f_meters))


def convert_to_hr_and_min_to_seconds():  # DCS uses seconds from 00:00 as time of day (this converts hr&min to this)
    G.s_start_time = str(int(G.s_hour) * 3600 + (int(G.s_mins) * 60) + int(G.s_seconds))


def convert_knots_to_m_per_sec(f_knots):  # used to convert the supplied knots value to meters per second
    # 1 knot = 0.514444 m per sec
    f_mps = float(f_knots) * 0.514444
    return str(int(f_mps))


def convert_hpa_to_mmhg(f_kpa):  # cos we get data in kPa
    #  1 kPa = 7.5006157584566 mmHg
    f_mmhg = float(f_kpa) * 0.75006157584566
    return str(int(round(f_mmhg, 1)))


def debug_load():
    if G.b_debug_checkwx:
        json_weather = load_json_data(G.filename_checkwx)
        get_checkwx_all_weather_parameters(json_weather)
    else:
        json_weather = load_json_data(G.filename_avwx)
        get_avwx_all_weather_parameters(json_weather)


def extract_mission_file(s_file_path, s_zip_file_name, s_file_to_extract):  # use zip module to get our mission file
    s_zip_to_open = s_file_path + s_zip_file_name
    if os.path.isfile(G.s_mission_miz):
        archive = zipfile.ZipFile(s_zip_to_open)
        for file in archive.namelist():
            if file.startswith(s_file_to_extract):
                archive.extract(file, s_file_path)
    else:
        print("WARNING: specified miz file does not exist")
        exit(1)


def find_item_index_from_start(l_mission, s_search):  # used to find which index (first list item) something is
    i_index = 0
    i_max = len(l_mission)
    ret_val = False
    while i_index < i_max:
        if s_search in l_mission[i_index]:
            ret_val = i_index
            # print("index " , i_index , "    ", l_mission[i_index])
            break
        i_index += 1
    return ret_val


def find_item_index(l_mission, s_search, i_stop_position, i_start_position=0):  # used to find index of item with params
    ret_val = False
    i_index = i_start_position
    while i_index != i_stop_position:
        if s_search in l_mission[i_index]:
            return i_index
        i_index += 1
    return ret_val


def gen_rand_dev(s_value, i_min, i_max):  # used to change values for wind speed / direction at diff alts
    i_deviation = rd.randint(i_min, i_max)
    i_value = int(s_value) + i_deviation
    if i_value < 0:
        i_value = 360 + i_value
    if i_value >= 360:
        i_value -= 360
    return str(i_value)


def get_weather1():
    # first try the primary (first site) and see of we get data ok
    G.json_weather = weather_read_url_checkwx()
    if G.json_weather is not False:
        if G.b_json_save:
            save_json_data(G.json_weather, G.filename_checkwx)
            G.json_weather = load_json_data(G.filename_checkwx)

        # set values in G array
        get_checkwx_all_weather_parameters(G.json_weather)


def get_weather2():
    # try secondary
    G.json_weather = weather_read_url_avwx()

    if G.json_weather is not False:
        if G.b_json_save:
            save_json_data(G.json_weather, G.filename_avwx)
            G.json_weather = load_json_data(G.filename_avwx)
        # set values in G array
        get_avwx_all_weather_parameters(G.json_weather)


def not_setup_correctly():
    print("")
    print("ERROR: You have not set-up you API KEY YET")
    print("you need to register with www.checkwx.com/ create an account,")
    print("then request an api key (takes 24hrs or less)")
    print("once activated your key will appear in your API dashboard")
    print(" www.checkwx.com/apikey ")
    print("enter your key in s_api_key_checkwx variable near the top of this script")
    time.sleep(2)


def get_avwx_all_weather_parameters(json_weather_l):  # going to read ALL weather info from json then stick it in G vars
    G.s_temperature = str(get_avwx_json_temperature(json_weather_l))
    get_avwx_weather_cloud_atmosphere(json_weather_l)
    get_avwx_weather_wind(json_weather_l)
    s_raw_report = get_avwx_json_raw_report(json_weather_l)
    get_avwx_fog_visibility(json_weather_l)

    get_weather_fog(s_raw_report)
    get_weather_sand_storm(s_raw_report)

    get_weather_turbulence()

    get_avwx_weather_qnh(json_weather_l)
    check_weather_limits()  # used to check we are within the limits DCS editor has


def get_avwx_json_other_list(json_weather_l):
    return json_weather_l['other']


def get_avwx_json_raw_report(json_weather_l):
    return json_weather_l['raw']


def get_avwx_json_temperature(json_weather_l):

    return json_weather_l['temperature']['value']


def get_avwx_json_wind_direction(json_weather_l):
    if not json_weather_l.get('wind_direction'):
        print("NO wind_speed data")
        return

    s_direction = str(json_weather_l['wind_direction']['value'])
    if s_direction is None:
        s_direction = 'VRB'

    if s_direction in 'VRB':  # variable means not measured (unknown)
        return str(rd.randint(0, 359))
    elif s_direction == '000':
        return '0'
    else:
        return s_direction


def get_avwx_fog_visibility(json_weather_l):
    # set fog view visibility distance (how far you can see before fog obscures stuff)
    G.s_fog_visibility_m = json_weather_l['visibility']['value']
    G.s_sand_density_m = json_weather_l['visibility']['value']
    if int(G.s_fog_visibility_m) > int(G.s_fog_visibility_max):  # make sure its not out of bounds for DCS
        G.s_fog_visibility_m = G.s_fog_visibility_max
    if int(G.s_sand_density_m) > int(G.s_sand_visibility_max):  # make sure its not out of bounds for DCS
        G.s_sand_density_m = G.s_sand_visibility_max


def get_avwx_weather_qnh(json_weather_l):
    G.s_qnh = convert_hpa_to_mmhg(json_weather_l['altimeter']['value'])


def get_avwx_weather_cloud_atmosphere(json_weather_l):  # read json and set the cloud settings from it
    # get record count - how many cloud data items do we have
    s_raw_report = get_avwx_json_raw_report(json_weather_l)
    print("raw ", s_raw_report)
    if "CAVOK" in s_raw_report:
        return

    b_tmp = json_weather_l.get('clouds')
    if not b_tmp:
        G.s_cloud_density = '0'
        return
    else:
        i_max_cloud_records = len(b_tmp)
        if i_max_cloud_records == 0:
            G.s_cloud_density = '0'
            return

    # need to make sure there are some clouds first ? is Zero its a CLR day
    if i_max_cloud_records == 0:
        s_cloud_base = 5000
    else:
        s_cloud_base = json_weather_l['clouds'][0]['altitude']  # set cloud base as first record height (lowest clouds)

    if i_max_cloud_records == 1:
        # if only one cloud record then set cloud alt and cloud type
        G.s_cloud_thickness_m = str(rd.randint(200, 300))
        G.s_cloud_base_m = convert_feet_to_meters((int(s_cloud_base) * 100))
        s_cloud_cover = json_weather_l['clouds'][0]['type']

    elif i_max_cloud_records > 1:
        # if we have multiple cloud records use difference between max and min for cloud depth
        G.s_cloud_base_m = convert_feet_to_meters((int(s_cloud_base)) * 100)
        s_cloud_alt_max_ft = int(json_weather_l['clouds'][i_max_cloud_records - 1]['altitude']) * 100  # height alt ft
        s_cloud_alt_min_ft = int(json_weather_l['clouds'][0]['altitude']) * 100  # get low
        G.s_cloud_thickness_m = str(convert_feet_to_meters(s_cloud_alt_max_ft - s_cloud_alt_min_ft))  # top to bottom
        s_cloud_cover = json_weather_l['clouds'][i_max_cloud_records - 1]['type']  # get last record cloud type
    else:
        s_cloud_cover = 'CLR'  # stick a default value here (if there is no cloud records)

    # common parse could cover type into number
    G.s_cloud_density = '0'  # default value
    if s_cloud_cover in ('SKC', 'NCD', 'CLR', 'NSC'):
        G.s_cloud_density = '0'
    elif s_cloud_cover in 'FEW':
        G.s_cloud_density = str(rd.randint(1, 2))
    elif s_cloud_cover in 'SCT':
        G.s_cloud_density = str(rd.randint(3, 4))
    elif s_cloud_cover in 'BKN':
        G.s_cloud_density = str(rd.randint(5, 8))
    elif s_cloud_cover in 'OVC':
        G.s_cloud_density = '9'
        G.s_cloud_thickness_m = '200'
    elif s_cloud_cover in 'VV':
        G.s_cloud_density = str(rd.randint(2, 8))

    # Rules cloud >= 5 then, ["iprecptns"] = 0 = none , 1 = rain , 2 = thunderstorm(if cloud>=9)
    # if temp <=0 then,  3 = snow, 4 = snowstorm(if cloud>=9)
    s_raw_report = get_avwx_json_raw_report(json_weather_l)
    l_rain = ['RA', 'DZ', 'GR', 'UP']
    l_snow = ['SN', 'SG', 'PL']
    l_other = ['TS']  # thunderstorm

    if any(x in s_raw_report for x in l_rain):
        #  print("RA found")
        G.s_iprecptns = '1'  # rain
    elif any(x in s_raw_report for x in l_snow):
        if int(G.s_temperature) <= 2:  # is it cold enough for snow/snow storm ?
            if int(G.s_cloud_density) >= 9:
                G.s_iprecptns = '4'  # snow storm
            else:
                G.s_iprecptns = '3'  # snow
    elif any(x in s_raw_report for x in l_other):
        G.s_cloud_density = '9'  # over ride this to match DCS
        G.s_iprecptns = '2'  # thunderstorm
    else:
        G.s_iprecptns = '0'  # no rain at all


def get_avwx_weather_wind(json_weather_l):  # read json weather data and set the wind info from it
    # weather at ground

    if 'wind_speed' not in json_weather_l:
        print("AVWX: No wind speed data")
        return

    s_knots = json_weather_l['wind_speed']['value']
    s_mps = convert_knots_to_m_per_sec(float(s_knots))
    G.s_wind_speed_gnd = s_mps

    G.s_wind_dir_gnd = get_avwx_json_wind_direction(json_weather_l)  # this function will get a bullshit or real value

    l_wind_variable_dir = get_avwx_wind_variable_dir(json_weather_l)
    if not l_wind_variable_dir:
        i_winds_size = 0
    else:
        i_winds_size = len(l_wind_variable_dir)
    #  print("l_wind_variable_dir ",  l_wind_variable_dir, " size is ", i_winds_size)

    # if l_wind_variable_dir is None:
    if i_winds_size == 0:
        G.s_wind_speed_gnd = str(rd.randint(0, 10))
        G.s_wind_dir_2k = gen_rand_dev(G.s_wind_dir_gnd, -10, 10)
        G.s_wind_dir_8k = gen_rand_dev(G.s_wind_dir_gnd, -20, 20)
    else:
        if represents_int(l_wind_variable_dir[0]['repr']):
            if i_winds_size > 1:  # must have at least 2
                G.s_wind_dir_2k = l_wind_variable_dir[0]['repr']
                G.s_wind_dir_8k = l_wind_variable_dir[1]['repr']
            elif i_winds_size == 1:  # single
                G.s_wind_dir_2k = l_wind_variable_dir[0]['repr']
                G.s_wind_dir_8k = gen_rand_dev(G.s_wind_dir_gnd, -20, 20)  # randomise gnd dir
        else:
            print("No variable wind ")
            G.s_wind_dir_2k = gen_rand_dev(G.s_wind_dir_gnd, -10, 10)
            G.s_wind_dir_8k = gen_rand_dev(G.s_wind_dir_gnd, -20, 20)

    # wind at 2k - we use ground level value and randomise
    G.s_wind_speed_2k = gen_rand_dev(s_mps, 1, 3)

    # wind at 8k - we use ground level value and randomise a bit more
    G.s_wind_speed_8k = gen_rand_dev(s_mps, 2, 8)


def get_avwx_wind_variable_dir(json_weather_l):
    if not json_weather_l.get('wind_variable_direction'):
        return False
    else:
        return json_weather_l['wind_variable_direction']


def get_checkwx_json_raw_report(json_weather_l):
    return json_weather_l['data'][0].get('raw_text')


def get_checkwx_json_temperature(json_weather_l):
    # get temperature
    return str(json_weather_l['data'][0]['temperature']['celsius'])


def get_checkwx_weather_cloud_atmosphere(json_weather_l):
    # get clouds / atmosphere
    s_raw_report = get_checkwx_json_raw_report(json_weather_l)
    if "CAVOK" in s_raw_report:
        return

    if not json_weather_l['data'][0].get('clouds'):
        print("NO cloud data")
        G.s_cloud_density = '0'
        return

    i_max_cloud_records = len(json_weather_l['data'][0]['clouds'])
    # print("Max records is ", i_max_cloud_records)  # debug info

    s_cloud_cover = json_weather_l['data'][0]['clouds'][0]['code']
    if s_cloud_cover not in ('SKC', 'NCD', 'CLR', 'NSC', 'CAVOK'):

        if i_max_cloud_records == 0:
            s_cloud_base_m = 5000
        else:
            s_cloud_base_m = str(int(convert_feet_to_meters((round(json_weather_l['data'][0]['clouds'][0]
                                                                   ['base_feet_agl'], 0)))))
            # set cloud base as first record height (lowest clouds)

        if i_max_cloud_records == 1:
            # if only one cloud record then set cloud alt and cloud type
            G.s_cloud_thickness_m = str(rd.randint(200, 800))
            G.s_cloud_base_m = s_cloud_base_m
            s_cloud_cover = json_weather_l['data'][0]['clouds'][0]['code']
        elif i_max_cloud_records > 1:
            # if we have multiple cloud records use difference between max and min for cloud depth
            G.s_cloud_base_m = s_cloud_base_m
            s_cloud_alt_max_m = int(convert_feet_to_meters(round(json_weather_l['data'][0]['clouds']
                                                                 [i_max_cloud_records-1]['base_feet_agl'], 0)))
            s_cloud_alt_min_m = int(convert_feet_to_meters(round(json_weather_l['data'][0]['clouds'][0]
                                                                 ['base_feet_agl'], 0)))
            G.s_cloud_thickness_m = str(s_cloud_alt_max_m - s_cloud_alt_min_m)
            s_cloud_cover = json_weather_l['data'][0]['clouds'][i_max_cloud_records - 1]['code']
        else:
            s_cloud_cover = 'CLR'  # stick a default value here (if there is no cloud records)

    # common parse could cover type into number
    G.s_cloud_density = '0'  # default value
    if s_cloud_cover in ('SKC', 'CLR', 'NSC', 'CAVOK'):
        G.s_cloud_density = '0'
    elif s_cloud_cover in 'FEW':
        G.s_cloud_density = str(rd.randint(1, 2))
    elif s_cloud_cover in 'SCT':
        G.s_cloud_density = str(rd.randint(3, 4))
    elif s_cloud_cover in 'BKN':
        G.s_cloud_density = str(rd.randint(5, 8))
    elif s_cloud_cover in 'OVC':
        G.s_cloud_density = '9'
        G.s_cloud_thickness_m = '200'
    elif s_cloud_cover in 'VV':
        G.s_cloud_density = str(rd.randint(2, 8))

    s_raw_report = str(json_weather_l['data'][0]['raw_text'])
    # print("raw is ", s_raw_report)
    l_rain = ['RA', 'DZ', 'GR', 'UP']
    l_snow = ['SN', 'SG', 'PL']
    l_other = ['TS']  # thunderstorm

    if any(x in s_raw_report for x in l_rain):
        #  print("RA found")
        G.s_iprecptns = '1'  # rain
    elif any(x in s_raw_report for x in l_snow):
        if int(G.s_temperature) <= 2:  # is it cold enough for snow/snow storm ?
            if int(G.s_cloud_density) >= 9:
                G.s_iprecptns = '4'  # snow storm
            else:
                G.s_iprecptns = '3'  # snow
    elif any(x in s_raw_report for x in l_other):
        G.s_cloud_density = '9'  # over ride this to match DCS
        G.s_iprecptns = '2'  # thunderstorm
    else:
        G.s_iprecptns = '0'  # no rain at all


def get_checkwx_weather_qnh(json_weather_l):
    G.s_qnh = convert_hpa_to_mmhg(json_weather_l['data'][0]['barometer']['mb'])


def get_checkwx_weather_wind(json_weather_l):
    # get wind
    if not json_weather_l['data'][0].get('wind'):
        print("NO wind data")
        return

    i_wind_records = len(json_weather_l['data'][0]['wind'])
    s_direction = str(json_weather_l['data'][0]['wind']['degrees'])
    if s_direction is None:
        s_direction = '0'

    if 'VRB' in s_direction:  # variable means not measured (unknown)
        s_direction = str(rd.randint(0, 359))
        s_mps = str(rd.randint(0, 20))
        G.s_wind_speed_gnd = str(s_mps)
    else:
        if i_wind_records > 1:
            s_mps = int(json_weather_l['data'][0]['wind']['speed_mps'])
            G.s_wind_speed_gnd = str(s_mps)
        else:
            s_direction = '0'

    G.s_wind_dir_gnd = str(s_direction)
    G.s_wind_dir_2k = gen_rand_dev(G.s_wind_dir_gnd, -10, 10)
    G.s_wind_dir_8k = gen_rand_dev(G.s_wind_dir_gnd, -20, 20)
    G.s_wind_speed_2k = gen_rand_dev(G.s_wind_speed_gnd, 1, 3)
    G.s_wind_speed_8k = gen_rand_dev(G.s_wind_speed_gnd, 2, 8)


def get_checkwx_fog_visibility(json_weather_l):
    # set fog view visibility distance (how far you can see before fog obscures stuff)
    if not json_weather_l['data'][0].get('visibility'):
        print("NO visibility data")
        return

    i_tmp = json_weather_l['data'][0]['visibility']['meters']
    i_tmp = re.sub('[,+]', '', i_tmp)
    G.s_fog_visibility_m = i_tmp
    G.s_sand_density_m = i_tmp
    # print(G.s_fog_visibility_m)


def get_checkwx_all_weather_parameters(json_weather_l):
    G.s_temperature = get_checkwx_json_temperature(json_weather_l)
    get_checkwx_weather_cloud_atmosphere(json_weather_l)
    get_checkwx_weather_wind(json_weather_l)

    s_raw_report = json_weather_l['data'][0]['raw_text']

    get_checkwx_fog_visibility(json_weather_l)

    get_weather_fog(s_raw_report)
    get_weather_sand_storm(s_raw_report)

    # turbulence
    get_weather_turbulence()
    get_checkwx_weather_qnh(json_weather_l)
    # weather limits
    check_weather_limits()


def get_weather_turbulence():
    # 0 is nothing, 60 is crap your pants time ....  0.1* m = 6mps
    i_min_turbulence = 0
    i_max_turbulence = 20
    i_wind_speed_gnd = int(G.s_wind_speed_gnd)
    #  print("wind sped gnd ", i_wind_speed_gnd)
    if i_wind_speed_gnd <= 5:
        i_min_turbulence = 0
        i_max_turbulence = 12
    if 6 <= i_wind_speed_gnd <= 10:
        i_min_turbulence = 12
        i_max_turbulence = 25
    if 11 <= i_wind_speed_gnd <= 15:
        i_min_turbulence = 15
        i_max_turbulence = 35
    if 16 <= i_wind_speed_gnd <= 20:
        i_min_turbulence = 25
        i_max_turbulence = 50
    if 21 <= i_wind_speed_gnd <= 25:
        i_min_turbulence = 30
        i_max_turbulence = 60
    if i_wind_speed_gnd > 30:
        i_min_turbulence = 35
        i_max_turbulence = 70
    #  print("Turb min ", i_min_turbulence, " max ", i_max_turbulence)
    G.s_turbulence = str(rd.randint(i_min_turbulence, i_max_turbulence))


def get_mission_date_time():  # get the time date store in G.
    if G.i_time_index == 100:
        G.s_start_time = str(rd.randint(0, 86400))
        print("Using Random time")
        return

    elif G.i_time_index == 99:  # this is for real server time to set mission time
        print("Real time")
        # do real time calc stuff here
        a = datetime.datetime.now()
        now = a + datetime.timedelta(0, 180)  # add 180 seconds as it takes this long to spool the server up and load
        # due to summer/winter time check if between change date then + 1
        d_start = datetime.date(now.year, 10, 29)
        d_now_date = datetime.date(now.year, now.month, now.day)
        d_end = datetime.date(now.year + 1, 3, 26)
        if G.b_adjust_for_daylight_savings:
            if d_start < d_now_date < d_end:
                now = a + datetime.timedelta(0, 3780)  # add 1 hour 180 seconds forward

        G.s_year = str(now.year)
        G.s_month = str(now.month)
        G.s_day = str(now.day)
        G.s_hour = str(now.hour)
        G.s_mins = str(now.minute)
        G.s_seconds = str(now.second)
    else:
        # do time array stuff here
        print("Using array time/date # ", G.i_time_index)
        G.s_year = G.l_dates[G.i_time_index][0]
        G.s_month = G.l_dates[G.i_time_index][1]
        G.s_day = G.l_dates[G.i_time_index][2]
        G.s_hour = G.l_dates[G.i_time_index][3]
        G.s_mins = G.l_dates[G.i_time_index][4]
        G.s_seconds = str(0)
    convert_to_hr_and_min_to_seconds()


def get_weather_sand_storm(s_raw_report):
    if not G.b_sand_storm:
        print("NOT persian gulf mission")
        return
    print("Persian Gulf mission")
    l_sand = ['DU', 'SA']  # should I add 'HZ' to this array ?
    if not any(x in s_raw_report for x in l_sand):  # search it for ANY sand storm tags
        G.s_sand_enable = 'false'
        return False
    G.s_sand_enable = 'true'
    # G.s_fog_enable = 'false'


def get_weather_fog(s_raw_report):  # read raw report and see if any fog markers
    l_fog = ['BR', 'FG', 'FU', 'VA', 'HZ', 'PY']  # codes for obscure weather
    if not any(x in s_raw_report for x in l_fog):  # search it for ANY fog tags
        #  print("Fog NOT found")  # debug info
        if int(G.s_fog_visibility_m) >= 6000 or G.s_iprecptns == '0':  # if def val for dist intact? or greater than
            G.s_fog_enable = 'false'
            return False  # bail out and leave defaults as is

    G.s_fog_enable = 'true'
    G.s_fog_thickness_m = str(500 + rd.randint(-50, 200))  # generate a random thickness value
    G.s_fog_density = '7'  # set it to ON


def is_sandstorm_terrain(l_mission):
    s_persian_gulf = '["theatre"] = "PersianGulf"'
    if find_item_index_from_start(l_mission, s_persian_gulf):
        return True
    else:
        return False


def load_json_data(filename):
    with open(filename) as infile:
        data = json.load(infile)
        infile.close()
        return data


def read_mission_file(s_filename_to_read):  # read actual file mission into a list for changing
    file = open(s_filename_to_read, "rU", encoding="utf8")
    l_content = list(file)
    l_content = [x.rstrip('\x0A\x0D') for x in l_content]
    if l_content[0] == 'mission = {}':   # is this a DAWS mission file ?
        G.b_daws_mission = True
    return l_content


def retrieve_json_data_from_web(s_request, s_header=None):  # connect to url and grab METAR data
    print(s_request)
    try:  # Can we get connect to the website..... Better check first verify=False
        response = requests.get(s_request, headers=s_header, timeout=8, verify=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(requests.exceptions.HTTPError)
        return False
    except requests.exceptions.ReadTimeout:
        print("HTTP read time out")
        return False
    except requests.exceptions.Timeout:
        print("HTTP time out")
        return False
    except requests.exceptions.TooManyRedirects:
        print("Too many re-directs")
        return False
    except requests.exceptions.RequestException as e:  # catch any problem and print out what it is here
        print(e)
        sys.exit(1)
    else:
        #  print(response.text)  # print out raw data
        json_object = json.loads(response.text)
        if json_object is False:
            return False
        if 'Error' in json_object:  # this is to cover sometimes getting an error string from the server
            # print(json_object)
            return False
        # print(json_object)
        return json_object


def save_json_data(json_data, filename):
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)
        outfile.close()


def save_date_and_time(l_mission):  # save time/date info into mission list
    s_year = 'mission["date"]["Year"] ='
    s_day = 'mission["date"]["Day"] = '
    s_month = 'mission["date"]["Month"] = '
    i_mission_size = len(l_mission)

    if G.b_daws_mission:
        if G.i_time_index != 100:
            i_date_start = find_item_index(l_mission, 'mission["date"] = {}', i_mission_size)
            l_mission[i_date_start + 1] = s_year + G.s_year
            l_mission[i_date_start + 2] = s_day + G.s_day
            l_mission[i_date_start + 3] = s_month + G.s_month
        else:
            change_mission_data_item(l_mission, 'mission["start_time"] = ', str(G.s_start_time), '')
    else:
        if G.i_time_index != 100:
            print("Setting date")
            # set year , month and date in mission
            change_mission_data_item(l_mission, '["Year"] = ', str(G.s_year))
            # month
            change_mission_data_item(l_mission, '["Month"] = ', str(G.s_month))
            # day
            change_mission_data_item(l_mission, '["Day"] = ', str(G.s_day))
            # time, hmm tricky find ["forcedOptions"] then -1 write value cos it will be start_time in seconds 00:00
            # because start_time appears a lot thru the mission file

    i_forced = find_item_index(l_mission, '["forcedOptions"]', i_mission_size)
    l_mission[i_forced-1] = '\t' + '["start_time"] = ' + G.s_start_time + ','
    print("Writing seconds start value ", G.s_start_time)


def save_cloud_atmosphere(l_mission):  # save cloud data into mission file list
    s_cloud_start = '["clouds"]'
    s_daws_cloud_start = 'mission["weather"]["clouds"]["thickness"] = '
    s_thickness = '["thickness"] = '
    s_dense = '["density"] = '
    s_cloud_base = '["base"] = '
    s_cloud_rain = '["iprecptns"] = '

    i_max_line = len(l_mission)

    if G.b_daws_mission:
        i_start_clouds = find_item_index(l_mission, s_daws_cloud_start, i_max_line)
        l_mission[i_start_clouds] = s_daws_cloud_start + G.s_cloud_thickness_m  # thickness of clouds
        l_mission[i_start_clouds + 1] = 'mission["weather"]["clouds"]["density"] = ' + G.s_cloud_density
        l_mission[i_start_clouds + 2] = 'mission["weather"]["clouds"]["base"] = ' + G.s_cloud_base_m
        l_mission[i_start_clouds + 3] = 'mission["weather"]["clouds"]["iprecptns"] = ' + G.s_iprecptns

    else:
        # get record count (mission list size)
        i_start_clouds = find_item_index(l_mission, s_cloud_start, i_max_line)  # omitting start means begin index @ 0

        l_mission[i_start_clouds + 2] = '\t\t\t' + s_thickness + G.s_cloud_thickness_m + ","  # thickness of clouds
        l_mission[i_start_clouds + 3] = '\t\t\t' + s_dense + G.s_cloud_density + ","  # density of clouds
        l_mission[i_start_clouds + 4] = '\t\t\t' + s_cloud_base + G.s_cloud_base_m + ","  # cloud base

        change_mission_data_item(l_mission, s_cloud_rain, G.s_iprecptns, '\t\t\t')
        #  l_mission[i_start_clouds + 5] = '\t\t\t' + s_cloud_rain + G.s_iprecptns + ","


def save_data_to_mission(l_mission):  # save all data we have into mission list
    s_temp = '["temperature"] = '
    s_temp_daws = 'mission["weather"]["season"]["temperature"] = '
    s_turb = '["groundTurbulence"] = '
    s_turb_daws = 'mission["weather"]["groundTurbulence"] = '

    save_fog(l_mission)
    save_sand(l_mission)
    save_cloud_atmosphere(l_mission)
    save_wind(l_mission)
    save_qnh(l_mission)
    if G.b_daws_mission:
        i_max_line = len(l_mission)
        i_start_turb = find_item_index(l_mission, s_turb_daws, i_max_line)
        l_mission[i_start_turb] = s_turb_daws + G.s_turbulence
        i_start_temp = find_item_index(l_mission, s_temp_daws, i_max_line)
        l_mission[i_start_temp] = s_temp_daws + G.s_temperature
    else:
        change_mission_data_item(l_mission, s_turb, G.s_turbulence, '\t\t')
        change_mission_data_item(l_mission, s_temp, G.s_temperature, '\t\t\t')


def save_fog(l_mission):  # save fog data into mission list
    s_fog_start = '["fog"]'
    s_fog_vis = '["visibility"] = '
    s_fog_enable = '["enable_fog"] = '
    s_fog_enable_daws = 'mission["weather"]["enable_fog"] = '
    s_thickness = '["thickness"] = '
    s_fog_start_daws = 'mission["weather"]["fog"]["thickness"] = '

    i_max_line = len(l_mission)

    if G.b_daws_mission:
        i_fog_start = find_item_index(l_mission, s_fog_start_daws, i_max_line)
        l_mission[i_fog_start] = s_fog_start_daws + G.s_fog_thickness_m
        l_mission[i_fog_start + 1] = 'mission["weather"]["fog"]["visibility"] = ' + G.s_fog_visibility_m
        # l_mission[i_fog_start + 2] = 'mission["weather"]["fog"]["density"] = ' + G.s_fog_density
        i_fog_en = find_item_index(l_mission, s_fog_enable_daws, i_max_line)
        l_mission[i_fog_en] = s_fog_enable_daws + G.s_fog_enable
    else:
        # find start of fog data stuff
        i_fog_start = find_item_index_from_start(l_mission, s_fog_start)
        i_fog_end = find_item_index_from_start(l_mission, 'end of ["fog"]')

        change_mission_data_item(l_mission_data, s_fog_enable, G.s_fog_enable, '\t\t')  # enable fog flag
        # set fog thickness (height above ground before fog
        change_mission_data_item_v2(l_mission, s_thickness, G.s_fog_thickness_m, i_fog_start, i_fog_end, s_tab='\t\t\t')
        # l_mission[i_fog_start + 2] = '\t\t\t' + s_thickness + G.s_fog_thickness_m + ","  # fog view thickness

        # set fog view visibility distance (how far you can see before fog obscures stuff)
        change_mission_data_item_v2(l_mission, s_fog_vis, G.s_fog_visibility_m, i_fog_start, i_fog_end, s_tab='\t\t\t')
        # l_mission[i_fog_start + 3] = '\t\t\t' + s_fog_vis + G.s_fog_visibility_m + ","  # fog view visibility

        # set fog density - fuck knows what this does but 7 seems ok
        # l_mission[i_fog_start + 3] = '\t\t\t' + s_fog_density + G.s_fog_density + ","  # fog density


def save_qnh(l_mission):
    s_qnh = '["qnh"] = '
    s_qnh_daws = 'mission["weather"]["qnh"] = '
    if not G.b_qnh_update:
        return
    if G.b_daws_mission:
        i_max_line = len(l_mission)
        i_start_qnh = find_item_index(l_mission, s_qnh_daws, i_max_line)
        l_mission[i_start_qnh] = s_qnh_daws + G.s_qnh
    else:
        change_mission_data_item(l_mission_data, s_qnh, G.s_qnh, '\t\t')


def save_sand(l_mission):
    s_sand_enable = '["enable_dust"] = '
    s_sand_density = '["dust_density"] = '
    change_mission_data_item(l_mission_data, s_sand_enable, G.s_sand_enable, '\t\t')
    change_mission_data_item(l_mission_data, s_sand_density, G.s_sand_density_m, '\t\t')


def save_wind(l_mission):  # save wind speed direction info into mission list
    s_wind_speed = '["speed"] = '
    s_wind_dir = '["dir"] = '
    s_wind_at_8k = '["at8000"]'
    s_wind_at_gnd = '["atGround"]'
    s_wind_at_2k = '["at2000"]'
    s_wind_start8k = 'mission["weather"]["wind"]["at8000"]["speed"] = '
    s_wind_startgnd = 'mission["weather"]["wind"]["atGround"]["speed"] = '
    s_wind_start2k = 'mission["weather"]["wind"]["at2000"]["speed"] = '

    i_max_line = len(l_mission)

    if G.b_daws_mission:
        i_start_wind8k = find_item_index(l_mission, s_wind_start8k, i_max_line)
        l_mission[i_start_wind8k] = s_wind_start8k + G.s_wind_speed_8k
        l_mission[i_start_wind8k + 1] = 'mission["weather"]["wind"]["at8000"]["dir"] = ' + G.s_wind_dir_8k

        i_start_windgnd = find_item_index(l_mission, s_wind_startgnd, i_max_line)
        l_mission[i_start_windgnd] = s_wind_startgnd + G.s_wind_speed_gnd
        l_mission[i_start_windgnd + 1] = 'mission["weather"]["wind"]["atGround"]["dir"] = ' + G.s_wind_dir_gnd

        i_start_wind2k = find_item_index(l_mission, s_wind_start2k, i_max_line)
        l_mission[i_start_wind2k] = s_wind_start2k + G.s_wind_speed_2k
        l_mission[i_start_wind2k + 1] = 'mission["weather"]["wind"]["at2000"]["dir"] = ' + G.s_wind_dir_2k

    else:
        # find start of WIND ground section
        i_start_wind_at_gnd = find_item_index(l_mission, s_wind_at_gnd, i_max_line)  # omitting start  begin index @ 0
        l_mission[i_start_wind_at_gnd + 2] = '\t\t\t\t' + s_wind_speed + G.s_wind_speed_gnd + ","
        l_mission[i_start_wind_at_gnd + 3] = '\t\t\t\t' + s_wind_dir + G.s_wind_dir_gnd + ","

        # find start of WIND 2K section
        i_start_wind_at_2k = find_item_index(l_mission, s_wind_at_2k, i_max_line)  # omitting start begin index @ 0
        l_mission[i_start_wind_at_2k + 2] = '\t\t\t\t' + s_wind_speed + G.s_wind_speed_2k + ","
        l_mission[i_start_wind_at_2k + 3] = '\t\t\t\t' + s_wind_dir + G.s_wind_dir_2k + ","

        # find start of WIND 8K section
        i_start_wind_at_8k = find_item_index(l_mission, s_wind_at_8k, i_max_line)  # omitting start  begin index @ 0
        l_mission[i_start_wind_at_8k + 2] = '\t\t\t\t' + s_wind_speed + G.s_wind_speed_8k + ","
        l_mission[i_start_wind_at_8k + 3] = '\t\t\t\t' + s_wind_dir + G.s_wind_dir_8k + ","


def print_all_data():  # debug just so we can see what values we have
    print("b_daws_mission is ", G.b_daws_mission)
    print("s_temperature is ", G.s_temperature)
    print("s_cloud_thickness_m is ", G.s_cloud_thickness_m)
    print("s_cloud_density is ", G.s_cloud_density)
    print("s_cloud_base_m is ", G.s_cloud_base_m)
    print("s_iprecptns is ", G.s_iprecptns)
    print("s_qnh is ", G.s_qnh)
    print("s_wind_speed_8k is ", G.s_wind_speed_8k)
    print("s_wind_dir_8k is ", G.s_wind_dir_8k)
    print("s_wind_speed_2k is ", G.s_wind_speed_2k)
    print("s_wind_dir_2k is ", G.s_wind_dir_2k)
    print("s_wind_speed_gnd is ", G.s_wind_speed_gnd)
    print("s_wind_dir_gnd is ", G.s_wind_dir_gnd)
    print("s_turbulence is ", G.s_turbulence)
    print("s_fog_enable ", G.s_fog_enable)
    print("s_fog_visibility_m ", G.s_fog_visibility_m)
    print("s_fog_thickness_m ", G.s_fog_thickness_m)
    print("s_fog_density ", G.s_fog_density)
    print("s_sand_enable ", G.s_sand_enable)
    print("s_sand_density ", G.s_sand_density_m)
    print("s_primary_airport ", G.s_primary_airport)
    print("s_backup_airport ", G.s_backup_airport)
    print("s_year ", G.s_year)
    print("s_month ", G.s_month)
    print("s_day ", G.s_day)
    print("s_hour ", G.s_hour)
    print("s_mins ", G.s_mins)
    print("s_seconds ", G.s_seconds)
    print("s_start_time ", G.s_start_time)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def represents_int(s_value):
    try:
        int(s_value)
        return True
    except ValueError:
        return False


def weather_read_url_checkwx():  # try to read metar data for airport(s) from internet
    if G.s_api_key_checkwx == 'NOT_SET_YET':
        not_setup_correctly()

    s_url1 = 'https://api.checkwx.com/metar/' + G.s_primary_airport + '/decoded'
    s_url2 = 'https://api.checkwx.com/metar/' + G.s_backup_airport + '/decoded'
    s_headers = {'X-API-Key': G.s_api_key_checkwx}

    json_object = False  # just stuck this here to stick pycharm whining like a little bitch
    # we should try primary twice with a 5 second wait between attempts
    i_count = 0
    while i_count < 1:
        json_object = retrieve_json_data_from_web(s_url1, s_headers)  # try primary airport
        if json_object is not False:
            break
        time.sleep(5)
        i_count += 1

    if json_object is False:
        i_count = 0
        while i_count < 2:
            json_object = retrieve_json_data_from_web(s_url2, s_headers)  # try backup airport
            if json_object is not False:
                break
            time.sleep(5)
            i_count += 1

    return json_object


def weather_read_url_avwx():  # try to read metar data for airport(s) from internet
    s_url_base = "https://avwx.rest/api/preview/metar/"
    # s_url_base = "https://avwx.rest/api/metar/"
    s_url1 = s_url_base + G.s_primary_airport
    s_url2 = s_url_base + G.s_backup_airport
    json_object = False  # just stuck this here to stick pycharm whining like a little bitch

    # we should try primary twice with a 5 second wait between attempts
    i_count = 0
    while i_count < 1:
        json_object = retrieve_json_data_from_web(s_url1)  # try primary airport
        if json_object is not False:
            break
        time.sleep(5)
        i_count += 1

    if json_object is False:
        i_count = 0
        while i_count < 2:
            json_object = retrieve_json_data_from_web(s_url2)  # try backup airport
            if json_object is not False:
                break
            time.sleep(5)
            i_count += 1

    return json_object


def write_mission_file(s_filename_to_write, l_mission):  # write mission list into mission file
    f = open(s_filename_to_write, 'w', encoding="utf8")
    s1 = '\x0D'.join(l_mission)
    f.write(s1)
    f.close()
    change_newline_chars_in_file(s_filename_to_write)  # do not ask ..... problems with extra chars being added


# extract mission file from mission miz
extract_mission_file(G.s_mission_miz_path, G.s_mission_miz_filename, 'mission')

# read mission file into a list item
l_mission_data = read_mission_file(G.s_mission_miz_path + 'mission')

G.b_sand_storm = is_sandstorm_terrain(l_mission_data)

# get realtime date and change in mission file (if necessary)
if G.b_change_time:
    get_mission_date_time()
    save_date_and_time(l_mission_data)

print_all_data()  # debug just for seeing what things started at

if G.b_update_weather:
    if G.b_debug_load:
        debug_load()
    else:
        if G.s_api_key_checkwx == 'NOT_YET_SET':
            not_setup_correctly()
            # exit(1)

        get_weather1()
        if G.json_weather is False:
            get_weather2()

            if G.json_weather is False:
                print("WARNING - METAR data read failure")
                print("Using default weather values instead")

print(G.json_weather)
save_data_to_mission(l_mission_data)  # write G. global variables for weather into mission list

print_all_data()  # debug just for seeing what things actually are in the file

write_mission_file('mission', l_mission_data)  # now take mission list and write it back to file

print("weather.py", s_version_info, " exiting")
