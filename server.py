import socket
import threading

host, port = "localhost", 6009
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients, nicks = list(), list()


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        
        try:
            message = client.recv(1024)
            broadcast(message)
            
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            
            nick = nicks[index]
            broadcast(f"{nick} has left the chat".format().encode("utf-8"))
            nicks.remove(nick)
            break


def receive():

    while True:
        
        client, address = server.accept()
        address, port = client.getsockname()
        clients.append(client)
        
        print(f"[INFO] NEW_CONNECTION {address}:{port}")    
        client.send("SET_NICK".encode("utf-8"))

        nick = client.recv(1024).decode("utf-8")
        nicks.append(nick)

        print(f"[INFO] NEW_USER: {nick}")
        broadcast("{} has joined!".format(nick).encode("utf-8"))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()