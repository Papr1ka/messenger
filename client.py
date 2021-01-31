from Socket import Socket
import asyncio
from datetime import datetime
from os import system


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.load = False
        self.messages = ""

    def set_up(self):
        try:
            self.socket.connect(("127.0.0.1", 5565))
        except ConnectionRefusedError:
            print("сервер недоступен")
            ans = str(input("подключиться заново? Y/N "))
            if ans == "Y":
                return self.set_up()
            else:
                return
        self.socket.setblocking(False)
        print("You are connected")
        self.login()
        self.start()


    async def listen_socket(self, listened_socked = None):
        while True:
            try:
                data = await self.mainloop.sock_recv(self.socket, self.packages if self.load else self.packages * 50)
                self.load = True
            except ConnectionResetError:
                print("You are disconnected")
                return
            system("cls")
            self.messages += data.decode('utf-8')
            print(self.messages)

    async def send_data(self, data = None):
        while True:
            data = await self.mainloop.run_in_executor(None, input)
            if data != "":
                data = f"{datetime.now().strftime('%H:%M')} | {self.name} | {data}\n"
                await self.mainloop.sock_sendall(self.socket, data.encode("utf-8"))
    
    async def main(self):
        listening_task = self.mainloop.create_task(self.listen_socket())
        sending_task = self.mainloop.create_task(self.send_data())
        await asyncio.gather(listening_task, sending_task)
    
    def login(self):
        self.name = input("Your Nick: ")
        if 1 < len(self.name) < 13:
            self.name = " " * ((12 - len(self.name)) // 2) + self.name + " " * (12 - len(self.name) - (12 - len(self.name)) // 2)
        else:
            print("Your neme is must be 2 to 12 symbols")
            self.login()

if __name__ == "__main__":
    client = Client()
    client.set_up()