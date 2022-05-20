import socket
import threading

nick = input("Set nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 6009))


def receive():
    while True:  # Подтверждение соединения
        try:
            msg = client.recv(1024).decode("utf-8")
            match msg:
                case "USER_BAN_LEN":
                    print("Sorry but chat is full")
                    break
                
                case "SET_NICK":
                    client.send(nick.encode("utf-8"))
                case _:
                    print(msg)

        except Exception as error:
            print(f"CANNOT CONNECT: {error}")
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nick, input("SEND: "))
        client.send(message.encode("utf-8"))


def get_msg():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()


def push_msg():
    write_thread = threading.Thread(target=write)
    write_thread.start()
  
    
get_msg()
push_msg()