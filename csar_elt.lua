

-- CSAR_ELT.LUA
-- Calls Ciribob's DCS-SimpleTextToSpeech (DCS.STTS)
-- and plays "ELT_2m.mp3" on Guard (243.000Mhz)
-- when
-- assert(loadfile("C:/HypeMan/s2c/csar_elt.lua"))()

-- Requires  Mist, and DCS.STTS, ie:
-- assert(loadfile("C:/HypeMan/mist.lua"))()
-- assert(loadfile("C:/HypeMan/DCS-SimpleTextToSpeech.lua"))()

-- OPTIONS:
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
			STTS.PlayMP3("ELT_2m.mp3","243.000","AM","0.5","Multiple",0)		
		end
	end
end

mist.addEventHandler(CSARPilotEjectHandler)
