// Configuration du jeu
const GAME_CONFIG = {
    tesla: { time: 30, emoji: '🚗', name: 'Tesla' },
    porsche: { time: 20, emoji: '🏎️', name: 'Porsche' },
    bugatti: { time: 15, emoji: '🏁', name: 'Bugatti' }
};

// Variables globales du jeu
let gameState = {
    level: 'tesla',
    score: 0,
    timeLeft: 30,
    gameActive: false,
    startTime: null,
    gameTimer: null,
    clickTimes: []
};

// Éléments DOM
const elements = {
    prepareScreen: document.getElementById('prepare-screen'),
    gameScreen: document.getElementById('game-screen'),
    finishScreen: document.getElementById('finish-screen'),
    levelTitle: document.getElementById('level-title'),
    levelDescription: document.getElementById('level-description'),
    countdown: document.getElementById('countdown'),
    startBtn: document.getElementById('start-btn'),
    clickButton: document.getElementById('click-button'),
    buttonEmoji: document.getElementById('button-emoji'),
    timeLeft: document.getElementById('time-left'),
    currentScore: document.getElementById('current-score'),
    progressFill: document.getElementById('progress-fill'),
    finalScore: document.getElementById('final-score'),
    finalTime: document.getElementById('final-time'),
    cps: document.getElementById('cps'),
    sendScoreBtn: document.getElementById('send-score-btn'),
    playAgainBtn: document.getElementById('play-again-btn')
};

/**
 * Initialise le jeu au chargement de la page
 * Utilité : Configure le niveau selon l'URL et prépare l'interface
 */
function initGame() {
    // Récupère le niveau depuis l'URL
    const urlParams = new URLSearchParams(window.location.search);
    gameState.level = urlParams.get('level') || 'tesla';
    
    // Configure l'interface selon le niveau
    const config = GAME_CONFIG[gameState.level];
    gameState.timeLeft = config.time;
    
    elements.levelTitle.textContent = `${config.emoji} ${config.name}`;
    elements.levelDescription.textContent = `Tu as ${config.time} secondes pour cliquer !`;
    elements.buttonEmoji.textContent = config.emoji;
    elements.timeLeft.textContent = gameState.timeLeft;
    
    // Indique à Telegram que la WebApp est prête
    if (window.Telegram?.WebApp) {
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
    }
}

/**
 * Démarre le compte à rebours avant le jeu
 * Utilité : Prépare le joueur avec un décompte de 3 secondes
 */
function startCountdown() {
    let count = 3;
    elements.startBtn.style.display = 'none';
    
    const countdownInterval = setInterval(() => {
        elements.countdown.textContent = count;
        count--;
        
        if (count < 0) {
            clearInterval(countdownInterval);
            startGame();
        }
    }, 1000);
}

/**
 * Lance le jeu principal
 * Utilité : Active le mode jeu et démarre le chronomètre
 */
function startGame() {
    // Masque l'écran de préparation
    elements.prepareScreen.style.display = 'none';
    elements.gameScreen.style.display = 'block';
    
    // Initialise l'état du jeu
    gameState.gameActive = true;
    gameState.score = 0;
    gameState.startTime = Date.now();
    gameState.clickTimes = [];
    
    // Met à jour l'affichage
    updateDisplay();
    
    // Démarre le timer principal
    gameState.gameTimer = setInterval(() => {
        gameState.timeLeft--;
        updateDisplay();
        
        if (gameState.timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

/**
 * Gère un clic sur le bouton principal
 * Utilité : Incrémente le score et enregistre le timing
 */
function handleClick() {
    if (!gameState.gameActive) return;
    
    gameState.score++;
    gameState.clickTimes.push(Date.now());
    
    // Animation visuelle du clic
    elements.clickButton.style.transform = 'scale(0.95)';
    setTimeout(() => {
        elements.clickButton.style.transform = 'scale(1)';
    }, 100);
    
    updateDisplay();
}

/**
 * Met à jour l'affichage pendant le jeu
 * Utilité : Synchronise l'interface avec l'état du jeu
 */
function updateDisplay() {
    elements.currentScore.textContent = gameState.score;
    elements.timeLeft.textContent = gameState.timeLeft;
    
    // Met à jour la barre de progression
    const config = GAME_CONFIG[gameState.level];
    const progress = ((config.time - gameState.timeLeft) / config.time) * 100;
    elements.progressFill.style.width = `${progress}%`;
}

/**
 * Termine le jeu et affiche les résultats
 * Utilité : Calcule les statistiques finales et prépare l'envoi des données
 */
function endGame() {
    gameState.gameActive = false;
    clearInterval(gameState.gameTimer);
    
    // Calcule les statistiques
    const totalTime = (Date.now() - gameState.startTime) / 1000;
    const clicksPerSecond = (gameState.score / totalTime).toFixed(1);
    
    // Affiche l'écran de fin
    elements.gameScreen.style.display = 'none';
    elements.finishScreen.style.display = 'block';
    
    // Met à jour les statistiques finales
    elements.finalScore.textContent = gameState.score;
    elements.finalTime.textContent = totalTime.toFixed(1);
    elements.cps.textContent = clicksPerSecond;
}

/**
 * Envoie le score au bot Telegram
 * Utilité : Transmet les données de jeu au bot via l'API WebApp
 */
function sendScore() {
    const gameData = {
        score: gameState.score,
        level: gameState.level,
        time: ((Date.now() - gameState.startTime) / 1000).toFixed(1),
        clicks_per_second: (gameState.score / ((Date.now() - gameState.startTime) / 1000)).toFixed(1)
    };
    
    if (window.Telegram?.WebApp) {
        // Envoie les données au bot
        Telegram.WebApp.sendData(JSON.stringify(gameData));
    } else {
        // Fallback pour les tests hors Telegram
        alert(`Score: ${gameData.score} (${gameData.level})`);
    }
}

/**
 * Redémarre le jeu
 * Utilité : Remet le jeu à zéro pour une nouvelle partie
 */
function restartGame() {
    // Remet à zéro l'état du jeu
    gameState.score = 0;
    gameState.timeLeft = GAME_CONFIG[gameState.level].time;
    gameState.gameActive = false;
    
    // Affiche l'écran de préparation
    elements.finishScreen.style.display = 'none';
    elements.prepareScreen.style.display = 'block';
    elements.startBtn.style.display = 'block';
    elements.countdown.textContent = '3';
}

// Event Listeners - Gèrent les interactions utilisateur
elements.startBtn.addEventListener('click', startCountdown);
elements.clickButton.addEventListener('click', handleClick);
elements.sendScoreBtn.addEventListener('click', sendScore);
elements.playAgainBtn.addEventListener('click', restartGame);

// Initialise le jeu au chargement de la page
document.addEventListener('DOMContentLoaded', initGame);
