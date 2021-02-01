from Socket import Socket
import asyncio
from socket import gethostname, gethostbyname

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        print("the server is listening")
        self.users = []
        self.last_messages = []
        self.limit = 50
        self.hello_message = "Welcome to Messanger, you see the last 100 posts\n".encode('utf-8')

    def set_up(self):
        self.socket.bind((gethostbyname(gethostname()), 5565))
        print(gethostbyname(gethostname()))
        self.socket.listen()
        self.socket.setblocking(False)
        self.socket.settimeout(0)
    
    async def listen_socket(self, listened_socked = None):
        if not listened_socked:
            return
        while True:
            try:
                data = await self.mainloop.sock_recv(listened_socked, self.packages)
                await self.logging(data)
                print(f"user send {data}")
                await self.send_data(data)
            except ConnectionResetError:
                print("User disconnect")
                self.users.remove(listened_socked)
                return


    async def logging(self, data):
        if len(self.last_messages) >= self.limit:
            self.last_messages.remove(self.last_messages[0])
        self.last_messages.append(data)

    async def send_data(self, data):
        for user in self.users:
            await self.mainloop.sock_sendall(user, data)
    
    async def accept_sockets(self):
        while True:
            user_socket, adress = await self.mainloop.sock_accept(self.socket)
            print(f"User {adress} connected")
            self.users.append(user_socket)
            await self.mainloop.sock_sendall(user_socket, self.hello_message)
            for i in self.last_messages:
                await self.mainloop.sock_sendall(user_socket, i)
            print(f"send last messages : {len(self.last_messages)}")
            self.mainloop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.mainloop.create_task(self.accept_sockets())

if __name__ == "__main__":
    LocalServer = Server()
    LocalServer.set_up()
    LocalServer.start()
