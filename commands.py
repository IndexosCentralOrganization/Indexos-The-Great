import discord
import validators as val
import DB.manageDB as mdb
from discord.ext import commands
from discord.ext.commands import bot
from os import remove as rm

PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")


class BaseCommands(commands.Cog):
    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def Ladd(self, ctx, link, tag1 = None, tag2 = None, tag3 = None):
        """
        params :
        link -> lien
        tag1/2/3 -> Les trois tags
        """
        msg = ""
        authID = ctx.author.id
        chanName = ctx.channel.name

        if val.url(link):
            # Cas où ça marche
            if tag1 is not None or tag2 is not None or tag3 is not None:
                msg = "Lien ajoute avec les tags :"
                if(tag1):
                    tag1 = tag1.lower()
                    msg += " "+tag1
                if(tag2):
                    tag2 = tag2.lower()
                    msg += " "+tag2
                if(tag3):
                    tag3 = tag3.lower()
                    msg += " "+tag3
            else:
                msg = "Lien ajoute sans tag"
            try:
                mdb.addLink(link, authID, chanName, tag1, tag2, tag3)
            except:
                msg = "Le lien existe déjà dans la base de donnée ou une erreur a eu lieu."
        else:
            msg = "Le lien n'est pas conforme"

        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def Ldel(self, ctx, link):
        if mdb.deleteLink(link, ctx.author.id):
            await ctx.channel.send("Lien supprimé")
            await ctx.message.delete()
        else:
            await ctx.channel.send("Le lien n'a pas pu être supprimé")

    @commands.command(pass_context=True)
    async def Lsearch(self, ctx, tag):
        tag = tag.lower()
        reslist = list(set(mdb.searchByTag(tag)) | set(mdb.searchByChan(tag)))
        print(reslist)
        if reslist:
            str = "Liens correspondants à votre recherche :\n"
            for elem in reslist:
                str += "  **>** "+elem[0]+" \n"
        else:
            str = "Aucun lien ne correspond à votre recherche"
        await ctx.channel.send(str)

    @commands.command(pass_context=True)
    async def github(self, ctx):
        await ctx.channel.send("https://github.com/gnouf1/Indexos-The-Great")

    @commands.command(pass_context=True)
    async def toptag(self, ctx, nb=10):
        tag1List = mdb.occurenceInField("tag1")
        tag2List = mdb.occurenceInField("tag2")
        tag3List = mdb.occurenceInField("tag3")

        res = dict()

    # Va ecrire dans res l'ensemble des tags et l'ensemble de leur occurences
        for item in tag1List:
            try:
                res[item[0]] += item[1]
            except KeyError:
                res[item[0]] = item[1]

        for item in tag2List:
            try:
                res[item[0]] += item[1]
            except KeyError:
                res[item[0]] = item[1]

        for item in tag3List:
            try:
                res[item[0]] += item[1]
            except KeyError:
                res[item[0]] = item[1]

        del(res[None])
        if nb > len(res) or nb == -1:
            nb = len(res)

        msg = "**Les {} tags les plus utilisés sont :**\n".format(str(nb))

        # Reverse car il classe en croissant.
        # res devient une liste
        res = sorted(res.items(), key=lambda x: x[1], reverse=True)

        # Mesure anti flood
        if nb <= 10:
            for i in range(0, nb):
                msg += "**{}.** {} ({})\n".format(str(i+1), res[i][0], res[i][1])

            await ctx.channel.send(msg)
        else:
            for i in range(0, nb):
                msg += "**{}.** {} ({})\n".format(str(i+1), res[i][0], res[i][1])
                if i % 50 == 0 and i != 0:
                    await ctx.author.send(msg)
                    msg = ""
            await ctx.author.send(msg)

    @commands.command(pass_context=True)
    async def DBdump(self, ctx):
        await ctx.author.send("Création du fichier...")
        fp = mdb.dumpAllDB()
        fileD = discord.File(fp, "dump_file.sql")
        await ctx.author.send(file=fileD)
        rm(fp)
        await ctx.channel.send("Fichier envoyé")


    @commands.command(pass_context=True)
    async def merge(self, ctx, old, new):
        if len(mdb.searchByTag(old)) != 0 and len(mdb.searchByTag(new)) != 0:
            mdb.changetags(old, new)
            await ctx.channel.send("Les tags *{}* ont été fusionné avec *{}*".format(old, new))
        else:
            await ctx.channel.send("Les tags que vous essayez de fusionner n'existe pas.")

def setup(bot):
    bot.add_cog(BaseCommands(bot))
    open("help/cogs.txt", "a").write("BaseCommands\n")
