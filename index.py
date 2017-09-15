# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#

# importacao das bibliotecas
import socket

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# mantem o socket ativo mesmo apos a conexao ser encerrada (faz o reuso do endereco do servidor)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ("Serving HTTP on port %s ..." % PORT)

# declaracao das respostas do servidor
fileDoc = open('doc.html')
htmlDoc = "HTTP/1.1 200 OK \r\n\r\n%s\r\n" % fileDoc.read()
file200 = open('200.html')
html200 = "HTTP/1.1 200 OK \r\n\r\n%s\r\n" % file200.read()
file400 = open('400.html')
html400 = "HTTP/1.1 400 Bad Request \r\n\r\n%s\r\n" % file400.read()
file404 = open('404.html')
html404 = "HTTP/1.1 404 Not Found \r\n\r\n%s\r\n" % file404.read()

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket e converte em string
    request = client_connection.recv(1024).decode()
    # pega metodo e rota que o cliente enviou ao servidor
    metodo = request.split(' ')[0]
    rota = request.split(' ')[1]
    # imprime na tela o que o cliente enviou ao servidor
    print ("Nova requisicao de %s: %s %s" % (client_address, metodo, rota))
    # retorno padrão para o cliente caso não satisfaça nenhuma condicao
    res = html400
    if metodo.lower() == 'get':
        if rota.lower() == '/' or rota.lower() == '/index.html':
            res = html200
        elif rota.lower() == '/doc' or rota.lower() == '/doc/' or rota.lower() == '/doc/index.html':
            res = htmlDoc
        else:
            res = html404
    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(res.encode())
    # encerra a conexao
    client_connection.close()