from gnews import GNews

google_news = GNews(language='fr',country='FR',period='7d',max_results=5)

def call_news(category_or_keyword="general",max_results=5):
    """
    Récupère soit une catégorie de news, soit une recherche par mot-clé,
    avec titre, résumé et URL.
    """
    category_map = {
        "general": "À la une",
        "business": "Économie",
        "entertainment": "Divertissement",
        "health": "Santé",
        "science": "Science",
        "sports": "Sports",
        "technology": "Technologie"
    }

    # Si c'est une catégorie connue
    if category_or_keyword in category_map:
        topic = category_map[category_or_keyword]
        try:
            articles = google_news.get_news_by_topic(topic)
        except Exception as e:
            return [(f"Erreur lors de la récupération des news (topic): {e}", "", "")]
    else:
        # Sinon mot-clé
        try:
            articles = google_news.get_news(category_or_keyword)
        except Exception as e:
            return [(f"Erreur lors de la récupération des news (keyword): {e}", "", "")]

    if not articles:
        return [("Aucune actualité trouvée", "", "")]

    # On prend titre, description et URL
    results = []
    for a in articles[:max_results]:
        title = a.get("title", "Sans titre")
        desc = a.get("description", "Pas de résumé disponible")
        url = a.get("url", "")
        results.append((title, desc, url))
    return results


async def news(update,context):
    if not context.args:
        await update.message.reply_text(
            "Utilisation : /news <categorie|mot-clé>\n\n"
            "Catégories disponibles : business, entertainment, general, health, science, sports, technology\n"
            "Exemples :\n"
            "   /news sports\n"
            "   /news Messi"
        )
        return

    query = context.args[0].lower()
    await update.message.reply_text("Recherche des news en cours... ⏳")

    articles = call_news(query, max_results=5)

    for title, desc, url in articles:
        message = f"📰 *{title}*\n\n📝 {desc}\n\n🔗 {url}"
        await update.message.reply_text(message, parse_mode="Markdown")

    print("✅ News avec résumés affichées !")
