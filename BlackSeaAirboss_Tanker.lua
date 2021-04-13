-------------------------
-- AIRBOSS --
-------------------------

-- Set mission menu.
AIRBOSS.MenuF10Root=MENU_MISSION:New("Airboss").MenuPath

-- No MOOSE settings menu.
_SETTINGS:SetPlayerMenuOff()

local tanker=RECOVERYTANKER:New(UNIT:FindByName("CVN73"), "Texaco")
tanker:SetTakeoffAir()
tanker:SetRadio(260)
tanker:SetAltitude(8500)
tanker:SetModex(703)
tanker:SetTACAN(60, "TKR")
tanker:__Start(2)

local hightanker=RECOVERYTANKER:New(UNIT:FindByName("CVN73"), "Arco")
hightanker:SetTakeoffAir()
hightanker:SetRadio(268)
hightanker:SetAltitude(15000)
hightanker:SetRacetrackDistances(25, 8)
hightanker:SetModex(611)
hightanker:SetTACAN(55, "ARC")
hightanker:Start()

local rescuehelo=RESCUEHELO:New(UNIT:FindByName("CVN73"), "Rescue Helo")
rescuehelo:SetHomeBase(AIRBASE:FindByName("USS Ticonderoga"))
rescuehelo:SetTakeoffAir()
rescuehelo:SetRescueDuration(1)
rescuehelo:SetRescueHoverSpeed(5)
rescuehelo:SetRescueZone(90)
rescuehelo:SetModex(42)
rescuehelo:Start()

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

local Washington=AIRBOSS:New("CVN73")
-- Delete auto recovery window.
function Washington:OnAfterStart(From,Event,To)
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
  Washington:SetTrapSheet()
end

--credit for the Sierra Hotel Break goes to Sickdog from the Angry Arizona Pilots - thank you!
function Washington:OnAfterLSOGrade(From, Event, To, playerData, myGrade)

  local string_grade = myGrade.grade
  local player_callsign = playerData.callsign
  local unit_name = playerData.unitname
  local player_name = playerData.name
  local player_wire = playerData.wire
  local player_case = myGrade.case
  local player_detail = myGrade.details

  player_name = player_name:gsub('[%p]', '')

  --local gradeForFile
  if  string_grade == "_OK_" and player_wire >1 then
    --if  string_grade == "_OK_" and player_wire == "3" and player_Tgroove >=15 and player_Tgroove <19 then
    timer.scheduleFunction(underlinePass, {}, timer.getTime() + 5)
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "_OK_<SH>"
      myGrade.points = myGrade.points
      client_performing_sh:Set(0)
      Washington:SetTrapSheet(nil, "SH_unicorn_AIRBOSS-trapsheet-"..player_name)
      timer.scheduleFunction(underlinePassSH, {}, timer.getTime() + 5)
    else
      Washington:SetTrapSheet(nil, "unicorn_AIRBOSS-trapsheet-"..player_name)
    end

  elseif string_grade == "OK" and player_wire >1 then
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "OK<SH>"
      myGrade.points = myGrade.points + 0.5
      client_performing_sh:Set(0)
      Washington:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      Washington:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end

  elseif string_grade == "(OK)" and player_wire >1 then
    Washington:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "(OK)<SH>"
      myGrade.points = myGrade.points + 1.00
      client_performing_sh:Set(0)
      Washington:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      Washington:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end

  elseif string_grade == "--" and player_wire >1 then
    if client_performing_sh:Get() == 1 then
      myGrade.grade = "--<SH>"
      myGrade.points = myGrade.points + 1.00
      client_performing_sh:Set(0)
      Washington:SetTrapSheet(nil, "SH_AIRBOSS-trapsheet-"..player_name)
    else
      Washington:SetTrapSheet(nil, "AIRBOSS-trapsheet-"..player_name)
    end
	
  elseif string_grade == "-- (BOLTER)" then
      Washington:SetTrapSheet(nil, "Bolter_AIRBOSS-trapsheet-"..player_name) 
  elseif string_grade == "WOFD" then
      Washington:SetTrapSheet(nil, "WOFD_AIRBOSS-trapsheet-"..player_name)
  elseif string_grade == "OWO" then
      Washington:SetTrapSheet(nil, "OWO_AIRBOSS-trapsheet-"..player_name)
  elseif string_grade == "CUT" then
     if player_wire ==1 then
      myGrade.points = myGrade.points + 1.00
      Washington:SetTrapSheet(nil, "Cut_AIRBOSS-trapsheet-"..player_name)
     else
	  Washington:SetTrapSheet(nil, "Cut_AIRBOSS-trapsheet-"..player_name)
     end
 end 
 
  if player_case == 3 and player_detail == "    " then
      Washington:SetTrapSheet(nil, "NIGHT5_AIRBOSS-trapsheet-"..player_name)
      myGrade.grade = "_OK_"
      myGrade.points = 5.0
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
end

