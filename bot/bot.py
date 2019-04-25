import config
import utils
import datamanager

import socket
import re
import random
import time
from _thread import start_new_thread
from time import sleep


def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASSWORD).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICKNAME).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHANNEL).encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    #utils.mess(s, ":)")
    if not datamanager.checkDataFileExist():
        datamanager.initEmptyFileData()

    start_new_thread(utils.fillOpList, ())
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            print('User: ' + username + "   _   Text: " + message)

            newMessageFromChat(s, username, message)

        sleep(1)

def newMessageFromChat(s, username, message): #s = socket
    # add command like !time
    if message.strip() == "!armletmetr":
        utils.mess(s, "Твой армлет: " + str(random.randint(8, 25)) + " см длинной SeemsGood ")

    if (message.strip() == "!time"):
        utils.mess(s, "У меня сейчас " + time.strftime('%d/%m/%Y %H:%M:%S'))

    if (message.strip() == "!botinfo"):
        utils.mess(s, 'Личный аниме бот 02, ня')

    if (message.strip() == "!девочка"):
        utils.mess(s, 'https://www.youtube.com/watch?v=Kkgu4lgv3HM')

    if ("!addgood" in message.strip()):
        users = utils.getUsersFromString(message.strip())
        datamanager.addToGoodPerson(users)

    if ("!deletegood" in message.strip()):
        users = utils.getUsersFromString(message.strip())
        datamanager.deleteFromGoodPerson(users)

    if ("!goodpersons" in message.strip()):
        users = datamanager.getListFromJson(datamanager.GOODPERSONS)
        if (len(users) == 0):
            utils.mess(s, "К сожалению, на этом стриме ещё нет хороших людей")
        else:
            utils.mess(s, "Список норм челов: " + ' '.join(users))

    if ("!addfagot" in message.strip()):
        users = utils.getUsersFromString(message.strip())
        datamanager.addToFagotPerson(users)

    if ("!deletefagot" in message.strip()):
        users = utils.getUsersFromString(message.strip())
        datamanager.deleteFromFagotPerson(users)

    if ("!fagotpersons" in message.strip()):
        users = datamanager.getListFromJson(datamanager.FAGOTPERSONS)
        if (len(users) == 0):
            utils.mess(s, "К сожалению, на этом стриме ещё нет плохих людей")
        else:
            utils.mess(s, "Список уебанов: " + ' '.join(users))

    if (message.strip() == "!help"):
        string = "Мой хозяин (извращенец) научил меня только этому: "
        string += " ".join(["!armletmetr", "!time", "!addgood", "!deletegood", "!goodpersons",
                            "!addfagot", "!deletefagot", "!fagotpersons"])
        utils.mess(s, string)

    # if (message.strip() == "!oplist"):
    #     utils.mess(s, config.oplist)

if __name__ == "__main__":
    main()