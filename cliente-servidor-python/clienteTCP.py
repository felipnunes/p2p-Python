import socket

ServerAddress = '127.0.0.1'
Port = 5000
bufferSize = 1024

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
else:
    print("Conexão não aprovada. Peer não foi adicionado à rede.")

# Fecha o socket do cliente
TCPClientSocket.close()
