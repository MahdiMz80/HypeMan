
JSON = (loadfile "JSON.lua")() -- one-time load of the routines
dofile('private_api_keys.lua')

print(PRIVATE_HYPEMAN_BOT_CLIENT_ID)
print(PRIVATE_HYPEMAN_CHANNEL_ID)

local BOT_CLIENT_ID = PRIVATE_HYPEMAN_BOT_CLIENT_ID
local CHANNEL_ID = PRIVATE_HYPEMAN_CHANNEL_ID

local CQ_BOT_ID = PRIVATE_CQ_CLIENT_ID
local CQ_BOT_CHANNEL_ID = PRIVATE_CQ_CHANNEL_ID

local privmsgid = PRIVATE_COMMAND_ID

local PORT =  10081
local HOST = '0.0.0.0'
local ServerName = 'Rob Rulez!!!'

local dgram = require('dgram')
local discordia = require('discordia')

local client = discordia.Client()
local ch = nil

local cqbot = discordia.Client()
local cqch = nil


function tableHasKey(table,key)
    return table[key] ~= nil
end

client:on('ready', function()
    print('Logged in as '.. client.user.username)
    ch = client:getChannel(CHANNEL_ID)
   -- ch:send('HypeMan is ready to hype.  Imma relay messages from Join Top Swing Dedicated Server (Too)')
end)

cqbot:on('ready', function()
    print('Logged in as '.. cqbot.user.username)
    cqch = cqbot:getChannel(CQ_BOT_CHANNEL_ID)
  --  cqch:send('Negative Ghostrider, the pattern is full.')
end)

--local function has_value (tab, val)
--    for index, value in ipairs(tab) do
--        if value == val then
--            return true
--        end
--    end
--
--    return false
--end

client:on('messageCreate', function(message)	
	
	if message.content == '!connect' and message.author.id == privmsgid and message.channel.guild == nil then	
		print('Message was !connect received')
		message.channel:send('connecting to voice comms.')
		ConnectVoice()
		return
	end
	
	if message.content == '!disconnect' and message.author.id == privmsgid and message.channel.guild == nil then
	    message.channel:send('disconnecting from voice comms.')
		DisconnectVoice()
		return
	end	
	
	if message.author.id == privmsgid and message.channel.guild == nil then
		print('Creating Message '..message.content)
		CreateVoiceMp3(message.content)
	end
		
	if id  == CHANNEL_ID then
		local content = message.content
		if content == '!info' or content == '!about' or content == '!hypeman' then			
			message.channel:send('HypeMan is an experimental Discord bot to announce Digital Combat Simulator (DCS) game events to Discord.  See https://aggressors.ca/hypeman for more information')		
		end
	end	
end)

client:run(BOT_CLIENT_ID)
cqbot:run(CQ_BOT_ID)

local s2 = dgram.createSocket('udp4')

p('PORT',PORT)
s2:bind(PORT,HOST)

-- local s1 = dgram.createSocket('udp4')
-- s1:bind(PORT,HOST)
-- s1:send('HELLO', PORT+1, '127.0.0.1')

