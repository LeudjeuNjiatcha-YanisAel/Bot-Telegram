# 🤖 Machine_11Bot

## 📌 Description

**Machine_11Bot** est un bot **Telegram multifonctions** développé en **Python**.
Il propose des outils pratiques comme :

* 🧮 **Mathématiques** (additions, multiplications, divisions, etc.)
* 💬 **Messagerie privée** entre utilisateurs du bot
* 🌦 **Météo** avec OpenWeather API
* ⏰ **Heure locale** d’une ville (API TimeZoneDB)
* 🎼 **Téléchargement et lecture de musiques** (via `yt-dlp`)
* 🤖 **Intelligence Artificielle** (réponses avec **Google Gemini**)
* 📝 **Utilitaires divers** : PIN, phrases aléatoires, Google, nettoyage de chat, etc.

Le bot sauvegarde automatiquement les **utilisateurs enregistrés** dans un fichier JSON.

---

## ⚙️ Fonctionnalités principales

### 🔹 Commandes générales

* `/start` → Démarre et enregistre l’utilisateur
* `/help` → Liste toutes les commandes
* `/about` → Infos sur le bot

### 🔹 Mathématiques

* `/add x y` → Addition
* `/sub x y` → Soustraction
* `/mul x y` → Multiplication
* `/div x y` → Division
* `/mod x y` → Modulo

### 🔹 Messagerie

* `/msg chat_id texte` → Envoyer un message par **ID**
* `/send Nom message` → Envoyer à un utilisateur par nom ou username
* `/clear` → Nettoyer la messagerie (ou supprimer 50 messages dans un groupe)
* `/listusers` → Liste des utilisateurs enregistrés
* `/getid` → Voir ton **chat_id**

### 🔹 Utilitaires

* `/gen_phrase mots…` → Générer une phrase aléatoire
* `/pin` → Générer un code PIN (4 chiffres)
* `/google` → Lien direct vers Google
* `/time ville` → Heure locale d’une ville
* `/meteo ville` → Météo locale (°C, humidité, description)

### 🔹 Musique

* `/play titre` → Recherche et télécharge une musique en MP3 via **yt-dlp**

### 🔹 Intelligence Artificielle

* `/ask question` → Poser une question au bot (**Gemini AI**)
* Réponse automatique en groupe si on mentionne `@Machine_11Bot`

---

## 🛠️ Technologies utilisées

* **Python 3**
* **Telegram Bot API** (`python-telegram-bot`)
* **OpenWeather API** (Météo)
* **TimeZoneDB API** (Heure locale)
* **Google Generative AI (Gemini)**
* **yt-dlp** (Téléchargement audio)
* **JSON** (stockage utilisateurs et météo)

---

## 📂 Fichiers

* `main.py` → Script principal du bot
* `users.json` → Sauvegarde des utilisateurs
* `meteo.json` → Historique météo consulté
* `music/` → Dossier contenant les musiques téléchargées

---

## ⚡ Installation et configuration

### 1. Cloner le projet

```bash
git clone https://github.com/votre-repo/Machine_11Bot.git
cd Machine_11Bot
```

### 2. Installer les dépendances

```bash
pip install python-telegram-bot requests google-genai
```

⚠️ Il faut aussi installer **yt-dlp** :

```bash
pip install yt-dlp
```

### 3. Configurer les clés API

* **Telegram Bot** : créer un bot avec [@BotFather](https://t.me/BotFather) et récupérer le **TOKEN**
* **Météo (OpenWeather)** : [openweathermap.org](https://openweathermap.org/)
* **Heure (TimeZoneDB)** : [timezonedb.com](https://timezonedb.com/)
* **Google Gemini** : [ai.google.dev](https://ai.google.dev/)

Remplacer les clés dans le script :

```python
TOKEN = "VOTRE_TOKEN_TELEGRAM"
METEO_API = "VOTRE_CLE_METEO"
KEY_TIME = "VOTRE_CLE_TIMEZONE"
```

### 4. Lancer le bot

```bash
python main.py
```

---

## 🎯 Exemple d’utilisation

```
Utilisateur → /start
Bot → Salut Machine, tu es maintenant enregistré ✅
     Bienvenue dans Machine_11Bot 🤖

Utilisateur → /add 5 7
Bot → Résultat : 5 + 7 = 12

Utilisateur → /meteo Paris
Bot → Ville : Paris
       Température : 18°C
       Humidité : 65%
       Description : ciel dégagé
```

---

## ✅ Améliorations futures

* Détection automatique du **sentiment** dans les messages
* Support pour **traduction multilingue**
* Exportation des données en **CSV / JSON**
* Interface Web (Streamlit ou Flask) pour gérer les utilisateurs

---

## 👨‍💻 Auteur

* **Machine** (Concepteur du bot)
* 📱 Contact : [WhatsApp](https://wa.me/237620834784)
* 🔗 Lien du bot : [Machine_11Bot sur Telegram](https://t.me/Machine_11bot)
