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
        """
        tags -> tuple avec soit des tag soit sous la forme `lang=??` et `chan=??` la langue ou le channel voulu
        """

        for item in tags:
            if "lang=" in item:
                index_item = tags.index(item)
                lang = tags[index_item].split('=')[1]
                tags = tags[:index_item] + tags[index_item+1:]
            elif "chan=" in item:
                index_item = tags.index(item)
                chan = tags[index_item].split('=')[1]
                tags = tags[:index_item] + tags[index_item+1:]

        print(lang)
        print(tags)

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

    @commands.command(pass_context=True)
    async def Lmodify(self, ctx, link, arg, *tags):
        """
        arg -> "add"|"del" permet de savoir si l'utilisateur souhaite supprimer ou ajouter un tag
        link -> str : le lien dont on doit modifier les tags
        tags -> tuple : tuple de tags a ajouter ou supprimer
        """
        if mdb.searchLienByPrimKey(link)[0][3] == ctx.author.id:
            if arg == "add":
                for tag in tags:
                    tag_tmp = mdb.searchSynonymeByPrimKey(tag)
                    if tag_tmp:
                        tag = tag_tmp[0][2]

                    mdb.addTag(tag, "", ctx.author.id)
                    mdb.addTagmap(link, tag)
                await ctx.channel.send("Tag(s) bien ajouté(s).")

            elif arg == "del":
                setTags = set()
                listTagmap = mdb.simpleItemSearch("tagmap", "lien_url", link)
                for tagmap in listTagmap:
                    setTags.add(tagmap[2])
                tmpSet = set(tags)

                if tmpSet.issubset(setTags):
                    for tagmap in listTagmap:
                        if tagmap[2] in tags:
                            mdb.deleteTagmap(tagmap[0])
                    await ctx.channel.send("Tag(s) bien supprimé(s).")
                else:
                    await ctx.channel.send("Tag(s) impossible a supprimer car absent de la liste original.")

            else:
                await ctx.channel.send("Veuillez préciser `add` ou `del`.")

        else:
            await ctx.channel.send("Vous devez être l'auteur du lien pour le modifier. Son auteur est : <@{0}>".format(mdb.searchLienByPrimKey(link)[0][3]))


def setup(bot):
    bot.add_cog(LienCommands(bot))
