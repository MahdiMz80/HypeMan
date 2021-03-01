-------------------------
-- AIRBOSS --
-------------------------

-- Set mission menu.
AIRBOSS.MenuF10Root=MENU_MISSION:New("Airboss").MenuPath

-- No MOOSE settings menu.
_SETTINGS:SetPlayerMenuOff()
  
local hightanker=RECOVERYTANKER:New(UNIT:FindByName("CVN71"), "Arco")
hightanker:SetTakeoffAir()
hightanker:SetRadio(268)
hightanker:SetAltitude(15000)
hightanker:SetRacetrackDistances(25, 8)
hightanker:SetModex(611)
hightanker:SetTACAN(55, "ARC")
hightanker:SetSpeed(350)
hightanker:Start()

local rescuehelo=RESCUEHELO:New(UNIT:FindByName("CVN71"), "Rescue Helo")   
rescuehelo:SetHomeBase(AIRBASE:FindByName("USS Ticonderoga"))
rescuehelo:SetTakeoffAir()
rescuehelo:SetRescueDuration(1)
rescuehelo:SetRescueHoverSpeed(5)
rescuehelo:SetRescueZone(90)
rescuehelo:SetModex(42)
rescuehelo:Start()

local tanker=RECOVERYTANKER:New(UNIT:FindByName("CVN71"), "Texaco")
tanker:SetTakeoffHot()
tanker:SetRadio(262)
tanker:SetModex(511)
tanker:SetTACAN(60, "TKR")
tanker:Start()

--local awacs=RECOVERYTANKER:New("CVN71", "Wizard")
--awacs:SetAWACS()
--awacs:SetRadio(260)
--awacs:SetAltitude(25000)
--awacs:SetCallsign(CALLSIGN.AWACS.Wizard)
--awacs:SetRacetrackDistances(30, 15)
--awacs:SetModex(611)
--awacs:SetTACAN(2, "WIZ")
--awacs:__Start(1)

local AirbossCVN_71=AIRBOSS:New("CVN71")

-- Delete auto recovery window.
function AirbossCVN_71:OnAfterStart(From,Event,To)
  self:DeleteAllRecoveryWindows()
end

local function cutPass()
  trigger.action.outSound("Airboss Soundfiles/GetYourButtsUptoVipersOffice.ogg")
end

local function underlinePass()
  
  cvn = GROUP:FindByName( "CVN71" )
  cvnZONE = ZONE_GROUP:New( "ZoneCVN", cvn, 100 )
  cvnZONE:FlareZone( FLARECOLOR.Red, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.White, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Green, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Yellow, 10, 60 )
  trigger.action.outSound("Airboss Soundfiles/ffyrtp.ogg")

end

local function underlinePassSH()
  
  cvn = GROUP:FindByName( "CVN71" )
  cvnZONE = ZONE_GROUP:New( "ZoneCVN", cvn, 100 )
  cvnZONE:FlareZone( FLARECOLOR.Red, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.White, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Green, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Yellow, 10, 60 )
  trigger.action.outSound("Airboss Soundfiles/sureshot.ogg")
 
end

local function resetTrapSheetFileFormat()
  AirbossCVN_71:SetTrapSheet()
end

