import socket
import os
import random

ServerAddress = '127.0.0.1'
Port = 5000
bufferSize = 1024

def getFilesInDirectory(directory):
    fileNames = [filename for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
    return fileNames

def ChoseOwnerPeer(search_results):
    random_index = random.randint(0, len(search_results) - 1) #Escolhe peer aleatorio dentre a lista de peers que possuem o arquivo
    return search_results[random_index]


def MakeDownloadRequest(client, fileToBeDownloaded, selectedOwnerPeer):
    downloadRequest = f"DOWNLOAD;{fileToBeDownloaded}"
    client.send(downloadRequest.encode())
    response = client.recv(bufferSize).decode()

    



def StartConnection():
    # Cria um socket TCP
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faz a conexão com o servidor
    TCPClientSocket.connect((ServerAddress, Port))

    # Informações do peer que está se juntando à rede
    fileNames = getFilesInDirectory("Files")

    # Monta a requisição JOIN com os dados do cliente
    print(fileNames)
    join_request = f"JOIN;{fileNames}"

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

                # Monta a requisição SEARCH com a consulta do cliente
                search_request = f"SEARCH;{search_query}"

                # Envia a requisição SEARCH ao servidor
                TCPClientSocket.send(search_request.encode())

                # Recebe a resposta do servidor
                search_results = TCPClientSocket.recv(bufferSize).decode()

                # Imprime os resultados da busca
                print("Resultados da busca:", search_results)

                #Escolhe o peer ao qual pedirá o arquivo
                selectedOwnerPeer = ChoseOwnerPeer()

                #opções de ações
                print("Opções:")
                print("Solicitar download do arquivo?")
                print("1. Sim")
                print("2. Não")
                
                option = input("Digite o número da opção desejada: ")
                if(option == "1"):   
                    MakeDownloadRequest(TCPClientSocket, search_query, selectedOwnerPeer)
                


            elif option == "2":
                break

    else:
        print("Conexão não aprovada. Peer não foi adicionado à rede.")

    # Fecha o socket do cliente
    TCPClientSocket.close()

StartConnection()