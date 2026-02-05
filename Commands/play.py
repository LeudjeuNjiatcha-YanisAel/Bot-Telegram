import os
import tempfile
import subprocess

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