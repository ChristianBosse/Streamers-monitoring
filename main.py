from pathlib import Path
import time
import json
import requests
import webbrowser

config = Path('./config.txt')
backupConfig = Path('./config_backup.txt')
version = '1.0.1'

def checkIfFileExists():
    if config.is_file() and backupConfig.is_file():
        return True
    else:
        return False


def createConfig():
    print('Creating config file')
    data = {
        'streamers': [],
        'version': version
    }
    
    with open('config.txt', 'w') as outfile:
        json.dump(data, outfile)
        
    backupData = {
        'streamers': [],
        'version': version
    }
    
    with open('config_backup.txt', 'w') as outfileBackup:
        json.dump(backupData, outfileBackup)


def addToConfig():
    config = loadConfig()
    print('Enter streamers name')
    name = input()
    print('Do you want to enable auto open when streamer goes live? y/n')
    flag = input()
    new_data = {
        'name': name,
        'flag': flag
    }
    config.append(new_data)
    editConfig({'streamers': config, 'version': version})

def loadConfig():
    with open('config_backup.txt', 'r') as file:
        data = json.load(file)
        file_data = data['streamers']
        return file_data

def editConfig(data):
    with open('config_backup.txt', 'w') as file:
        json.dump(data, file, indent=4)

def addNewStreamer():
    print('Do you want to add a new streamer? y/n')
    choice = input()
    
    while True:
        if choice.lower() == 'y':
            addToConfig()
            print('Do you want to add another streamer? y/n')
            choice = input()
        else:
            return False

def removeFromConfig():
    config = loadConfig()
    print('Enter streamers name')
    name = input()
    for streamer in config:
        if streamer['name'] == name:
            config.remove(streamer)
            editConfig({'streamers': config, 'version': version})
            print('Streamer removed')
            break

def removeStreamer():
    print('Do you want to remove a streamer? y/n')
    choice = input()
    
    while True:
        if choice.lower() == 'y':
            removeFromConfig()
            print('Do you want to remove another streamer? y/n')
            choice = input()
        else:
            return False

def openStreamersPage(name):
    webbrowser.open('https://www.twitch.tv/%s' % name, new=2)

def editConfigFlag(data):
    with open('config.txt', 'w') as file:
        json.dump(data, file, indent=4)

def checkIfStreamersOnline():
    with open('config.txt', 'r') as file:
        data = json.load(file)
        file_data = data['streamers']
        for streamer in file_data:
            name = streamer['name']
            response = requests.get('https://decapi.me/twitch/uptime/% s' % name)
            answer = response.text
            if answer == "% s is offline" % name:
                print(answer)
            else:
                print("%s has been live for %s" % (name, answer))
                if streamer['flag'] == 'y':
                    # open once in entire loop
                    openStreamersPage(name)
                    # update flag to n
                    streamer['flag'] = 'n'
                    editConfigFlag({'streamers': file_data, 'version': version})
                    
def createNewConfig():
    data = loadConfig()
    
    newData = {
        'streamers': data,
        'version': version
    }
    
    editConfig(newData)

def checkIfCorrectVersion():
    with open('config_backup.txt', 'r') as file:
        data = json.load(file)
        if "version" not in data:
            print('config is not correct, switching to new version')
            createNewConfig()
        file_data = data["version"]
        if file_data != version:
            print('config is not correct, switching to new version')
            createNewConfig()

while True:
    doesFileExists = checkIfFileExists()
    if doesFileExists:
        checkVersion = checkIfCorrectVersion()
        checkIfFinishAdding = addNewStreamer()
        checkIfFinishRemoving = removeStreamer()
        if checkIfFinishAdding == False:
            break
        if checkIfFinishRemoving == False:
            break
    else:
        createConfig()
    time.sleep(1)

resetConfigWithBackupOnStart = Path('./config.txt').is_file()
if resetConfigWithBackupOnStart:
    with open('config_backup.txt', 'r') as file:
            data = json.load(file)
            with open('config.txt', 'w') as outfile:
                json.dump(data, outfile)

while True:
    checkIfStreamersOnline()
    time.sleep(25)