-- Instructions: include HypeMan in a mission either with a DO SCRIPT FILE, or a
-- DO SCRIPT containing the following:
-- assert(loadfile("C:/HypeMan/HypeMan.lua"))()
--
-- The DO SCRIPT assert(loadfile())() is preferred because then HypeMan can be updated and modified
-- and applied to all .miz files without having to modify each individually.

-- HypeMan requires JSON.lua from here http://regex.info/blog/lua/json in C:\HypeMan
JSON = (loadfile "C:/HypeMan/JSON.lua")() -- one-time load of the routines

HypeMan = {}
-- Configuration Options
local HypeManDebugMessages = false
local HypeManFlightLogging = true
local HypeManFlightLogTimer = 30
local HypeManAnnounceTakeoffs = true
local HypeManAnnounceLandings = true
local HypeManAnnounceMissionStart = true
local HypeManAnnounceMissionEnd = true
local HypeManAnnounceAIPlanes = false
local HypeManAnnouncePilotDead = true
local HypeManAnnouncePilotEject = true
local HypeManAnnouncePilotCrash = false
local HypeManAnnounceHits = false
local HypeManAnnounceRefueling = false
local HypeManMinimumFlightTime = 0.0  -- minimum flight time to report in minutes

package.path  = package.path .. ';.\\LuaSocket\\?.lua;'
package.cpath = package.cpath .. ';.\\LuaSocket\\?.dll;'
local socket = require("socket")

HypeMan.UDPSendSocket = socket.udp()
HypeMan.UDPSendSocket:settimeout(0)

-- Table to store takeoff times
HypeManTakeOffTime = {}

-- Table to store the Flight Log information
HypeManFlightLog = {}

HypeManRefuelingTable = {}

-- table to store hits on aircraft
HypeManHitTable = {}

-- This is the function that can be called in any mission to send a message to discord.
-- From the Mission Editor add a Trigger and a DO SCRIPT action and enter as the script:
-- HypeMan.sendBotMessage('Roses are Red.  Violets are blue.  I only wrote this poem to test my Discord Bot.')

HypeMan.sendBotTable = function(tbl)
	-- env.info(msg)  -- for debugging
	local tbl_json_txt = JSON:encode(tbl)
	socket.try(HypeMan.UDPSendSocket:sendto(tbl_json_txt, '127.0.0.1', 10081))
	-- msg = nil  -- setting to nil in attempt to debug why message queue seems to grow
end

HypeMan.sendDebugMessage = function(msg)
	if HypeManDebugMessages then
		messageTable = {}
		messageTable.messageType = 1
		messageTable.messageString = "DEBUG_MESSAGE: " .. msg
		HypeMan.sendBotTable(messageTable)
		-- msg = nil
	end
end

HypeMan.sendBotMessage  = function(msg)
	messageTable = {}
	messageTable.messageType = 1
	messageTable.messageString = msg
	HypeMan.sendBotTable(messageTable)
	-- msg = nil  -- setting to nil in attempt to debug why message queue seems to grow
end

-- Mission Start announcement done by a function right in the script as the S_EVENT_MISSION_START event is
-- nearly impossible to catch in a script as it gets sent the moment the mission is unpaused
if HypeManAnnounceMissionStart then
	local theDate = mist.getDateString(true, true)
	local theTime = mist.getClockString()
	local theatre = env.mission.theatre
	HypeMan.sendBotMessage('$SERVERNAME - New mission launched in the ' .. theatre .. '.  HypeMan standing by to stand by. Flight Logging Enabled, hold on to yo tits.  Local mission time is ' .. theTime .. ', ' .. theDate)
end

local function addFlightTime(flID)
	HypeMan.sendDebugMessage(' addFlightTime() called for ID: ' .. flID)
	
	if HypeManFlightLog[flID] == nil then
		return
	end
	
	if HypeManFlightLog[flID].departureTimer ~= nil then
		HypeManFlightLog[flID].trackedTime = HypeManFlightLog[flID].trackedTime +  timer.getAbsTime() - HypeManFlightLog[flID].departureTimer
		HypeManFlightLog[flID].departureTimer = nil -- set to nil to let other event handlers know that the time has been tracked
	end
end


local function sendFlightLog(flID)
	
	if HypeManFlightLog[flID].submitted ~= true then
		HypeMan.sendDebugMessage(' sendFlightLog via UDP for ID: '..flID)	
		HypeMan.sendBotTable(HypeManFlightLog[flID])
		HypeManFlightLog[flID].submitted = true
		HypeManFlightLog[flID].departureTimer = nil
	else
		HypeMan.sendDebugMessage(' sendFlightLog() called log for ID '.. ' but it was already submitted.  Disregard.')	
	end
