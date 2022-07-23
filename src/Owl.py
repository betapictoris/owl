import asyncio
import hikari
import logging
import os
import sys
import threading

from colorama import Fore, Back, Style
from DiscordWebhook import DiscordWebhook
from Irc import Irc

print(Fore.CYAN + '''

     ██████╗ ██╗    ██╗██╗     
    ██╔═══██╗██║    ██║██║     
    ██║   ██║██║ █╗ ██║██║     
    ██║   ██║██║███╗██║██║     
    ╚██████╔╝╚███╔███╔╝███████╗
     ╚═════╝  ╚══╝╚══╝ ╚══════╝
                              
''' + Style.RESET_ALL)

textFormat = f'{Fore.YELLOW}%(asctime)s:{Style.RESET_ALL} %(message)s'
dateFormat = '%H:%M:%S'
logging.basicConfig(format=textFormat, level=logging.INFO, datefmt=dateFormat)
logging.info('Starting...')

class Config:
    class Irc:
        enabled = bool(os.environ['IrcEnabled'])        # Enable the IRC client
        server  = str (os.environ['IrcServer'])         # IRC server for connection
        port    = int (os.environ['IrcPort'])           # IRC port
        channel = str (os.environ['IrcChannel'])        # IRC channel to read/send from/to
        botnick = str (os.environ['IrcBotnick'])        # Nick name for the bot

    class Discord:
        enabled = bool(os.environ['DiscordEnabled'])    # Enable the Discord client 
        token   = str (os.environ['DiscordToken'])      # Discord bot token 
        webhook = str (os.environ['DiscordWebhook'])    # Discord webhook (used for sending messages to the Discord server)
        guild   = str (os.environ['DiscordGuild'])      # Discord guild to send/read messages to/from
        channel = str (os.environ['DiscordChannel'])    # Discord channel to send/read message to/from

# Create clients
def IrcClient():
    global irc
    irc = Irc()
    logging.info('IRC socket created!')

    if Config.Irc.enabled:
        logging.info('Starting IRC client...')
        irc.connect(Config.Irc.server, Config.Irc.port, Config.Irc.botnick, channel=Config.Irc.channel)

        while True:
            text = irc.get_response()
 
            if 'PRIVMSG' in text and Config.Irc.channel in text:
                # If 'text' is a message to #CHAN then send it to the log as INFO, and use the webhook to send it to Discord.
                logging.info(f'IRC: {text}')

                username = text.split(':')[1].split('!')[0]
                message  = text.split(Config.Irc.channel + ' :')[-1]

                DiscordWebhook.send(url=Config.Discord.webhook, msg=message, username=username)
            else:
                logging.debug(f'IRC: {text}')

def DiscordClient():
    bot = hikari.GatewayBot(token=Config.Discord.token, banner=None)
    logging.info('Discord bot created!')

    if Config.Discord.enabled:
        logging.info('Starting Discord client...')

        @bot.listen()
        async def onMessage(event: hikari.GuildMessageCreateEvent) -> None:
            logging.debug('Message in ' + str(event.channel_id))
            if event.is_bot or not event.content or event.is_webhook:
                logging.debug('Message was not a user')
                return

            elif event.channel_id == int(Config.Discord.channel):
                irc.send(Config.Irc.channel, f'{event.message.author}: {event.message.content}')
                logging.info(f'Discord: {event.message.author}: {event.message.content}')

        bot.run()
        logging.info('Discord bot running...')

# Start threads
logging.info('Starting Discord thread...')
discordThread = threading.Thread(target=DiscordClient)
discordThread.start()

logging.info('Starting IRC thread...')
ircThread = threading.Thread(target=IrcClient)
ircThread.start()

logging.info(f'Threads started!')

for t in [discordThread, ircThread]:
    while t.is_alive():
        t.join(timeout=0.5)

