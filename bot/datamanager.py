import config
import json

import os
GOODPERSONS = "goodpersons"
FAGOTPERSONS = "fagotpersons"

projectPath = os.path.abspath(os.path.dirname(__file__))

fileName = projectPath + "\\data" "\\data_{}.json".format(config.CHANNEL)

def addToGoodPerson(nicknames):
    writeToJson(GOODPERSONS, nicknames)

def addToFagotPerson(nicknames):
    writeToJson(FAGOTPERSONS, nicknames)


def deleteFromGoodPerson(nicknames):
    try:
        deleteFromJson(GOODPERSONS, nicknames)
    except:
        print("Error delete from GoodPerson")

def deleteFromFagotPerson(nicknames):
    try:
        deleteFromJson(FAGOTPERSONS, nicknames)
    except:
        print("Error delete from FagotPerson")

def writeToJson(listName, listUsers):
    with open(fileName, 'r+') as outfile:
        data = json.load(outfile)

        data[listName].extend(listUsers)
        data[listName] = list(set(data[listName]))
        outfile.seek(0)
        outfile.truncate()
        json.dump(data, outfile, indent=4)

def deleteFromJson(listName, listUsers):
    with open(fileName, 'r+') as outfile:
        try:
            data = json.load(outfile)
        except json.decoder.JSONDecodeError:
            return

        try:
            for user in listUsers:
                data[listName].remove(user)
        except:
            pass

        outfile.seek(0)
        outfile.truncate()
        json.dump(data, outfile, indent=4)

def getListFromJson(listName):
    result = []
    with open(fileName, 'r') as outfile:
        try:
            data = json.load(outfile)
        except json.decoder.JSONDecodeError:
            return result

        result = data[listName]
    return result

def initEmptyFileData():
    data = {}
    data[GOODPERSONS] = []
    data[FAGOTPERSONS] = []
    with open(fileName, 'w+') as outfile:
        json.dump(data, outfile, indent=4)

def checkDataFileExist():
    with open(fileName, 'w+') as outfile:
        try:
            data = json.load(outfile)
            return True
        except json.decoder.JSONDecodeError:
            return False
