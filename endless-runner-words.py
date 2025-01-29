import pygame
import random
from typing import NamedTuple

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Automation Runner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont('Arial', 24)
word_font = pygame.font.SysFont('Arial', 20)

# Clock
clock = pygame.time.Clock()
FPS = 30

# Sounds
pygame.mixer.init()
run_sound = pygame.mixer.Sound("./sounds/run.wav")
collect_sound = pygame.mixer.Sound("./sounds/collect.wav")
hit_sound = pygame.mixer.Sound("./sounds/hit.wav")
sound_enabled = True

# Player
player_size = 50
player_x = 100
player_y = SCREEN_HEIGHT - player_size - 20
player_y_velocity = 0
gravity = 1
jump_power = -15
player = pygame.Rect(player_x, player_y, player_size, player_size)

# Hurdles
hurdle_width = 30
hurdle_height = 50
hurdles = []
hurdle_speed = 10
hurdle_spawn_rate = 1000  # Decreased to spawn hurdles more frequently
last_hurdle_time = 0

# Words
class Word(NamedTuple):
    text: str
    rect: pygame.Rect
    points: int

WORD_BANK = [
    "Selenium",
    "Python",
    "Java",
    "Docker",
    "Jenkins",
    "Git",
    "API",
    "AWS",
    "Kubernetes",
    "CI/CD",
    "Agile",
    "Scrum",
    "TDD",
    "BDD",
    "Clean Code",
    "Design Patterns",
    "RESTful",
    "GraphQL",
    "Microservices",
    "DevOps",
    "Containers",
    "Cloud",
    "Azure",
    "GCP",
    "Monitoring",
    "Logging",
    "Reporting",
    "Golang",
    "Rust",
    "Ruby",
    "Node.js",
    "JavaScript",
    "Java",
    "Jira",
]

# Randomize the value of words within the 3 values - 10, 20, 30
POINT_VALUES = [10, 20, 30]

words = []
word_speed = 5
word_spawn_rate = 3000  # in milliseconds
last_word_time = 0

# Score
score = 0
level = 1
game_level = "easy"
LEVEL_UP_SCORE = 200

def reset_game():
    global player_y, player_y_velocity, hurdles, words, score, last_hurdle_time, last_word_time, level, game_level, hurdle_speed, word_speed
    player_y = SCREEN_HEIGHT - player_size - 20
    player_y_velocity = 0
    hurdles = []
    words = []
    score = 0
    last_hurdle_time = 0
    last_word_time = 0
    level = 1
    game_level = show_menu()
    hurdle_speed = 10
    word_speed = 5

