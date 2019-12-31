import socket

SERVER_ADDRESS_PORT = ("127.0.0.1", 4353)
MAX_MSG_SIZE = 2048
MY_ADDRESS_PORT = ("127.0.0.1", 4354)
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(MY_ADDRESS_PORT)


f = open("received.txt", 'wb')

receiver_socket.sendto("NAME receiver".encode(), SERVER_ADDRESS_PORT)
data, addr = receiver_socket.recvfrom(MAX_MSG_SIZE)
print(data)

data, addr = receiver_socket.recvfrom(MAX_MSG_SIZE)
try:
    while data:
        f.write(data)
        receiver_socket.settimeout(2)
        data, addr = receiver_socket.recvfrom(MAX_MSG_SIZE)
        print(data)
except socket.timeout:
    f.close()
    #
    print("File Downloaded")


receiver_socket.sendto("QUIT".encode(), SERVER_ADDRESS_PORT)
receiver_socket.close()