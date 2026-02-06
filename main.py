from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import threading
from Config.config import TOKEN
from uptimebot import run_flask,keep_alive

from Core.startup import start, about
from Core.auto_reply import auto_reply

# J'importe Mes Commandes
from Commands.math import add,sub,div,mul,mod
from Commands.games import dice,chefumi,squidgame,piece,quit
from Commands.misc import ping,pin
from Commands.help import help_command
from Commands.meteo import meteo
from Commands.football import football
from Commands.youtube import youtube_se
from Commands.time import times
from Commands.news import news
from Commands.pp_sticker import pp,sticker
from Commands.other import open_google,getid,gen_phrase,clear
from Commands.play import play
from Commands.listusers import listusers
from Commands.send_message import sendall,send,msg

from AI.gemini import ask


async def handle_channel_message(update,context):
    print("Message reçu du canal")
    print(update.channel_post.chat.id)

async def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("ping",ping))
    app.add_handler(CommandHandler("help",help_command))
    app.add_handler(CommandHandler("add",add))
    app.add_handler(CommandHandler("sub",sub))
    app.add_handler(CommandHandler("mul",mul))
    app.add_handler(CommandHandler("div",div))
    app.add_handler(CommandHandler("mod",mod))
    app.add_handler(CommandHandler("pin",pin))
    app.add_handler(CommandHandler("gen_phrase",gen_phrase))
    app.add_handler(CommandHandler("msg",msg))
    app.add_handler(CommandHandler("send",send))
    app.add_handler(CommandHandler("about",about))
    app.add_handler(CommandHandler("listusers",listusers))
    app.add_handler(CommandHandler("getid",getid))
    app.add_handler(CommandHandler("time",times))
    app.add_handler(CommandHandler("clear",clear))
    app.add_handler(CommandHandler("ask",ask))
    app.add_handler(CommandHandler("pp",pp))
    app.add_handler(CommandHandler("sticker",sticker))
    app.add_handler(CommandHandler("google",open_google))
    app.add_handler(CommandHandler("squidgame",squidgame))
    app.add_handler(CommandHandler("play",play))
    app.add_handler(CommandHandler("dice",dice))
    app.add_handler(CommandHandler("shifumi",chefumi))
    app.add_handler(CommandHandler("piece",piece))
    app.add_handler(CommandHandler("video",youtube_se))
    app.add_handler(CommandHandler("football",football))
    app.add_handler(CommandHandler("sendall",sendall))
    app.add_handler(CommandHandler("news",news))
    app.add_handler(CommandHandler("quit",quit))
    app.add_handler(CommandHandler("meteo",meteo))
    app.add_handler(
    MessageHandler(filters.ChatType.CHANNEL,handle_channel_message))
    print("Machine_Bot a démarré...")
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))
    
    await app.run_polling()
  
if __name__ == "__main__": 
    threading.Thread(target=run_flask).start()   
    import nest_asyncio
    nest_asyncio.apply()  

    from telegram.ext import ApplicationBuilder
    import asyncio

    app = ApplicationBuilder().token(TOKEN).build()

    # Ajoute ici tes handlers, exactement comme dans main()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping",ping))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add",add))
    app.add_handler(CommandHandler("sub",sub))
    app.add_handler(CommandHandler("mul",mul))
    app.add_handler(CommandHandler("div",div))
    app.add_handler(CommandHandler("mod",mod))
    app.add_handler(CommandHandler("pin",pin))
    app.add_handler(CommandHandler("gen_phrase",gen_phrase))
    app.add_handler(CommandHandler("msg",msg))
    app.add_handler(CommandHandler("send",send))
    app.add_handler(CommandHandler("about",about))
    app.add_handler(CommandHandler("listusers",listusers))
    app.add_handler(CommandHandler("getid",getid))
    app.add_handler(CommandHandler("time",times))
    app.add_handler(CommandHandler("clear",clear))
    app.add_handler(CommandHandler("ask",ask))
    app.add_handler(CommandHandler("pp",pp))
    app.add_handler(CommandHandler("sticker",sticker))
    app.add_handler(CommandHandler("google",open_google))
    app.add_handler(CommandHandler("squidgame",squidgame))
    app.add_handler(CommandHandler("play",play))
    app.add_handler(CommandHandler("dice",dice))
    app.add_handler(CommandHandler("shifumi",chefumi))
    app.add_handler(CommandHandler("piece",piece))
    app.add_handler(CommandHandler("video",youtube_se))
    app.add_handler(CommandHandler("football",football))
    app.add_handler(CommandHandler("news",news))
    app.add_handler(CommandHandler("quit",quit))
    app.add_handler(CommandHandler("meteo",meteo))
    app.add_handler(
    MessageHandler(filters.ChatType.CHANNEL,handle_channel_message))
    # Lancement du bot
    print("Machine_Bot a démarré...")
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))
    
    asyncio.run(main())