def game_over_screen():
    screen.fill(WHITE)
    
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    
    game_over_text = font.render("Game Over! Press 'R' to Restart", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    reset_game()

def draw_stickman(surface, x, y):
    # Head
    pygame.draw.circle(surface, BLACK, (x + 25, y + 10), 10)
    # Body
    pygame.draw.line(surface, BLACK, (x + 25, y + 20), (x + 25, y + 50), 2)
    # Arms
    pygame.draw.line(surface, BLACK, (x + 25, y + 30), (x + 15, y + 40), 2)
    pygame.draw.line(surface, BLACK, (x + 25, y + 30), (x + 35, y + 40), 2)
    # Legs
    pygame.draw.line(surface, BLACK, (x + 25, y + 50), (x + 15, y + 70), 2)
    pygame.draw.line(surface, BLACK, (x + 25, y + 50), (x + 35, y + 70), 2)

def show_menu():
    screen.fill(WHITE)
    title_text = font.render("Game Level", True, BLACK)
    easy_text = font.render("1. Easy", True, BLACK)
    medium_text = font.render("2. Medium", True, BLACK)
    hard_text = font.render("3. Hard", True, BLACK)
    sound_text = font.render("Press S to Toggle Sound", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(sound_text, (SCREEN_WIDTH // 2 - sound_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "medium"
                if event.key == pygame.K_3:
                    return "hard"
                if event.key == pygame.K_s:
                    global sound_enabled
                    sound_enabled = not sound_enabled

def spawn_hurdle():
    global hurdle_spawn_rate
    hurdle_x = SCREEN_WIDTH
    if game_level == "easy":
        hurdle_y = SCREEN_HEIGHT - hurdle_height - 20
    else:
        hurdle_y = random.randint(50, SCREEN_HEIGHT - hurdle_height - 20)
    
    new_hurdle = pygame.Rect(hurdle_x, hurdle_y, hurdle_width, hurdle_height)
    
    # Ensure the new hurdle does not collide with the previous hurdle
    if hurdles and new_hurdle.colliderect(hurdles[-1]):
        return
    
    # Check for collision with existing hurdles and words
    for hurdle in hurdles:
        if new_hurdle.colliderect(hurdle):
            return  # Skip spawning this hurdle if it collides with an existing hurdle
    for word in words:
        if new_hurdle.colliderect(word.rect):
            return  # Skip spawning this hurdle if it collides with an existing word
    
    hurdles.append(new_hurdle)
    
    if game_level == "hard":
        hurdle_spawn_rate = 800  # Further decrease spawn rate for hard level

def spawn_word():
    word_text = random.choice(WORD_BANK)
    points = random.choice(POINT_VALUES)
    
    # Ensure the new word is not the same as the previous word
    if words and word_text == words[-1].text:
        return
    
    text_surface = word_font.render(word_text, True, BLUE)
    word_x = SCREEN_WIDTH
    word_y = random.randint(50, SCREEN_HEIGHT - 50)
    
    word_rect = text_surface.get_rect()
    word_rect.x = word_x
    word_rect.y = word_y
    
    # Check for collision with existing hurdles and words
    for hurdle in hurdles:
        if word_rect.colliderect(hurdle):
            return
    for word in words:
        if word_rect.colliderect(word.rect):
            return
    
    words.append(Word(word_text, word_rect, points))

# Game Loop
running = True
game_level = show_menu()
while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y + player_size >= SCREEN_HEIGHT - 20:
                player_y_velocity = jump_power
                if sound_enabled:
                    run_sound.play()
            if event.key == pygame.K_s:
                sound_enabled = not sound_enabled

    # Player Movement
    player_y_velocity += gravity
    player.y += player_y_velocity
    if player.y + player_size > SCREEN_HEIGHT - 20:
        player.y = SCREEN_HEIGHT - player_size - 20

    # Hurdle Logic
    current_time = pygame.time.get_ticks()
    if current_time - last_hurdle_time > hurdle_spawn_rate:
        spawn_hurdle()
        last_hurdle_time = current_time

    for hurdle in hurdles[:]:
        hurdle.x -= hurdle_speed
        if hurdle.x + hurdle_width < 0:
            hurdles.remove(hurdle)
        if player.colliderect(hurdle):
            if sound_enabled:
                run_sound.stop()  # Stop the running sound
                hit_sound.play()
            game_over_screen()

    # Word Logic
    if current_time - last_word_time > word_spawn_rate:
        spawn_word()
        last_word_time = current_time

    for word in words[:]:
        word.rect.x -= word_speed
        if word.rect.right < 0:
            words.remove(word)
        if player.colliderect(word.rect):
            score += word.points
            words.remove(word)
            if sound_enabled:
                collect_sound.play()

    # Level Progression
    if score >= LEVEL_UP_SCORE * level:
        level += 1
        if level > 3:
            level = 3  # Cap the level at 3
        if level == 2:
            game_level = "medium"
        elif level == 3:
            game_level = "hard"
        hurdle_speed += 2  # Increase hurdle speed
        word_speed += 1  # Increase word speed

    # Draw Player (Stickman)
    draw_stickman(screen, player.x, player.y)

    # Draw Hurdles
    for hurdle in hurdles:
        pygame.draw.rect(screen, RED, hurdle)

    # Draw Words
    for word in words:
        text_surface = word_font.render(word.text, True, BLUE)
        screen.blit(text_surface, word.rect)

    # Draw Score
    score_text = font.render(f"Score: {score} Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update Display
    pygame.display.flip()

    # Cap the Frame Rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()