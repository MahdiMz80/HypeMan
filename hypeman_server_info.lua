dofile('private_api_keys.lua')

print(PRIVATE_HYPEMAN_BOT_CLIENT_ID)
print(PRIVATE_HYPEMAN_CHANNEL_ID)

local BOT_CLIENT_ID = PRIVATE_HYPEMAN_BOT_CLIENT_ID
local CHANNEL_ID = PRIVATE_HYPEMAN_CHANNEL_ID


local dgram = require('dgram')
local discordia = require('discordia')

local client = discordia.Client()

client:on('ready', function()
    print('Logged in as '.. client.user.username)
end)

function readAll(file)
    local f = assert(io.open(file, "rb"))
    local content = f:read("*all")
    f:close()
    return content
end

client:on('messageCreate', function(message)	

	-- print('message received')
	
	--if message.content == '!server_info' and message.channel.guild ~= nil then	

	if message.content == '!server_info' then
		local final_string = 'server_info.bat'
		os.execute(final_string)
		local str = readAll('server_info.txt')
		message.channel:send(str)
		return
	end
	
end)

client:run(BOT_CLIENT_ID)
