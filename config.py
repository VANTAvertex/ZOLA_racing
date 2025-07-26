import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()

# Configuration du bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# Configuration du jeu
GAME_LEVELS = {
    "tesla": {
        "name": "🚗 Tesla VS Zola 🐆 (Easy)",
        "time_limit": 30,
        "target_score": 50,
        "emoji": "🚗"
    },
    "porsche": {
        "name": "🏎️ Porsche VS Zola 🐆 (Hard)", 
        "time_limit": 20,
        "target_score": 100,
        "emoji": "🏎️"
    },
    "bugatti": {
        "name": "🏁 Bugatti VS Zola 🐆 (Legend)",
        "time_limit": 15,
        "target_score": 150,
        "emoji": "🏁"
    }
}

# Messages du bot
MESSAGES = {
    "welcome": """
🏎️ **Welcome in Zola Click Race !**

A speed game where you have to click as quickly as possible !

Choose your level :
• Tesla (Easy) - 30 seconds
• Porsche (Hard) - 20 seconds  
• Bugatti (Legend) - 15 seconds

Tape /play pour commencer !
""",
    "choose_level": "🏁 Choose your speed level :",
    "game_finished": "🎉 Partie terminée ! Score : {score} points en {level}"
}
