--2/19/2021 Yoda
-- add SHB to miz

-- Set mission menu.
AIRBOSS.MenuF10Root=MENU_MISSION:New("Airboss").MenuPath

-- No MOOSE settings menu.
_SETTINGS:SetPlayerMenuOff()

local tanker=RECOVERYTANKER:New(UNIT:FindByName("CVN73"), "Texaco")
:SetTakeoffHot()
:SetRadio(260)
:SetAltitude(7500)
:SetModex(703)
:SetTACAN(60, "TKR")
:Start()
  
local hightanker=RECOVERYTANKER:New(UNIT:FindByName("CVN73"), "Arco")
:SetTakeoffAir()
:SetRadio(268)
:SetAltitude(15000)
:SetRacetrackDistances(25, 8)
:SetModex(611)
:SetTACAN(55, "ARC")
:Start()

local rescuehelo=RESCUEHELO:New(UNIT:FindByName("CVN73"), "Rescue Helo")   
:SetHomeBase(AIRBASE:FindByName("USS Ticonderoga"))
:SetTakeoffAir()
:SetRescueDuration(1)
:SetRescueHoverSpeed(5)
:SetRescueZone(90)
:SetModex(42)
:Start()

local awacs=RECOVERYTANKER:New("CVN73", "Wizard")
awacs:SetAWACS()
awacs:SetTakeoffAir()
awacs:SetRadio(285.65)
awacs:SetAltitude(25000)
awacs:SetCallsign(CALLSIGN.AWACS.Wizard)
awacs:SetRacetrackDistances(30, 15)
awacs:SetModex(611)
awacs:SetTACAN(52, "WIZ")
awacs:__Start(1)

local AirbossCVN_73=AIRBOSS:New("CVN73")
-- Delete auto recovery window.
function AirbossCVN_73:OnAfterStart(From,Event,To)
  self:DeleteAllRecoveryWindows()
end

local function cutPass()
  trigger.action.outSound("Airboss Soundfiles/GetYourButtsUptoVipersOffice.ogg")
end

local function underlinePass()
  
  cvn = GROUP:FindByName( "CVN73" )
  cvnZONE = ZONE_GROUP:New( "ZoneCVN", cvn, 100 )
  cvnZONE:FlareZone( FLARECOLOR.Red, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.White, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Green, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Yellow, 10, 60 )
  trigger.action.outSound("Airboss Soundfiles/ffyrtp.ogg")

end

local function underlinePassSH()
  
  cvn = GROUP:FindByName( "CVN73" )
  cvnZONE = ZONE_GROUP:New( "ZoneCVN", cvn, 100 )
  cvnZONE:FlareZone( FLARECOLOR.Red, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.White, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Green, 10, 60 )
  cvnZONE:FlareZone( FLARECOLOR.Yellow, 10, 60 )
  trigger.action.outSound("Airboss Soundfiles/sureshot.ogg")
 
end

local function resetTrapSheetFileFormat()
  AirbossCVN_73:SetTrapSheet()
end

