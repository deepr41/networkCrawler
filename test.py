import socket

url = input()

data = socket.gethostbyname_ex(url)

print(data)
