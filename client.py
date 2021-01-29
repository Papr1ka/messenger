from Socket import Socket
import asyncio
from datetime import datetime
from os import system


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""
        self.login()

    def set_up(self):
        self.socket.connect(("127.0.0.1", 5565))
        self.socket.setblocking(False)

    
    async def listen_socket(self, listened_socked = None):
        while True:
            data = await self.mainloop.sock_recv(self.socket, self.packages)
            self.messages += f"{datetime.now().strftime('%H:%M')} {data.decode('utf-8')}\n"
            system("cls")
            print(self.messages)

    async def send_data(self, data = None):
        while True:
            data = await self.mainloop.run_in_executor(None, input)
            data = f"| {self.name} | {data}"
            await self.mainloop.sock_sendall(self.socket, data.encode("utf-8"))
    
    async def main(self):
        listening_task = self.mainloop.create_task(self.listen_socket())
        sending_task = self.mainloop.create_task(self.send_data())
        await asyncio.gather(listening_task, sending_task)
    
    def login(self):
        self.name = input("Your Nick: ")

if __name__ == "__main__":
    client = Client()
    client.set_up()
    
    client.start()