Washington:SetMenuRecovery(60, 25, true, 0)
Washington:Load()
Washington:SetAutoSave()
Washington:SetTACAN(73, "X", "WFR")
Washington:SetICLS(13,"GWW")
Washington:SetLSORadio(265,AM)
Washington:SetLineupErrorThresholds(1.5,-1.5,-1.5,-2,-4,1.5,2,4)
Washington:SetMarshalRadio(264, AM)
Washington:SetPatrolAdInfinitum()
Washington:SetAirbossNiceGuy()
Washington:SetDefaultPlayerSkill(AIRBOSS.Difficulty.NORMAL)
Washington:SetMaxSectionSize(4)
Washington:SetMPWireCorrection(12)
Washington:SetRadioRelayLSO("LSO Huey")
Washington:SetRadioRelayMarshal("Marshal Huey")
Washington:SetSoundfilesFolder("Airboss Soundfiles/")
Washington:SetDespawnOnEngineShutdown()
Washington:SetRecoveryTanker(tanker)
Washington:SetMenuSingleCarrier(False)
Washington.trapsheet = false
local CarrierExcludeSet=SET_GROUP:New():FilterPrefixes("Arco"):FilterStart()
Washington:SetExcludeAI(CarrierExcludeSet)

--- Function called when recovery starts.
--
local function play_recovery_sound()
  trigger.action.outSound("Airboss Soundfiles/BossRecoverAircraft.ogg")
end
function Washington:OnAfterRecoveryStart(Event, From, To, Case, Offset)
  env.info(string.format("Starting Recovery Case %d ops.", Case))
  timer.scheduleFunction(play_recovery_sound, {}, timer.getTime() + 10)

end

-- Start airboss class.
Washington:Start()

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


        local function roundVelocity(player_velocity)
          return x>=0 and math.floor(x+0.5) or math.ceil(x-0.5)
        end

        local Play_SH_Sound = USERSOUND:New( "Airboss Soundfiles/GreatBallsOfFire.ogg" )
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
          local sh_message_to_discord = ('**'..player_name..' is performing a Sierra Hotel Break at '..player_velocity_round..' knots and '..player_alt_feet..' feet in a '..player_type..'!**')
          HypeMan.sendBotMessage(sh_message_to_discord)
          Play_SH_Sound:ToAll()
          client_in_zone_flag:Set(1)
          client_performing_sh:Set(1)
          timer.scheduleFunction(resetFlag, {}, timer.getTime() + 10)
        else
        end

      end
    )

  end, {}, 2, 1
)

-- Create AIRBOSS object.
local Tarawa=AIRBOSS:New("Tarawa")
function Tarawa:OnAfterLSOGrade(From, Event, To, playerData, myGrade)
  myGrade.messageType = 2
  myGrade.callsign = playerData.callsign
  myGrade.name = playerData.name
  HypeMan.sendBotTable(myGrade)
end

Tarawa:SetTACAN(108, "X", "LHA")
Tarawa:SetTrapSheet()
Tarawa:SetICLS(8)
Tarawa:Load()
Tarawa:SetLineupErrorThresholds(.5,-.5,-1,-2,-4,1,2,4)
Tarawa:SetStatusUpdateTime(1)
Tarawa:SetAutoSave()
Tarawa:SetRadioUnitName("UH1H Radio Relay")
Tarawa:SetMarshalRadio(306)
Tarawa:SetLSORadio(306)
Tarawa:SetSoundfilesFolder("Airboss Soundfiles/")
Tarawa:SetDespawnOnEngineShutdown()
Tarawa:SetMenuSingleCarrier()
Tarawa:SetMenuRecovery(60, 20, true)

Tarawa:Start()

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


-------JTAC Initial Spawn------------
do
  Spawn_JTAC1 = SPAWN:New("JTAC1")
    :InitKeepUnitNames(true)
    :InitLimit(1,0)
    :InitDelayOn()
    :OnSpawnGroup(
      function( SpawnGroup1 )
        ctld.JTACAutoLase(SpawnGroup1.GroupName, 1388, false, "all")
      end
    )
    :SpawnScheduled( 60,0 )

  Spawn_JTAC2 = SPAWN:New("JTAC2")
    :InitKeepUnitNames(true)
    :InitLimit(1,0)
    :InitDelayOn()
    :OnSpawnGroup(
      function( SpawnGroup2 )
        ctld.JTACAutoLase(SpawnGroup2.GroupName, 1488, false, "all")
      end
    )
    :SpawnScheduled( 60,0 )
end
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