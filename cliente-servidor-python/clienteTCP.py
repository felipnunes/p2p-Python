import socket

ServerAddress = '127.0.0.1'
Port = 5000
bufferSize = 1024

def StartConnection():
    # Cria um socket TCP
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faz a conexão com o servidor
    TCPClientSocket.connect((ServerAddress, Port))

    # Informações do peer que está se juntando à rede
    peerID = "Peer1"
    fileNames = "file1.txt;file2.txt;file3.txt"

    # Monta a requisição JOIN com os dados do cliente
    join_request = f"JOIN;{peerID};{fileNames}"

    # Envia a requisição JOIN ao servidor
    TCPClientSocket.send(join_request.encode())

    # Recebe a resposta do servidor
    response = TCPClientSocket.recv(bufferSize).decode()

    if response == "JOIN_OK":
        print("Conexão aprovada. Peer foi adicionado à rede.")
        # Continua executando ações dentro do loop
        while True:
            # Opções de ações
            print("Opções:")
            print("1. Realizar busca")
            print("2. Encerrar conexão")

            option = input("Digite o número da opção desejada: ")

            if option == "1":
                search_query = input("Digite os arquivos que deseja buscar (separados por ponto e vírgula): ")
                search_request = f"SEARCH;{search_query}"

                # Envia a requisição SEARCH ao servidor
                TCPClientSocket.send(search_request.encode())

                # Recebe a resposta do servidor
                search_results = TCPClientSocket.recv(bufferSize).decode()
                print("Resultados da busca:", search_results)

            elif option == "2":
                break

    else:
        print("Conexão não aprovada. Peer não foi adicionado à rede.")

    # Fecha o socket do cliente
    TCPClientSocket.close()

StartConnection()
