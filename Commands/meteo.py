import requests
import datetime
import json
from Config.config import KEY_TIME,METEO_API

async def met(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={METEO_API}&units=metric&lang=fr"
    reponse = requests.get(url)
    if reponse.status_code == 200:
        data = reponse.json()
    
        meteo = {
            "Ville":data["name"],
            "Temperature":data["main"]["temp"],
            "Humidite":data["main"]["humidity"],
            "Description":data["weather"][0]["description"],
            "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("meteo.json","a",encoding="utf-8") as f:
            f.write(json.dumps(meteo,ensure_ascii=False) + "\n")
            print("Donnees meteo enregistrees avec succes !")
        return f"Ville : {meteo['Ville']}\nTemperature : {meteo['Temperature']}°C\nHumidite : {meteo['Humidite']}%\nDescription : {meteo['Description']}"
    else :
        return "❌ Erreur lors de la recuperation : "

async def meteo(update,context):
    if not context.args:
        await update.message.reply_text("Utilisation : /meteo <Nom de la ville>")
        return
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter les donnees meteo ")
    
    ville = " ".join(context.args) 
    await update.message.reply_text(await met(ville))

async def local_time(city):
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