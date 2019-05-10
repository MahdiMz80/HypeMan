HypeMan = {}
-- Configuration Options
local HypeManAnnounceTakeoffs = true
local HypeManAnnounceMissionStart = true
local HypeManAnnounceMissionEnd = true
local HypeManAnnounceAIPlanes = false
local HypeManAnnouncePilotDead = true
local HypeManAnnouncePilotEject = true

package.path  = package.path..";.\\LuaSocket\\?.lua;"
package.cpath = package.cpath..";.\\LuaSocket\\?.dll;"
local socket = require("socket")

HypeMan.UDPSendSocket = socket.udp()
HypeMan.UDPSendSocket:settimeout(0)

-- Table to store takeoff times
TakeOffTime = {}

-- This is the function that can be called in any mission to send a message to discord.
-- From the Mission Editor add a Trigger and a DO SCRIPT action and enter as the script:
-- HypeMan.sendBotMessage('Roses are Red.  Violets are blue.  I only wrote this poem to test my Discord Bot.')
HypeMan.sendBotMessage  = function(msg)
	-- env.info(msg)  -- for debugging
	socket.try(HypeMan.UDPSendSocket:sendto(msg, '127.0.0.1', 10081))
	msg = nil  -- setting to nil in attempt to debug why message queue seems to grow
end

-- Mission Start announcement done by a function right in the script as the S_EVENT_MISSION_START event is
-- nearly impossible to catch in a script as it gets sent the moment the mission is unpaused
 if HypeManAnnounceMissionStart then		
 local theDate = mist.getDateString(true, true)	
	local theTime = mist.getClockString()
	
	local theatre = env.mission.theatre
	
	HypeMan.sendBotMessage('New server mission launched in the ' .. theatre .. '.  HypeMan standing by to stand by.  Local mission time is ' .. theTime .. ', ' .. theDate)
end

local function HypeManTakeOffHandler(event) 

	-- TODO move this check below the timing code
	if HypeManAnnounceTakeoffs ~= true then
		return true
	end
	
    if event.id == world.event.S_EVENT_TAKEOFF then 
	
		mist.utils.tableShow(event)
		
		local name = Unit.getPlayerName(event.initiator)
		
		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end
		
		if name == nil then
			return
		end
		
		--   env.info(_event.initiator:getPlayerName().."HIT! ".._event.target:getName().." with ".._event.weapon:getTypeName())
		
		local airfieldName = Airbase.getName(event.place)
		
		if airfieldName == nil then
			airfieldName = 'Unknown Airstrip'
		end
	
		HypeMan.sendBotMessage(name .. " took off from " .. airfieldName .. " in a " .. Unit.getTypeName(event.initiator) )
		
		TakeOffTime[Unit.getID(event.initiator)]=timer.getAbsTime()
    end 
end 

local function HypeManLandingHandler(event) 
    if event.id == world.event.S_EVENT_LAND then 
	
		mist.utils.tableShow(event)
		local name = Unit.getPlayerName(event.initiator)
		
		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then		
			name = Unit.getName(event.initiator)
		end
		
		if name == nil then
			return
		end
				
		--   env.info(_event.initiator:getPlayerName().."HIT! ".._event.target:getName().." with ".._event.weapon:getTypeName())
		
		local airfieldName = Airbase.getName(event.place)
		
		if airfieldName == nil then
			airfieldName = 'Unknown Airfield'
		end
		
		local t = TakeOffTime[Unit.getID(event.initiator)]
		
		TakeOffTime[Unit.getID(event.initiator)] = nil
		
		if t == nil then
			-- HypeMan.sendBotMessage("local t = TakeOffTime[Unit.getID(event.initiator)]  was nil... wtf")
			HypeMan.sendBotMessage(name .. " landed their " ..  Unit.getTypeName(event.initiator) .. " at " .. airfieldName .. ".  Looks like they air-started, no flight time available.")
			return
		end
			
		local cur = timer.getAbsTime()
		
		local tduration = cur - t
		local theTime = mist.getClockString(tduration)	
		
		HypeMan.sendBotMessage(name .. " landed their " ..  Unit.getTypeName(event.initiator) .. " at " .. airfieldName .. ".  Total flight time was " .. theTime)
    end 
end 

local function HypeManMissionEndHandler(event)
	if event.id == world.event.S_EVENT_MISSION_END then
		local theDate = mist.getDateString(true, true)	
		local theTime = mist.getClockString()
		-- HypeMan.sendBotMessage('Server shutting down, Hypeman going watch some porn and hit the hay.  Local time is ' .. theTime .. ', ' .. theDate)
		
		local timeInSec = mist.utils.round(timer.getAbsTime(), 0)
				
		-- local theTimeString = mist.getClockString(timeInSec)		
		local DHMS =  mist.time.getDHMS(mist.time.relativeToStart(timeInSec))
		local dayStr 
		if DHMS.d == 0 then
			dayStr = ''  -- leave days portion blank
		else
			dayStr = DHMS.d .. ' days '			
		end
		
		local theTimeString  = dayStr .. DHMS.h .. ' hours and ' .. DHMS.m .. ' minutes.'		
		
		HypeMan.sendBotMessage('Server shutting down, mission ran for ' .. theTimeString .. '  Hypeman going watch some military channel porn and hit the hay.');
		
	end
end

local function HypeManBirthHandler(event)
	if event.id == world.event.S_EVENT_BIRTH then
		local name = Unit.getPlayerName(event.initiator)
		
		if name == nil then
			name = Unit.getName(event.initiator)
		end
		
		TakeOffTime[Unit.getID(event.initiator)]=nil
		
	--	HypeMan.sendBotMessage('S_EVENT_BIRTH UNIT.name = ' .. name)
	end
end

local function HypeManPilotDeadHandler(event)
	if event.id == world.event.S_EVENT_PILOT_DEAD then
	
		local name = Unit.getPlayerName(event.initiator)
		
		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end
		
		if name == nil then
			return
		end
		
		-- if name == nil then
--			name = Unit.getName(event.initiator)
		-- end
		
		TakeOffTime[Unit.getID(event.initiator)]=nil
		
		HypeMan.sendBotMessage('RIP ' .. name .. '.  HypeMan pours out a little liquor for his homie.')		
	end
end 
	
	
local function HypeManPilotEjectHandler(event)
	if event.id == world.event.S_EVENT_EJECTION then
	
		local name = Unit.getPlayerName(event.initiator)
		
		-- for debugging get the AI plane names
		if HypeManAnnounceAIPlanes and name == nil then
			name = Unit.getName(event.initiator)
		end
		
		if name == nil then
			return
		end
		
		TakeOffTime[Unit.getID(event.initiator)]=nil		
		
		HypeMan.sendBotMessage(name .. ' has EJECTED from their' ..  Unit.getTypeName(event.initiator) .. '.  Send in the rescue helos!')		
	end
end 

mist.addEventHandler(HypeManTakeOffHandler)
mist.addEventHandler(HypeManLandingHandler)

-- needed to start the time
mist.addEventHandler(HypeManBirthHandler)

if HypeManAnnouncePilotEject then
	mist.addEventHandler(HypeManPilotEjectHandler)
end
	
if HypeManAnnouncePilotDead then
	mist.addEventHandler(HypeManPilotDeadHandler)
end

if HypeManAnnounceMissionEnd then
	mist.addEventHandler(HypeManMissionEndHandler)
end

