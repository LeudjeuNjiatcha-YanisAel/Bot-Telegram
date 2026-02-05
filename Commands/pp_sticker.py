from PIL import Image
from io import BytesIO

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