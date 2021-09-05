import config as config
import database as db
import discord
from discord.utils import get
from discord.ext import commands
from urllib.request import urlopen, Request
import requests
import dailyCog,testCog
import logging as logger
import operations as op

#import all the config data
dataConfig = config.Oauth()
TOKEN, ownerID = dataConfig.discordTOKEN()
intents = discord.Intents().all()
client = commands.Bot(command_prefix='.',
                      help_command=None,
                      owner_ids=ownerID,intents=intents)

database_ = db.Database()
message=0

cogs = [dailyCog,testCog]

for i in range(len(cogs)):
    cogs[i].setup(client)

  
@client.event
async def on_disconnect():
  logger.info("Bot disconnected.")


@client.event
async def on_guild_join(guild):
  logger.info("Bot connected to Server.")
  # overwrites = {
  #       guild.default_role: discord.PermissionOverwrite(read_messages=False),
  #       guild.owner: discord.PermissionOverwrite(read_messages=True)
  #   }
  channel = await guild.create_text_channel('Vocab Track')
  await guild.create_role(name="vocab", colour=discord.Colour.random())
  embed = discord.Embed(
    title="Welcome to VocabBot",
    description= """ Welcome to VocabBot. Improve your vocabulary while having fun.
  1. Admins should upload the vocabulary words as text file. Note every word should be on a different line and only words are required.
  2. Using the `.Daily` commmand 5 words will be sent in this channel with their meaning and example sentences.
  3. Using `.test` command a test word will be sent to those with `vocab` role.
  4. Those with role will be required to complete a sentence using that word and a score will be displayed.
  5. Hope you have fun while learning with Vocabot.  """,color=0x00ff00)
  message = await channel.send(embed=embed)
  await message.add_reaction('✅')
  # Necessary Arguments
  serverID = str(guild.id)
  serverName = guild.name
  textChannelsList = [channel.name for channel in guild.text_channels]

  rolesList = [role.name for role in guild.roles]
  database_.addServerInfo(serverID,serverName,textChannelsList,rolesList)
  

@client.event
async def on_raw_reaction_add(payload):
  if payload.member.name != "VocabBot":
    member = payload.member
    memberGuild = member.guild
    emoji = payload.emoji.name
    if emoji == "✅":
      role_name = discord.utils.get(memberGuild.roles, name="vocab")
      await member.add_roles(role_name)
      
@client.event
async def on_guild_remove(guild):

  serverId = str(guild.id)
  logger.info("Removed from database")


@client.event
async def on_ready():
  logger.info("Bot ready.")  #Add the server name


@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  if not isinstance(message.channel,discord.channel.DMChannel):
    if message.channel.name == "vocab-track" and not message.content.startswith("."):
      response = Request(message.attachments[0].url, headers={'User-Agent': 'Mozilla/5.0'})
      data = urlopen(response).read()

      # response = urlopen(message.attachments[0].url)
      # data = response.read()
      filename = "words.txt"
      file_ = open(filename, 'w')
      file_.write(str(data, 'UTF-8'))
      file_.close()
      with open('words.txt') as file:
        word_list = file.readlines()
        new_items = [x[:-1] for x in word_list]
        new_items = list(filter(None, new_items))
      database_.storeWords(str(message.author.guild.id),new_items)
      embed = discord.Embed(title="successful",color=0x00ff00)
      await message.channel.send(embed=embed)
      
    
  
  await client.process_commands(message)

client.run(TOKEN)


