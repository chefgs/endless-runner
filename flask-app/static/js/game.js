const socket = io();

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let gameState = {};

socket.on('game_state', (state) => {
    gameState = state;
    drawGame();
});

document.addEventListener('keydown', (event) => {
    if (event.code === 'Space') {
        socket.emit('jump');
    }
});

function drawGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw player
    ctx.fillStyle = 'black';
    ctx.fillRect(100, gameState.player_y, 50, 50);

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
    ctx.fillStyle = 'black';
    ctx.fillText(`Score: ${gameState.score}`, 10, 20);
}

function updateGame() {
    socket.emit('update');
}

setInterval(updateGame, 1000 / 30); // Update game 30 times per second