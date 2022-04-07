import socket
import sys
import threading
import sqlite3

# DB connection
conn = sqlite3.connect('messages.db')
#DB cursor
cur = conn.cursor()

#create a table for storing data if it doesn't exist yet 
cur.execute("""CREATE TABLE IF NOT EXISTS messages(
            client1 INT ,
            client2 INT,
            message TEXT,
            message_number INT PRIMARY KEY);
            """)
conn.commit()

# connect to rendezvous
rendezvous = ('52.170.57.76', 55555)
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))
sock.close()

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True)
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    message_no = 0
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))
    #push message sent to db
    #create tuple to hold values that will be saved to db 
    message = (ip, ip, msg, message_no)
    cur.execute("""INSERT INTO messages 
    VALUES(?, ?, ?, ?);""", message)
    conn.commit()
    message_no = message_no + 1

    