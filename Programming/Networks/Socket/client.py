import socket               

s = socket.socket()         
host = socket.gethostname() 
port = 12345               

s.connect((host, port))

if s.recv(1024).decode() == 'WANT_TO_PLAY':
    choice = input("Want to play rock, paper, scissors? (y/n): ")
    s.send(choice.encode())
    
    if choice == 'y':
        print(s.recv(1024).decode())
        
        while True:
            client_pick = input("Choose: rock, paper or scissors: ")
            if (client_pick not in ['rock', 'paper', 'scissors']):
                print('Incorrect input!')
                continue
            s.send(client_pick.encode())
            
            response = s.recv(1024).decode()
            if '|' in response:
                parts = response.split('|')
                for part in parts:
                    if part.startswith('OPPONENT_PICK:'):
                        print(f"Opponent picked: {part.split(':')[1]}")
                    elif part.startswith('RESULT:'):
                        print(f"Result: {part.split(':')[1]}")
                
                play_again = input("Play again? (y/n): ")
                s.send(play_again.encode())
                
                if play_again != 'y':
                    print(s.recv(1024).decode())
                    break
    else:
        print(s.recv(1024).decode())

s.close()