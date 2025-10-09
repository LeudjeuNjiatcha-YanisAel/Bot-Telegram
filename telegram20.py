import random
from random import shuffle
import datetime
from datetime import date,timedelta,datetime
import asyncio
import json
import os
from gnews import GNews
from PIL import Image
from io import BytesIO
import tempfile
import requests
import subprocess
from googleapiclient.discovery import build
from google.genai import types 
from google import genai
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN = "8404081837:AAF9lT_adIUY8ou8LPfdUDXNqqE6DDe86K0"
USERS_FILE = "users.json"
METEO_API  = "aa2133ea80381e8a274fc15873ff5677"
KEY_TIME = "9UJS6LPXID3A"
MUSIC = "music"
FOOTBALL = "a55174569e0a44248a0a9e02002d456e"
URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token":FOOTBALL}

google_news = GNews(language='fr',country='FR',period='7d',max_results=5)

youtube_api = "AIzaSyCdMKKFAzmf3Y1aZ7yQw8FgXJC6uvDsJd8"
youtube = build("youtube","v3",developerKey=youtube_api)
users = {}
user_numbers = {}

leagues = {
    "premier league": "PL",
    "la liga": "PD",
    "serie a": "SA",
    "bundesliga": "BL1",
    "ligue 1": "FL1",
    "champions league": "CL",
    "europa league": "EL",
    "world cup": "WC",
    "can": "AFRICA_CUP_OF_NATIONS",
    "nations league": "NATIONS_LEAGUE"
}

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        try:
            users = json.load(f)
        except:
            users = {}

nd = 0 
np = 0
nc = 0

