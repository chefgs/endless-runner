const socket = io();
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game constants
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 400;

let gameState = null;
let gameOver = false;

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('game_state', (state) => {
    gameState = state;
    if (!gameOver) {
        drawGame();
    }
});

socket.on('game_over', (state) => {
    gameOver = true;
    drawGameOverScreen(state);
});

document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' && !gameOver) {
        socket.emit('jump');
    }
    if ((event.key === 'r' || event.key === 'R') && gameOver) {
        gameOver = false;
        socket.emit('restart_game');
    }
});

function drawGame() {
    // Clear canvas
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    
    // Draw player
    ctx.fillStyle = 'blue';
    ctx.fillRect(100, gameState.player_y, 40, 50);
    
    // Draw hurdles
    ctx.fillStyle = 'red';
    gameState.hurdles.forEach(hurdle => {
        ctx.fillRect(hurdle.x, hurdle.y, hurdle.width, hurdle.height);
    });
    
    // Draw tools
    ctx.fillStyle = 'green';
    gameState.tools.forEach(tool => {
        ctx.fillRect(tool.x, tool.y, tool.width, tool.height);
    });
    
    // Draw score
    ctx.font = '20px Arial';
    ctx.fillStyle = 'black';
    ctx.fillText(`Score: ${gameState.score} Level: ${gameState.level}`, 10, 30);
}

function drawGameOverScreen(state) {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    
    ctx.font = '30px Arial';
    ctx.fillStyle = 'white';
    ctx.textAlign = 'center';
    ctx.fillText('Game Over!', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40);
    ctx.fillText(`Final Score: ${state.score}`, SCREEN_WIDTH/2, SCREEN_HEIGHT/2);
    ctx.fillText('Press R to Restart', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40);
}

function gameLoop() {
    if (!gameOver) {
        socket.emit('update');
    }
    requestAnimationFrame(gameLoop);
}

gameLoop();