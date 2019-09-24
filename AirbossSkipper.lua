-------------------------
-- AIRBOSS Test Script --
-------------------------

-- Switches if you want to include a rescue helo and/or a recovery tanker.
local Tanker=true
local HighTank=true
local Helo=true
local Traffic=false
local Stennis=true
local Tarawa=false

local Single=true --not (Stennis and Tarawa)

-- Set mission menu.
AIRBOSS.MenuF10Root=MENU_MISSION:New("Airboss").MenuPath

-- No MOOSE settings menu.
_SETTINGS:SetPlayerMenuOff()

if Tarawa then

  -- Create AIRBOSS object.
  local AirbossTarawa=AIRBOSS:New("Tarawa")
  
  -- Add recovery windows:
  -- Case I from 9 to 10 am.
  local window1=AirbossTarawa:AddRecoveryWindow( "9:00", "10:00", 1, nil, true, 20)
  -- Case II with +15 degrees holding offset from 15:00 for 60 min.
  local window2=AirbossTarawa:AddRecoveryWindow("15:00", "16:00", 2, 15)
  -- Case III with +30 degrees holding offset from 2100 to 2200.
  local window3=AirbossTarawa:AddRecoveryWindow("21:00", "22:00", 3, 30)
  
  -- Set TACAN
  AirbossTarawa:SetTACAN(108, "X", "LHA")
  AirbossTarawa:SetICLSoff()

  -- Single carrier menu optimization.
  AirbossTarawa:SetMenuSingleCarrier(Single)
  
  -- Load all saved player grades from your "Saved Games\DCS" folder (if lfs was desanitized).
  AirbossTarawa:Load()
  
  -- Automatically save player results to your "Saved Games\DCS" folder each time a player get a final grade from the LSO.
  AirbossTarawa:SetAutoSave()
  
  -- Set name of the unit transmitting the radio messages. This should be an aircraft as these are the only units where radio calls can be subtitled!
  --AirbossTarawa:SetRadioUnitName("SH-60B Radio Relay")
  
  --Set folder of airboss sound files within miz file.
  AirbossTarawa:SetSoundfilesFolder("Airboss Soundfiles/")
  
  -- Remove landed AI planes from flight deck.
  AirbossTarawa:SetDespawnOnEngineShutdown()
  
  -- Start Airboss.
  AirbossTarawa:Start()
  
  -- Spawn some AI flights as additional traffic.
  if Traffic then
    local AV8B1=SPAWN:New("AV8B AI Alpha Group"):InitModex(70)
    local AV8B2=SPAWN:New("AV8B AI Bravo Group"):InitModex(80)
    local AV8B3=SPAWN:New("AV8B AI Charlie Group"):InitModex(90)
    
    -- Spawn always 9 min before the recovery window opens.
    local spawntimes={"8:51", "14:51", "20:51"}
    for _,spawntime in pairs(spawntimes) do
      local _time=UTILS.ClockToSeconds(spawntime)-timer.getAbsTime()
      if _time>0 then
        SCHEDULER:New(nil, AV8B1.Spawn, {AV8B1}, _time)
        SCHEDULER:New(nil, AV8B2.Spawn, {AV8B2}, _time)
        SCHEDULER:New(nil, AV8B3.Spawn, {AV8B3}, _time)
      end
    end  
  end
  
end


if Stennis then

  -- S-3B Recovery Tanker spawning in air.
  local tanker=nil  --Ops.RecoveryTanker#RECOVERYTANKER
  if Tanker then
    tanker=RECOVERYTANKER:New("CVN74", "Texaco")
    tanker:SetTakeoffAir()
    tanker:SetRadio(262)
    tanker:SetModex(511)
    tanker:SetTACAN(60, "TKR")
    tanker:Start()
  end
  
  -- KC-130 HighTank spawning in air
  local hightank=nil  --Ops.RecoveryTanker#RECOVERYTANKER
  if HighTank then
    hightank=RECOVERYTANKER:New("CVN74", "Arco")
    hightank:SetTakeoffAir()
    hightank:SetRadio(268)
    hightank:SetAltitude(15000)
    hightank:SetRacetrackDistances(25, 8)
    hightank:SetModex(611)
    hightank:SetTACAN(55, "ARC")
    hightank:Start()
  end
  
  -- Rescue Helo spawned in air with home base USS Ticonderoga.
  if Helo then
    -- Has to be a global object!
    rescuehelo=RESCUEHELO:New("CVN74", "Rescue Helo")
    rescuehelo:SetHomeBase(AIRBASE:FindByName("USS Ticonderoga"))
    rescuehelo:SetTakeoffAir()
    rescuehelo:SetModex(42)
    rescuehelo:Start()
  end
    
  -- Create AIRBOSS object.
local AirbossStennis=AIRBOSS:New("CVN74")
  
-- Delete auto recovery window.
function AirbossStennis:OnAfterStart(From,Event,To)
  self:DeleteAllRecoveryWindows()
end

