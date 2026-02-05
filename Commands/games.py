import asyncio
import random

nd = 0 
np = 0
nc = 0

money = {}
async def dice(update,context):
    await update.message.reply_text("Vous avez choisir le *Jeu Tire un Dé*",parse_mode="Markdown")
    result = random.randint(1,6)
    await asyncio.sleep(2)
    await update.message.reply_text(f"🎲 Le dé a roulé tu as obtenu : *{result}*\n",parse_mode="Markdown")
    if result == 6:
        user = update.message.from_user.id
        money[user] = 100
        await update.message.reply_text(f"Votre gain est de {money[user]} FCFA")
    else :
        await update.message.reply_text(f"Votre gain est de {money[user]} FCFA")
    
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
            await update.message.reply_text("Veuillez Choisir Ciseau ✂️\t,Pierre 🔨\t,Feuille 📝️\t")
            await update.message.reply_text("⚠️ Usage : Tape /shifumi pierre ou /shifumi feuille ou /shifumi ciseau")
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
        await update.message.reply_text("...")
        
        
async def squidgame(update,context):
    global user_numbers
    user = update.message.from_user.id
    if user not in user_numbers:
        number = random.randint(1,456)
        user_numbers[user] = number
        await update.message.reply_text("🎮 Bienvenue dans SquidGame! 🎮\t")
        await update.message.reply_text(f"Joueur N°{number}")
        await update.message.reply_text("Jeux Disponibles : ")
        await update.message.reply_text(f"1./dice")
        await update.message.reply_text(f"2./piece")
        await update.message.reply_text(f"3./shifumi ex : /shifumi ciseau")
        await update.message.reply_text("4./quit Quitter la partie ")
        await update.message.reply_text("Choisis un jeu en tapant son nom (ex: /dice)")
    else:
        number = user_numbers[user]
        await update.message.reply_text(f"Tu es déjà dans la partie, joueur N°{number}")
        await update.message.reply_text("Jeux Disponibles : ")
        await update.message.reply_text(f"1./dice")
        await update.message.reply_text(f"2./piece")
        await update.message.reply_text(f"3./shifumi ex : /shifumi ciseau")
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