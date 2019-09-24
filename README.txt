HypeMan II: More Hyper.

HypeMan is a DCS lua script and Discord Bot that allows sending data and messages out of DCS and into discord or elsewhere.

Components:

HypeMan.lua - gets loaded by the DCS mission and sends messages out of DCS via UDP.

hypeman_listener.lua - the backend listener service that runs outside of DCS and receives UDP messages from DCS, and then responds on discord or uploads to google spreadsheets.

assert(loadfile("C:/HypeMan/mission_script_loader.lua"))()