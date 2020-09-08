import validators as val
import DB.manageDB as mdb
from discord.ext import commands


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

    #     tag1List = mdb.occurenceInField("tag1")
    #     tag2List = mdb.occurenceInField("tag2")
    #     tag3List = mdb.occurenceInField("tag3")
    #
    #     res = dict()
    #
    # # Va ecrire dans res l'ensemble des tags et l'ensemble de leur occurences
    #     for item in tag1List:
    #         try:
    #             res[item[0]] += item[1]
    #         except KeyError:
    #             res[item[0]] = item[1]
    #
    #     for item in tag2List:
    #         try:
    #             res[item[0]] += item[1]
    #         except KeyError:
    #             res[item[0]] = item[1]
    #
    #     for item in tag3List:
    #         try:
    #             res[item[0]] += item[1]
    #         except KeyError:
    #             res[item[0]] = item[1]
    #
    #     del(res[None])
    #     if nb > len(res) or nb == -1:
    #         nb = len(res)
    #
    #     msg = "**Les {} tags les plus utilisés sont :**\n".format(str(nb))
    #
    #     # Reverse car il classe en croissant.
    #     # res devient une liste
    #     res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    #
    #     # Mesure anti flood
    #     if nb <= 10:
    #         for i in range(0, nb):
    #             msg += "**{}.** {} ({})\n".format(str(i+1), res[i][0], res[i][1])
    #
    #         await ctx.channel.send(msg)
    #     else:
    #         for i in range(0, nb):
    #             msg += "**{}.** {} ({})\n".format(str(i+1), res[i][0], res[i][1])
    #             if i % 50 == 0 and i != 0:
    #                 await ctx.author.send(msg)
    #                 msg = ""
    #         await ctx.author.send(msg)
def setup(bot):
    bot.add_cog(tagCommands(bot))
