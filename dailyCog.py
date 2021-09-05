import discord
from discord.ext import commands
import random
import database as db

database_ = db.Database()

class Daily(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("daily Cog ready")
  
  @commands.command(name="daily",aliases=['Daily','DAily'])
  async def daily(self,message, help_type="None"):
    channels = ["vocab-track"]
    if message.channel.name in channels:
      for i in range(5):
        word,meaning,example = database_.sendWords(str(message.author.guild.id))
        
        embed = discord.Embed(title=f'{word}',color=0x00ff00)
        embed.add_field(name="Meaning",value=f"{meaning}")
        embed.add_field(name="Example",value=f"{example}", inline=True)
        await message.channel.send(embed=embed)
      role = discord.utils.get(message.guild.roles, name="vocab")
      await message.channel.send(f"{role.mention}")
      
def setup(client):
  client.add_cog(Daily(client))
      

	


# word,example = sendTestWords(serverID)

# userInput= 0 #

