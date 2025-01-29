from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
from typing import NamedTuple

app = Flask(__name__)
socketio = SocketIO(app)

# Game variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
player_size = 50
hurdle_width = 30
hurdle_height = 50
hurdle_speed = 10
tool_size = 30
tool_speed = 10
LEVEL_UP_SCORE = 200

class Word(NamedTuple):
    text: str
    rect: dict
    points: int

WORD_BANK = [
    "Selenium", "Python", "Java", "Docker", "Jenkins", "Git", "API", "AWS",
    "Kubernetes", "CI/CD", "Agile", "Scrum", "TDD", "BDD", "Clean Code",
    "Design Patterns", "RESTful", "GraphQL", "Microservices", "DevOps",
    "Containers", "Cloud", "Azure", "GCP", "Monitoring", "Logging",
    "Reporting", "Golang", "Rust", "Ruby", "Node.js", "JavaScript", "Java",
    "Jira"
]
POINT_VALUES = [10, 20, 30]

# Game state
game_state = {
    'player_y': SCREEN_HEIGHT - player_size - 20,
    'player_y_velocity': 0,
    'hurdles': [],
    'tools': [],
    'score': 0,
    'level': 1,
    'game_level': 'easy',
    'hurdle_speed': hurdle_speed,
    'tool_speed': tool_speed,
    'last_hurdle_time': time.time(),
    'last_tool_time': time.time()
}

def check_collision(rect1, rect2):
    return (rect1['x'] < rect2['x'] + rect2['width'] and
            rect1['x'] + rect1['width'] > rect2['x'] and
            rect1['y'] < rect2['y'] + rect2['height'] and
            rect1['y'] + rect1['height'] > rect2['y'])

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('game_state', game_state)

@socketio.on('jump')
def handle_jump():
    game_state['player_y_velocity'] = -15

@socketio.on('update')
def handle_update():
    current_time = time.time()

    # Update player position
    game_state['player_y_velocity'] += 1
    game_state['player_y'] += game_state['player_y_velocity']
    if game_state['player_y'] + player_size > SCREEN_HEIGHT - 20:
        game_state['player_y'] = SCREEN_HEIGHT - player_size - 20

    # Hurdle Logic
    if current_time - game_state['last_hurdle_time'] > 1.5:  # 1.5 seconds
        hurdle_x = SCREEN_WIDTH
        hurdle_y = SCREEN_HEIGHT - hurdle_height - 20
        game_state['hurdles'].append({
            'x': hurdle_x, 
            'y': hurdle_y, 
            'width': hurdle_width, 
            'height': hurdle_height
        })
        game_state['last_hurdle_time'] = current_time

    # Update hurdles
    player_rect = {
        'x': 100,
        'y': game_state['player_y'],
        'width': player_size,
        'height': player_size
    }

    for hurdle in game_state['hurdles'][:]:
        hurdle['x'] -= game_state['hurdle_speed']
        if hurdle['x'] + hurdle_width < 0:
            game_state['hurdles'].remove(hurdle)
        elif check_collision(player_rect, hurdle):
            game_over()

    # Tool Logic
    if current_time - game_state['last_tool_time'] > 2.0:  # 2 seconds
        tool_x = SCREEN_WIDTH
        tool_y = random.randint(50, SCREEN_HEIGHT - 50)
        game_state['tools'].append({
            'x': tool_x,
            'y': tool_y,
            'width': tool_size,
            'height': tool_size
        })
        game_state['last_tool_time'] = current_time

    # Update tools
    for tool in game_state['tools'][:]:
        tool['x'] -= game_state['tool_speed']
        if tool['x'] + tool_size < 0:
            game_state['tools'].remove(tool)
        elif check_collision(player_rect, tool):
            game_state['tools'].remove(tool)
            game_state['score'] += 10

    # Emit updated game state to all clients
    emit('game_state', game_state, broadcast=True)

def game_over():
    game_state['player_y'] = SCREEN_HEIGHT - player_size - 20
    game_state['player_y_velocity'] = 0
    game_state['hurdles'] = []
    game_state['tools'] = []
    game_state['score'] = 0
    emit('game_over', game_state)

if __name__ == '__main__':
    socketio.run(app, debug=True)