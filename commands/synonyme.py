import DB.manageDB as mdb
from discord.ext import commands
import discord


class synonymeCommands(commands.Cog):
    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def merge(self, ctx, old, new):
        auth = ctx.author.id
        tag = mdb.searchTagByPrimKey(old)
        if mdb.existTag(old) and mdb.existTag(new):
            if tag and tag[0][2] == auth:
                newBecomeOld = mdb.simpleItemSearch("synonyme", "new", old)
                if mdb.addSynonyme(auth, old, new):
                    if newBecomeOld:
                        for res in newBecomeOld:
                            mdb.updateItem("synonyme", "old", res[1], "new", new)
                    mdb.updateItem("tagmap", "tag_value", old, "tag_value", new)
                    msg = "Synonyme ajouté."

                else:
                    msg = "Ce synonyme existe déjà."
            else:
                msg = "Vous n'êtes pas l'indexeur du tag a supprimer, contacter <@{}>".format(tag[0][2])
        else:
            msg = "Erreur dans les tags. Au moins l'un des deux n'existe pas."
        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def listSyn(self, ctx):
        i = 0
        list = mdb.allSynonyme()
        msg = "Les synonymes sont :\n"
        for item in list:
            msg += "> {0} -> {1}  *(<@{2}>)*\n".format(item[1], item[2], item[0])
            if i % 20 == 0 and i != 0:
                await ctx.channel.send(msg)
                msg = ""
            i += 1
        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def delSyn(self, ctx, old):
        """
        old -> str : Old du synonyme a supprimer
        """
        if mdb.existSynonyme(old) and mdb.searchSynonymeByPrimKey(old)[0][0] == ctx.author.id:
            mdb.deleteSynonyme(old)
            msg = "Synonyme supprimé"
        else:
            msg = "Ce synonyme n'existe pas ou vous n'êtes pas son indexeur."
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(synonymeCommands(bot))
