import discord
from discord.ext import commands
from discord import Color
import os

path = os.path.realpath(__file__).replace('help.py', "")
print(path)

class Helpme(commands.Cog):

    def __init__(self, bot):
        self.PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, nameElem = None):
        """Affiche ce message !"""
        file = open("help/help_command.txt", 'r')
        content = file.read()
        msg = discord.Embed(title="Commandes disponible", color=Color.red(), url="https://github.com/gnouf1/Indexos-The-Great/blob/master/help/help_command.txt", description=content)

        await ctx.channel.send(embed=msg)
        # await ctx.channel.send("**Commandes disponibles*** :\n\n **Ladd :** `Ladd LIEN optTAG1 OPTtag2 OPTtag3`\n Permet d'ajouter un lien avec 0, 1, 2 ou 3 tags.\n\n**Ldel :** `Ldel LIEN `\n Permet de supprimer un lien **SI ON EST L'AUTEUR DE SON AJOUT**.\n\n**Lsearch :** `Lsearch ITEM`\n Permet de rechercher un lien dont soit un des tags est ITEM ou dont le salon d'origine a pour nom ITEM.\n\n**toptag :** `toptag optx`\n Affiche les x tags les plus utilisés, 10 par défaut.")


def setup(bot):
    bot.add_cog(Helpme(bot))
