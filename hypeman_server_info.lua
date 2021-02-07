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
	--print(message.content)
	--if message.content == '!server_info' and message.channel.guild ~= nil then	

	if message.content == '!server_info' then
		local final_string = 'server_info.bat'
		os.execute(final_string)
		local str = readAll('server_info.txt')
		-- Disabled to remove duplicate mesages
		--message.channel:send('```' .. str .. '```')
		return
	end

	if message.content == '#boatstuff -help' then
		local helpstr = 'Boatstuff scoring:\n  "best": best trap of a calendar day (Default).\n  "first": first wire of the day, average of passes until you catch a wire.\n  Squadrons use will use first scoring.\n\nSquadrons:\n  Scans your DCS callsign for a squadron tag, i.e. Vexx [VFA-86]\n\nBoatstuff commands\n  #boatstuff (-first)\n  #turkeystuff (-first)\n  #scooterstuff (-first)\n  #winderstuff\n  #checkmatestuff'
		message.channel:send('```' .. helpstr .. '```')
	end
	
	if message.content == '#boatstuff -first' then
		local final_string = 'boardroom2.bat hornet first'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}
		--channel.sendMessage("message").addFile(new File("path/to/file")).queue();
	end	
	
	if message.content == '#boatstuff' then
		local final_string = 'boardroom2.bat hornet'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}
		--channel.sendMessage("message").addFile(new File("path/to/file")).queue();
	end

	if message.content == '#turkeystuff -first' then
		local final_string = 'boardroom2.bat turkey first'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end	
	
	if message.content == '#turkeystuff' then
		local final_string = 'boardroom2.bat turkey'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end
	

	if message.content == '#scooterstuff -first' then
		local final_string = 'boardroom2.bat scooter first'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}			
	end
	
	if message.content == '#scooterstuff' then
		local final_string = 'boardroom2.bat scooter'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}			
	end
	
	if message.content == '#goshawkstuff' then
		local final_string = 'boardroom2.bat goshawk'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}			
	end

	if message.content == '#winderstuff' then
		local final_string = 'boardroom2.bat hornet first vfa86'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end
	
	if message.content == '#checkmatestuff' then
		local final_string = 'boardroom2.bat turkey first vf211'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end	
	
	if message.content == '#harrierstuff' then
		local final_string = 'boardroom2.bat harrier'
		os.execute(final_string)
		message.channel:send {
			file = "final.jpg",
		}		
	end
	
end)

client:run(BOT_CLIENT_ID)
