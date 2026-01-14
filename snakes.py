import pgzrun
import random
import time

# Configurações da tela
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
WIDTH = TILE_SIZE * GRID_WIDTH
HEIGHT = TILE_SIZE * GRID_HEIGHT
TITLE = "Snake - Willames 2026"

# Estado inicial da cobrinha
snake = [(5, 7), (4, 7), (3, 7)]
direction = (1, 0)
food = None
game_over = False
score = 0
menu = True   # começa na tela inicial

# Controle de velocidade
last_move = time.time()
move_delay = 0.15   # segundos entre movimentos

# área do botão Play
play_button = Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 80)

def draw():
    screen.clear()

    # repete a imagem de fundo em mosaico
    bg_width = images.background.get_width()
    bg_height = images.background.get_height()

    for x in range(0, WIDTH, bg_width):
        for y in range(0, HEIGHT, bg_height):
            screen.blit("background", (x, y))

    # resto do desenho (menu, cobrinha, comida, etc.)
    if menu:
        screen.draw.filled_rect(play_button, "darkgreen")
        screen.draw.text("PLAY", center=play_button.center, fontsize=50, color="white")
    else:
        if food:
            screen.blit("food", (food[0]*TILE_SIZE, food[1]*TILE_SIZE))
        for sx, sy in snake:
            screen.blit("snake", (sx*TILE_SIZE, sy*TILE_SIZE))
        screen.draw.text(f"Pontos: {score}", topleft=(10, 10), fontsize=30, color="white")

        if game_over:
            screen.draw.text("GAME OVER! ESPAÇO pra jogar de novo", center=(WIDTH/2, HEIGHT/2), fontsize=40, color="red")


def update():
    global snake, food, game_over, score, last_move

    if menu or game_over:
        if game_over and keyboard.space:
            reset_game()
        return

    if time.time() - last_move < move_delay:
        return
    last_move = time.time()

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
        new_head in snake):
        sounds.collision.play()
        game_over = True
        return

    snake.insert(0, new_head)

    if new_head == food:
        sounds.eat.play()
        score += 1
        food = gerar_comida()
    else:
        snake.pop()

def on_key_down(key):
    global direction
    if key == keys.UP and direction != (0, 1):
        direction = (0, -1)
    elif key == keys.DOWN and direction != (0, -1):
        direction = (0, 1)
    elif key == keys.LEFT and direction != (1, 0):
        direction = (-1, 0)
    elif key == keys.RIGHT and direction != (-1, 0):
        direction = (1, 0)

def on_mouse_down(pos):
    global menu, food
    if menu and play_button.collidepoint(pos):
        menu = False
        food = gerar_comida()

def gerar_comida():
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake:
            return pos

def reset_game():
    global snake, direction, food, game_over, score, menu, last_move
    snake = [(5, 7), (4, 7), (3, 7)]
    direction = (1, 0)
    food = gerar_comida()
    game_over = False
    score = 0
    menu = True
    last_move = time.time()

pgzrun.go()
