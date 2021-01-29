from Socket import Socket
import asyncio

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        print("the server is listening")
        self.users = []
        self.last_messages = [] #limit = 100

    def set_up(self):
        self.socket.bind(("127.0.0.1", 5565))
        self.socket.listen()
        self.socket.setblocking(False)
        self.socket.settimeout(0)
    
    async def listen_socket(self, listened_socked = None):
        if not listened_socked:
            return
        while True:
            data = await self.mainloop.sock_recv(listened_socked, self.packages)
            print(f"user send {data}")
            await self.send_data(data)
    
    async def send_data(self, data):
        if len(self.last_messages) > 100:
            self.last_messages.remove(self.last_messages[0])
        self.last_messages.append(data)
        for user in self.users:
            await self.mainloop.sock_sendall(user, data)
    
    async def accept_sockets(self):
        while True:
            user_socket, adress = await self.mainloop.sock_accept(self.socket)
            print(f"User {adress} connected")
            self.users.append(user_socket)
            self.mainloop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.mainloop.create_task(self.accept_sockets())

if __name__ == "__main__":
    LocalServer = Server()
    LocalServer.set_up()
    LocalServer.start()
