import socket            
import random

options = ['rock', 'paper', 'scissors']
beats = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

def getRandomOption():
    return options[random.randint(0,2)]

def play_round(client_pick):
    server_pick = getRandomOption()
    
    if client_pick == server_pick:
        result = 'Draw'
    elif beats[server_pick] == client_pick:
        result = 'You lost'
    else:
        result = 'You won'
    
    return server_pick, result

s = socket.socket()         
host = socket.gethostname() 
port = 12345               
s.bind((host, port))        
s.listen(5)  

print(f"Server started on {host}:{port}")

while True:
    c, addr = s.accept()     
    print('Got connection from: ', addr)
    
    c.send(b'WANT_TO_PLAY')
    response = c.recv(1024).decode()
    
    if response == 'y':
        c.send(b'START_GAME')
        
        while True:
            client_pick = c.recv(1024).decode()
            server_pick, result = play_round(client_pick)
            
            message = f"OPPONENT_PICK:{server_pick}|RESULT:{result}|PLAY_AGAIN?"
            c.send(message.encode())
            
            play_again = c.recv(1024).decode()
            if play_again != 'y':
                c.send(b'GOODBYE')
                c.close()
                break
    else:
        c.send(b'DECLINED')
        c.close()