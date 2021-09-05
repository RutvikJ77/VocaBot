import random
import pymongo
import string
import requests
import config

clientObj = config.Oauth()
client = clientObj.databaseTOKEN()


class Database():
  
  def __init__(self):
    self.dataBase = client["serverData"]
  

  def addServerInfo(self,serverID, serverName, textChannels, roles):
    #to add all the serverinfo when the bot is addded to the server for 1st time
    self.serverInfo = self.dataBase['serverInfo']
    serverData = {
        "server_id": serverID,
        "server_name": serverName,
        "text_channels": textChannels,
        "roles": roles,
        
    }
    self.serverInfo.insert_one(serverData)
    
    # self.serverCollection = self.createCollection(serverID)

  def removeServerInfo(serverID):
    #to delete all server info when the bot is kicked from the server
    
    client.drop_dataBase(serverID)


  def storeWords(self,serverID,wordList):
    word= self.dataBase[serverID]
  
    for words in wordList:
      link = "https://api.dictionaryapi.dev/api/v2/entries/en/" + words
      wordData = requests.get(link).json()
      #print(wordData)
      try:
        wordDataToAdd = {
          "word":words,
          "definition":wordData[0]["meanings"][0]["definitions"][0]["definition"],
          "example":wordData[0]["meanings"][0]["definitions"][0]["example"],
          "screened":False
        }
        word.insert_one(wordDataToAdd)
      except:
        pass
    
      
      
  def sendWords(self,serverID):
    word = self.dataBase[serverID]
    data = word.find({"screened":False})
    #all non displayed words
    total = data.count()
    #count
    randomNumber = random.randint(0, total-1)
    selectedWord = data[randomNumber]
    id = selectedWord["_id"]
    word.update_one({"_id": id}, {"$set": {"screened": True}})
    return selectedWord["word"] , selectedWord["definition"] , selectedWord["example"]
    
  def sendTestWord(self,serverID):
    word = self.dataBase[serverID]
    data = word.find({"screened":True})
    #all displayed words
    total = data.count() #count
    randomNumber = random.randint(0, total-1)
    selectedWord = data[randomNumber]
    id = selectedWord["_id"]
    word.update_one({"_id": id}, {"$set": {"test": True}})
    return selectedWord["word"] , selectedWord["example"]                      