# -*- coding: utf-8 -*-
"""
HypeMan in python
"""

import configparser
import socketserver
#import time
import json
import threading
import discord
import os

config = configparser.ConfigParser()

config.read('hypeman.ini')
BOT_ID = config['HYPEMAN']['BOT_ID']
PORT = config.getint('HYPEMAN', 'PORT')
HOST = config['HYPEMAN']['HOST']

DEBUG_PRINT_UDP_MESSAGES = True
print('Starting HYPEMAN LISTENER VERSION')
print('   DCS Serrver UDP parameters:')
print('      Host: ', HOST)
print('      port: ', PORT)

client = discord.Client()

# @client.event("ready")
# def ready(client):
#     '''
#     Spawns the thread once we are connected to the Server
#     '''
#     Thread(target=gamestatus, args=(client,)).start()


@client.event
async def on_ready():
    print('Discord BOT logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    print('message received')
    print(message.content)

    if message.content == "!server_info2":
        print('Server Info received')
        await message.channel.send('Replying to server_info from python.')
        return

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


def discordBotFunc(bot_id, client):
    client.run(bot_id)


async def discordBotQuit(client):
    await client.logout()


class DCS_UDP_Handler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        # todo - calling both .strip() and .decode('utf-8') on the data is unappealing
        # possible multiple allocations and traversing the data for each UDP message
        data = self.request[0].strip()
        #socket = self.request[1]
        # socket.sendto(data.upper(), self.client_address)
        print("{} new message from DCS server: ".format(
            self.client_address[0]))
        if DEBUG_PRINT_UDP_MESSAGES:
            print(data.decode('utf-8'))
            dt = json.loads(data)
            print(json.dumps(dt, indent=4, sort_keys=True))


if __name__ == "__main__":
    # start the Discord bot in it's own thread
    discordThread = threading.Thread(
        target=discordBotFunc, args=(BOT_ID, client))
    discordThread.start()

    with socketserver.UDPServer((HOST, PORT), DCS_UDP_Handler) as server:
        try:
            server.serve_forever()
        except:
            print('Keyboard Control+C exception detected, quitting.')
            os._exit(0)