--credit for the Sierra Hotel Break goes to Sickdog from the Angry Arizona Pilots - thank you!
function AirbossCVN_71:OnAfterLSOGrade(From, Event, To, playerData, myGrade)
  
  local string_grade = myGrade.grade
  local player_callsign = playerData.callsign
  local unit_name = playerData.unitname
  local player_name = playerData.name
  local player_wire = playerData.wire

  player_name = player_name:gsub('[%p]', '')

  --local gradeForFile
  if  string_grade == "_OK_" then
  --if  string_grade == "_OK_" and player_wire == "3" and player_Tgroove >=15 and player_Tgroove <19 then
    timer.scheduleFunction(underlinePass, {}, timer.getTime() + 5) 
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "_OK_<SH>"
      myGrade.points = myGrade.points
      client_performing_sh:Set(0)
      AirbossCVN_71:SetTrapSheet(nil, "SH_unicorn_AIRBOSS-trapsheet-"..player_name)
      timer.scheduleFunction(underlinePassSH, {}, timer.getTime() + 5) 
    else
      AirbossCVN_71:SetTrapSheet(nil, "unicorn_AIRBOSS-trapsheet-"..player_name)
    end
	
  elseif string_grade == "OK" and player_wire >1 then 
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "OK<SH>"
      myGrade.points = myGrade.points + 0.5
      client_performing_sh:Set(0)
      AirbossCVN_71:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_71:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
	
  elseif string_grade == "(OK)" and player_wire >1 then 
    AirbossCVN_71:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "(OK)<SH>"
      myGrade.points = myGrade.points + 1.00
      client_performing_sh:Set(0)
      AirbossCVN_71:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_71:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
	
  elseif string_grade == "--" and player_wire >1 then
     if client_performing_sh:Get() == 1 then
      myGrade.grade = "--<SH>"
      myGrade.points = myGrade.points + 1.00
      client_performing_sh:Set(0)
      AirbossCVN_71:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_71:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end

  end
  myGrade.messageType = 2
  myGrade.callsign = playerData.callsign
  myGrade.name = playerData.name
	if playerData.wire == 1 then
	myGrade.points = myGrade.points -1.00
	local onewire_to_discord = ('**'..player_name..' almost had a rampstrike with that 1-wire!**')
	HypeMan.sendBotMessage(onewire_to_discord)
	end
  self:_SaveTrapSheet(playerData, mygrade)
  HypeMan.sendBotTable(myGrade)

  timer.scheduleFunction(resetTrapSheetFileFormat, {}, timer.getTime() + 10) 
  --local myScheduleTime = TIMER:New(10, nil,nil):resetTrapSheetFileFormat()	
end


AirbossCVN_71:SetMenuRecovery(60, 25, true, 0)
AirbossCVN_71:Load()
AirbossCVN_71:SetAutoSave()
--AirbossCVN_71:SetTrapSheet()
AirbossCVN_71:SetTACAN(71, "X", "RHR")
AirbossCVN_71:SetICLS(11,"RRI")
AirbossCVN_71:SetLSORadio(265,AM)
AirbossCVN_71:SetPatrolAdInfinitum()
AirbossCVN_71:SetAirbossNiceGuy()
AirbossCVN_71:SetDefaultPlayerSkill(AIRBOSS.Difficulty.NORMAL)
AirbossCVN_71:SetMaxSectionSize(4)  
AirbossCVN_71:SetRadioRelayLSO("LSO Huey")
AirbossCVN_71:SetRadioRelayMarshal("Marshal Huey")
AirbossCVN_71:SetSoundfilesFolder("Airboss Soundfiles/")
AirbossCVN_71:SetDespawnOnEngineShutdown()
AirbossCVN_71:SetMenuSingleCarrier(False)
AirbossCVN_71:SetRecoveryTanker(tanker)
AirbossCVN_71.trapsheet = false							   
local CarrierExcludeSet=SET_GROUP:New():FilterPrefixes("Arco"):FilterStart()
AirbossCVN_71:SetExcludeAI(CarrierExcludeSet)

 --- Function called when recovery starts.
 local function play_recovery_sound()
  trigger.action.outSound("Airboss Soundfiles/BossRecoverAircraft.ogg")
end
  function AirbossCVN_71:OnAfterRecoveryStart(Event, From, To, Case, Offset)
    env.info(string.format("Starting Recovery Case %d ops.", Case))
    timer.scheduleFunction(play_recovery_sound, {}, timer.getTime() + 10) 
    
  end

  
     -- Start airboss class.
AirbossCVN_71:Start()  

local cvnGroup = GROUP:FindByName( "CVN71" )
local CVN_GROUPZone = ZONE_GROUP:New('cvnGroupZone', cvnGroup, 1111)

local BlueCVNClients = SET_CLIENT:New():FilterCoalitions("blue"):FilterStart()

