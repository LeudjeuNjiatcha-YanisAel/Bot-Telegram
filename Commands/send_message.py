from Core.users import users

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

async def sendall(update,context):
    id = update.message.from_user.id
    owner = 5441882239
    own = 7799721970
    tasks = []
    message = " ".join(context.args)
    if str(id) == str(owner) or str(id) == str(own):
        for chat_id in users.keys():
            try:
                task = asyncio.create_task(await app.bot.send_message(chat_id=int(chat_id),text=message))
                tasks.append(task)
                await asyncio.gather(*tasks,return_exceptions=True)
            except Exception as e:
                print(f"Erreur en envoyant à {chat_id}: {e}")
    else :
        await update.message.reply_text("❌ Vous Devez Etre Administrateur Pour Utiliser Cette Commande")