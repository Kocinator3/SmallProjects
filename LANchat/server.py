import socket
import threading

# server settings
HOST = "0.0.0.0"
PORT = 5555
clients = []

def client_service(client, adress):
    print("New connection:" + str(adress))
    while True:
        try:
            # waiting for a message
            message = client.recv(1024)
            if not message:
                break # Pokud přijde prázdná zpráva, klient se odpojil
            
            # Musíme byty dekódovat na text, abychom mohli kontrolovat formát
            text = message.decode("utf-8")
            words = text.split(" ")
            
            # checking whisper
            if "|" in words[0]:
                whispering_to = words[0].split("|")[1]
                # Tady pak dopíšeš logiku šeptání...
                
            else: 
                # sending message to others
                for k in clients:
                    # Chceme poslat zprávu všem OSTATNÍM, ne sami sobě
                    if k != client:
                        try:
                            # Posíláme originální zprávu (už je v bytech)
                            k.send(message)
                        except:
                            pass
        except:
            # Pokud nastane jakákoliv chyba (klient spadne), přerušíme cyklus
            break
            
    # cleaning - Odsazeno MIMO cyklus while True!
    if client in clients:
        clients.remove(client)
    client.close()  # Byla tu chyba "clients.close()"
    print("Lost connection with:" + str(adress))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
          
print("Server is running on port " + str(PORT) + " and is waiting for a connection.")

while True:
    client, adress = server.accept()
    clients.append(client)
    thread = threading.Thread(target=client_service, args=(client, adress))
    thread.start()