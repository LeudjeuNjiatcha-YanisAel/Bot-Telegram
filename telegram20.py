import random
from random import shuffle
import datetime
import asyncio
import json
import os
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
FOOTBALL = "A2OwCG4H2Hq5t0fAG0stROYqwwr1kx8qgN3akj1IUKZ5PotxHkZwUTQry5u7"
NEWS = "a3f9296a48a446e8b0f3626481922e3a"
youtube_api = "AIzaSyCdMKKFAzmf3Y1aZ7yQw8FgXJC6uvDsJd8"
youtube = build("youtube","v3",developerKey=youtube_api)
users = {}

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        try:
            users = json.load(f)
        except:
            users = {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

async def ping(update,context):
    await update.message.reply_text("Pong! 🤖 MACHINE BOT est en ligne ✅")

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
    text = (
        "╔════════════════════════════╗\n"
        "     🤖 *Machine_11bot* 🤖\n"
        "╚════════════════════════════╝\n\n"
        "✨ *Version* : `20.6`\n"
        "💫 *Technologies* :\n"
        "   🥇 Python\n"
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
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧮 *Mathématiques*\n"
        "/app x y → Addition\n"
        "/sub x y → Soustraction\n"
        "/mul x y → Multiplication\n"
        "/div x y → Division\n"
        "/mod x y → Modulo\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 *Messagerie*\n"
        "/msg chat_id texte → Envoyer un message\n"
        "/send Nom message → Envoyer à un utilisateur\n"
        "/clear → Nettoyer la messagerie\n"
        "/listusers → Liste des utilisateurs\n"
        "/getid → Voir ton ID\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ *Autres*\n"
        "/gen_phrase mots… → Générer une phrase\n"
        "/pin → Générer un code PIN\n"
        "/google → Ouvrir Google\n"
        "/time ville → Heure locale\n"
        "/play titre de la musique → Jouez une musique\n"
        "/video nom de la video → Rechercher une video\n"
        "/news sujet → Rechercher des actualités\n"
        "/meteo ville → Météo locale\n"
        "/ask question → Poser une question au bot\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 *Aide*\n"
        "/ping → Verifie si le bot est en ligne\n"
        "/help → Afficher cette aide\n"
        "/about → Informations sur le bot\n"
        "Mentionne-moi avec @NomDuBot dans un groupe pour discuter avec moi ! 🤖"
    )

async def add(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        await update.message.reply_text(f"Résultat : {n1} + {n2} = {n1+n2}")
        print("La fonction addition a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /app 'nombre1' 'nombre2'")

async def sub(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        await update.message.reply_text(f"Résultat : {n1} - {n2} = {n1-n2}")
        print("La fonction soustraction a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /sub 'nombre1' 'nombre2'")

async def mul(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        await update.message.reply_text(f"Résultat : {n1} × {n2} = {n1*n2}")
        print("La fonction multiplication a été utiliser avec succès!")
    except:
        await update.message.reply_text("Usage : /mul 'nombre1' 'nombre2'")

async def div(update,context):
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
                context.bot.send_message(
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
    question = " ".join(context.args)
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a poser cette question au bot : {question}")
    if not question:
        await update.message.reply_text("❌ Utilisation : /ask <ta question>")
        return

    try:
        client = genai.Client(api_key="AIzaSyBXylzIdR5bMdb9NwtywO-MgJB1V134548")

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=question
        )

        answer = response.text
        for i in range(0,len(answer),2000) :
            await update.message.reply_text("Machine_IA🤖 \n ")
            await update.message.reply_text("💡 Réponse : "+answer[i:i+2000])
    except Exception as e:
        await update.message.reply_text(f"⚠️ Machine IA : {e}")

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
            "date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("meteo.json","a",encoding="utf-8") as f:
            f.write(json.dumps(meteo,ensure_ascii=False) + "\n")
            print("Donnees meteo enregistrees avec succes !")
        return f"Ville : {meteo['Ville']}\nTemperature : {meteo['Temperature']}°C\nHumidite : {meteo['Humidite']}%\nDescription : {meteo['Description']}"
    else :
        return "❌ Erreur lors de la recuperation : "

async def meteo(update, context):
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
    chat = update.message.chat
    chat_id = chat.id
    message_id = update.message.message_id

    if chat.type == "private":
        empty_block = "\n\n".join(["\u200E" for _ in range(100)])
        await update.message.reply_text("🧹 Nettoyage de ta messagerie en cours...\n\n" + empty_block + "\n\n✅ Messagerie nettoyée")
        return

    if chat.type in ["group","supergroup"]:
        try:
            for i in range(message_id,message_id-100,-1):
                try:
                   await context.bot.delete_message(chat_id=chat_id,message_id=i)
                except:
                    pass
            await update.message.reply_text("✅ 50 derniers messages supprimés")
        except:
            await update.message.reply_text("❌ Impossible de nettoyer (le bot doit être admin et avoir la permission de suppression)")

async def send_online(app):
    for chat_id in users.keys():
        try:
            print("Message envoye ! ✅")
            await app.bot.send_message(chat_id=int(chat_id),text="🤖 Le bot est en ligne ✅")
        except Exception as e:
            print(f"Erreur en envoyant à {chat_id}: {e}")
            
async def auto_reply(update,context):
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

def call_news(category="general",country="fr",max_results=5):
    """
    Récupère les dernières actualités par catégorie depuis NewsAPI.
    
    :param category: catégorie (ex: general, technology, sports, business, health, entertainment, science)
    :param country: code pays (fr, us, gb, etc.)
    :param max_results: nombre max d'articles à afficher
    :return: liste de tuples (titre, url)
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey":NEWS,
        "category":category,
        "country":country,
        "pageSize":max_results
    }

    response = requests.get(url,params=params)
    data = response.json()

    if data.get("status") != "ok":
        return [("Erreur lors de la récupération des news", "")]

    articles = data.get("articles", [])
    return [(a["title"], a["url"]) for a in articles]

async def news(update,context):
    if not context.args:
        await update.message.reply_text("Utilisation : /news <sujet>")
        return
    
    await update.message.reply_text("Domaine Disponible : business,entertainment,general,health,science,sports,technology")
    await update.message.reply_text("Exemple : /news technology")
    await update.message.reply_text("Recherche des news en cours... ⏳")
    
    category = context.args[0].lower() 
    articles = call_news(category,country="fr",max_results=5)
    
    for title, url in articles:
        await update.message.reply_text(f"📰 {title}\n🔗 {url}")
    print("Informations des news affichées avec succès ! ✅")


async def football(update,context):
    if not context.args:
        await update.message.reply_text("Utilisation : /football <nom du championnat>")
        return
    
    league_name = " ".join(context.args).lower()
    league_id = None
    leagues = {
        "premier league":39,
        "la liga":140,
        "serie a":135,
        "bundesliga":78,
        "ligue 1":61
    }
    
    for name, id in leagues.items():
        if league_name in name:
            league_id = id
            break
    
    if not league_id:
        await update.message.reply_text("Championat non reconnu. Exemples : Premier League, La Liga, Serie A, Bundesliga, Ligue 1")
        return
    
    url = f"https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key":FOOTBALL}
    params = {"league": league_id, "season": 2023, "next": 5}
    
    response = requests.get(url,headers=headers,params=params)
    data = response.json()
    
    if data.get("results") == 0:
        await update.message.reply_text("Aucun match trouvé pour ce championnat.")
        return
    
    fixtures = data.get("response", [])
    message = f"📅 Prochains matchs de {league_name.title()}:\n\n"
    
    for fixture in fixtures:
        teams = fixture["teams"]
        date = fixture["fixture"]["date"]
        venue = fixture["fixture"]["venue"]["name"]
        message += f"{teams['home']['name']} vs {teams['away']['name']}\nDate: {date}\nLieu: {venue}\n\n"
    
    await update.message.reply_text(message)
    
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
    app.add_handler(CommandHandler("google",open_google))
    app.add_handler(CommandHandler("play",play))
    app.add_handler(CommandHandler("video",youtube_se))
    app.add_handler(CommandHandler("football",football))
    app.add_handler(CommandHandler("news",news))
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
    app.add_handler(CommandHandler("google",open_google))
    app.add_handler(CommandHandler("play",play))
    app.add_handler(CommandHandler("video",youtube_se))
    app.add_handler(CommandHandler("football",football))
    app.add_handler(CommandHandler("news",news))
    app.add_handler(CommandHandler("meteo",meteo))
    
    # Lancement du bot
    print("Machine_Bot a démarré...")
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))
    
    app.run_polling()

   

