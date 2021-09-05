import discord
from discord.ext import commands
import random
import database as db
import operations as op

database_ = db.Database()

class Test(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("test cog ready")
  
  @commands.command(name="test",aliases=['Test','TEst'])
  async def daily(self,message, help_type="None"):
    self.word,self.example = database_.sendTestWord(str(message.guild.id))
    channels = ["vocab-track"]
    role = discord.utils.get(message.guild.roles, name="vocab")
    for member in message.guild.members:
      if role in member.roles:
        await member.send(f"""Welcome to Vocabot Test. Please build a sentence with word as {self.word} """)

  @commands.Cog.listener()
  async def on_message(self,message):
    if isinstance(message.channel,discord.channel.DMChannel) and message.author.name != "VocabBot":
      msg =  op.dataProcess(str(message.content),self.example)
      await message.author.send(msg)
      
def setup(client):
  client.add_cog(Test(client))
      