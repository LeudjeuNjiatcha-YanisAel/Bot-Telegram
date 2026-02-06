import asyncio
from datetime import datetime,timedelta,datetime
from Commands.help import help_command
from Commands.meteo import local_time
from google import genai
from Config.config import GEMINI_API


async def auto_reply(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    bot_username = context.bot.username.lower()
    text = update.message.text.lower()
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a envoye ce message : {text} au bot ")
    if (update.message.chat.type != 'private') and (f"@{bot_username}" not in text):
        return
    text = text.replace(f"@{bot_username}", "").strip()
    
    if "bonjour" in text or "salut" in text or "bjr" in text or "yo" in text:
        reply = "Salut 👋 comment tu vas ?"
        await update.message.reply_text("Machine_Bot🤖 : " + reply)
    elif "ça va" in text:
        reply = "Oui ça va très bien merci 🤖 et toi ?"
        await update.message.reply_text("Machine_Bot🤖 : " + reply)
    elif "bien" in text:
        reply = "Idem de mon cote"
        await update.message.reply_text("Machine_Bot🤖 : " + reply)
    elif "merci" in text:
        reply = "Avec plaisir 😎"
        await update.message.reply_text("Machine_Bot🤖 : " + reply)
    elif "heure" in text:
        
        # Vérifier si l’utilisateur a demandé l’heure dans une ville spécifique
        if "en " in text or "a " in text or "au " in text:
            try:
                ville = text.split("en",1)[1].strip()
                ville = text.split("a",1)[1].strip()
                ville = text.split("au",1)[1].strip()
                heure_ville = await local_time(ville)
                reply = f"⏰ Il est actuellement {heure_ville} à {ville.title()}"
            except Exception as e:
                reply = f"❌ Impossible de récupérer l'heure demandée ({e})"
                reply = "Rassurer-vous entrer le nom d'une ville existant !"
        else:
            now = datetime.datetime.now()
            reply = f"⏰ Il est actuellement {now.strftime('%H:%M:%S')} au Cameroun"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "imbécile" in text:
        reply = "Et toi tu es idiot"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "ton nom" in text or "qui est tu" in text:
        reply = "Je suis ton bot multifonctions 🤖 créé par Machine 😎"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "idiot" in text or "fou" in text or "tu es bete" in text:
        reply = "Va te faire foutre🖕️"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "mouf" in text:
        reply = "Sale Gros con "
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "con" in text:
        reply = "Espece de feignant"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "ta maman" in text :
        reply = "Ca ne m'atteint pas "
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "acer" in text or "asser" in text:
        reply = "Que veux tu faire aujourd'hui"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "enfoirés" in text:
        reply = "Ignorant"
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif "ton cu" in text:
        reply = "Stupide que tu es "
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
        reply = "Encule 🖕️ "
        await update.message.reply_text("Machine_Bot🤖 : " +reply)
    elif  "aide" in text or "help" in text:
        reply = await help_command(update,context)
        await update.message.reply_text("Machine_Bot🤖 \n" +reply)
    else:
        try:
            client = genai.Client(api_key=GEMINI_API)

            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=text
            )

            answer = response.text
            for i in range(0,len(answer),2000) :
                await update.message.reply_text("Machine_IA🤖 : "+answer[i:i+4096])
        except Exception as e:
            print(f"Erreur API Gemini : {e}")
            await update.message.reply_text("⚠️ Impossible de causer avec le bot pour le moment, réessaie plus tard.")