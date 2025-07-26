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
        "name": "🚗 Tesla VS Zola 🐆 (Facile)",
        "time_limit": 30,
        "target_score": 50,
        "emoji": "🚗"
    },
    "porsche": {
        "name": "🏎️ Porsche VS Zola 🐆 (Moyen)", 
        "time_limit": 20,
        "target_score": 100,
        "emoji": "🏎️"
    },
    "bugatti": {
        "name": "🏁 Bugatti VS Zola 🐆 (Difficile)",
        "time_limit": 15,
        "target_score": 150,
        "emoji": "🏁"
    }
}

# Messages du bot
MESSAGES = {
    "welcome": """
🏎️ **Bienvenue dans Zola Click Race !**

Un jeu de rapidité où tu dois cliquer le plus vite possible !

Choisis ton niveau :
• Tesla (Facile) - 30 secondes
• Porsche (Moyen) - 20 secondes  
• Bugatti (Difficile) - 15 secondes

Tape /play pour commencer !
""",
    "choose_level": "🏁 Choisis ton niveau de difficulté :",
    "game_finished": "🎉 Partie terminée ! Score : {score} points en {level}"
}
