from Core.users import users

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