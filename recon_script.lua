-- DCS RECON SCRIPT
-- Description:
-- Client aircraft with Group Names starting with 'Recon' are considered reconnaissance units.
-- Every 5 seconds the script checks for enemy units within a given radius around the aircraft.
-- If enemy units are spotted their location is written to Discord in a reconnaissance report.
-- Once an enemy unit has been spotted it won't be reported again.
--
-- This script is a preliminary work in progress.
-- Requires Mist, Moose, HypeMan (https://aggressors.ca/HypeManII, https://github.com/robscallsign/HypeMan)


local BlueClientSet = SET_CLIENT:New():FilterActive():FilterStart()

local searchRadius=2000
local reconGroupPrefix = 'Recon'

local function starts_with(str, start)
   return str:sub(1, #start) == start
end

spottedUnits = {}

function doClientRecon ( Client )	
	if starts_with(Client:GetClientGroupName(), reconGroupPrefix) then	
			
		local unitname = Client:GetClientGroupDCSUnit():getName()
					
		if unitname ~= nil then			
			
			retval = mist.getUnitsInMovingZones(mist.makeUnitTable({'[red]'}), {unitname}, searchRadius, 'cylinder' )
			
			if retval ~= nil and next(retval) ~= nil then
				outputString = ''
				for i = 1, #retval do									
					local curId = retval[i]
					if spottedUnits[curId.id_] == nil then		
					
						-- prevent spotted units from being called again in recon reports
						spottedUnits[curId.id_] = true
						
						local typeName = Unit.getTypeName(curId)						
						local _lat, _lon = coord.LOtoLL(Unit.getPosition(retval[i]).p)
						local _latLngStr = mist.tostringLL(_lat, _lon, 3, true)
						local _mgrsString = mist.tostringMGRS(coord.LLtoMGRS(coord.LOtoLL(Unit.getPosition(retval[i]).p)), 5)
												
						outputString = outputString .. 'Recon report by: ' .. Client:GetPlayerName() ..  ', a ' .. typeName .. ' was spotted at: ' .. _latLngStr .. ' (' .. _mgrsString .. ')\n'					
					end
				end 
				
			end				
			if outputString ~= '' then
				HypeMan.sendBotMessage('```'.. outputString .. '```')
			end
		end		
	end
end
	
	
function RunReconTimer(ourArgument, time)	
	BlueClientSet:ForEachClient(doClientRecon)	
   return time + 5
end

timer.scheduleFunction(RunReconTimer, 1, timer.getTime() + 5)
