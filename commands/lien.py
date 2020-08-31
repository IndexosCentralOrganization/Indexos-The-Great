import discord
import validators as val
import DB.manageDB as mdb
from discord.ext import commands
from discord.ext.commands import bot
from os import remove as rm


class LienCommands(commands.Cog):
    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def Ladd(self, ctx, link, *tags):
        """
        params :
        link -> lien
        tag1/2/3 -> Les trois tags
        """
        msg = ""
        authID = ctx.author.id
        chanName = ctx.channel.name

        for tag in tags:
            tag = tag.lower()

        if val.url(link):
            # Cas où ça marche
            if tags:
                msg = "Lien ajouté avec les tags :"
                for tag in tags:
                    tag_tmp = mdb.searchSynonymeByPrimKey(tag)
                    if tag_tmp:
                        tag = tag_tmp[0][2]
                    
                    msg =+ " " + tag
            else:
                msg = "Lien ajouté sans tag"
            if not mdb.addLien(link, chanName, "??", authID):
                msg = "Le lien existe déjà dans la base de donnée ou une erreur a eu lieu."
        else:
            "Le lien n'est pas conforme"

        await ctx.channel.send(msg)

def setup(bot):
    bot.add_cog(LienCommands(bot))
