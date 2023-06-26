import socket
import threading

class Client:
    def __init__(self, client_socket, client_ip):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.fileStrings = []

def HandleJoinRequest(client, request):
    # Extrai as informações da requisição JOIN do cliente
    join_info = request.split(";")
    file_names = join_info[1]

    # Armazena as strings de arquivos do cliente no objeto client
    client.fileStrings = file_names.split(",")

    # Realiza a lógica de negócio para verificar e aprovar a conexão do cliente
    # Exemplo: sempre aprova a conexão
    response = "JOIN_OK"

    # Envia a resposta ao cliente
    client.client_socket.send(response.encode())

def HandleSearchRequest(clientList, request):
    fileToSearch = request  # A requisição é o próprio nome do arquivo
    ownerPeers = SearchForFile(fileToSearch, clientList)
    ownerPeersIPs = []

    if ownerPeers != []:
        for peer in ownerPeers:
            ownerPeersIPs.append(peer.client_ip)
    else:
        print("O arquivo não foi encontrado em nenhum peer e ownerPeers = ", ownerPeers)

def GetConnectedIPs(clientList):
    connected_ips = []
    for client in clientList:
        connected_ips.append(client.client_ip)
    return connected_ips

# Busca pelo arquivo em todos os peers da rede e retorna a lista de peers que o possui ou None caso nenhum possua
def SearchForFile(fileToSearch, clientList):
    ownerPeersList = []
    for client in clientList:
        for file in client.fileStrings:
            if file == fileToSearch:
                 ownerPeersList.append(client)
    return ownerPeersList

def HandleClient(client, clientList, bufferSize):
    while True:
        # Recebe a requisição do cliente
        request = client.client_socket.recv(bufferSize).decode()

        print("O request é o seguinte:", request)

        if not request:
            # Se não houver mais dados recebidos, o cliente encerrou a conexão
            print("Conexão encerrada com o cliente:", client.client_ip)
            break

        # Verifica o tipo de requisição
        if request.startswith("JOIN"):
            HandleJoinRequest(client, request)
            print("Lista de arquivos do novo cliente:", client.fileStrings)
            print("IPs dos clientes conectados:", GetConnectedIPs(clientList))

        elif request.startswith("SEARCH"):
            HandleSearchRequest(clientList, request)

        else:
            pass  # Inserir outras requisições aqui

def RunServer():
    localPort = 5000
    bufferSize = 1024
    clientList = []

    # Cria um socket TCP
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faz o bind de endereço IP e porta
    tcp_server_socket.bind(('', localPort))
    tcp_server_socket.listen()

    print("Servidor TCP aguardando conexões...")

    def AcceptClients():
        while True:
            client_socket, client_address = tcp_server_socket.accept()
            new_client = Client(client_socket, client_address)
            clientList.append(new_client)

            print("Conexão estabelecida com o cliente:", client_address)

            # Inicia uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target = HandleClient, args=(new_client, clientList, bufferSize))
            client_thread.start()

    accept_thread = threading.Thread(target = AcceptClients)
    accept_thread.start()

    # Aguarda a thread de aceitação de clientes finalizar (isso não deve acontecer a menos que ocorra algum erro)
    accept_thread.join()

    # Fecha os sockets dos clientes
    for client in clientList:
        client.client_socket.close()

    # Fecha o socket do servidor
    tcp_server_socket.close()


RunServer()