--credit for the Sierra Hotel Break goes to Sickdog from the Angry Arizona Pilots - thank you!
function AirbossCVN_73:OnAfterLSOGrade(From, Event, To, playerData, myGrade)
  
  local string_grade = myGrade.grade
  local player_callsign = playerData.callsign
  local unit_name = playerData.unitname
  local player_name = playerData.name

  player_name = player_name:gsub('[%p]', '')

  --local gradeForFile
  if string_grade == "CUT" then 
    timer.scheduleFunction(cutPass, {}, timer.getTime() + 10) 
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "CUT<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end

  elseif string_grade == "_OK_" then
    timer.scheduleFunction(underlinePass, {}, timer.getTime() + 5) 
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "_OK_<SH>"
      myGrade.points = myGrade.points + 0.5
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_unicorn_AIRBOSS-trapsheet-"..player_name)
      timer.scheduleFunction(underlinePassSH, {}, timer.getTime() + 5) 
    else
      AirbossCVN_73:SetTrapSheet(nil, "unicorn_AIRBOSS-trapsheet-"..player_name)
    end
  elseif string_grade == "OK" then 
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "OK<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
  elseif string_grade == "(OK)" then 
    AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)

    if client_performing_sh:Get() == 1 then
      myGrade.grade = "(OK)<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-CARRIER-trapsheet-"..player_name)
    end
  elseif string_grade == "--" then 
 

    if client_performing_sh:Get() == 1 then
      myGrade.grade = "--<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
  elseif string_grade == "WO" then 

    if client_performing_sh:Get() == 1 then
      myGrade.grade = "WO<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
  elseif string_grade == "WOFD" then

    if client_performing_sh:Get() == 1 then
      myGrade.grade = "WOFD<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
  elseif string_grade == "OWO" then
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "OWO<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-CARRIER-trapsheet-"..player_name)
    end
  elseif string_grade == "WOP" then
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "WOP<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
  elseif string_grade == "-- (BOLTER)" then
    if client_performing_sh:Get() == 1 then
      myGrade.grade = " B (BOLTER)<SH>"
      myGrade.points = myGrade.points + 0.25
      client_performing_sh:Set(0)
      AirbossCVN_73:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      AirbossCVN_73:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
  end
  myGrade.messageType = 2
  myGrade.callsign = playerData.callsign
  myGrade.name = playerData.name

  self:_SaveTrapSheet(playerData, mygrade)
  HypeMan.sendBotTable(myGrade)

  timer.scheduleFunction(resetTrapSheetFileFormat, {}, timer.getTime() + 10) 
  --local myScheduleTime = TIMER:New(10, nil,nil):resetTrapSheetFileFormat()	
end

AirbossCVN_73:SetMenuRecovery(60, 25, true, 20)
AirbossCVN_73:Load()
AirbossCVN_73:SetAutoSave()
--AirbossCVN_73:SetTrapSheet()
AirbossCVN_73:SetTACAN(73, "X", "WFR")
AirbossCVN_73:SetICLS(13,"GWW")
AirbossCVN_73:SetLSORadio(265,AM)
AirbossCVN_73:SetMarshalRadio(264, AM)
AirbossCVN_73:SetPatrolAdInfinitum()
AirbossCVN_73:SetAirbossNiceGuy()
AirbossCVN_73:SetDefaultPlayerSkill(AIRBOSS.Difficulty.NORMAL)
AirbossCVN_73:SetMaxSectionSize(4)  
AirbossCVN_73:SetRadioRelayLSO("LSO Huey")
AirbossCVN_73:SetRadioRelayMarshal("Marshal Huey")
AirbossCVN_73:SetSoundfilesFolder("Airboss Soundfiles/")
AirbossCVN_73:SetDespawnOnEngineShutdown()
AirbossCVN_73:SetRecoveryTanker(tanker)
AirbossCVN_73:SetMenuSingleCarrier(False)
AirbossCVN_73.trapsheet = false
local CarrierExcludeSet=SET_GROUP:New():FilterPrefixes("Arco"):FilterStart()
AirbossCVN_73:SetExcludeAI(CarrierExcludeSet)

 --- Function called when recovery starts.
 local function play_recovery_sound()
  trigger.action.outSound("Airboss Soundfiles/BossRecoverAircraft.ogg")
end
  function AirbossCVN_73:OnAfterRecoveryStart(Event, From, To, Case, Offset)
    env.info(string.format("Starting Recovery Case %d ops.", Case))
    timer.scheduleFunction(play_recovery_sound, {}, timer.getTime() + 10) 
    
  end
  
     -- Start airboss class.
AirbossCVN_73:Start()  

local cvnGroup = GROUP:FindByName( "CVN73" )
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
          local sh_message_to_discord = ('**'..player_name..' is performing a Sierra Hotel Break!**')
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
  
AirbossTarawa:SetTACAN(108, "X", "LHA")
AirbossTarawa:SetTrapSheet()
AirbossTarawa:SetICLS(8)
AirbossTarawa:Load()
AirbossTarawa:SetAutoSave()
AirbossTarawa:SetRadioUnitName("UH1H Radio Relay")
AirbossTarawa:SetMarshalRadio(306)
AirbossTarawa:SetLSORadio(306)
AirbossTarawa:SetSoundfilesFolder("Airboss Soundfiles/")
AirbossTarawa:SetDespawnOnEngineShutdown()
AirbossTarawa:SetMenuSingleCarrier()
AirbossTarawa:SetMenuRecovery(60, 20, true)

AirbossTarawa:Start()

--AWACS/big wing Tankers

