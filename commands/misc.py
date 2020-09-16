from discord.ext import commands
import discord
import DB.manageDB as mdb
from os import remove as rm


class MiscCommands(commands.Cog):
    def __init__(self, ctx):
        pass

    @commands.command(pass_context=True)
    async def github(self, ctx):
        await ctx.channel.send("Github du projet : https://github.com/gnouf1/Indexos-The-Great")

    @commands.command(pass_context=True)
    async def version(self, ctx):
        F = open("core/version.txt","r")
        v = F.read()
        await ctx.channel.send("Version : **{}**".format(v))

    @commands.command(pass_context=True)
    async def DBdump(self, ctx):
        await ctx.author.send("Création du fichier...")
        fp = mdb.dumpAllDB()
        fileD = discord.File(fp, "dump_file.sql")
        await ctx.author.send(file=fileD)
        rm(fp)
        await ctx.channel.send("Fichier envoyé")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