end

local function flightLogNewEntry()
-- this function fills in an empty flight log entry with no details about the flight
	elem = {}
	elem.messageType = 3 -- messageType = 3 for flight logging

	elem.submitted = false
	elem.pending = false
	elem.trackedTime = 0  -- this is where we track the total amount of time in this flight
	elem.numTakeoffs = 0
	elem.numLandings = 0

	elem.coalition = 0
	elem.missionType = 0

	elem.departureField = ''
	elem.arrivalField1 = ''
	elem.arrivalField2 = ''

	-- elem.wasHit = 0
	elem.humanFailure = 0
	elem.refueled = 0
	elem.ejected = 0
	elem.dead = 0
	-- elem.fired = 0
	elem.crash = 0
	elem.missionEnd = 0
	elem.airStart = 0
	elem.theatre = env.mission.theatre

	return elem
end

local function FlightLogCreateNewEntry(flID, flType, flAirStart, flCallsign, flCoalition)
	-- this is a new entry to the flight log
	
	logEntry = flightLogNewEntry()

	local airStartNum = 0
	if flAirStart then
		airStartNum = 1
	end
	
	logEntry.acType = flType
	logEntry.airStart = airStartNum
	logEntry.callsign = flCallsign	
	logEntry.coalition = flCoalition
	
	if flAirStart then
		logEntry.departureField = 'Air'
	end
	
	HypeManFlightLog[flID] = logEntry
end

local function FlightLogDeparture(flID, flAirfield)
	HypeMan.sendDebugMessage(' Flight Log Departure called.  ID: ' .. flID .. ' airfield: ' .. flAirfield)
	if HypeManFlightLog[flID] == nil then
		HypeMan.sendDebugMessage(' object ID was nil.  wtf is going on.')
		return
	end
	
	HypeManFlightLog[flID].departureField = flAirfield
	HypeManFlightLog[flID].pending = false	
	HypeManFlightLog[flID].numTakeoffs = HypeManFlightLog[flID].numTakeoffs + 1
	HypeManFlightLog[flID].departureTimer = timer.getAbsTime()
end

-- This function is called when a plane arrives at an airfield
local function FlightLogArrival(flID, flAirfield)

	if HypeManFlightLog[flID] == nil then
		-- this is what happens when you have an AI air start plane land and you're tracking AI stats/messages
		return
	end

	-- the logic here is that the first airfield you touch down on goes into arrivalField1
	-- if you touch down on more airfields then the last airfield you touch down on is in arrivalField2
	if HypeManFlightLog[flID].arrivalField1 == '' then
		HypeManFlightLog[flID].arrivalField1 = flAirfield
	else
		HypeManFlightLog[flID].arrivalField2 = flAirfield
	end

	addFlightTime(flID)

	HypeManFlightLog[flID].numLandings = HypeManFlightLog[flID].numLandings + 1

	-- after the specified time submit the flight log
	HypeManFlightLog[flID].pending = true
	timer.scheduleFunction(sendFlightLog, flID, timer.getTime() + HypeManFlightLogTimer )
end

local function HypeManGetName(initiator)
	if initiator == nil then
		return false, nil;
	end

	-- need to be careful here because it seems like the player has a chance to die before we can query their name
	local statusflag, name = pcall(Unit.getPlayerName, initiator)

	if statusflag == false then
		return false, nil;
	end

	return true, name;
end

local function HypeManTakeOffHandler(event)

	if event.id == world.event.S_EVENT_TAKEOFF then

		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		-- local airfieldName = Airbase.getName(event.place)
		local statusflag2, airfieldName = pcall(Airbase.getName, event.place)

		if statusflag2 == false then
			airfieldName = 'Unknown'
		end

		if airfieldName == nil then
			airfieldName = 'Unknown'
		end

		local flID = Unit.getID(event.initiator)
		local acType = Unit.getTypeName(event.initiator)
		HypeManTakeOffTime[flID] = timer.getAbsTime()

		if HypeManFlightLogging then
			if HypeManFlightLog[flID] == nil then
				-- this check is here because AI units don't trigger an S_EVENT_BIRTH, but then will trigger a takeoff event.  It's handy to keep track of AI units
				-- note that above the HypeManAnnounceAIPlanes check ensures we don't get here if we're not tracking AI planes
				--FlightLogCreateNewEntry(flID, flType, flAirStart, flCallsign, flCoalition)
				HypeMan.sendDebugMessage('FlightLogCreateEntry called inside S_EVENT_TAKEOFF called for object ID: ' .. flID)				
				FlightLogCreateNewEntry(flID, acType, 0, name, event.initiator:getCoalition())
			end
			HypeMan.sendDebugMessage('FlightLogDeparture called for object ID: ' .. flID)
			FlightLogDeparture(flID, airfieldName)
		end

		if HypeManAnnounceTakeoffs == true then
			HypeMan.sendBotMessage(name .. " took off from " .. airfieldName .. " in a " .. acType .. " on $SERVERNAME")
		end
	end
