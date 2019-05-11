dofile('discord_api_key.lua') -- bring in the channel 
dofile('discord_channel_key.lua') -- bring in the channel 
print(HYPEMAN_BOT_CLIENT_ID)
print(HYPEMAN_CHANNEL_ID)
local CHANNEL_ID = HYPEMAN_CHANNEL_ID
local BOT_CLIENT_ID = HYPEMAN_BOT_CLIENT_ID

local PORT =  10081
local HOST = '0.0.0.0'

local dgram = require('dgram')
local discordia = require('discordia')
local client = discordia.Client()
local ch = nil

client:on('ready', function()
    print('Logged in as '.. client.user.username)
    ch = client:getChannel(CHANNEL_ID)
    ch:send('HypeMan is ready to hype.  Imma relay messages from Join Top Swing Dedicated Server')
end)

client:on('messageCreate', function(message)	

	local id = message.channel.id
	-- print(id)
	
	if id  == CHANNEL_ID then
		-- message.channel:send('Message sent on the correct channel')
	
		local content = message.content
		if content == '!info' or content == '!about' or content == '!hypeman' then			
			message.channel:send('HypeMan is an experimental Discord bot to announce Digital Combat Simulator (DCS) game events to Discord.  See https://aggressors.ca/hypeman for more information')		
		end		
	end	
end)

client:run(BOT_CLIENT_ID)

local s2 = dgram.createSocket('udp4')

p('PORT',PORT)
s2:bind(PORT,HOST)

-- local s1 = dgram.createSocket('udp4')
-- s1:bind(PORT,HOST)
-- s1:send('HELLO', PORT+1, '127.0.0.1')

local function f(msg)
    if ch ~= nil then
		-- local t2 = os.date()
        -- ch:send(t2 .. ' : ' .. msg)
		ch:send(msg)		
    end	
end

    
s2:on('message', function(msg, rinfo)
	-- local t = os.date()	
    p('Message received: ')
    p(msg)
    
    if ch ~= nil then
		botSendMessage = coroutine.wrap (f)
        botSendMessage(msg)
    end
	-- nilling the message here.  Somehow the message was getting appended to and growing?  not sure how or why that happened
	-- msg = nil
	-- Seemed to only be due to time acceleration in DCS?  I don't know.
end)