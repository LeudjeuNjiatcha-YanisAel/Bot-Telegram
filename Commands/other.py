from random import shuffle
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def open_google(update,context):
    keyboard = [ [InlineKeyboardButton("Ouvrir Google 🌐", url="https://www.google.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Clique sur le bouton pour ouvrir Google :", reply_markup=reply_markup)
    
async def gen_phrase(update,context):
    if not context.args:
        await update.message.reply_text("Usage : /gen_phrase 'mot1' 'mot2' ...")
        return
    mots = context.args[:]
    shuffle(mots)
    phrase = ' '.join(mots).capitalize() + '.'
    await update.message.reply_text("Voici une phrase :")
    await update.message.reply_text(phrase)

async def getid(update,context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Ton chat_id est : {chat_id}")

async def clear(update,context):
    id = update.message.from_user.id
    owner = 5441882239
    own = 7799721970
    chat = update.message.chat
    chat_id = chat.id
    message_id = update.message.message_id

    if chat.type == "private":
        empty_block = "\n\n".join(["\u200E" for _ in range(100)])
        await update.message.reply_text("🧹 Nettoyage de ta messagerie en cours...\n\n" + empty_block + "\n\n✅ Messagerie nettoyée")
        return
    if id != owner and id != own:
        await update.message.reply_text("❌️ Permission Non Accorder Pour Cette Commande")
        return
    
    if chat.type in ["group","supergroup"]:
        try:
            for i in range(message_id,message_id-10,-1):
                try:
                   await context.bot.delete_message(chat_id=chat_id,message_id=i)
                except:
                    pass
            await update.message.reply_text("✅ 10 derniers messages supprimés")
        except:
            await update.message.reply_text("❌ Impossible de nettoyer (le bot doit être admin et avoir la permission de suppression)")