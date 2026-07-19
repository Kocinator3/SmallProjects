import socket
import threading

# server settings
HOST = "0.0.0.0"
PORT = 5555
clients = []
names = {"[SERVER]":[0,0]}
adresses = {}

def client_service(client, adress):
    global names, clients
    print("New connection:" + str(adress))
    while True:
        try:
            # waiting for a message
            message = client.recv(1024)
            if not message:
                break            
            text = message.decode("utf-8")
            words = text.split(" ")
            name = words[0][:-1]
            if "|" in name:
                whispering_to = name.split("|")[1]
                name = name.split("|")[0]
            if name in names:
                if adress != names[name][0]:
                    client.send("[SERVER]: Your name is used by someone else choose different using /name NEW_NAME\n".encode("utf-8"))
                    continue
            else:
                if adress in adresses:
                    del names[adresses[adress]]
                    del adresses[adress]
                names[name]=[adress,client]
                adresses[adress]= name
            if "|" in text.split(" ")[0]:
                message = (str(name) + " is whispering to you" + text[len(name) + len(whispering_to) + 1:]).encode("utf-8")
                if whispering_to != "[SERVER]":
                    names[whispering_to][1].send(message)
                else: print(message.decode("utf-8"))
            else:
                # sending message to others
                for k in clients:
                    if k != client:
                        try:
                            k.send(message)
                        except:
                            pass
        except:
            del names[adresses[adress]]
            del adresses[adress]
            break
            
    if client in clients:
        clients.remove(client)
    client.close() 
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