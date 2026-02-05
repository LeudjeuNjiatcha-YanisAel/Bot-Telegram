from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Core.users import users,save_users
import asyncio


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
        "📩 /sendall message → Envoyer un message a tous les utilisateurs\n"
        "🎮️ /squidgame → Demarrer Un Jeu\n"
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
        "╔════════════════════════════╗\t\t\t\t\n"
        "     🤖 *Machine_11bot* 🤖\n"
        "╚════════════════════════════╝\t\t\t\t\n\n"
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