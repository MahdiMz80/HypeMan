# HypeMan
HypeMan brings the hype

# Introduction
HypeMan.lua This is the script that gets included with your DCS mission. 
hypeman_listener.lua - this is the backend listener that receives the messages from Discord and sends the messages to Discord

#Requirements: #
- Mist 4.7.4 or higher
- Discordia lua Discord API
- luvit lua REPL or similar

#INSTALLATION#
Include this file in your mission with a DO SCRIPT, or DO SCRIPT FILE any time after Mist has been loaded.

TIPS AND TRICKS
Load HypeMan from an external file using this DO SCRIPT:
```
assert(loadfile("C:/HypeMan/HypeMan.lua"))() 
```

This allows HypeMan to be updated for every mission it is included with by simply changing the external file.
Simply add that code to any mission, even if you do not have HypeMan running or installed.  Because the loadfile
is wrapped in an assert() call any errors are supressed.

#USAGE#
Once loaded, HypeMan monitors for several events: takeoffs, landings, crash, eject, etc, and will automatically report
these events to Discord.
HypeMan also provides a function that can be called anywhere in the mission: hypeman.sendBotMessage().  This allows
Mission creators to send messages to the Discord based on events in the mission.

-- i.e. TRIGGER TYPE ONCE, IF GROUP DEAD('RED TANKS') THEN DO SCRIPT hypeman.sendBotMessage('The Red Tanks have been destroyed!  Move forward!')

#FAQ#

1.) I'm worried about performance and stability.  Does HypeMan take a lot of resources in the mission?

HypeMan is pretty light, and the messages are sent over UDP with no locking or waiting for acknowledgement.  HypeMan should not negatively impact server or mission performance.

2.) Because all multiplayer clients get a full copy of the .miz file in the multiplayer track, won't that expose my private Discord bot API key to every multiplayer client?

No, the private Discord API key is only used by the Hypeman_listener.lua backend, and this file is not included with the DCS .miz file, so no private API keys are exposed to multiplayer clients.

3.) I want to stop HypeMan from sending messages while I experiment with the Server

Simply stop the hypeman_listener backend.  The backend listener can be started, stopped, and restarted at any time while the mission is running.

4.) I don't want to install HypeMan on the many computers I edit DCS missions on, and I want virtual squadron members to be able to edit missions and not worry about having to have all these external .lua file dependencies.

```
assert(loadfile("C:/HypeMan/HypeMan.lua"))() 
```

Using the assert/loadfile code snippet to load HypeMan means that if the lua file is not found, the errors are just supressed and the mission will continue even if HypeMan is not found.

