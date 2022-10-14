# Práctica 1 - Sockets
# Joan Pascual Alcaraz

# Imports
import socket
import time
import random
from _thread import *
import threading
import errno

# Declaraciones
host = '127.0.0.1'
port = 1233
clientCount = 0 # Número de clientes conectados al servidor
maxMsg = 10 # Número de mensajes de ayuda a pedir
msgHelped = 0 # Número de mensajes que han sido ayudados
helpMsgs = [0] * maxMsg # Lista de ayudas a todos los mensajes
timeAsleep = [0] * maxMsg # Array donde guardo los timeout de cada mensaje
lock = threading.Lock()

# Función que se encarga de la comunicación con el cliente
def client_handler(connection):
    global msgHelped
    global maxMsg
    global helpMsgs
    global timeAsleep

    connection.setblocking(False) # Importante para que no espere a la respuesta del cliente
    connection.send(str.encode('You are now connected to the server'))
    while (clientCount != 3): # Sala de espera de 3 clientes
            pass
    time.sleep(1) # Para sincronizar los clientes
    for numMsg in range(maxMsg):
        #Envía el mensaje de ayuda
        connection.sendall(str.encode("help " + str(numMsg)))
        print("Help " + str(numMsg))
        time.sleep(timeAsleep[numMsg]) # Duerme entre 1 y 5 segundos
        try: # Se comprueba la respuesta
            data = connection.recv(1024)
            message = data.decode('utf-8')
            if message == "yes": # Se cuenta el número de yes
                helpMsgs[numMsg] += 1
            print(message)
        except socket.error as e: # Si no se ha recibido nada
            if e.args[0] == errno.EWOULDBLOCK: 
                print('no answer')
            else:
                print(e)
                break
    connection.sendall(str.encode("end"))
    global lock
    if (lock.locked()):
        connection.close()
    else: # Para que estos mensajes solo se impriman una vez
        lock.acquire()
        time.sleep(1) # Para sincronizar los clientes
        print(helpMsgs)
        print("")
        for numMsg in range(maxMsg):
            if (helpMsgs[numMsg] >= 2):
                msgHelped += 1
        # Se imprime la ayuda recibida
        print(str(msgHelped) + " out of "+ str(maxMsg) + " messages were helped")
        percent = (msgHelped / maxMsg) * 100
        print(str(percent) + "% satisfaction")
        connection.close()

# Función que se encarga de establecer conexión con clientes en distintos hilos
def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept() # Acepta la conexión
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    global clientCount
    clientCount += 1 # Se ncrementa el número de clientes conectados
    start_new_thread(client_handler, (Client, )) # Se lanza un hilo
    
# Función que inicia el servidor 
def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()

    for numMsg in range(maxMsg):
        # Así en cada iteración cada mensaje tendrá un tiempo de timeout aleatorio
        # (entre 1 y 7 s), pero en cada hilo será el mismo para cada mensaje
        timeAsleep[numMsg] = random.randint(1, 7)
    
    while True:
        accept_connections(ServerSocket)

start_server(host, port)