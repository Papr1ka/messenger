import socket
import asyncio
import requests

class Socket():
    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.packages = 2048
        self.mainloop = asyncio.get_event_loop()
    
    async def send_data(self, data):
        raise NotImplementedError()

    async def listen_socket(self, listened_socked = None):
        raise NotImplementedError()

    async def main(self):
        raise NotImplementedError()

    def start(self):
        self.mainloop.run_until_complete(self.main())

    def set_up(self):
        raise NotImplementedError()

    def getName(self):
        try:
            # Use a get request for api.duckduckgo.com
            raw = requests.get('https://api.duckduckgo.com/?q=ip&format=json')
            # load the request as json, look for Answer.
            # split on spaces, find the 5th index ( as it starts at 0 ), which is the IP address
            answer = raw.json()["Answer"].split()[4]
        # if there are any connection issues, error out
        except Exception as e:
            return 'Error: {0}'.format(e)
        # otherwise, return answer
        else:
            return answer