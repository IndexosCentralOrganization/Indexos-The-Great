import discord
import validators as val
import DB.manageDB as mdb
from discord.ext import commands
from discord.ext.commands import bot

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
            mdb.addLink(link, authID, chanName, tag1, tag2, tag3)
        else:
            msg = "Le lien n'est pas conforme"

        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def Ldel(self, ctx, link):
        if mdb.deleteLink(link, ctx.author.id):
            await ctx.channel.send("Lien supprime")
        else:
            await ctx.channel.send("Le lien n'a pas pu être supprime")

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
        msg = "**Les {} tags les plus utilisés sont :**\n".format(str(nb))
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
        # Reverse car il classe en croissant.
        # res devient une liste
        res = sorted(res.items(), key=lambda x: x[1], reverse=True)

        for i in range(0, nb):
            msg += "**{}.** {} ({})\n".format(str(i+1), res[i][0], res[i][1])

        await ctx.channel.send(msg)





def setup(bot):
    bot.add_cog(BaseCommands(bot))
    open("help/cogs.txt", "a").write("BaseCommands\n")