end

local function HypeManLandingHandler(event)
    if event.id == world.event.S_EVENT_LAND then
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		local statusflag2, airfieldName = pcall(Airbase.getName, event.place)

		if statusflag2 == false then
			airfieldName = 'Unknown'
		end

		-- TODO - not sure this second check is necessary, or ever called.
		if airfieldName == nil then
			airfieldName = 'Unknown'
		end

		local flID = Unit.getID(event.initiator)

		if HypeManFlightLogging then
			if HypeManFlightLog[flID] == nil then
				-- this check is here because AI units don't trigger an b event but then will trigger a takeoff event.  It's handy to keep track of AI units
				-- note that above the HypeManAnnounceAIPlanes check ensures we don't get here if we're not tracking AI planes
				--FlightLogCreateNewEntry(flID, flType, flAirStart, flCallsign, flCoalition)
				-- This is confusing we can assume that it was probably an air start AI if this code gets called.... set airstart to 1
				FlightLogCreateNewEntry(flID, acType, 1, name, event.initiator:getCoalition())
			end
			
			FlightLogArrival(flID, airfieldName)
		end

		-- beyond this point we are just dealing with announcing a landing message to the discord bot
		local t = HypeManTakeOffTime[flID]
		
		if t == nil then
			-- AI airstart unit does not trigger a b event
			return
		end

		HypeManTakeOffTime[flID] = nil
		local tduration = timer.getAbsTime() - t
	
		if HypeManAnnounceLandings and tduration > HypeManMinimumFlightTime then
			HypeMan.sendBotMessage(name .. " landed their " ..  Unit.getTypeName(event.initiator) .. " at " .. airfieldName .. " on $SERVERNAME. Total flight time was " .. mist.getClockString(tduration))
		end
	end
end

local function HypeManMissionEndHandler(event)
	if event.id == world.event.S_EVENT_MISSION_END then
	
		if HypeManFlightLogging then
			-- If the mission has ended loop through everything in the flight log and submit flight logs
			-- for any elements that haven't landed
			for flID, v in pairs(HypeManFlightLog) do
				if v.submitted == false then
					addFlightTime(flID)
					HypeManFlightLog[flID].pending = true
					HypeManFlightLog[flID].missionEnd = 1
					sendFlightLog(flID)	
				end
			end
		end
		
		if HypeManAnnounceMissionEnd then
			local DHMS =  mist.time.getDHMS( mist.time.relativeToStart(mist.utils.round(timer.getAbsTime(), 0)) )
			local dayStr = ''
			if DHMS.d == 0 then
				dayStr = ''  -- leave days portion blank
			else
				dayStr = DHMS.d .. ' days '
			end
			
			local theTimeString  = dayStr .. DHMS.h .. ' hours and ' .. DHMS.m .. ' minutes.'
			HypeMan.sendBotMessage('$SERVERNAME shutting down, mission ran for ' .. theTimeString .. ' HypeMan going watch the TOPGUN2 preview again.');
		end
	end
end

local function HypeManBirthHandler(event)
	if event.id == world.event.S_EVENT_BIRTH then
		HypeMan.sendDebugMessage('S_EVENT_BIRTH called.  We are at the fucking top of the handler.') 
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		HypeMan.sendDebugMessage('S_EVENT_BIRTH called.  statusflag was not false.  i fucking hate you dcs.') 

		if name == nil then
			return
		end
		
		HypeMan.sendDebugMessage('S_EVENT_BIRTH called.  statusflag was not false.  and name was not nil. i fucking hate you dcs.') 

		-- changed to allow landing/flight time of airstart clients
		-- HypeManTakeOffTime[Unit.getID(event.initiator)]=nil
		local flID = Unit.getID(event.initiator)
		HypeManTakeOffTime[flID] = timer.getAbsTime()

		if HypeManFlightLogging then
			HypeMan.sendDebugMessage('S_EVENT_BIRTH for object ID: ' .. flID) 
			FlightLogCreateNewEntry(flID, Unit.getTypeName(event.initiator), event.initiator:inAir(), name, event.initiator:getCoalition())
		end
	end
end

