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
        if val.url(link):
            # Cas où ça marche
            if tag1 is not None or tag2 is not None or tag3 is not None:
                msg = "Lien ajouté avec les tags :"
                if(tag1):
                    msg += " "+tag1
                if(tag2):
                    msg += " "+tag2
                if(tag3):
                    msg += " "+tag3
            else:
                msg = "Lien ajouté sans tag"
            mdb.addLink(link, tag1, tag2, tag3)
        else:
            msg = "Le lien n'est pas conforme"

        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(BaseCommands(bot))
    open("help/cogs.txt", "a").write("BaseCommands\n")
