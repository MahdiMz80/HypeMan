

-- DOCUMENATION:
-- This is how you should load this:
-- assert(loadfile("C:/HypeMan/s2c/csar_elt.lua"))()


-- PRECONDITIONS:
-- This script requires a lot: 
-- Moost, Mist, HypeMan, JSON, DCS-SimpleTextToSpeech
-- You need to include these in your mission.  They are commented out now.
-- assert(loadfile("C:/HypeMan/mist.lua"))()
-- assert(loadfile("C:/HypeMan/Moose.lua"))()-- 
-- JSON = (loadfile "C:/HypeMan/JSON.lua")() -- one-time load of the routines
-- assert(loadfile("C:/HypeMan/HypeMan.lua"))()
-- assert(loadfile("C:/HypeMan/DCS-SimpleTextToSpeech.lua"))()

-- SET THIS TO TRUE IF YOU WAN TO ANNOUNCE AI AIRCRAFT!
local CSAR_ELT_AI_AIRCRAFT = false

local function CSARGetPlayerName(initiator)
	if initiator == nil then
		return false, nil;
	end
	
	local statusflag, name = pcall(Unit.getPlayerName, initiator)
	
	if statusflag == false then
		return false, nil;
	end
	
	return true, name;
end


local function CSARPilotEjectHandler(event)
	if event.id == world.event.S_EVENT_EJECTION then
		-- env.info('HYPEMAN - DCS EJECT EVENT')
						
		-- local name = Unit.getPlayerName(event.initiator)
		local statusflag, name = CSARGetPlayerName(event.initiator)
		
		if statusflag == false then
			return
		end
		
		-- for debugging get the AI plane names
		if CSAR_ELT_AI_AIRCRAFT and name == nil then
			name = Unit.getName(event.initiator)
		end
		
		if name == nil then			
			return
		end
		
		-- Check for blue coalition.
		-- According to https://wiki.hoggitworld.com/view/DCS_func_getCoalition
		-- the blue coalition is "2"
		if Unit.getCoalition(event.initiator) == 2 then			
			STTS.PlayMP3("C:\\HypeMan\\s2c\\ELT_2m.mp3","243.000","AM","0.5","Multiple",0)		
			-- trigger.action.outText("ding", 2)
			-- trigger.action.outSound('ding.wav')		
		end
	end
end

mist.addEventHandler(CSARPilotEjectHandler)
