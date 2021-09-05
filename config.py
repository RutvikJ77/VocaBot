import pymongo
import os 
class Oauth():

  def init(self):
    self.TOKEN =os.environ["TOKEN"]
    self.OWNER_IDS = os.environ["OWNER_IDS"]

    self.API_TOKEN = os.environ["API_TOKEN"]
    #database token
    self.db_link =os.environ["db_link"]
    self.client = pymongo.MongoClient(self.db_link)



  def discordTOKEN(self):
    return self.TOKEN , self.OWNER_IDS

  def databaseTOKEN(self):
    return self.client
  def checkerTOKEN(self):
    return self.API_TOKEN