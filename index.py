# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# ALUNOS: ISAAC BARBOSA, JUDSON COSTA
#
# SCRIPT: Base de um servidor HTTP (python 3)

# importacao das bibliotecas
import socket
from datetime import datetime

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# Gera resposta do HEAD formatada
def getHead(size, conn):
    return '''
Date: %s
Server: Meu Host /v1 (Redes - UFRN)
Content-Length: %s
Connection: %s
''' % (datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'), size, conn)

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# mantem o socket ativo mesmo apos a conexao ser encerrada (faz o reuso do endereco do servidor)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o 'bind' do servidor com a porta)
listen_socket.bind((HOST, PORT))

# 'escuta' pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print('Serving HTTP on port %s ...' % PORT)

# declaracao das respostas do servidor
fileDoc = open('doc.html', 'r')
htmlDoc = 'HTTP/1.1 200 OK \r\n\r\n%s\r\n' % fileDoc.read()
sizeDoc = fileDoc.tell()
fileDoc.close()
file200 = open('200.html', 'r')
html200 = 'HTTP/1.1 200 OK \r\n\r\n%s\r\n' % file200.read()
size200 = file200.tell()
file200.close()
file400 = open('400.html', 'r')
html400 = 'HTTP/1.1 400 Bad Request \r\n\r\n%s\r\n' % file400.read()
file400.close()
file404 = open('404.html', 'r')
html404 = 'HTTP/1.1 404 Not Found \r\n\r\n%s\r\n' % file404.read()
size404 = file404.tell()
file404.close()

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # guarda todo o texto da requisicao
    data = ''
    # retorno padrao para o cliente caso nao satisfaca nenhuma condicao
    res = html400
    while True:
        # o metodo .recv recebe os dados enviados por um cliente atraves do socket e converte em string
        request = client_connection.recv(1024).decode()
        if request.find('User-Agent') >= 0: # se for navegador
            data = request
            break # nao esperar quebra de linha
        if request == '\r\n': # se deu apenas enter
            if data == '': # se nao escreveu algo antes
                continue
            else: # se ja escreveu algo antes
                break
        else: # se escreveu e deu enter
            data += request
            continue

    # pega metodo, rota e conexao escrito pelo cliente
    metodo = data.split(' ')[0]
    rota = data.split(' ')[1] if len(data.split(' ')) > 1 else ''
    connection = 'keep-alive' if data.find('keep-alive') >= 0 else 'close'

    # imprime na tela o que o cliente enviou ao servidor
    print('Requisicao de %s: Connection(%s); Metodo(%s); Rota(%s)' % (client_address, connection, metodo, rota))

    if rota.lower() == '/' or rota.lower() == '/index.html':
        if metodo.lower() == 'get':
            res = html200
        elif metodo.lower() == 'head':
            res = getHead(size200, connection)
    elif rota.lower() == '/doc' or rota.lower() == '/doc/' or rota.lower() == '/doc/index.html':
        if metodo.lower() == 'get':
            res = htmlDoc
        elif metodo.lower() == 'head':
            res = getHead(sizeDoc, connection)
    else:
        if metodo.lower() == 'get':
            res = html404
        elif metodo.lower() == 'head':
            res = getHead(size404, connection)

    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(res.encode())
    # encerra a conexao
    client_connection.close()
