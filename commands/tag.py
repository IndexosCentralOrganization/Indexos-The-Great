import DB.manageDB as mdb
from discord.ext import commands
import discord
import wikipedia as wiki

wiki.set_lang("fr")


class tagCommands(commands.Cog):
    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def toptag(self, ctx, nb=10):
        resList = mdb.colOccurence("tag_value", "tagmap")
        msg = ""
        if resList:
            if nb > len(resList) or nb == -1:
                nb = len(resList)
            resList.sort(key=lambda x: x[1], reverse=True)
        # Mesure anti flood
            if nb <= 10:
                for i in range(0, nb):
                    msg += "**{}.** {} ({})\n".format(str(i+1), resList[i][0], resList[i][1])

                await ctx.channel.send(msg)
            else:
                for i in range(0, nb):
                    msg += "**{}.** {} ({})\n".format(str(i+1), resList[i][0], resList[i][1])
                    if i % 50 == 0 and i != 0:
                        await ctx.author.send(msg)
                        msg = ""
                await ctx.author.send(msg)
        else:
            await ctx.channel.send("Il n'y pas de tags")

    @commands.command(pass_context=True)
    async def infotag(self, ctx, tag):
        flag = 0
        dataTag = mdb.searchTagByPrimKey(tag)[0]
        name = dataTag[0]
        desc = dataTag[1]
        auth = dataTag[2]
        # updater = ctx.author.id

        if desc == "":
            desc_wiki = ""
            try:
                desc_wiki = "[issu de wikipedia] " + wiki.summary(tag, sentences=3)
                mdb.updateItem("tag", "value", tag, "description", desc_wiki)
                flag = 1
            except wiki.exceptions.DisambiguationError:
                flag = 0

        if flag:
            desc_ = "Ajouté par : <@{0}> \n\n **==========**\n***DESCRIPTION***\n**==========**\n\n".format(auth) + desc
            msg = discord.Embed(title=name, color=35723, description=desc_)
            await ctx.channel.send(embed=msg)
        else:
            msg = "Il n'y a pas de description sur ce tag ! Ecrivez-en une !"
            await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(tagCommands(bot))
