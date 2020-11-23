-- Create a simple target range and show how to get the
-- Range Bomb impacts to Discord via HypeMan


TargetRange=RANGE:New("Target Range")

bombTargets = {'BombTarget01', 'BombTarget02', 'BombTarget03'}
TargetRange:AddBombingTargets(bombTargets, 20, false)

strafe_targets = {'StrafePit01', 'StrafePit02'}

TargetRange:AddStrafePit(strafe_targets, 3000, 500, nil, true, 20, 610)

function TargetRange:OnAfterImpact(From, Event, To, result, player)  
  local text=string.format("%s, impact %03d° for %d ft", player.playername, result.radial, UTILS.MetersToFeet(result.distance))  
  text=text..string.format(" %s hit.", result.quality)  
  HypeMan.sendBotMessage(text)
  
  -- Debugging - see the raw results table in Discord to see what fields are available  
  -- HypeMan.sendBotMessage(JSON:encode(result))	
end

TargetRange:Start()

HypeMan.sendBotMessage("Range Script loaded.")