magicAWACS = SPAWN
:New("Magic")
:InitLimit(1,0)
:InitRepeatOnLanding()
:OnSpawnGroup(
  function (magic_51)
  magic_51:CommandSetCallsign(2,5)
  magic_51:CommandSetFrequency(291.875)
  end
  )
:SpawnScheduled(60,0)

--KC-135 Shell (North) TCN 59X - 25,000' 259.0MHz (Hornet Ch.11)
local shellNorth = SPAWN
:New("Shell North")
:InitLimit(1,0)
:InitRepeatOnLanding()
:OnSpawnGroup(
  function (shell_41)
  shell_41:CommandSetCallsign(3,4)
  shell_41:CommandSetFrequency(259)
  local sh41Beacon = shell_41:GetBeacon()
  sh41Beacon:AATACAN(59, "SDN", true)
  end
  )
  :SpawnScheduled(60,0)

--KC-135 Shell (South) TCN 63X - 25,000' 263.0MHz (Hornet Ch.15)
local shellSouth = SPAWN
:New("Shell South")
:InitLimit(1,0)
:InitRepeatOnLanding()
:OnSpawnGroup(
  function (shell_21)
  shell_21:CommandSetCallsign(3,2)
  shell_21:CommandSetFrequency(263)
  local sh21Beacon = shell_21:GetBeacon()
  sh21Beacon:AATACAN(63, "SDS", true)
  end
  )
:SpawnScheduled(60,0)

--KC-135 Texaco (North Boom) TCN 61X - 26,000' 261.0MHz
local texacoNorth = SPAWN
:New("Texaco North")
:InitLimit(1,0)
:InitRepeatOnLanding()
:OnSpawnGroup(
  function (texaco_31)
  texaco_31:CommandSetCallsign(1,3)
  texaco_31:CommandSetFrequency(261)
  local tx31Beacon = texaco_31:GetBeacon()
  tx31Beacon:AATACAN(61, "TBN", true)
  end
  )
  :SpawnScheduled(60,0)

--KC-135 Texaco (South Boom) TCN 67X - 26,000' 267.0MHz
local texacoSouth = SPAWN
:New("Texaco South")
:InitLimit(1,0)
:InitRepeatOnLanding()
:OnSpawnGroup(
  function (texaco_21)
  texaco_21:CommandSetCallsign(1,2)
  texaco_21:CommandSetFrequency(267)
  local tx21Beacon = texaco_21:GetBeacon()
  tx21Beacon:AATACAN(67, "TBS", true)
  end
  )
:SpawnScheduled(60,0)

--KC-135 Texaco (East Boom) TCN 57X -12,000' 257.0 MHz
local texacoEast = SPAWN:
New("Texaco East")
:InitLimit(1,0)
:InitRepeatOnLanding()
:OnSpawnGroup(
  function (texaco_51)
  texaco_51:CommandSetCallsign(1,5)
  texaco_51:CommandSetFrequency(257)
  local tx51Beacon = texaco_51:GetBeacon()
  tx51Beacon:AATACAN(57, "TBE", true)
  end
  )
:SpawnScheduled(60,0)

--JTAC

--Range
  RangeCau1=RANGE:New("Tuapse Range")
  RangeCau1:AddBombingTargetGroup(GROUP:FindByName("Russian Forces"), 50, false)
  RangeCau1:Start()
  
  RangeCau2=RANGE:New("X-Airstrip Range")
  RangeCau2:AddBombingTargetGroup(GROUP:FindByName("Russian Forces-1"), 50, false)
  RangeCau2:Start()
  
  local clawrtargets={"CLAWR Range", "CLAWR Range-1", "CLAWR Range-2", "CLAWR Range-3", "CLAWR Range-4", "CLAWR Range-5", "CLAWR Range-6", "CLAWR Range-7", "CLAWR Range-8", "CLAWR Range-9", "CLAWR Range-10", "CLAWR Range-11", "CLAWR Range-11", "CLAWR Range-12", "CLAWR Range-13", "CLAWR Range-14"}
  local strafepit={"CLAWR Strafe Pit"}
  RangeCAU3=RANGE:New("CLAWR Range")
  RangeCAU3:AddBombingTargets(clawrtargets)
  RangeCAU3:AddStrafePit(strafepit,3000,300,nil,true,20,fouldist)
  RangeCAU3:Start()
