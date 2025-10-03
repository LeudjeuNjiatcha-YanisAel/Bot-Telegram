import random
from random import shuffle
import datetime
import json
import os
import sys
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import subprocess
from googleapiclient.discovery import build
from google.genai import types 
from google import genai
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters

TOKEN = "8404081837:AAF9lT_adIUY8ou8LPfdUDXNqqE6DDe86K0"
USERS_FILE = "users.json"
METEO_API  = "aa2133ea80381e8a274fc15873ff5677"
KEY_TIME = "9UJS6LPXID3A"
MUSIC = "music"
youtube_api = "AIzaSyCdMKKFAzmf3Y1aZ7yQw8FgXJC6uvDsJd8"
youtube = build("youtube","v3",developerKey=youtube_api)
users = {}
jeux_en_cours1 = {}
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        try:
            users = json.load(f)
        except:
            users = {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def start(update,context):
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
        "➕ /add x y → Addition\n"
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
        "🌦 /meteo ville → Météo locale\n"
        "🤔 /ask question → Poser une question au bot\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 *Aide*\n"
        "❓ /help → Voir toutes les commandes\n"
        "   /about → Infos sur le bot-telegram\n\n"
        "_Mentionne-moi avec @NomDuBot dans un groupe pour discuter avec moi ! 🤖")
    keyboard = [
        [InlineKeyboardButton("📖 Voir l'aide", callback_data="help")],
        [InlineKeyboardButton("🌐 Google", url="https://www.google.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

def about(update,context):
    text = (
        "╔════════════════════════════╗\n"
        "     🤖 *Machine_11bot* 🤖\n"
        "╚════════════════════════════╝\n\n"
        "✨ *Version* : `13.15`\n"
        "💫 *Technologies* :\n"
        "   🥇 Python\n"
        "   🥈 VPS (Serveurs Linux)\n\n"
        "👨‍💻 *Concepteur* : *Machine*\n"
        "📱 *Contact* : [WhatsApp](https://wa.me/237620834784)\n\n"
        "🎁 *Lien du bot* : [Clique ici](https://t.me/Machine_11bot)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ Multi-fonctions : Maths, Musique, Météo, Jeux, IA\n"
        "━━━━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = [
        [InlineKeyboardButton("📖 Aide",callback_data="help_command")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
def help_command(update,context):
    update.message.reply_text(
        "📖 *Aide - Machine_11bot* 📖\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧮 *Mathématiques*\n"
        "/add x y → Addition\n"
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
        "/meteo ville → Météo locale\n"
        "/ask question → Poser une question au bot\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 *Aide*\n"
        "/help → Afficher cette aide\n"
        "/about → Informations sur le bot\n"
        "Mentionne-moi avec @NomDuBot dans un groupe pour discuter avec moi ! 🤖"
    )

def add(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        update.message.reply_text(f"Résultat : {n1} + {n2} = {n1+n2}")
        print("La fonction addition a été utiliser avec succès!")
    except:
        update.message.reply_text("Usage : /add 'nombre1' 'nombre2'")

def sub(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        update.message.reply_text(f"Résultat : {n1} - {n2} = {n1-n2}")
        print("La fonction soustraction a été utiliser avec succès!")
    except:
        update.message.reply_text("Usage : /sub 'nombre1' 'nombre2'")

def mul(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        update.message.reply_text(f"Résultat : {n1} × {n2} = {n1*n2}")
        print("La fonction multiplication a été utiliser avec succès!")
    except:
        update.message.reply_text("Usage : /mul 'nombre1' 'nombre2'")

def div(update,context):
    try:
        n1 = float(context.args[0])
        n2 = float(context.args[1])
        if n2 == 0:
            update.message.reply_text("Erreur : Division par zéro ❌")
        else:
            update.message.reply_text(f"Résultat : {n1} ÷ {n2} = {n1/n2}")
            print("La fonction division a été utiliser avec succès!")
    except:
        update.message.reply_text("Usage : /div 'nombre1' 'nombre2'")
        
def mod(update,context):
    try:
        n1 = int(context.args[0])
        n2 = int(context.args[1])
        if n2 == 0:
            update.message.reply_text("Impossible d'effectuer le modulo ❌")
            print("La fonction modulo a été utiliser avec succès!")
        else:
            update.message.reply_text(f"Résultat : {n1} mod {n2} = {n1%n2}")
    except:
        update.message.reply_text("Usage : /mod 'nombre1' 'nombre2'")

def open_google(update,context):
    keyboard = [ [InlineKeyboardButton("Ouvrir Google 🌐", url="https://www.google.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Clique sur le bouton pour ouvrir Google :", reply_markup=reply_markup)
    
def gen_phrase(update,context):
    if not context.args:
        update.message.reply_text("Usage : /gen_phrase 'mot1' 'mot2' ...")
        return
    mots = context.args[:]
    shuffle(mots)
    phrase = ' '.join(mots).capitalize() + '.'
    update.message.reply_text("Voici une phrase :")
    update.message.reply_text(phrase)

def pin(update,context):
    code = "".join([str(random.randint(0, 9)) for _ in range(4)])
    update.message.reply_text(f"🔑 Ton code PIN : {code}")
    print("Un code PIN a été generer")
    
def send(update,context):
    try:
        if len(context.args) < 2:
            update.message.reply_text("❌ Utilisation : /send 'Nom' 'message'")
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
            update.message.reply_text(f"✅ Message envoyé à {name}")
            print(f"Le client {sender} a envoye un message a {name}")
        else:
            update.message.reply_text(f"❌ Utilisateur '{name}' introuvable.")
    
    except Exception as e:
        update.message.reply_text(f"⚠️ Erreur : {e}\n\n\n\nUtilisation : /send <username|full_name|id> <message>")

def msg(update,context):
    try:
        chat_id = int(context.args[0])
        texte = " ".join(context.args[1:])
        sender = update.message.from_user.first_name
        context.bot.send_message(chat_id=chat_id,text=f"📩 Message de {sender} :\n\n\n\n{texte}")
        update.message.reply_text("✅ Message envoyer avec succès !")
        print(f"Le client {sender} a envoye un message ")
    except:
        update.message.reply_text("❌ Utilisation : /msg 'chat_id' 'texte'")

def ask(update,context):
    question = " ".join(context.args)
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a poser cette question au bot : {question}")
    if not question:
        update.message.reply_text("❌ Utilisation : /ask <ta question>")
        return

    try:
        client = genai.Client(api_key="AIzaSyBXylzIdR5bMdb9NwtywO-MgJB1V134548")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )

        answer = response.text
        for i in range(0,len(answer),4096) :
            update.message.reply_text("Machine_IA🤖 : "+answer[i:i+4096])
    except Exception as e:
        update.message.reply_text(f"⚠️ Machine IA : {e}")

def met(city):
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

def meteo(update, context):
    if not context.args:
        update.message.reply_text("Utilisation : /meteo <Nom de la ville>")
        return
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter les donnees meteo ")
    
    ville = " ".join(context.args) 
    update.message.reply_text(met(ville))

def local_time(city):
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

def time(update,context): 
    if not context.args:
        update.message.reply_text("Utilisation : /time <Nom de la ville>")
        return
    
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter l'heure de sa ville")
    
    ville = " ".join(context.args)
    update.message.reply_text(local_time(ville))
    
def listusers(update,context):
    if not users:
        update.message.reply_text("❌ Aucun utilisateur enregistré.")
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
    
    update.message.reply_text(message)

def getid(update,context):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Ton chat_id est : {chat_id}")

def clear(update,context):
    chat = update.message.chat
    chat_id = chat.id
    message_id = update.message.message_id

    if chat.type == "private":
        empty_block = "\n\n".join(["\u200E" for _ in range(50)])
        update.message.reply_text("🧹 Nettoyage de ta messagerie en cours...\n\n" + empty_block + "\n\n✅ Messagerie nettoyée")
        return

    if chat.type in ["group", "supergroup"]:
        try:
            for i in range(message_id, message_id-50, -1):
                try:
                    context.bot.delete_message(chat_id=chat_id, message_id=i)
                except:
                    pass
            update.message.reply_text("✅ 50 derniers messages supprimés")
        except:
            update.message.reply_text("❌ Impossible de nettoyer (le bot doit être admin et avoir la permission de suppression)")
def send_online(bot,text):
    for chat_id in users.keys():
        try:
            print("Message envoye ! ✅")
            bot.send_message(chat_id=int(chat_id), text=text)
        except Exception as e:
            print(f"Erreur en envoyant à {chat_id}: {e}")
            
def auto_reply(update,context):
    bot_username = context.bot.username.lower()
    text = update.message.text.lower()
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a envoye ce message : {text} au bot ")
    
    if (update.message.chat.type != 'private') and (f"@{bot_username}" not in text):
        return
    text = text.replace(f"@{bot_username}", "").strip()
    
    if "bonjour" in text or "salut" in text or "bjr" in text or "yo" in text:
        reply = "Salut 👋 comment tu vas ?"
        update.message.reply_text("🤖Machine_Bot🤖 : " + reply)
    elif "ça va" in text:
        reply = "Oui ça va très bien merci 🤖 et toi ?"
        update.message.reply_text("🤖Machine_Bot🤖 : " + reply)
    elif "bien" in text:
        reply = "Idem de mon cote"
        update.message.reply_text("🤖Machine_Bot🤖 : " + reply)
    elif "merci" in text:
        reply = "Avec plaisir 😎"
        update.message.reply_text("🤖Machine_Bot🤖 : " + reply)
    elif "heure" in text:
        # Vérifier si l’utilisateur a demandé l’heure dans une ville spécifique
        if "en " in text or "a" in text:
            try:
                ville = text.split("en", 1)[1].strip()
                heure_ville = local_time(ville)
                reply = f"⏰ Il est actuellement {heure_ville} à {ville.title()}"
            except Exception as e:
                reply = f"❌ Impossible de récupérer l'heure demandée ({e})"
                reply = "Rassurer-vous entrer le nom d'une ville existant !"
        else:
            now = datetime.datetime.now()
            reply = f"⏰ Il est actuellement {now.strftime('%H:%M:%S')} au Cameroun"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "imbécile" in text:
        reply = "Et toi tu es idiot"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "ton nom" in text or "qui est tu" in text:
        reply = "Je suis ton bot multifonctions 🤖 créé par Machine 😎"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "idiot" in text or "fou" in text or "tu es bete" in text:
        reply = "Va te faire foutre🖕️"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "mouf" in text:
        reply = "Sale Gros con "
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "con" in text:
        reply = "Espece de feignant"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "ta maman" in text :
        reply = "Ca ne m'atteint pas "
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "acer" in text or "asser" in text:
        reply = "Que veux tu faire aujourd'hui"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "enfoirés" in text:
        reply = "Ignorant"
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    elif "ton cu" in text:
        reply = "Stupide que tu es "
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
        reply = "Encule 🖕️ "
        update.message.reply_text("🤖Machine_Bot🤖 : " +reply)
    else:
        try:
            client = genai.Client(api_key="AIzaSyBXylzIdR5bMdb9NwtywO-MgJB1V134548")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=text
            )
            answer = response.text
            for i in range(0, len(answer), 1000):
                update.message.reply_text("🤖Machine_Bot🤖 : " + answer[i:i+1500])
        except Exception as e:
            print(f"Erreur API Gemini : {e}")
            update.message.reply_text("⚠️ Impossible de causer avec le bot pour le moment, réessaie plus tard.")

def search_video(name):
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
def info_playlist(playlist_id):
    request = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=50)
    
    response = request.execute()
    total_videos = response.get("pageInfo",{}).get("totalResults",0)
    return total_videos

# Code Pour Les Commentaires
def commentaries(video_id,max_results=10):
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
def analyse_playlist(playlist_id,playlist_title):
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
    model = "gemini-2.5-flash"

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
def analyse_comments(comments):
    client = genai.Client(api_key=("AIzaSyAQBpi-rDqpY4rqSZbeFc0Szjg0dsCYixQ"))
    # Ici on prend les commentaires les plus likes
    input_text = "\n".join(
        [f"- {txt} ({likes} likes)" for txt,likes in sorted(comments,key=lambda x:x[1],reverse=True)[:5]]
    )

    prompt = f"""Voici des commentaires d'une vidéo récupérés sur YouTube : {input_text}
    Analyse ces commentaires et dit moi ci en 1 la video est pertinente , en 2 pour quelle type de spectatuers c'est reserver , en 3 tu donne une note /10 pour la pertinence , 
    en 4 tu donne une raison pour laquelle tu recommanderait cette video
    ."""

    model = "gemini-2.5-flash"

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


def youtube_se(update,context):
    if not context.args :
        update.message.reply_text("Utilisation correcte /video <nom de la video a rechercher>")
        return 
    
    name = " ".join(context.args)      
    (video_id,title,likes,vues),(playlist_id,playlist_title) = search_video(name)

    # Partie vidéo
    update.message.reply_text(f"\n\tVideo trouvee : {title} ✅")
    update.message.reply_text(f"lien ▶️: https://www.youtube.com/watch?v={video_id}")
    update.message.reply_text(f"Nombres De Likes 👍 : {likes} | 👁️ Vues : {vues} ")
    print("Video Afficher Avec Succes ✅")
    update.message.reply_text("Analyses des commentaires des differentes video ...")

    # Récupération des commentaires
    comment = commentaries(video_id)
    recommandation = analyse_comments(comment)

    update.message.reply_text("Meilleur Commentaire Trouvee ")
    update.message.reply_text(f"{len(comment)} commentaires recuperes.")
    update.message.reply_text("\n=== Video recommandee a partir des commentaires ===")
    update.message.reply_text(recommandation)
    print("Recommandation Afficher Avec Succes ✅")
    update.message.reply_text("\n")

    # Partie playlist
    update.message.reply_text(f"\n\t=== 📂 Meilleure Playlist Trouvée Pour {name} : {playlist_title} ===")
    update.message.reply_text(f"-URL de la playlist : https://www.youtube.com/playlist?list={playlist_id}")
    print("Playlist Afficher Avec Succes ✅")

    total = info_playlist(playlist_id)
    update.message.reply_text(f" 📺Nombre De Video De La Playlist {total} videos")
    update.message.reply_text("\n=== Recommandation de la Playlist ===")
    analyse = analyse_playlist(playlist_id, playlist_title)
    update.message.reply_text(analyse)

    
def play(update,context):
    if not context.args:
        update.message.reply_text("Utilisation de la commande : /play <nom de la musique>")
    # musique a rechercher
    music_query = " ".join(context.args)
    user = update.message.from_user
    
    # ici on verifie que le dossier MUSIC sinon on le cree
    os.makedirs(MUSIC,exist_ok=True)
    
    # Modèle de nom qu'on utilisera en sortie par exemple titre.mp3
    output_path = os.path.join(MUSIC,"%(title).50s.%(ext)s")

    # Dans cette partie nous commençons a telecharger le media
    try :
        subprocess.run([
            # Ici on appelle la commande yt-dlp
            "yt-dlp",
            # Extrait slt l'audio
            "--extract-audio",
            # Convertit le fichier en mp3
            "--audio-format", "mp3",   
            # On définit la qualité correcte
            "--audio-quality", "192K",
            # Ici on accepte les cookiers du navigateur
            "--cookies-from-browser", "chrome",
            # On indique le modele de nom du fichier
            "-o",output_path,
            # La derniere etape c'est la recherche
            f"ytsearch1:{music_query}"],check=True)
        
        # Ici on liste les fichiers du dossier ça donne ts les fichiers contenus dans le dossier
        files = os.listdir(MUSIC)
        
        # Ici on recupere les fichiers .mp3
        files = [f for f in files if f.endswith("mp3")]
        
        # C'est pour recuperer la date et heure de la derniere modification via getmtime
        files.sort(key=lambda f: os.path.getmtime(os.path.join(MUSIC,f)))
        
        # Prend le dernier fichier telecharger
        latest_file = os.path.join(MUSIC,files[-1])
        
        with open(latest_file,"rb") as audio:
            update.message.reply_audio(audio)
        update.message.reply_text("Voici ta musique !")
    except Exception as e:
        update.message.reply_text(f"Erreur : {e}")        

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("add",add))
    dp.add_handler(CommandHandler("sub",sub))
    dp.add_handler(CommandHandler("mul",mul))
    dp.add_handler(CommandHandler("div",div))
    dp.add_handler(CommandHandler("mod",mod))
    dp.add_handler(CommandHandler("pin",pin))
    dp.add_handler(CommandHandler("gen_phrase",gen_phrase))
    dp.add_handler(CommandHandler("msg",msg))
    dp.add_handler(CommandHandler("send",send))
    dp.add_handler(CommandHandler("about",about))
    dp.add_handler(CommandHandler("listusers",listusers))
    dp.add_handler(CommandHandler("getid",getid))
    dp.add_handler(CommandHandler("time",time))
    dp.add_handler(CommandHandler("clear",clear))
    dp.add_handler(CommandHandler("ask",ask))
    dp.add_handler(CommandHandler("google",open_google))
    dp.add_handler(CommandHandler("play",play))
    dp.add_handler(CommandHandler("video",youtube_se))
    dp.add_handler(CommandHandler("meteo",meteo))
   
    print("Machine_Bot a démarré...")
    send_online(updater.bot,"🤖 Le bot est en ligne ✅")    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command,auto_reply))
    def handle_exit(sig,frame):
        print("Arrêt du bot...")
        send_online(updater.bot," 🤖 Le bot a été déconnecté par son proprietaire ❌")
        sys.exit(0)

    #capter les signaux d’arrêt (CTRL+C, kill, systemd, etc.)

    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGTSTP, handle_exit)
   
    updater.start_polling()
    updater.idle()

main()