function AirbossStennis:OnAfterLSOGrade(From, Event, To, playerData, myGrade)
	myGrade.messageType = 2
	myGrade.name = playerData.name
	HypeMan.sendBotTable(myGrade)
end

  -- Start airboss class.
AirbossStennis:Start()

-- Add Skipper menu to start recovery via F10 radio menu.
AirbossStennis:SetMenuRecovery(60, 25, true)

--Add Offset for CASE II/III
AirbossStennis:SetHoldingOffsetAngle(0)
  
-- Load all saved player grades from your "Saved Games\DCS" folder (if lfs was desanitized).
AirbossStennis:Load()
  
-- Automatically save player results to your "Saved Games\DCS" folder each time a player get a final grade from the LSO.
AirbossStennis:SetAutoSave()
  
--Set Airboss Trap Sheet
  AirbossStennis:SetTrapSheet()
  
  --Set ICLS to channel 9
  AirbossStennis:SetTACAN(104, "X", "STN")
  AirbossStennis:SetICLS(9,"CVN")
  
  --Set Patrol route Ad Infinitum
  AirbossStennis:SetPatrolAdInfinitum()
  
  --Set Airboss Nice guy
  AirbossStennis:SetAirbossNiceGuy()
  
  --Set Airboss Section Size
  AirbossStennis:SetMaxSectionSize(4)  
  
  -- Set name of the unit transmitting the radio messages. This should be an aircraft as these are the only units where radio calls can be subtitled!
  AirbossStennis:SetRadioRelayLSO("LSO Huey")
  AirbossStennis:SetRadioRelayMarshal("Marshal Huey")
  
  -- Set folder of airboss sound files within miz file.
  AirbossStennis:SetSoundfilesFolder("Airboss Soundfiles/")
  
  -- AI groups explicitly excluded from handling by the Airboss
  local CarrierExcludeSet=SET_GROUP:New():FilterPrefixes("Arco"):FilterStart()
  AirbossStennis:SetExcludeAI(CarrierExcludeSet)
   
  -- Single carrier menu optimization.
  AirbossStennis:SetMenuSingleCarrier(Single)
  
  -- Remove landed AI planes from flight deck.
  AirbossStennis:SetDespawnOnEngineShutdown()
  
    -- Set recovery tanker.
  if Tanker then
    AirbossStennis:SetRecoveryTanker(tanker)
  end
  
  --- Function called when recovery starts.
  function AirbossStennis:OnAfterRecoveryStart(Event, From, To, Case, Offset)
    env.info(string.format("Starting Recovery Case %d ops.", Case))
    --AirbossStennis:__RecoveryStop(300)
  end
  
  -- Spawn some AI flights as additional traffic.
  if Traffic then
    local F181=SPAWN:New("FA18 Group 1"):InitModex(101) -- Coming in from NW after  ~6 min
    local F182=SPAWN:New("FA18 Group 2"):InitModex(201) -- Coming in from NW after ~20 min
    local F183=SPAWN:New("FA18 Group 3"):InitModex(301) -- Coming in from W  after ~18 min
    local F14=SPAWN:New("F-14A 2ship"):InitModex(401)   -- Coming in from SW after  ~4 min
    local E2D=SPAWN:New("E-2D Group"):InitModex(501)    -- Coming in from NE after ~10 min
    local S3B=SPAWN:New("S-3B Group"):InitModex(601)    -- Coming in from S  after ~16 min
    
    -- Spawn always 9 min before the recovery window opens.
    local spawntimes={"8:51", "14:51", "20:51"}
    for _,spawntime in pairs(spawntimes) do
      local _time=UTILS.ClockToSeconds(spawntime)-timer.getAbsTime()
      if _time>0 then
        SCHEDULER:New(nil, F181.Spawn, {F181}, _time)
        SCHEDULER:New(nil, F182.Spawn, {F182}, _time)
        SCHEDULER:New(nil, F183.Spawn, {F183}, _time)
        SCHEDULER:New(nil, F14.Spawn,  {F14},  _time)
        SCHEDULER:New(nil, E2D.Spawn,  {E2D},  _time)
        SCHEDULER:New(nil, S3B.Spawn,  {S3B},  _time)
      end
    end  
  end
end

  
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

--Tanker and AWAC objects
--local RefuelNorth = ZONE:New("Refuel North") 
--local RefuelSouth = ZONE:New("Refuel South")
--local AWACs = ZONE:New("AWACs")  

Spawn_Awacs = SPAWN:New("Magic"):InitLimit(1,0)
Spawn_Shell_North = SPAWN:New("Shell North"):InitLimit(1,0)
Spawn_Shell_South = SPAWN:New("Shell South"):InitLimit(1,0)

--Repeat on Landing
Spawn_Awacs:InitRepeatOnLanding()
Spawn_Shell_North:InitRepeatOnLanding()
Spawn_Shell_South:InitRepeatOnLanding()

--Spawn
Spawn_Awacs:SpawnScheduled(60,0)
Spawn_Shell_North:SpawnScheduled(60,0)
Spawn_Shell_South:SpawnScheduled(60,0)
--End Tanker/Awacs




