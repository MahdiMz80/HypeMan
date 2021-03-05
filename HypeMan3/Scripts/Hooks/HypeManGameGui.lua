JSON = (loadfile "C:/HypeMan/JSON.lua")() -- one-time load of the routines

net.log('HYPEMANGAMEGUI LOGGING EXAMPLE')

package.path  = package.path..";.\\LuaSocket\\?.lua;"
package.cpath = package.cpath..";.\\LuaSocket\\?.dll;"
local socket = require("socket")

local HypeMan = {}
HypeMan.UDPSendSocket = socket.udp()
HypeMan.UDPSendSocket:settimeout(0)

HypeMan.sendBotTable = function(tbl)
	-- env.info(msg)  -- for debugging
	local tbl_json_txt = JSON:encode(tbl)   
	--local tbl_json_txt = "SENDING VIA UDP OUT OF SERVER ENVIRONMENT"
	socket.try(HypeMan.UDPSendSocket:sendto(tbl_json_txt, '127.0.0.1', 10081))
	-- msg = nil  -- setting to nil in attempt to debug why message queue seems to grow
end

HypeMan.sendBotMessage  = function(msg)
	-- env.info(msg)  -- for debugging
	--socket.try(HypeMan.UDPSendSocket:sendto(msg, '127.0.0.1', 10081))
	messageTable = {}
	messageTable.messageType = 1
	messageTable.messageString = msg
	HypeMan.sendBotTable(messageTable)
	msg = nil  -- setting to nil in attempt to debug why message queue seems to grow
end

local hypemanGui = {}

function hypemanGui.onNetConnect(localPlayerID)
	net.log('HYPEMANGAMEGUI onNetConnect')
	HypeMan.sendBotMessage('HYPEMANGAMEGUI onNetConnect')
end

function hypemanGui.onPlayerChangeSlot(id)
    -- a player successfully changed the slot
    -- this will also come as onGameEvent('change_slot', playerID, slotID),
    -- if allowed by server.advanced.event_Connect setting
	net.log('HYPEMANGAMEGUI onPlayerChangeSlot')
end

function hypemanGui.onPlayerConnect(id)
	net.log('HYPEMANGAMEGUI onPlayerConnect')
	HypeMan.sendBotMessage('HYPEMANGAMEGUI onPlayerConnect')
end


function hypemanGui.onSimulationStart()
	net.log('HYPEMANGAMEGUI onSimulationStart')
	HypeMan.sendBotMessage('HYPEMANGAMEGUI onSimulationStart')
    --print('Current mission is '..DCS.getMissionName())
end

function hypemanGui.onPlayerTryConnect(ipaddr, name, ucid, playerID)
	net.log('HYPEMANGAMEGUI onPlayerTryConnect')
	HypeMan.sendBotMessage('HYPEMANGAMEGUI onPlayerTryConnect')
	msg = {}
	msg.ip = ipaddr
	msg.name = name
	msg.ucid = ucid
	msg.playerID = playerID
	msg.mission = DCS.getMissionName()
	msg.messageType = 5
	HypeMan.sendBotTable(msg)
    -- print('onPlayerTryConnect(%s, %s, %s, %d)', ipaddr, name, ucid, playerID)
    -- if you want to gently intercept the call, allowing other user scripts to get it,
    -- you better return nothing here
    return true -- allow the player to connect
end

DCS.setUserCallbacks(hypemanGui)  -- here we set our callbacks