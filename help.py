import discord
import logging as logger
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    logger.info("Help cog ready")

  @commands.command(name="help",aliases=['Help', 'HElp', 'HELp', 'HELP', 'hELP', 'heLP', 'helP', 'HeLp', 'hElP'])
  async def help(self,message,help_type=None):
    channels=['events-schedule']
    prefix ="reg "
    if message.channel.name in channels:
      if help_type is None:
        embed = discord.Embed(title="Bot Commands List", description="we have some really amazing commands")
        embed.add_field(name=':regional_indicator_c: Daily', value=f"`{prefix}help Daily`", inline=True)
        embed.add_field(name=':x: Test', value=f"`{prefix}help Test`", inline=True)
        await message.channel.send(embed=embed)
      elif help_type.upper()=='DAILY':
        embed = discord.Embed(title=":regional_indicator_c: Daily",description=f'You can send daily words using command',colour=0x00ff00)
        await message.channel.send(embed=embed)
			
def setup(client):
  client.add_cog(Help(client))