local function starts_with(str, start)
   return str:sub(1, #start) == start
end

--    * *Name*: The player name.
--    * *Pass*: A running number counting the passes of the player
--    * *Points Final*: The final points (i.e. when the player has landed). This is the average over all previous bolters or waveoffs, if any.
--    * *Points Pass*: The points of each pass including bolters and waveoffs.
--    * *Grade*: LSO grade.
--    * *Details*: Detailed analysis of deviations within the groove.
--    * *Wire*: Trapped wire, if any.
--    * *Tgroove*: Time in the groove in seconds (not applicable during Case III).
--    * *Case*: The recovery case operations in progress during the pass.
--    * *Wind*: Wind on deck in knots during approach.
--    * *Modex*: Tail number of the player.
--    * *Airframe*: Aircraft type used in the recovery.
--    * *Carrier Type*: Type name of the carrier.
--    * *Carrier Name*: Name/alias of the carrier.
--    * *Theatre*: DCS map.
--    * *Mission Time*: Mission time at the end of the approach.
--    * *Mission Date*: Mission date in yyyy/mm/dd format.
--    * *OS Date*: Real life date from os.date(). Needs **os** to be desanitized.

local function getCaseString(mygrade)

	local caseNumber = mygrade.case
	
	if caseNumber == 1 then
		return '(CASE I)' 
	elseif caseNumber == 2 then
		return '(CASE II)' 
	elseif caseNumber == 3 then
		return '(CASE III)'
	else
		return ''
	end
end

local function getWireString(mygrade)
	local mywire = mygrade.wire
	
	if mywire == nil then
		return 'no wire'
	end
	
	if mywire == 1 then
		return '1-wire'
	elseif mywire == 2 then
		return '2-wire'
	elseif mywire == 3 then
		return '3-wire'
	elseif mywire == 4 then
		return '4-wire'
	else
		return 'no wire'
	end
end

--mygrade = {}
--mygrade.grade = '_OK_'
--mygrade.points = 3.0
--mygrade.finalscore = 2.5
--mygrade.details = 'LOL HIM XAR'
--mygrade.wire=3
--mygrade.Tgroove = 16.6
--mygrade.case = 1
--mygrade.wind= 25
--mygrade.modex = 300
--mygrade.airframe = 'F/A-18C hornet'
--mygrade.carriertype = 'CVN99'
--mygrade.carriername = 'HMCS Don Cherry'
--mygrade.theatre = 'Persian Gulf'
--mygrade.mitime = '01:02:03+1'
--mygrade.midate= '1999/03/24'
--mygrade.osdate = '2019/09/10 01:02:03'

-- this function was called wrap in quotes because it originally wrapped
-- any value in quotes.  But now it joins values with a , but the name is kept.
local function wiq(str)
	return str..', '
end

local function getCsvString(mygrade)
-- This function generates the CSV row that gets sent to google sheet.
-- Every value gets wiq'd (wrapped in quotes (a single quote) )
-- The google sheet upload is handled by a python script that uploads the CSV string
	local my_string = wiq(mygrade.name)
	my_string = my_string .. wiq( mygrade.grade)
	my_string = my_string .. wiq( mygrade.points)
	my_string = my_string .. wiq( mygrade.finalscore)
	my_string = my_string .. wiq( mygrade.details)
	my_string = my_string .. wiq( mygrade.wire)
	my_string = my_string .. wiq( mygrade.Tgroove)
	my_string = my_string .. wiq( mygrade.case)
	my_string = my_string .. wiq( mygrade.wind)
	my_string = my_string .. wiq( mygrade.modex)
	my_string = my_string .. wiq( mygrade.airframe)
	my_string = my_string .. wiq( mygrade.carriertype)
	my_string = my_string .. wiq( mygrade.carriername)
	my_string = my_string .. wiq( mygrade.theatre)
	my_string = my_string .. wiq( mygrade.mitime)
	my_string = my_string .. wiq(mygrade.midate)
	my_string = my_string .. ' Server: ' .. ServerName
	--my_string = my_string .. wiq( mygrade.osdate)
	return my_string
end

local function getGradeString(mygrade)
-- This is the function that formats the grade string that will get sent to Discord reporting the grade.
-- Example: Rob, OK, 3.0 PT, H_LUL_X _SLO_H_LUL_IM  SLOLOLULIC LOAR, 3-wire, groove time 17.0 seconds, (CASE I)
	print ('LSO Grade, '.. mygrade.name .. ' trapped, sending to Discord')
	local msg_string = mygrade.name .. ', ' .. mygrade.grade .. ', ' .. mygrade.points .. ' PT, ' .. mygrade.details .. ', ' .. getWireString(mygrade) .. ', groove time ' .. mygrade.Tgroove .. ' seconds' .. ', ' .. mygrade.airframe .. ', ' .. getCaseString(mygrade)
	return msg_string
end

local function f(msg)

	local lua_table = JSON:decode(msg)
	
	if lua_table['messageType']  ~= nil then
		local msg_id = lua_table['messageType']
		
		if msg_id == 1 then
			-- print the message
			if ch ~= nil then
				local msg_string = lua_table['messageString']
				
				if msg_string ~= nil then
					ch:send(msg_string)
				end
			end
	
		elseif msg_id == 2 then
			-- AIRBOSS GRADE IS messageType = 2			
						
			if cqch ~= nil then
				-- cqch:send('MessageType = 2')
				local msg_string = getGradeString(lua_table)
				print(msg_string)
				--cqch:send(msg)
				cqch:send(msg_string)
				local msg2 = getCsvString(lua_table)
				local execString = "\".\\gsheet_upload.bat " .. "\"" .. msg2 .. "\"\""
				print(execString)
				io.popen(execString,'w')
			end

		elseif msg_id == 3 then
			-- PILOT FLIGHT TIME MESSAGE?
			
		elseif msg_id == 4 then
			-- WEAPON RELEASE MESSAGE?
			
		elseif msg_id == 5 then
			-- HIT OR DAMAGE MESSAGE?
		end
	end
	
	
end

--local msg2 = "TG, (OK), 3.0 PT, F(LOLUR)X F(LOLUR)IM  (F)IC , 1-wire, groove time 22.0 seconds, (CASE I)"    
--local execString = "\".\\gsheet_upload.bat " .. "\"" .. msg2 .. "\"\""
--print(execString)
--pcall(io.popen(execString,'w'))
			
s2:on('message', function(msg, rinfo)
	-- local t = os.date()	
    p('Message received: ')
    p(msg)
    
    if ch ~= nil then
		botSendMessage = coroutine.wrap (f)
        botSendMessage(msg)
    end
	-- nilling the message here.  Somehow the message was getting appended to and growing?  not sure how or why that happened
	-- msg = nil
	-- Seemed to only be due to time acceleration in DCS?  I don't know.
end)