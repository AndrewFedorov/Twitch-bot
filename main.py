import config
import help_func
import socket
import re
import threading
from time import sleep
from log import Log

def main():
    help_func.DB().createTables()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.HOST, config.PORT))
        s.sendall("PASS {}\r\n".format(config.PASS).encode("utf-8"))
        s.sendall("NICK {}\r\n".format(config.NICK).encode("utf-8"))
        s.sendall("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))

        chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        threading.Thread(target=help_func.fillListOfViewers).start()
        Log().addText('Bot launched')
        while True:
            try:
                response = s.recv(1024).decode("utf-8")
                if response == "PING :tmi.twitch.tv\r\n":
                    s.sendall("POND :tmi.twitch.tv\r\n".encode("utf-8"))
                else:
                    nickname = re.search(r"\w+", response).group(0)
                    message = chat_message.sub("", response)
                    Log().addText(response)
                    if message.find('!bet') != -1:
                        help_func.Bet.make(nickname, message)
                    if message.find('!points') != -1:
                        help_func.sendToTwitch(s, 'Количество очков {0}: {1}'.format(nickname, help_func.DB().getPoints(nickname)))
            except Exception as e:
                Log().addError(str(e))
            sleep(1)