Scheduler, SchedulerID = SCHEDULER:New( nil, 
  function ()
    
    local clientData={}
    local player_name

    BlueCVNClients:ForEachClientInZone( CVN_GROUPZone, 
    function( MooseClient )
        
      local function resetFlag()   
        --trigger.action.setUserFlag(555, 0)
        --trigger.action.outText('RESET SH Pass FLAG)', 5 ) 
        client_in_zone_flag:Set(0) 
      end
     
      local player_velocity = MooseClient:GetVelocityKNOTS()
      local player_name = MooseClient:GetPlayerName() 
      local player_alt = MooseClient:GetAltitude()
      local player_type = MooseClient:GetTypeName()
	  
	  player_alt_feet = player_alt * 3.28
	  player_alt_feet = player_alt_feet/10
	  player_alt_feet = math.floor(player_alt_feet)*10
	  
	  player_velocity_round = player_velocity/10
	  player_velocity_round = math.floor(player_velocity_round)*10
	  
        --client_fuel1 = MooseClient:GetFuel() -- Get the current amount of fuel every 5 seconds
        --trigger.action.outText(player_name..' has '..client_fuel1.. ' % of fuel onboard', 10)
        --local test = 'Test parameter'
        --[[
        clientData.clientName = MooseClient:GetPlayerName()
        clientData.clientFuel1 = MooseClient:GetFuel()
        clientData.clientFuel2 = nil
        clientData.in_air_bool = MooseClient:InAir()
        clientData.alt = MooseClient:GetAltitude()
        clientData.unitType = MooseClient:GetTypeName()
        clientData.start_time = nil
        clientData.stop_time = nil
        clientData.clientID = MooseClient:GetClientGroupID()
        clientData.fuelDif = nil
        ]]
        local Play_SH_Sound = USERSOUND:New( "Airboss Soundfiles/GreatBallsOfFire.ogg" )
        --trigger.action.outText(player_name..' altitude is '..player_alt, 5)
        --trigger.action.outText(player_name..' speed is '..player_velocity, 5)
        if client_in_zone_flag == nil then
          client_in_zone_flag = USERFLAG:New(MooseClient:GetClientGroupID() + 10000000)
        else
        end

        if client_performing_sh == nil then
          client_performing_sh = USERFLAG:New(MooseClient:GetClientGroupID() + 100000000)
        else
        end

        if client_in_zone_flag:Get() == 0 and player_velocity > 475 and player_alt < 213 then
				-- Requirements for Shit Hot break are velocity >475 knots and less than 213 meters (700')
          trigger.action.outText(player_name..' performing a Sierra Hotel Break!', 10)
          local sh_message_to_discord = ('**'..player_name..' is performing a Sierra Hotel Break at '..player_velocity_round..' knots and '..player_alt_feet..' feet!**')
	      HypeMan.sendBotMessage(sh_message_to_discord)
          Play_SH_Sound:ToAll()
          client_in_zone_flag:Set(1) 
          client_performing_sh:Set(1)
          timer.scheduleFunction(resetFlag, {}, timer.getTime() + 10) 
          else
        end

        --trigger.action.outText('ForEachClientInZone: Client name is '..clientData.clientName , 5)
        --trigger.action.outText('ForEachClientInZone: Client fuel1 is '..clientData.clientFuel1 , 5)

        --timer.scheduleFunction(send_fuel_amount_5_sec_later,clientData, timer.getTime() + 5) -- run function to compare fuel 5 seconds later

        --send_fuel_amount_5_sec_later(clientData)
    end
  )

  end, {}, 2, 1 
)
-- Create AIRBOSS object.
local AirbossTarawa=AIRBOSS:New("Tarawa")

function AirbossTarawa:OnAfterLSOGrade(From, Event, To, playerData, myGrade)
  myGrade.messageType = 2
  myGrade.callsign = playerData.callsign
  myGrade.name = playerData.name
  HypeMan.sendBotTable(myGrade)
end
  
AirbossTarawa:SetTACAN(108, "X", "LHA")
AirbossTarawa:SetTrapSheet()							
AirbossTarawa:SetICLS(8)
AirbossTarawa:Load()
AirbossTarawa:SetTrapSheet()
AirbossTarawa:SetAutoSave()
AirbossTarawa:SetRadioUnitName("UH1H Radio Relay")
AirbossTarawa:SetMarshalRadio(243)
AirbossTarawa:SetLSORadio(265)
AirbossTarawa:SetSoundfilesFolder("Airboss Soundfiles/")
AirbossTarawa:SetDespawnOnEngineShutdown()
AirbossTarawa:SetMenuSingleCarrier()
AirbossTarawa:SetMenuRecovery(60, 20, true)

AirbossTarawa:Start()

  
local HornetSet = SET_STATIC:New()
:FilterPrefixes("zDS_")
:FilterStart()

local function HornetDestroy(HornetUnit)

HornetUnit:Destroy()

end

HornetSet:ForEachStatic(
function(HornetUnit)

timer.scheduleFunction(HornetDestroy, HornetUnit, timer.getTime() + 300 )

end
)
