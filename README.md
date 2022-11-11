Práctica 1 - Sockets
Joan Pascual Alcaraz

Multicomunicación en sockets, donde un agente (server) envía un mensaje de ayuda 
y los otros 3 agentes (client) le responden sí o no (o no responder si se 
encuentran dormidos). Cada mensaje de ayuda tiene un tiempo de expiración, 
y los clientes responden al mensaje de ayuda más reciente. Un 30% de las veces 
responden sí y el otro 70% responden no.

Está implementado en Python sobre el protocolo TCP. Se gestiona la entrada de 
los clientes mediante una sala de espera: no empieza hasta que se han conectado 
3 clientes al servidor. Es importante definir setBlocking(False) para que el 
servidor no se quede esperando la respuesta del cliente. En el modo no bloqueante 
el servidor lee una vez el canal y si no hay mensaje lanza una excepción que, 
controlada en un try: except, permite continuar con la ejecución como si no se 
hubiese recibido respuesta.

Los 3 clientes se gestionan desde la parte del servidor con 3 hilos concurrentes. 
Para empezar la ejecución, lanzar el servidor en la terminal y, en 3 terminales 
distintas, lanzar los 3 clientes. El resultado completo de la ejecución aparecerá 
en el servidor.
