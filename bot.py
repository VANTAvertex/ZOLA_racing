import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import BOT_TOKEN, WEBAPP_URL, GAME_LEVELS, MESSAGES

# Configuration des logs pour déboguer
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation du bot et du dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Stockage temporaire des scores (en production, utilise une vraie DB)
user_scores = {}

@dp.message(CommandStart())
async def start_command(message: types.Message):
    """
    Utilité : Accueille l'utilisateur et explique le jeu
    Déclenché par : /start
    """
    await message.answer(
        MESSAGES["welcome"],
        parse_mode="Markdown"
    )

@dp.message(Command("play"))
async def play_command(message: types.Message):
    """
    Utilité : Affiche les boutons pour choisir le niveau
    Déclenché par : /play
    """
    # Création des boutons pour chaque niveau
    keyboard_buttons = []
    
    for level_key, level_data in GAME_LEVELS.items():
        button = InlineKeyboardButton(
            text=level_data["name"],
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?level={level_key}")
        )
        keyboard_buttons.append([button])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(
        MESSAGES["choose_level"],
        reply_markup=keyboard
    )

@dp.message(Command("scores"))
async def scores_command(message: types.Message):
    """
    Utilité : Affiche les meilleurs scores de l'utilisateur
    Déclenché par : /scores
    """
    user_id = message.from_user.id
    
    if user_id not in user_scores:
        await message.answer("🤷‍♂️ Tu n'as pas encore joué ! Tape /play pour commencer.")
        return
    
    scores_text = "🏆 **Tes meilleurs scores :**\n\n"
    for level, score in user_scores[user_id].items():
        level_emoji = GAME_LEVELS[level]["emoji"]
        scores_text += f"{level_emoji} {GAME_LEVELS[level]['name']}: {score} points\n"
    
    await message.answer(scores_text, parse_mode="Markdown")

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    """
    Utilité : Reçoit et traite les données de la WebApp (scores)
    Déclenché par : Quand la WebApp envoie des données
    """
    try:
        # Parse les données JSON envoyées par la WebApp
        data = json.loads(message.web_app_data.data)
        
        user_id = message.from_user.id
        score = data.get("score", 0)
        level = data.get("level", "tesla")
        time_played = data.get("time", 0)
        
        # Validation basique anti-triche
        max_possible_score = GAME_LEVELS[level]["time_limit"] * 14  # 14 clics/seconde max
        if score > max_possible_score:
            await message.answer("🚫 Score suspect détecté ! Essaie de jouer normalement.")
            return
        
        # Sauvegarde du score
        if user_id not in user_scores:
            user_scores[user_id] = {}
        
        # Garde seulement le meilleur score par niveau
        if level not in user_scores[user_id] or score > user_scores[user_id][level]:
            user_scores[user_id][level] = score
            is_new_record = True
        else:
            is_new_record = False
        
        # Message de réponse
        level_name = GAME_LEVELS[level]["name"]
        response = f"🎮 **Partie terminée !**\n\n"
        response += f"Niveau : {level_name}\n"
        response += f"Score : {score} points\n"
        response += f"Temps : {time_played}s\n"
        
        if is_new_record:
            response += f"\n🎉 **Nouveau record personnel !**"
        
        response += f"\n\nTape /play pour rejouer ou /scores pour voir tes records !"
        
        await message.answer(response, parse_mode="Markdown")
        
    except json.JSONDecodeError:
        await message.answer("❌ Erreur lors de la réception des données du jeu.")
    except Exception as e:
        logger.error(f"Erreur dans handle_web_app_data: {e}")
        await message.answer("❌ Une erreur s'est produite.")

@dp.message()
async def unknown_command(message: types.Message):
    """
    Utilité : Répond aux messages non reconnus
    Déclenché par : Tout message qui ne correspond à aucune commande
    """
    await message.answer(
        "🤔 Je ne comprends pas cette commande.\n\n"
        "Commandes disponibles :\n"
        "• /start - Commencer\n"
        "• /play - Jouer\n"
        "• /scores - Voir tes scores"
    )

async def main():
    """
    Utilité : Lance le bot et commence à écouter les messages
    """
    logger.info("🚀 Démarrage du bot...")
    
    # Supprime les anciens webhooks si ils existent
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Démarre le polling (écoute des messages)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Point d'entrée du programme
    asyncio.run(main())