money = {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

async def dice(update,context):
    await update.message.reply_text("Vous avez choisir le *Jeu Tire un Dé*",parse_mode="Markdown")
    result = random.randint(1,6)
    await asyncio.sleep(2)
    await update.message.reply_text(f"🎲 Le dé a roulé tu as obtenu : *{result}*",parse_mode="Markdown")
    if(result == 6):
        user = update.message.from_user.id
        money[user] += 100
        await update.message.reply_text(f"Votre gain est de {money[user]}")
    nd +=1
    return nd
    
async def piece(update,context):
    
    await update.message.reply_text("Vous avez choisir le *pile ou face*",parse_mode = "Markdown")
    result = random.choice(["pile","face"])
    await update.message.reply_text(f"📀️ tu as obtenu : *{result}*",parse_mode = "Markdown")
    np = np + 1
    return np

async def chefumi(update,context):
    try :
        player = "".join(context.args).lower()
        choice = ["pierre","feuille","ciseau"] 
        if player not in choice:
            await update.message.reply_text("Veuillez Choisir Ciseau ✂️ \t, Pierre 🔨 \t, Feuille 📝️\t")
            return
        
        result = random.choice(["ciseau","pierre","feuille"])
        
        await update.message.reply_text("Pierre ...")
        await asyncio.sleep(1)
        await update.message.reply_text("Feuille ...")
        await asyncio.sleep(1)
        await update.message.reply_text("Ciseau ...")
        await asyncio.sleep(1)
        
        await update.message.reply_text(f"J'ai tire {result} et toi {player} ")
        if result == player :
            await update.message.reply_text("😌️ Partie Nulle")
        elif (player == "ciseau" and result == "feuille") or \
            (player == "pierre" and result == "ciseau") or \
            (player == "feuille" and result == "pierre"):
            await update.message.reply_text("✅ Tu as gagne ")
        else :
            await update.message.reply_text("❌️ Tu as perdu")
        nc +=1
        return nc
    except :
        await update.message.reply_text("⚠️ Usage : Tape /pierre ou /feuille ou /ciseau")
        
        
async def squidgame(update,context):
    global user_numbers
    user = update.message.from_user.id
    if user not in user_numbers:
        number = random.randint(1,456)
        user_numbers[user] = number
        await update.message.reply_text("🎮 Bienvenue dans SquidGame! 🎮\t")
        await update.message.reply_text(f"Joueur N°{number}")
        await update.message.reply_text("Jeux Disponibles : ")
        await update.message.reply_text(f"1./dice en ligne {nd}")
        await update.message.reply_text(f"2./piece en ligne {np}")
        await update.message.reply_text(f"3./shifumi en ligne {nc} ex : /chefumi ciseau")
        await update.message.reply_text("4./quit Quitter la partie ")
        await update.message.reply_text("Choisis un jeu en tapant son nom (ex: /dice)")
    else:
        number = user_numbers[user]
        await update.message.reply_text(f"Tu es déjà dans la partie, joueur N°{number}")
        await update.message.reply_text("Jeux Disponibles : ")
        await update.message.reply_text(f"1./dice en ligne  {nd}")
        await update.message.reply_text(f"2./piece en ligne {np}")
        await update.message.reply_text(f"3./shifumi en ligne {nc} ex : /chefumi ciseau")
        await update.message.reply_text("4./quit Quitter la partie")
        await update.message.reply_text("Choisis un jeu en tapant son nom (ex: /dice)")
        
async def quit(update,context):
    user = update.message.from_user.id
    if user in user_numbers:
        await update.message.reply_text(f"Vous avez quitté la partie, joueur N°{user_numbers[user]}")
        del user_numbers[user]
        user_numbers[user].clear()
    else:
        await update.message.reply_text("Vous n'êtes pas encore dans la partie.")
    nd = 0
    np = 0
    nc = 0
    return nd,np,nc 
      
async def ping(update,context):
    await update.message.reply_text("🤖 MACHINE BOT \n \n\n🏓 Pong! Je suis en ligne ✅")

async def start(update,context):  
    user = update.message.from_user
    users[str(user.id)] = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": f"{user.first_name} {user.last_name}" if user.last_name else user.first_name,
        "username": user.username
    }
    save_users()
    print("Nouvel utilisateur detecter")
    text = (
        f"👋 *Salut {user.first_name}*, tu es maintenant enregistré ✅\n\n"
        "🤖 *Bienvenue dans Machine_11bot* 🤖\n\n"
        "Voici ce que je peux faire pour toi :\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧮 *Mathématiques*\n"
        "➕ /app x y → Addition\n"
        "➖ /sub x y → Soustraction\n"
        "✖️ /mul x y → Multiplication\n"
        "➗ /div x y → Division\n"
        "🪙 /mod x y → Modulo\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 *Messagerie*\n"
        "📨 /msg chat_id texte → Envoyer un message\n"
        "📩 /send Nom message → Envoyer à un utilisateur\n"
        "🧹 /clear → Nettoyer la messagerie\n"
        "👥 /listusers → Liste des utilisateurs\n"
        "🆔 /getid → Voir ton ID\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ *Autres Fonctions*\n"
        "📝 /gen_phrase mots… → Générer une phrase\n"
        "🔑 /pin → Générer un code PIN\n"
        "🌐 /google → Ouvrir Google\n"
        "⏰ /time ville → Heure locale\n"
        "🎼️ /play titre de la musique → Jouez une musique\n"
        "▶️ /video nom de la video → Rechercher une video\n"
        "📰 /news sujet → Rechercher des actualités\n"
        "🌦 /meteo ville → Météo locale\n"
        "📷️ /pp → Recupere La Photo de profil\n"
        "🎮️ /squidgame → Demarrer Un Jeu"
        "🤔 /ask question → Poser une question au bot\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 *Aide*\n"
        "❓ /help → Voir toutes les commandes\n"
        "🎾️ /ping → Verifie si le bot est en ligne\n"
        "🎏 /about → Infos sur le bot-telegram\n\n"
        "_Mentionne-moi avec @NomDuBot dans un groupe pour discuter avec moi ! 🤖")
    keyboard = [
        [InlineKeyboardButton("📖 Voir l'aide", callback_data="help")],
        [InlineKeyboardButton("🌐 Google", url="https://www.google.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def about(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    text = (
        "╔════════════════════════════╗          \n"
        "     🤖 *Machine_11bot* 🤖\n"
        "╚════════════════════════════╝           \n\n"
        "✨ *Version* : `20.6`\n"
        "💫 *Technologies* :\n"
        "   🥇 Python3\n"
            "API du bot Telegram ( python-telegram-bot)"
            "API OpenWeather (Météo)"
            "API YouTube (Recherche Vidéo)"
            "PI TimeZoneDB (Heure locale)"
            "IA générative de Google (Gemini)"
        "   🥈 VPS (Serveurs)\n\n"
        "👨‍💻 *Concepteur* : *Machine*\n"
        "📱 *Contact* : [WhatsApp](https://wa.me/237620834784)\n\n"
        "🎁 *Lien du bot* : [Clique ici](https://t.me/Machine_11bot)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ Multi-fonctions : Maths, Musique, Météo,Youtube, IA\n"
        "━━━━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = [
        [InlineKeyboardButton("📖 Aide",callback_data="help_command")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text,parse_mode="Markdown",reply_markup=reply_markup)

async def help_command(update,context):
    await update.message.reply_text(
        "📖 *Aide - Machine_11bot* 📖\n\n"
        "Voici ce que je peux faire pour toi :\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧮 *Mathématiques*\n"
        "➕ /app x y → Addition\n"
        "➖ /sub x y → Soustraction\n"
        "✖️ /mul x y → Multiplication\n"
        "➗ /div x y → Division\n"
        "🪙 /mod x y → Modulo\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 *Messagerie*\n"
        "📨 /msg chat_id texte → Envoyer un message\n"
        "📩 /send Nom message → Envoyer à un utilisateur\n"
        "🧹 /clear → Nettoyer la messagerie\n"
        "👥 /listusers → Liste des utilisateurs\n"
        "🆔 /getid → Voir ton ID\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ *Autres Fonctions*\n"
        "📝 /gen_phrase mots… → Générer une phrase\n"
        "🔑 /pin → Générer un code PIN\n"
        "🌐 /google → Ouvrir Google\n"
        "⏰ /time ville → Heure locale\n"
        "🎼️ /play titre de la musique → Jouez une musique\n"
        "▶️ /video nom de la video → Rechercher une video\n"
        "📰 /news sujet → Rechercher des actualités\n"
        "🌦 /meteo ville → Météo locale\n"
        "📷️ /pp → Recupere La Photo de profil\n"
        "🎮️ /squidgame → Demarrer Un Jeu\n"
        "⚽ /football Nom du championnat → Voir les matchs de football en direct\n"
        "🤔 /ask question → Poser une question au bot\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 *Aide*\n"
        "❓ /help → Voir toutes les commandes\n"
        "🎾️ /ping → Verifie si le bot est en ligne\n"
        "🎏 /about → Infos sur le bot-telegram\n\n"
        "_Mentionne-moi avec @NomDuBot dans un groupe pour discuter avec moi ! 🤖"
    )

async def add(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        await update.message.reply_text(f"Résultat : {n1} + {n2} = {n1+n2}")
        print("La fonction addition a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /app 'nombre1' 'nombre2'")

async def sub(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        await update.message.reply_text(f"Résultat : {n1} - {n2} = {n1-n2}")
        print("La fonction soustraction a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /sub 'nombre1' 'nombre2'")

async def mul(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        await update.message.reply_text(f"Résultat : {n1} × {n2} = {n1*n2}")
        print("La fonction multiplication a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /mul 'nombre1' 'nombre2'")

async def div(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        if n2 == 0:
            await update.message.reply_text("Erreur : Division par zéro ❌")
        else:
            await update.message.reply_text(f"Résultat : {n1} ÷ {n2} = {n1/n2}")
            print("La fonction division a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /div 'nombre1' 'nombre2'")
        
async def mod(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    try:
        n1 = int(context.args[0])
        n2 = int(context.args[1])
        if n2 == 0:
            await update.message.reply_text("Impossible d'effectuer le modulo ❌")
            print("La fonction modulo a été utiliser avec succès!")
        else:
            await update.message.reply_text(f"Résultat : {n1} mod {n2} = {n1%n2}")
    except:
        await update.message.reply_text("Usage : /mod 'nombre1' 'nombre2'")

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

async def pin(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    
    code = "".join([str(random.randint(0, 9)) for _ in range(4)])
    await update.message.reply_text(f"🔑 Ton code PIN : {code}")
    print("Un code PIN a été generer")
    
async def send(update,context):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("❌ Utilisation : /send 'Nom' 'message'")
            return
        
        name = context.args[0]
        texte = " ".join(context.args[1:])
        sender = update.message.from_user.first_name
        found = False
        
        for uid, info in users.items():
            username = (info.get("username") or "").lower()
            first_name = (info.get("first_name") or "").lower()
            last_name = (info.get("last_name") or "").lower()
            full_name = (info.get("full_name") or "").lower()
            
            if name.lower() in [username, first_name, last_name, full_name] or str(uid) == name:
                chat_id = int(uid)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"📩 Message de {sender} :\n\n\n\n{texte}"
                )
                found = True
                break
        
        if found:
            await update.message.reply_text(f"✅ Message envoyé à {name}")
            print(f"Le client {sender} a envoye un message a {name}")
        else:
            await update.message.reply_text(f"❌ Utilisateur '{name}' introuvable.")
    
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erreur : {e}\n\n\n\nUtilisation : /send <username|full_name|id> <message>")

async def msg(update,context):
    try:
        chat_id = int(context.args[0])
        texte = " ".join(context.args[1:])
        sender = update.message.from_user.first_name
        context.bot.send_message(chat_id=chat_id,text=f"📩 Message de {sender} :\n\n\n\n{texte}")
        await update.message.reply_text("✅ Message envoyer avec succès !")
        print(f"Le client {sender} a envoye un message ")
    except:
        await update.message.reply_text("❌ Utilisation : /msg 'chat_id' 'texte'")

async def ask(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    question = " ".join(context.args)
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a poser cette question au bot : {question}")
    if not question:
        await update.message.reply_text("❌ Utilisation : /ask <ta question>")
        return
    async def thread():
        try:
            client = genai.Client(api_key="AIzaSyBXylzIdR5bMdb9NwtywO-MgJB1V134548")

            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=question
            )

            answer = response.text
            for i in range(0,len(answer),2000) :
                await update.message.reply_text("Machine_IA🤖 \n ")
                await update.message.reply_text("💡 Réponse : "+answer[i:i+4096])
        except Exception as e:
            await update.message.reply_text(f"⚠️ Machine IA : {e}")
    asyncio.create_task(thread())

async def met(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={METEO_API}&units=metric&lang=fr"
    reponse = requests.get(url)
    if reponse.status_code == 200:
        data = reponse.json()
    
        meteo = {
            "Ville":data["name"],
            "Temperature":data["main"]["temp"],
            "Humidite":data["main"]["humidity"],
            "Description":data["weather"][0]["description"],
            "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("meteo.json","a",encoding="utf-8") as f:
            f.write(json.dumps(meteo,ensure_ascii=False) + "\n")
            print("Donnees meteo enregistrees avec succes !")
        return f"Ville : {meteo['Ville']}\nTemperature : {meteo['Temperature']}°C\nHumidite : {meteo['Humidite']}%\nDescription : {meteo['Description']}"
    else :
        return "❌ Erreur lors de la recuperation : "

async def meteo(update,context):
    if not context.args:
        await update.message.reply_text("Utilisation : /meteo <Nom de la ville>")
        return
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter les donnees meteo ")
    
    ville = " ".join(context.args) 
    await update.message.reply_text(await met(ville))

async def local_time(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={METEO_API}"
    response = requests.get(url)    
    data = response.json()
    latitude = data["coord"]["lat"]
    longitude = data["coord"]["lon"]
    
    # Apres avoir obtenu la latitude et la longitude de la ville on va demande une requete API
    url1 = f"http://api.timezonedb.com/v2.1/get-time-zone?key={KEY_TIME}&format=json&by=position&lat={latitude}&lng={longitude}"
    reponse = requests.get(url1)
    data1 = reponse.json()
    
    if latitude is None or longitude is None:
        return "Ville Introuvable"
    print("Heure locale affichee avec succès !")
    return data1["formatted"]

async def time(update,context): 
    if not context.args:
        await update.message.reply_text("Utilisation : /time <Nom de la ville>")
        return
    
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter l'heure de sa ville")
    
    ville = " ".join(context.args)
    await update.message.reply_text(await local_time(ville))
    
async def listusers(update,context):
    if not users:
        await update.message.reply_text("❌ Aucun utilisateur enregistré.")
        return
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter les utilisateurs enregistres !  ")
    
    message = "📋 Utilisateurs enregistrés :\n\n\n\n"
    for uid, info in users.items():
        first_name = info.get("first_name", "")
        last_name = info.get("last_name", "")
        full_name = info.get("full_name") or f"{first_name} {last_name}".strip()
        username = info.get("username")
        uname = f"@{username}" if username else "❌ (pas de username)"
        
        message += f"👤 {full_name} | ID: {uid} | Username: {uname}\n\n"
    
    await update.message.reply_text(message)

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

async def send_online(app):
    tasks = []
    for chat_id in users.keys():
        try:
            print("Message envoye ! ✅")
            task = asyncio.create_task(await app.bot.send_message(chat_id=int(chat_id),text="🤖 Le bot est en ligne ✅"))
            tasks.append(task)
            await asyncio.gather(*tasks,return_exceptions=True)
        except Exception as e:
            print(f"Erreur en envoyant à {chat_id}: {e}")
            
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
            client = genai.Client(api_key="AIzaSyBXylzIdR5bMdb9NwtywO-MgJB1V134548")

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

async def search_video(name):
   requests = youtube.search().list(q = name,part="snippet",type="video",maxResults=1)
   # Ici on veut trouver l'ID d'une video via son nom
   response = requests.execute()
   # Ici on envoie une requete et on obtient une reponse
   
   if response["items"]:
       video = response["items"][0]["id"]["videoId"]
       # Ca recupere l'id de la video
       title = response["items"][0]["snippet"]["title"]
       stats = youtube.videos().list(part="statistics",id=video)
       stats_res = stats.execute()
       stats = stats_res["items"][0]["statistics"]
       like_count = stats.get("likeCount", "N/A")
       vues = stats.get("viewCount", "N/A")
       
       # recherche playlist
       req_playlist = youtube.search().list(q=name, part="snippet", type="playlist", maxResults=1)
       res_playlist = req_playlist.execute()
       playlist_id, playlist_title = (None, None)
       if res_playlist["items"]:
            playlist_id = res_playlist["items"][0]["id"]["playlistId"]
            playlist_title = res_playlist["items"][0]["snippet"]["title"]
       return (video,title,like_count,vues),(playlist_id,playlist_title)
   return None,None,None,None


# Pour recuperer le nombre de video d'une playlist
async def info_playlist(playlist_id):
    request = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=50)
    
    response = request.execute()
    total_videos = response.get("pageInfo",{}).get("totalResults",0)
    return total_videos

# Code Pour Les Commentaires
async def commentaries(video_id,max_results=10):
    comments = []
    requests = youtube.commentThreads().list(part = "snippet",videoId=video_id,textFormat="plainText",maxResults=max_results)
    # On a construit la requete pour recuperer les commentaires
    response = requests.execute()
    # Lancement de la requete
    for commentary in response["items"]:
        pet = commentary["snippet"]["topLevelComment"]["snippet"]
        #Ca va chercher le vrai commentaire
        text = pet["textDisplay"]
        #Recupere le texte du commentaire
        like = pet["likeCount"]
        comments.append((text,like))
    return comments

# Code Pour Analyser une Playlist
async def analyse_playlist(playlist_id,playlist_title):
    videos = []
    req = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=20)
    res = req.execute()

    for item in res.get("items", []):
        title = item["snippet"]["title"]
        videos.append(title)

    if not videos:
        return "Impossible d’analyser : la playlist est vide."

    input_text = "\n".join([f"- {t}" for t in videos])

    prompt = f"""Voici les titres des vidéos de la playlist "{playlist_title}" :
    {input_text}
    Analyse cette playlist et réponds :
    1. Résume en quelques phrases ce que couvre cette playlist.
    2. Pour quel type de spectateurs est-elle adaptée ?
    3. Donne une note de pertinence /10.
    4. Dis si tu la recommanderais, et pourquoi.
    """

    client = genai.Client(api_key="AIzaSyAQBpi-rDqpY4rqSZbeFc0Szjg0dsCYixQ")
    model = "gemini-2.5-pro"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(response_modalities=["TEXT"])

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if getattr(chunk, "text", None):
            output += chunk.text

    return output.strip()

# Code Recuperer Dans Google AI studio
async def analyse_comments(comments):
    client = genai.Client(api_key=("AIzaSyAQBpi-rDqpY4rqSZbeFc0Szjg0dsCYixQ"))
    # Ici on prend les commentaires les plus likes
    input_text = "\n".join(
        [f"- {txt} ({likes} likes)" for txt,likes in sorted(comments,key=lambda x:x[1],reverse=True)[:5]]
    )

    prompt = f"""Voici des commentaires d'une vidéo récupérés sur YouTube : {input_text}
    Analyse ces commentaires et dit moi ci en 1 la video est pertinente , en 2 pour quelle type de spectatuers c'est reserver , en 3 tu donne une note /10 pour la pertinence , 
    en 4 tu donne une raison pour laquelle tu recommanderait cette video
    ."""

    model = "gemini-2.5-pro"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(response_modalities=["TEXT"])

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if getattr(chunk,"text",None):
            output += chunk.text

    return output.strip()


async def youtube_se(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    if not context.args :
        await update.message.reply_text("Utilisation correcte /video <nom de la video a rechercher>")
        return 
    
    name = " ".join(context.args)      
    (video_id,title,likes,vues),(playlist_id,playlist_title) = await search_video(name)

    # Partie vidéo
    await update.message.reply_text(f"\n\tVideo trouvee : {title} ✅")
    await update.message.reply_text(f"lien ▶️ : https://www.youtube.com/watch?v={video_id}")
    await update.message.reply_text(f"Nombres De Likes 👍 : {likes} | 👁️ Vues : {vues} ")
    print("Video Afficher Avec Succes ✅")
    await update.message.reply_text("Analyses des commentaires des differentes video ...")

    # Récupération des commentaires
    comment = await commentaries(video_id)
    recommandation = await analyse_comments(comment)

    await update.message.reply_text("Meilleur Commentaire Trouvee ")
    await update.message.reply_text(f"{len(comment)} commentaires recuperes.")
    await update.message.reply_text("\n=== Video recommandee a partir des commentaires ===")
    await update.message.reply_text(recommandation)
    print("Recommandation Afficher Avec Succes ✅")
    await update.message.reply_text("\n")

    # Partie playlist
    await update.message.reply_text(f"\n\t=== 📂 Meilleure Playlist Trouvée Pour {name} : {playlist_title} ===")
    await update.message.reply_text(f"-URL de la playlist : https://www.youtube.com/playlist?list={playlist_id}")
    print("Playlist Afficher Avec Succes ✅")

    total = await info_playlist(playlist_id)
    await update.message.reply_text(f" 📺 Nombre De Video De La Playlist {total} videos")
    await update.message.reply_text("\n=== Recommandation de la Playlist ===")
    analyse = await analyse_playlist(playlist_id, playlist_title)
    await update.message.reply_text(analyse)

    
async def play(update,context):
    if not context.args:
        await update.message.reply_text("Utilisation de la commande : /play <nom de la musique>")
        return
    
    # musique a rechercher
    music_query = " ".join(context.args)
     
    # Dans cette partie nous commençons a telecharger le media
    try :
        # Creation d'un dossier temporaire
        with tempfile.TemporaryDirectory() as tmpdir:
        # Modèle de nom qu'on utilisera en sortie par exemple titre.mp3
            output_path = os.path.join(tmpdir,"%(title).50s.%(ext)s")
        
            subprocess.run([
                # Ici on appelle la commande yt-dlp
                "yt-dlp",
                # Extrait slt l'audio
                "--extract-audio",
                # Convertit le fichier en mp3
                "--audio-format", "mp3",   
                # On définit la qualité correcte
                "--audio-quality", "192K",
                # On indique le modele de nom du fichier
                "-o",output_path,
                # La derniere etape c'est la recherche
                f"ytsearch1:{music_query}"],check=True)
        
            # Ici on liste les fichiers du dossier ça donne ts les fichiers contenus dans le dossier
            files = os.listdir(tmpdir)
            
            # Ici on recupere les fichiers .mp3
            files = [f for f in files if f.endswith("mp3")]
            
            # C'est pour recuperer la date et heure de la derniere modification via getmtime
            files.sort(key=lambda f: os.path.getmtime(os.path.join(tmpdir,f)))
            
            # Prend le dernier fichier telecharger
            latest_file = os.path.join(tmpdir,files[-1])
            
            with open(latest_file,"rb") as audio:
                await update.message.reply_audio(audio)
            await update.message.reply_text("Voici ta musique !")
    except Exception as e:
        await update.message.reply_text(f"Erreur : {e}")        

def call_news(category_or_keyword="general",max_results=5):
    """
    Récupère soit une catégorie de news, soit une recherche par mot-clé,
    avec titre, résumé et URL.
    """
    category_map = {
        "general": "À la une",
        "business": "Économie",
        "entertainment": "Divertissement",
        "health": "Santé",
        "science": "Science",
        "sports": "Sports",
        "technology": "Technologie"
    }

    # Si c'est une catégorie connue
    if category_or_keyword in category_map:
        topic = category_map[category_or_keyword]
        try:
            articles = google_news.get_news_by_topic(topic)
        except Exception as e:
            return [(f"Erreur lors de la récupération des news (topic): {e}", "", "")]
    else:
        # Sinon mot-clé
        try:
            articles = google_news.get_news(category_or_keyword)
        except Exception as e:
            return [(f"Erreur lors de la récupération des news (keyword): {e}", "", "")]

    if not articles:
        return [("Aucune actualité trouvée", "", "")]

    # On prend titre, description et URL
    results = []
    for a in articles[:max_results]:
        title = a.get("title", "Sans titre")
        desc = a.get("description", "Pas de résumé disponible")
        url = a.get("url", "")
        results.append((title, desc, url))
    return results


async def news(update,context):
    if not context.args:
        await update.message.reply_text(
            "Utilisation : /news <categorie|mot-clé>\n\n"
            "Catégories disponibles : business, entertainment, general, health, science, sports, technology\n"
            "Exemples :\n"
            "   /news sports\n"
            "   /news Messi"
        )
        return

    query = context.args[0].lower()
    await update.message.reply_text("Recherche des news en cours... ⏳")

    articles = call_news(query, max_results=5)

    for title, desc, url in articles:
        message = f"📰 *{title}*\n\n📝 {desc}\n\n🔗 {url}"
        await update.message.reply_text(message, parse_mode="Markdown")

    print("✅ News avec résumés affichées !")

async def pp(update,context):
    # Reponses a un message
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = update.message.from_user.id
    photos = await context.bot.get_user_profile_photos(user_id)
    
    if photos.total_count == 0:
        await update.message.reply_text("❌ Cet utilisateur n’a pas de photo de profil.")
        return
    # Prendre la plus récente (dernier élément de la liste)
    photo_file_id = photos.photos[0][-1].file_id

    # Envoyer la photo au chat
    await update.message.reply_photo(photo_file_id,caption="📸 Photo de profil récupérée ✅")   

async def sticker(update,context):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("❌ Réponds à une photo  avec /sticker.")
        return
    
    # Recuperation de la photo
    photo_file = await update.message.reply_to_message.photo[-1].get_file()
    photo_bytes = BytesIO()
    await photo_file.download_to_memory(out=photo_bytes)
    photo_bytes.seek(0)
    
    # Creation du sticker
    image = Image.open(photo_bytes)
    # Redimensionner l'image
    max_size = 512
    image.thumbnail((max_size, max_size))
    
    # Sauvegarde dans un buffer
    output = BytesIO()
    output.name = "sticker.png"
    image.save(output,format="PNG")
    output.seek(0)
    
    #envoie du sticker
    await update.message.reply_sticker(sticker=output)
    
# ---- Fonction utilitaire pour prédiction ----
def predict_match(home_rank, away_rank, home_form, away_form, home_goals, away_goals):
    """Retourne une prédiction simple basée sur classement, forme et buts."""
    score = 0
    if home_rank and away_rank:
        score += (away_rank - home_rank) * 0.4
    score += (home_form - away_form) * 0.3
    score += (home_goals - away_goals) * 0.3
    if score > 0.5:
        return "Victoire probable de l’équipe à domicile 🏠"
    elif score < -0.5:
        return "Victoire probable de l’équipe à l’extérieur ✈️"
    else:
        return "Match serré — nul probable 🤝"

# ---- Commande Telegram ----
async def football(update,context):
    # Afficher la liste des championnats disponibles
    ligues_dispo = "\n".join([f"- {nom.title()}" for nom in leagues.keys()])
    await update.message.reply_text(f"🏆 Championnats disponibles :\n + {ligues_dispo}")
    await update.message.reply_text("Recherche des matchs en cours et à venir... ⏳")
    await asyncio.sleep(2)
    
    if not context.args:
        await update.message.reply_text(
            "Utilisation : /football <nom du championnat>\n"
            "Exemples : /football premier league, /football can\n\n"
        )

    league_name = " ".join(context.args).lower()
    league_id = leagues.get(league_name)

    if not league_id:
        await update.message.reply_text("❌ Championnat inconnu.")
        return

    headers = {"X-Auth-Token":FOOTBALL}

    # Période : aujourd'hui jusqu'à 14 jours dans le futur
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=7)

    url = (
        f"{URL}/competitions/{league_id}/matches"
        f"?dateFrom={today}&dateTo={end_date}&status=LIVE,FINISHED,SCHEDULED"
    )
    response = requests.get(url, headers=headers)
    data = response.json()
    if "matches" not in data or not data["matches"]:
        await update.message.reply_text("Aucun match prévu ou joué pour cette période.")
        return

    message = f"📅 *Matchs récents et à venir — {league_name.title()}*\n\n"

    # Récupérer le classement pour prédiction
    standings_url = f"{URL}/competitions/{league_id}/standings"
    standings_resp = requests.get(standings_url, headers=headers).json()
    table = standings_resp.get("standings", [{}])[0].get("table", [])

    for match in data["matches"]:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        status = match["status"]
        match_date = match["utcDate"][:10]

        # Scores si disponibles
        home_score = match["score"]["fullTime"]["home"]
        away_score = match["score"]["fullTime"]["away"]

        # 1️⃣ Match terminé
        if status in ["FINISHED", "AWARDED"]:
            message += f"Termine🏁 {home} {home_score} - {away_score} {away} (le {match_date})\n\n"

        # 2️⃣ Match en cours
        elif status == "LIVE":
            message += f"🔥 En direct : {home} {home_score or 0} - {away_score or 0} {away} (le {match_date})\n\n"

        # 3️⃣ Match à venir
        else:
            home_rank = away_rank = home_form = away_form = home_goals = away_goals = None

            # Chercher dans le classement
            for t in table:
                if t["team"]["name"] == home:
                    home_rank = t["position"]
                    home_form = t["points"]
                    home_goals = t["goalsFor"]
                if t["team"]["name"] == away:
                    away_rank = t["position"]
                    away_form = t["points"]
                    away_goals = t["goalsFor"]

            prediction = predict_match(
                home_rank, away_rank,
                home_form or 0, away_form or 0,
                home_goals or 0, away_goals or 0
            )
            message += f"⚽ {home} vs {away} (prévu le {match_date})\n🔮 {prediction}\n\n"

    await update.message.reply_text(message, parse_mode="Markdown")

        
async def main():
    app = ApplicationBuilder().token(TOKEN).post_init(send_online).build()
    
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
    app.add_handler(CommandHandler("time",time))
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
   
    print("Machine_Bot a démarré...")
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))
    
    await app.run_polling()
  
if __name__ == "__main__":    
    import nest_asyncio
    nest_asyncio.apply()  

    from telegram.ext import ApplicationBuilder
    import asyncio

    app = ApplicationBuilder().token(TOKEN).post_init(send_online).build()

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
    app.add_handler(CommandHandler("time",time))
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
    
    # Lancement du bot
    print("Machine_Bot a démarré...")
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))
    
    asyncio.run(main())

