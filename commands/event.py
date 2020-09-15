import validators as val
import DB.manageDB as mdb
from discord.ext import commands
import discord
from webpreview import web_preview
import datetime

from commands.lien import LienCommands


class EventsCommands(commands.Cog):
    """docstring for EventsCommands."""

    def __init__(self, ctx):
        self.ERROR_FORMAT_DATE = -1
        self.ERROR_DATE_IN_PAST = -2

    def dateHandler(self, date):
        months = 1, 2 ,3 ,4 ,5, 6, 7, 8, 9, 10, 11, 12
        months_p = 1, 3, 5, 7, 8, 10, 12
        months_ip =  4, 6, 9, 11
        feb = 2

        dateEl = date.split("/")
        if int(dateEl[0]) < 2000:
            # DD/MM/YYYY
            dateY = int(dateEl[2])
            dateM = int(dateEl[1])
            dateD = int(dateEl[0])
        elif int(dateEl[0]) > 2000:
            # YYYY/MM/DD
            dateY = int(dateEl[0])
            dateM = int(dateEl[1])
            dateD = int(dateEl[2])

        dateEvent = datetime.datetime(dateY, dateM, dateD)
        if dateEvent >= datetime.datetime.today():
            dateSupp = datetime.datetime(dateY, dateM, dateD + 1)

            if dateM in months:
                if dateM in months_p:
                    if dateD == 31:
                        dateSupp = datetime.datetime(dateY, dateM, 1)
                    else:
                        dateSupp = datetime.datetime(dateY, dateM, dateD + 1)
                elif dateM in months_ip:
                    if dateD == 30:
                        dateSupp = datetime.datetime(dateY, dateM, 1)
                    else:
                        dateSupp = datetime.datetime(dateY, dateM, dateD + 1)
                elif dateM == feb:
                    if dateD == 28 or dateD == 29:
                        dateSupp = datetime.datetime(dateY, dateM, 1)
                    else:
                        dateSupp = datetime.datetime(dateY, dateM, dateD + 1)
            else:
                print("Error date format")
                return self.ERROR_FORMAT_DATE

            return dateEvent, dateSupp
        else:
            return self.ERROR_DATE_IN_PAST

    @commands.command(pass_context=True)
    async def Eadd(self, ctx, link, date, *tags):
        """
        params:
        link -> lien
        tags
        date : date de l'event
        """
        event = self.dateHandler(date)

        if event != self.ERROR_FORMAT_DATE and event != self.ERROR_DATE_IN_PAST:

            msg = ""
            authID = ctx.author.id
            chanName = ctx.channel.name

            lienAjoute = bool()

            for tag in tags:
                tag = tag.lower()

            if val.url(link):
                # cas ou ça marche
                title, description = "", ""
                try:
                    ret = web_preview(link)
                    title, description = ret[0], ret[1]
                except:
                    pass

                lienAjoute = mdb.addLien(link, chanName, "??", authID, title, description)
                if lienAjoute:
                    eventAdded = mdb.addEvent(link, event[0], event[1], authID)
                    if eventAdded:
                        if tags:
                            msg = "Event ajouté avec les tags :"
                            for tag in tags:
                                tag_tmp = mdb.searchSynonymeByPrimKey(tag)
                                if tag_tmp:
                                    tag = tag_tmp[0][2]

                                mdb.addTag(tag, "", authID)
                                mdb.addTagmap(link, tag)
                                msg += " " + tag
                        else:
                            msg = "Event ajouté sans tag"
                    else:
                        mdb.deleteLien(link)
                        liste_id_tm = mdb.simpleItemSearch("tagmap", "lien_url", link)
                        for id_tm in liste_id_tm:
                            mdb.deleteTagmap(id_tm[0])
                        msg = "L'event existe déjà dans la base de donnée ou une erreur a eu lieu."
                if not lienAjoute:
                    msg = "Le lien existe déjà dans la base de donnée ou une erreur a eu lieu."
            else:
                msg = "Le lien n'est pas conforme"
        else:
            msg = "La date n'est pas conforme"

        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def Edel(self, ctx, link):
        msg = ""
        if mdb.existEvent(link):
            if mdb.searchLienByPrimKey(link)[0][3] == ctx.author.id:
                print(mdb.simpleItemSearch("event", "url", link)[0][0])
                mdb.deleteEvent(mdb.simpleItemSearch("event", "url", link)[0][0])
                mdb.deleteLien(link)
                liste_id_tm = mdb.simpleItemSearch("tagmap", "lien_url", link)
                for id_tm in liste_id_tm:
                    mdb.deleteTagmap(id_tm[0])
                msg = "Event supprimé"
            else:
                msg = "Vous n'êtes pas l'auteur de cet Event, veuillez contacter <@{}>".format(mdb.searchLienByPrimKey(link)[0][3])
        else:
            if mdb.existLien(link):
                msg = "Le lien n'est pas un event."
            else:
                msg = "L'event existe pas."
        await ctx.channel.send(msg)


    @commands.command(pass_context=True)
    async def Esearch(self, ctx, link, date, *tags):
        pass

    @commands.command(pass_context=True)
    async def calendar(self, ctx):
        pass

    @commands.command(pass_context=True)
    async def Emodify(self, ctx, link, date, *tags):
        pass


def setup(bot):
    bot.add_cog(EventsCommands(bot))
