from Commands.meteo import local_time

async def times(update,context): 
    if not context.args:
        await update.message.reply_text("Utilisation : /time <Nom de la ville>")
        return
    
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter l'heure de sa ville")
    
    ville = " ".join(context.args)
    await update.message.reply_text(await local_time(ville))