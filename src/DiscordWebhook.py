import logging
import requests

class DiscordWebhook():
    '''
    Class for functions relating to Discord Webhooks
    '''

    def send(url: str, msg: str, username: str = None):
        '''
        Send a message ("msg") to the webhook ("url") with the username ("username")
        '''

        data = {
            'content': msg,
            'username': username
        }

        r = requests.post(url=url, json=data)
        logging.debug(r.text)