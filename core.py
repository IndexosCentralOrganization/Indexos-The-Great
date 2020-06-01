import discord
import DB.manageDB as mdb
from discord.ext import commands
from discord.ext.commands import Bot

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = commands.Bot(command_prefix="{0}".format(PREFIX))
NONE = open("help/cogs.txt", "w")
NONE = open("help/help.txt", "w")

# Au demarrage du Bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    activity = discord.Activity(type=discord.ActivityType.playing, name="Prefix = {0}".format(PREFIX))
    await client.change_presence(status=discord.Status.online, activity=activity)
    if mdb.initDB():
        print("DB Valide")
    else:
        print("DB invalide")
    print("Indexos is ready for index stuff !")

client.load_extension('commands')

try:
    client.run(TOKEN)
except (KeyboardInterrupt, SystemExit):
    quit()
