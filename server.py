import socket
import re
import time
from struct import unpack


def refreshParse(sock):

    print ('parsing')

    players = {}
    info = {}
    
    for i in range(0, 32):
        players[i] = {}
        nameLength = unpack('B', sock.recv(1))[0]
        players[i]['name'] = sock.recv(nameLength).decode()
        sock.recv(24 - nameLength)

    for i in range(0, 32):
        players[i]['hwid'] = sock.recv(12).decode()

    for i in range(0, 32):
        players[i]['team'] = unpack('B', sock.recv(1))[0]

    for i in range(0, 32):
        players[i]['kills'] = unpack('H', sock.recv(2))[0]

    for i in range(0, 32):
        players[i]['deaths'] = unpack('H', sock.recv(2))[0]

    for i in range(0, 32):
        players[i]['ping'] = unpack('B', sock.recv(1))[0]

    for i in range(0, 32):
        players[i]['id'] = unpack('B', sock.recv(1))[0]

    for i in range(0, 32):
        players[i]['ip'] = '.'.join([str(v) for v in unpack('BBBB', sock.recv(4))])

    info['score'] = {
        'alpha': unpack('H', sock.recv(2))[0],
        'bravo': unpack('H', sock.recv(2))[0],
        'charlie': unpack('H', sock.recv(2))[0],
        'delta': unpack('H', sock.recv(2))[0],
    }

    mapLength = unpack('B', sock.recv(1))[0]
    info['map'] = sock.recv(mapLength)
    sock.recv(16 - mapLength)

    info['timeLimit'] = unpack('i', sock.recv(4))[0]
    info['currentTime'] = unpack('i', sock.recv(4))[0]
    info['killLimit'] = unpack('H', sock.recv(2))[0]
    info['mode'] = unpack('B', sock.recv(1))[0]

    #print ('info: %s' % info)

    info['players'] = players

    #print(info['players'][0])
    for attr, value in info['players'].items():
        print(value) if value['name'] else ''

    return info

pw = 'admin\n'
ip = '192.168.254.136'
port = 23073
buf = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    try:
        data = s.recv(1)
    except Exception as e:
        break

    if not data:
        break

    buf = buf + data.decode()

    if re.search('\r?\n$', buf):
        if buf == 'Soldat Admin Connection Established.\r\n':
            print ('connected')
            s.send(pw.encode())
        elif buf == 'Welcome, you are in command of the server now.\r\n':
            print('authed')
            s.send("REFRESHX\n".encode())
        elif buf == 'REFRESHX\r\n':
            print ('refresh packet inbound')
            info = refreshParse(s)
            #print(info)
        else:
            print (buf)

        buf = ''


s.close()