import asyncio

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