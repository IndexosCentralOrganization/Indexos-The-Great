import discord
import DB.manageDB as mdb
from discord.ext import commands
from discord.ext.commands import Bot
import apscheduler as sc
from os import remove as rm
import DB.manageDB as mdb
import datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# initialisation des variables.
DEFAUT_PREFIX = "!"

date = dt.datetime.now()
DATE = "{}-{}-{}".format(str(date.day), str(date.month), str(date.year))
VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = commands.Bot(command_prefix="{0}".format(PREFIX))
NONE = open("help/cogs.txt", "w")
NONE = open("help/help.txt", "w")

client.remove_command("help")

async def backup():
    channel = client.get_channel(728749737968271500)  # ID du chan "backup"
    await channel.send("Backup du {}".format(DATE))
    fp = mdb.dumpAllDB()
    fileD = discord.File(fp, "backup{}.sql".format(DATE))
    await channel.send(file=fileD)
    rm(fp)
    await channel.send("**=============**")

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

    scheduler = AsyncIOScheduler()
    scheduler.add_job(backup, 'interval', hours=24)
    scheduler.start()
    print("Indexos is ready for index stuff !")

client.load_extension('commands')
client.load_extension('help.help')

try:
    client.run(TOKEN)
except (KeyboardInterrupt, SystemExit):
    quit()
