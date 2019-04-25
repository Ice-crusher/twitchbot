import config
import datamanager
import urllib.request

import socket
import json
import time
import threading
import re
from time import sleep


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHANNEL, message).encode("utf-8"))


def ban(sock, user):
    mess(sock, ".ban {}".format(user))


def timeout(sock, user, seconds=500):
    mess(sock, ".timeout {} {}".format(user, seconds))


def fillOpList():
    while True:
        try:
            url = "https://tmi.twitch.tv/group/user/{}/chatters".format(config.CHANNEL)
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            res = urllib.request.urlopen(req).read().decode("utf-8")
            if res.find("502 bad gateway") == - 1:
                config.oplist.clear()
                data = json.loads(res)
                for p in data["chatters"]["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.oplist[p] = "staff"
        except:
            print("Url catch error!")
    sleep(5)


def isOp(user):
    return user in config.oplist

def getUsersFromString(users): #@name @name;
    list = re.findall(r"@\w+", users)
    return list


