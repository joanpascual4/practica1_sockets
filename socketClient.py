# Práctica 1 - Sockets
# Joan Pascual Alcaraz

# Imports
import socket
import random
import time

# Declaraciones
host = '127.0.0.1'
port = 1233
answers = ["yes", "no", "no", "yes", "no", "no", "yes", "no", "no", "no"] # 30% yes 70% no

ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

message = ClientSocket.recv(1024)
decoded_msg = message.decode('utf-8')
print(decoded_msg)
while True:
    time.sleep(random.randint(1, 10)) # Duerme entre 1 y 10 s
    message = ClientSocket.recv(1024) # Lee si hay algún mensaje del servidor
    decoded_msg = message.decode('utf-8')
    print(decoded_msg)
    if "end" in decoded_msg:
      break
    answer = answers[random.randint(0, 9)] # Se elige una respuesta aleatoria
    ClientSocket.send(str.encode(answer))
    print(answer)

ClientSocket.close()