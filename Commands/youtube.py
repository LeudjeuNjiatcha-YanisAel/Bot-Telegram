from Config.config import youtube_api
import asyncio
from google import genai
from google.genai import types
from googleapiclient.discovery import build

youtube = build("youtube","v3",developerKey=youtube_api)

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
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
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