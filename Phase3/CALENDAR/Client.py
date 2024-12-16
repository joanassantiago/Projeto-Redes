import socket
import signal
import sys

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

##

ip_addr = sys.argv[1]
tcp_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

while True:
    try: 
        response = sock.recv(4096).decode()
        if len(response)>1:
             print('Server : {}'.format(response))
             s_mess=input().encode()
             sock.send(s_mess)
       
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)


