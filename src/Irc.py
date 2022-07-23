import logging
import socket
import time

class Irc:
    irc = socket.socket()

    def __init__(self):
        '''
        Create the IRC socket
        '''
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, channel: str, msg: str):
        '''
        Snend data to remote server, in most cases this would be a message. 

        channel: String - The channel to send 'msg' to. 
        msg:     String - The message to send to 'channel'. 
        '''
        self.irc.send(bytes('PRIVMSG ' + channel + ' :' + msg + '\n', 'UTF-8'))

    def join(self, channel):
        '''
        Join the channel 'channel'

        channel: String  - The channel to join.
        '''
        logging.info(f'Joinging {channel}...')
        self.irc.send(bytes('JOIN ' + channel + '\n', 'UTF-8'))
        logging.info(f'Joined {channel}!')

    def connect(self, server, port, nick, passwd=None, channel=None):
        '''
        Start a connection to a remote server

        server:  String  - The server to connect to.
        port:    Integer - The port to connect to.
        nick:    String  - The nickname of the bot.
        passwd:  String  - The nickname password.
        channel: String  - The channel to join.
        '''
        logging.info(f'Connecting to {server}...')
        self.irc.connect((server, port))

        # Perform user authentication
        logging.info(f'Logging in...')
        self.irc.send(bytes('USER ' + nick + ' ' + nick +' ' + nick + ' :python\n', 'UTF-8'))
        self.irc.send(bytes('NICK ' + nick + '\n', 'UTF-8'))
        if passwd:
            logging.info('Logging into NICKSERV...')
            self.irc.send(bytes('NICKSERV IDENTIFY ' + nick + ' ' + passwd + '\n', 'UTF-8'))
        time.sleep(5)

        # Join the channel
        if channel:
            self.join(channel=channel)

    def get_response(self):
        '''
        Read remote server responses
        '''
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode('UTF-8')
        
        if resp.find('PING') != -1:                      
            self.irc.send(bytes('PONG ' + resp.split() [1] + '\r\n', 'UTF-8')) 
 
        return resp