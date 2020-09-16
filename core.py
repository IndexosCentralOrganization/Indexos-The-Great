import discord
import DB.manageDB as mdb
from discord.ext import commands
from os import remove as rm
from os import urandom as urand
import datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Crypto.Cipher import AES
import subprocess
import json


# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = commands.Bot(command_prefix="{0}".format(PREFIX))
NONE = open("help/cogs.txt", "w")
NONE = open("help/help.txt", "w")

client.remove_command("help")


# crypto
def cryptBackup(fileBackupDb):
    """
    Encrypt the backup file and generate the decrypt key file
    params : backup file
    """
    # init variables
    key = urand(16)
    date = dt.datetime.now()
    DATE = "{}-{}-{}".format(str(date.day), str(date.month), str(date.year))

    # prepare Cipher
    cipher = AES.new(key, AES.MODE_EAX)
    nonce =  cipher.nonce
    nonceF = open("noncefile.txt", "wb")
    nonceF.write(nonce)

    # encrypt the sql file
    fileSql = open(fileBackupDb, "r")
    data = fileSql.read()
    dataf = bytes(data, 'utf-8')
    ciphertext, tag = cipher.encrypt_and_digest(dataf)
    file = open("backup{}.sql".format(DATE), "wb")
    file.write(ciphertext)
    file.close()

    # generate key file
    keyF = open("backUpKey{}.k".format(DATE), "wb")
    keyF.write(key)
    keyF.close()

    return file.name, keyF.name, nonceF.name


async def backup():
    date = dt.datetime.now()
    DATE = "{}-{}-{}".format(str(date.day), str(date.month), str(date.year))
    channel = client.get_channel(728749737968271500)  # ID du chan "backup"
    await channel.send("Backup du {}".format(DATE))
    fp = mdb.dumpAllDB()
    res = cryptBackup(fp)

    backupCryptedFile = open(res[0], "rb")
    keyFile = open(res[1], "rb")
    nonceFile = open(res[2], "rb")

    output = subprocess.getoutput("curl -F \"file=@{}\" https://api.anonfiles.com/upload".format(backupCryptedFile.name))
    parseN = output.count("\n")
    data = output.split("\n")
    dataF = json.loads(data[parseN])

    await channel.send("** You can download todays backup through this link and the key file to decrypt it! **")
    await channel.send(dataF['data']['file']['url']['full'])
    fileD = discord.File(keyFile, "backupKeyFile{}.k".format(DATE))
    fileN = discord.File(nonceFile, "nonceFile-{}.txt".format(DATE))
    await channel.send(file=fileD)
    await channel.send(file=fileN)
    await channel.send("**=============**")
    rm(fp)
    rm(nonceFile.name)
    rm(backupCryptedFile.name)
    rm(keyFile.name)

scheduler = AsyncIOScheduler()
scheduler.add_job(backup, 'cron', day='*')
scheduler.start()


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

    print("Indexos is ready to index stuff !")

# client.load_extension('commands')
client.load_extension('commands.lien')
client.load_extension('commands.synonyme')
client.load_extension('commands.tag')
client.load_extension('commands.event')
client.load_extension('help.help')

try:
    client.run(TOKEN)
except (KeyboardInterrupt, SystemExit):
    quit()