local function HypeManPilotDeadHandler(event)
	if event.id == world.event.S_EVENT_PILOT_DEAD then

		-- local name = Unit.getPlayerName(event.initiator)
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		local flID = Unit.getID(event.initiator)

		-- I can't remember why I'm checking unitid and the initiator here before niling out the flight time
		if flID ~= nil and event.iniator ~= nil then
			HypeManTakeOffTime[flID] = nil
		end

		if HypeManAnnouncePilotDead then
			HypeMan.sendBotMessage('RIP ' .. name .. '.  HypeMan pours out a little liquor for his homie.')
		end

		if HypeManFlightLogging and HypeManFlightLog[flID] ~= nil then
			HypeManFlightLog[flID].dead = 1

			addFlightTime(flID)
			
			if HypeManFlightLog[flID].submitted == false and HypeManFlightLog[flID].pending == false then
				HypeManFlightLog[flID].pending = true
				timer.scheduleFunction(sendFlightLog, flID, timer.getTime() + HypeManFlightLogTimer )
			end
		end
	end
end

local function HypeManCrashHandler(event)
	if event.id == world.event.S_EVENT_CRASH then
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		local flID = Unit.getID(event.initiator)
		
		HypeManTakeOffTime[flID]=nil

		if HypeManAnnouncePilotCrash then
			HypeMan.sendBotMessage(name .. ' has CRASHED from their' ..  Unit.getTypeName(event.initiator) .. ' on $SERVERNAME.  Send in the rescue helos!')
		end

		if HypeManFlightLogging and HypeManFlightLog[flID] ~= nil then
			HypeManFlightLog[flID].crash = 1

			addFlightTime(flID)
			
			if HypeManFlightLog[flID].submitted == false and HypeManFlightLog[flID].pending == false then
				HypeManFlightLog[flID].pending = true
				timer.scheduleFunction(sendFlightLog, flID, timer.getTime() + HypeManFlightLogTimer )
			end
		end
	end
end

local function HypeManPilotEjectHandler(event)
	if event.id == world.event.S_EVENT_EJECTION then

		-- local name = Unit.getPlayerName(event.initiator)
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		local flID = Unit.getID(event.initiator)
		HypeManTakeOffTime[flID] = nil

		if HypeManAnnouncePilotEject then
			HypeMan.sendBotMessage(name .. ' has EJECTED from their' ..  Unit.getTypeName(event.initiator) .. ' on $SERVERNAME.  Send in the rescue helos!')
		end

		if HypeManFlightLogging and HypeManFlightLog[flID] ~= nil then
			HypeManFlightLog[flID].ejected = 1

			addFlightTime(flID)

			if HypeManFlightLog[flID].submitted == false and HypeManFlightLog[flID].pending == false then
				HypeManFlightLog[flID].pending = true
				timer.scheduleFunction(sendFlightLog, flID, timer.getTime() + HypeManFlightLogTimer )
			end
		end
	end
end

local function HypeManHumanFailureHandler(event)
	if event.id == world.event.S_EVENT_HUMAN_FAILURE then
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		-- this check might not be necessary, AI aircraft wont register system failures
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		local flID = Unit.getID(event.initiator)

		if HypeManFlightLogging and HypeManFlightLog[flID] ~= nil then
			HypeManFlightLog[flID].humanFailure = HypeManFlightLog[flID].humanFailure + 1
		end
	end
end

local function HypeManRefuelingHandler(event)
	if event.id == world.event.S_EVENT_REFUELING then
		local statusflag, name = HypeManGetName(event.initiator)

		if statusflag == false then
			return
		end

		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end

		if name == nil then
			return
		end

		local flID = Unit.getID(event.initiator)
		
		if HypeManFlightLogging and HypeManFlightLog[flID] ~= nil then
			HypeManFlightLog[flID].refueled = HypeManFlightLog[flID].refueled + 1
		end
	end
end

if HypeManAnnounceRefueling or HypeManFlightLogging then
	mist.addEventHandler(HypeManRefuelingHandler)
end

if HypeManFlightLogging or HypeManAnnounceLandings or HypeManAnnounceTakeoffs then
	mist.addEventHandler(HypeManBirthHandler)
end

if HypeManAnnouncePilotCrash or HypeManFlightLogging then
	mist.addEventHandler(HypeManCrashHandler)
end

if HypeManAnnounceTakeoffs or HypeManFlightLogging then
	mist.addEventHandler(HypeManTakeOffHandler)
end

if HypeManAnnounceLandings or HypeManFlightLogging then
	mist.addEventHandler(HypeManLandingHandler)
end

if HypeManAnnouncePilotEject or HypeManFlightLogging then
	mist.addEventHandler(HypeManPilotEjectHandler)
end

if HypeManAnnouncePilotDead or HypeManFlightLogging then
	mist.addEventHandler(HypeManPilotDeadHandler)
end

if HypeManAnnounceMissionEnd or HypeManFlightLogging then
	mist.addEventHandler(HypeManMissionEndHandler)
end

