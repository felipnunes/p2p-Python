import socket

class Client():
    def __init__(self, client_socket, client_ip, id):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.id = id
        self.filesList = []
        
    

def assignId():
    global actualId
    actualId += 1
    return actualId    

localPort   = 5000
bufferSize  = 1024
actualId = 0
#cria uma lista vazia que serve para adicionar os peers conectados
clientList = []

# Cria um socket TCP
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# Faz o bind de endereço IP e porta
TCPServerSocket.bind(('', localPort))
TCPServerSocket.listen()

while(True):
    print("Aguardando solicitação de conexão de um cliente")
    newClient = Client(*TCPServerSocket.accept(), assignId())
    clientList.append(newClient)
    data = newClient.client_socket.recv(bufferSize)
    print('Mensagem recebida do cliente: ', data)
    newClient.client_socket.send(data.upper())
    #newClient.client_socket.close()    
    print(newClient.id)

 


