from Config.config import leagues,FOOTBALL,URL
from datetime import datetime,timedelta
import requests
import asyncio

# ---- Fonction utilitaire pour prédiction ----
def predict_match(home_rank, away_rank, home_form, away_form, home_goals, away_goals):
    """Retourne une prédiction simple basée sur classement, forme et buts."""
    score = 0
    if home_rank and away_rank:
        score += (away_rank - home_rank) * 0.4
    score += (home_form - away_form) * 0.3
    score += (home_goals - away_goals) * 0.3
    if score > 0.5:
        return "Victoire probable de l’équipe à domicile 🏠"
    elif score < -0.5:
        return "Victoire probable de l’équipe à l’extérieur ✈️"
    else:
        return "Match serré — nul probable 🤝"

async def football(update,context):
    # Afficher la liste des championnats disponibles
    ligues_dispo = "\n".join([f"- {nom.title()}" for nom in leagues.keys()])
    await update.message.reply_text(f"🏆 Championnats disponibles :\n + {ligues_dispo}")
    await update.message.reply_text("Recherche des matchs en cours et à venir... ⏳")
    await asyncio.sleep(2)
    
    if not context.args:
        await update.message.reply_text(
            "Utilisation : /football <nom du championnat>\n"
            "Exemples : /football premier league, /football can\n\n"
        )

    league_name = " ".join(context.args).lower()
    league_id = leagues.get(league_name)

    if not league_id:
        await update.message.reply_text("❌ Championnat inconnu.")
        return

    headers = {"X-Auth-Token":FOOTBALL}

    # Période : aujourd'hui jusqu'à 14 jours dans le futur
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=14)

    url = (
        f"{URL}/competitions/{league_id}/matches"
        f"?dateFrom={today}&dateTo={end_date}&status=LIVE,FINISHED,SCHEDULED"
    )
    response = requests.get(url,headers=headers)
    data = response.json()
    if "matches" not in data or not data["matches"]:
        await update.message.reply_text("Aucun match prévu ou joué pour cette période.")
        return

    message = f"📅 *Matchs récents et à venir — {league_name.title()}*\n\n"

    # Récupérer le classement pour prédiction
    standings_url = f"{URL}/competitions/{league_id}/standings"
    standings_resp = requests.get(standings_url, headers=headers).json()
    table = standings_resp.get("standings", [{}])[0].get("table", [])

    for match in data["matches"]:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        status = match["status"]
        match_date = match["utcDate"][:10]

        # Scores si disponibles
        home_score = match["score"]["fullTime"]["home"]
        away_score = match["score"]["fullTime"]["away"]

        # 1️⃣ Match terminé
        if status in ["FINISHED", "AWARDED"]:
            message += f"Termine🏁 {home} {home_score} - {away_score} {away} (le {match_date})\n\n"

        # 2️⃣ Match en cours
        elif status == "LIVE":
            message += f"🔥 En direct : {home} {home_score or 0} - {away_score or 0} {away} (le {match_date})\n\n"

        # 3️⃣ Match à venir
        else:
            home_rank = away_rank = home_form = away_form = home_goals = away_goals = None

            # Chercher dans le classement
            for t in table:
                if t["team"]["name"] == home:
                    home_rank = t["position"]
                    home_form = t["points"]
                    home_goals = t["goalsFor"]
                if t["team"]["name"] == away:
                    away_rank = t["position"]
                    away_form = t["points"]
                    away_goals = t["goalsFor"]

            prediction = predict_match(
                home_rank, away_rank,
                home_form or 0, away_form or 0,
                home_goals or 0, away_goals or 0
            )
            message += f"⚽ {home} vs {away} (prévu le {match_date})\n🔮 {prediction}\n\n"

    await update.message.reply_text(message, parse_mode="Markdown")