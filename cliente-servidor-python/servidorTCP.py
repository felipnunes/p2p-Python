import socket

class Client:
    def __init__(self, client_socket, client_ip, id):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.id = id
        self.fileStrings = []

def HandleJoinRequest(client, request):
    # Extrai as informações da requisição JOIN do cliente
    join_info = request.split(";")
    file_names = join_info
    
    # Armazena as strings de arquivos do cliente no objeto client
    client.fileStrings = join_info
    # Realiza a lógica de negócio para verificar e aprovar a conexão do cliente


    # Exemplo: sempre aprova a conexão
    response = "JOIN_OK"

    # Envia a resposta ao cliente
    client.client_socket.send(response.encode())

def run_server():
    local_port = 5000
    buffer_size = 1024
    actual_id = 0
    client_list = []

    # Cria um socket TCP
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faz o bind de endereço IP e porta
    tcp_server_socket.bind(('', local_port))
    tcp_server_socket.listen()

    print("Servidor TCP aguardando conexões...")

    while (True):
        client_socket, client_address = tcp_server_socket.accept()
        new_client = Client(client_socket, client_address, actual_id)
        client_list.append(new_client)
        actual_id += 1

        print("Conexão estabelecida com o cliente:", client_address)
        
        # Recebe a requisição do cliente
        request = client_socket.recv(buffer_size).decode()

        # Verifica o tipo de requisição
        if request.startswith("JOIN"):
            HandleJoinRequest(new_client, request)
            print("lista de arquivos do novo cliente = " , new_client.fileStrings)
        else:
            # Lógica para lidar com outras requisições (caso necessário)
            pass
    

    # Fecha os sockets dos clientes
    for client in client_list:
        client.client_socket.close()

    # Fecha o socket do servidor
    tcp_server_socket.close()


run_server()
