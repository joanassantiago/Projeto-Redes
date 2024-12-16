import socket
import threading
import signal
import sys
import random

def signal_handler(sig, frame):
    print('\nServer shutting down!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

def handle_client_connection(client_socket, address): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_socket.send("What is your name?\n".encode())
    p_name=client_socket.recv(1024).decode()
    try:
        while True:  # Loop to allow multiple games
            tries = 0
            random_n = random.randint(1, 50)
            client_socket.send("Guess a number between 1 and 50:\n".encode())
            
            while True:  # Single game loop
                request = client_socket.recv(1024)
                if not request:
                    print('Client {} disconnected.'.format(address))
                    client_socket.close()
                    return
                
                g_num = int(request.decode())
                if g_num < random_n:
                    tries += 1
                    client_socket.send("Guess higher!\n".encode())
                elif g_num > random_n:
                    tries += 1
                    client_socket.send("Guess lower!\n".encode())
                else:
                    tries += 1
                    client_socket.send(f"YOU WON!! You guessed the number in {tries} tries.\n".encode())
                    print("Player name: {}, IP address: {}, Port: {}, N of tries: {}".format(p_name,address[0],address[1],tries))
                    break  # Exit the single game loop
            
            # Ask if the player wants to play again
            client_socket.send("Do you want to play again? (yes/no):\n".encode())
            response = client_socket.recv(1024).decode().strip().lower()
            if response != 'yes':
                client_socket.send("Goodbye!\n".encode())
                client_socket.close()
                print('Client {}, exited the game.'.format(address))
                
                return

    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))
        client_socket.close()

ip_addr = "203.107.191.250"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, tcp_port))
server.listen(5)  # Max backlog of connections

print('Listening on {}:{}'.format(ip_addr, tcp_port))

while True:
    client_sock, address = server.accept()
    client_handler = threading.Thread(target=handle_client_connection, args=(client_sock, address), daemon=True)
    client_handler.start()

