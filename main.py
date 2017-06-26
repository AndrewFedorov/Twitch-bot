import config
import bot
import socket
import re
import time
import threading
from time import sleep


def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.HOST, config.PORT))
        s.sendall("PASS {}\r\n".format(config.PASS).encode("utf-8"))
        s.sendall("NICK {}\r\n".format(config.NICK).encode("utf-8"))
        s.sendall("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))

        chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        #bot.mess(s, "start bot")

        threading.Thread(target=bot.fillOpList).start()

        while True:
            response = s.recv(1024).decode("utf-8")
            if response == "PING :tmi.twitch.tv\r\n":
                s.sendall("POND :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                username = re.search(r"\w+", response).group(0)
                message = chat_message.sub("", response)
                print(response)
            
            sleep(3)

if __name__ == "__main__":
    main()