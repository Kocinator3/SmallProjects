import socket
import threading
import sys

def message_receiving(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if not message:
                break
            # prints received message
            print(f"\n{message}")
        except:
            print("\nConnection with server was lost.")
            sock.close()
            break
        
# Client settings
only_one = False

SERVER_IP = input("Your Server IP Adress: ")
PORT = input("Your Server Port: ")
while not only_one:
    NAME = input("Your Name: ")
    if " " in NAME:
        print("\nYou cannot use spaces, write it again.\n")
    else:
        only_one = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((SERVER_IP, int(PORT)))
    print("\nConnection to server was succesful! for help write /help\n")
except Exception as e:
    print(f"An error accured: {e}")
    sys.exit()

receiving_thread = threading.Thread(target=message_receiving, args=(client,))
receiving_thread.daemon = True
receiving_thread.start()

client.send((f"{NAME}|[SERVER]: testing name").encode("utf-8"))

# main cycle
while True:
    try:
        text = input()
        if not text.strip():
            continue
        
        words = text.split(" ")
        
        if text.lower() == "/quit":
            client.close()
            break
        elif text.lower() == "/help":
            print("\nto quit \t/quit\nto whisper something to someone \t/whisper NAME MESSAGE\nto see this dialog \t/help\nto set new name \t/name NEW_NAME\n")
            continue
        elif text.startswith("/whisper"):
            if len(words) >= 3:
                relNAME = str(NAME) + "|" + str(words[1])
                first = len(words[0]) + len(words[1]) + 2
                relText = 	text[first:]
            else:
                print("[SERVER]: Incorrect formate. /whisper NAME MESSAGE")
                continue
        elif text.startswith("/name"):
            if len(words) > 2:
                print("[SERVER]: You cannot use spaces in your name")
                continue
            elif len(words) == 1:
                print("[SERVER]: Incorrect formate. /name NEW_NAME")
                continue
            NAME = words[1].encode("utf-8").decode("unicode_escape")
            client.send((f"{NAME}|[SERVER]: testing name").encode("utf-8"))
            continue
        else:
            relNAME = NAME
            relText = text
        
        message = f"{relNAME}: {relText}"
        client.send(message.encode("utf-8"))
    except KeyboardInterrupt:
        client.close()
        break