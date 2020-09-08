import validators as val
import DB.manageDB as mdb
from discord.ext import commands


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

        lienAjoute = bool()

        for tag in tags:
            tag = tag.lower()

        if val.url(link):
            # Cas où ça marche
            lienAjoute = mdb.addLien(link, chanName, "??", authID)
            if tags:
                msg = "Lien ajouté avec les tags :"
                for tag in tags:
                    tag_tmp = mdb.searchSynonymeByPrimKey(tag)
                    if tag_tmp:
                        tag = tag_tmp[0][2]

                    mdb.addTag(tag, "", authID)
                    mdb.addTagmap(link, tag)
                    msg += " " + tag
            else:
                msg = "Lien ajouté sans tag"
            if not lienAjoute:
                msg = "Le lien existe déjà dans la base de donnée ou une erreur a eu lieu."
        else:
            "Le lien n'est pas conforme"

        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def Ldel(self, ctx, link):
        if mdb.searchLienByPrimKey(link)[0][3] == ctx.author.id:
            mdb.deleteLien(link)
            liste_id_tm = mdb.simpleItemSearch("tagmap", "lien_url", link)
            for id_tm in liste_id_tm:
                mdb.deleteTagmap(id_tm[0])
            await ctx.channel.send("Lien supprimé")
            await ctx.message.delete()
        else:
            await ctx.channel.send("Le lien n'a pas pu être supprimé")

    @commands.command(pass_context=True)
    async def Lsearch(self, ctx, *tags):

        resLinks = mdb.searchLinkFromTags(tags)

        if resLinks:
            str = "Liens correspondants à votre recherche :\n"
            for link in resLinks:
                dataLink = mdb.simpleItemSearch("tagmap", "lien_url", link[0])
                tagsList = list()

                for data in dataLink:
                    tagsList.append(data[2])

                del(dataLink)

                str += "  **>** "+link[0]+" ["

                for tag in tagsList:
                    if tag in tags:
                        str += " **{0}** ".format(tag)
                    else:
                        str += " {0} ".format(tag)
                str += "]"
                await ctx.channel.send(str)
                str = ""
        else:
            str = "Aucun lien ne correspond à votre recherche"
            await ctx.channel.send(str)


def setup(bot):
    bot.add_cog(LienCommands(bot))
