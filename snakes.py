import pgzrun
import random

# config de tela
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
WIDTH = TILE_SIZE * GRID_WIDTH
HEIGHT = TILE_SIZE * GRID_HEIGHT
TITLE = "Snake Action Dungeon"

# stado do jogo
hero_segments = []
move_direction = (1, 0)
is_game_over = False
score = 0
is_in_menu = True
level = 1
dungeon_map = []
enemies = []  
exit_portal = None
animation_frame = 1
is_muted = False
mute_button = Rect(WIDTH - 50, 10, 40, 40) # Posição no canto superior direito
# button_exit = Actor("exit_button") só funcionario se usasse a sys para fechar o jogo 
# button_exit.center = (WIDTH // 2, (HEIGHT//2) + 100)

# Actors
game_over_logo = Actor("gameover")
game_over_logo.center = (WIDTH // 2, HEIGHT // 2)

button_play = Actor("play_button")
button_play.center = (WIDTH // 2, HEIGHT // 2)

def draw():
    screen.clear()

    # Desenha o fundo
    background_width = images.background.get_width()
    background_height = images.background.get_height()
    for x_position in range(0, WIDTH, background_width):
        for y_position in range(0, HEIGHT, background_height):
            screen.blit("background", (x_position, y_position))
    
    if is_in_menu:
        button_play.draw()
        
        
    else:

        # desenha as paredes da masmorra
        for column_index in range(GRID_WIDTH):
            for row_index in range(GRID_HEIGHT):
                if dungeon_map[column_index][row_index] == 1:
                    screen.blit("wall", (column_index * TILE_SIZE, row_index * TILE_SIZE))
        
        # desenha a porta para proxima fase 
        if exit_portal:
            screen.blit("stairs", (exit_portal[0] * TILE_SIZE, exit_portal[1] * TILE_SIZE))
        
        # logica de como é desenhada a cobrinha
        for segment_index, segment_position in enumerate(hero_segments):
            pixel_x = segment_position[0] * TILE_SIZE
            pixel_y = segment_position[1] * TILE_SIZE
            
            if segment_index == 0:
                # seleciona a imagem certa para a cabeça da cobrinha 
                direction_x, direction_y = move_direction
                head_sprite = "snake_head_right" # Default
                
                if direction_x == 1: head_sprite = "snake_head_right"
                elif direction_x == -1: head_sprite = "snake_head_left"
                elif direction_y == -1: head_sprite = "snake_head_up"
                elif direction_y == 1: head_sprite = "snake_head_down"
                
                screen.blit(head_sprite, (pixel_x, pixel_y))
            else:
                previous_segment = hero_segments[segment_index - 1]
                diff_x = previous_segment[0] - segment_position[0]
                diff_y = previous_segment[1] - segment_position[1]
                body_sprite = 'snake_body_horizontal'

                if diff_x != 0:
                    body_sprite = 'snake_body_horizontal'
                elif diff_y != 0:
                    body_sprite = 'snake_body_vertical'
            
                # desenha o corpo com os outros segmentos 
                screen.blit(body_sprite, (pixel_x, pixel_y))
            
        # desenha o inimigos animados 
        for enemy_x, enemy_y, enemy_face in enemies:
            sprite_name = f"rat_{enemy_face}{animation_frame}"
            screen.blit(sprite_name, (enemy_x * TILE_SIZE, enemy_y * TILE_SIZE))
        
        # Desenha o score na tela 
        screen.draw.text(f"Level: {level}  Score: {score}", topleft=(10, 10), fontsize=28, shadow=(1,1))

        # cria a logica do volume e coloca na tela 
        mute_icon = 'volume_off' if is_muted else 'volume_on'
        screen.blit(mute_icon, (mute_button.x, mute_button.y))
        if is_game_over:
            game_over_logo.draw()
            screen.draw.text(f"Score: {score}\n[SPACE] to Restart", 
                             color='white', center=(WIDTH/2, HEIGHT/2 + 70), 
                             shadow=(1, 1), scolor='black', fontsize=45)
    
def update():
    #verifica se o jogo acabou e se foi pressionado o space, então reseta o jogo
    if is_game_over and keyboard.space:
        reset_to_menu()

def on_key_down(key):

    global move_direction

    #verifica se está no menu ou se esta no fim do jogo se tiver impede que o personagem se mova
    if is_in_menu or is_game_over: return

    # salva a direção atual na hora que apertou a tecla
    current_direction_x, current_direction_y = move_direction
    new_direction = move_direction

    #faz o mapeamento das teclas e define o vetor de movimento para essa direção (y,x)
    if key == keys.UP:
        new_direction = (0, -1)
    elif key == keys.DOWN:
        new_direction = (0, 1)
    elif key == keys.LEFT:
        new_direction = (-1, 0)
    elif key == keys.RIGHT:
        new_direction = (1, 0)

    # impede que ela vire para tras ( a soma dos vetores não pode ser 0 então ela não vira)
    if (new_direction[0] + current_direction_x != 0) or (new_direction[1] + current_direction_y != 0):
        move_direction = new_direction
        move_hero()

def move_hero():
    global is_game_over, score, level
    head_x, head_y = hero_segments[0]
    
    new_head_position = (head_x + move_direction[0], head_y + move_direction[1])
    target_x, target_y = new_head_position
    
    #verifica se saiu pela esquerda ou direita (eixo x), pela esquerda(eixo y) e se bateu na masmorra (0 não e 1 colide)
    if (target_x < 0 or target_x >= GRID_WIDTH or target_y < 0 or target_y >= GRID_HEIGHT or
        dungeon_map[target_x][target_y] == 1 or new_head_position in hero_segments):
        play_sound("hit")
        is_game_over = True
        sounds.background_theme.stop()
        return
    
    hero_segments.insert(0, new_head_position)
    
    # Check Enemy Collision
    has_eaten_enemy = False
    for enemy_data in enemies[:]:
        if (enemy_data[0], enemy_data[1]) == new_head_position:
            enemies.remove(enemy_data)
            score += 1
            play_sound("eat")
            has_eaten_enemy = True
    
    if not has_eaten_enemy:
        hero_segments.pop()
    
    # Check Level Completion
    if new_head_position == exit_portal:
        level += 1
        play_sound("disappear")
        generate_dungeon(level)

def update_enemies():
    global is_game_over, animation_frame
    if is_in_menu or is_game_over or not hero_segments: return

    animation_frame = 2 if animation_frame == 1 else 1
    player_head_position = hero_segments[0]

    for index in range(len(enemies)):
        enemy_x, enemy_y, current_face = enemies[index]
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        random.shuffle(possible_moves)
        
        for delta_x, delta_y in possible_moves:
            target_x, target_y = enemy_x + delta_x, enemy_y + delta_y
            if (0 <= target_x < GRID_WIDTH and 0 <= target_y < GRID_HEIGHT and 
                dungeon_map[target_x][target_y] == 0 and (target_x, target_y) not in hero_segments):
                
                new_face = current_face
                if delta_x == 1: new_face = "right"
                elif delta_x == -1: new_face = "left"
                
                enemies[index] = (target_x, target_y, new_face)
                break
        
        if (enemies[index][0], enemies[index][1]) == player_head_position:
            play_sound("hit")
            is_game_over = True
            sounds.background_theme.stop()

def generate_dungeon(current_level):
    global dungeon_map, exit_portal, enemies, hero_segments
    dungeon_map = [[1 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    rooms_list = []
    
    for _ in range(50):
        if len(rooms_list) >= 3 + (current_level // 2): break
        room_width = random.randint(3, 6)
        room_height = random.randint(3, 5)
        room_x = random.randint(1, GRID_WIDTH - room_width - 1)
        room_y = random.randint(1, GRID_HEIGHT - room_height - 1)
        
        if any(not (room_x + room_width < other_x or room_x > other_x + other_w or 
                    room_y + room_height < other_y or room_y > other_y + other_h) 
               for other_x, other_y, other_w, other_h in rooms_list): 
            continue
            
        rooms_list.append((room_x, room_y, room_width, room_height))
        for tile_x in range(room_x, room_x + room_width):
            for tile_y in range(room_y, room_y + room_height): 
                dungeon_map[tile_x][tile_y] = 0

    for index in range(len(rooms_list) - 1):
        x1, y1 = rooms_list[index][0] + rooms_list[index][2]//2, rooms_list[index][1] + rooms_list[index][3]//2
        x2, y2 = rooms_list[index+1][0] + rooms_list[index+1][2]//2, rooms_list[index+1][1] + rooms_list[index+1][3]//2
        for corridor_x in range(min(x1, x2), max(x1, x2) + 1): dungeon_map[corridor_x][y1] = 0
        for corridor_y in range(min(y1, y2), max(y1, y2) + 1): dungeon_map[x2][corridor_y] = 0

    start_x, start_y = rooms_list[0][0], rooms_list[0][1]
    hero_segments[:] = [(start_x + 2, start_y + 1), (start_x + 1, start_y + 1), (start_x, start_y + 1)]
    
    exit_portal = (rooms_list[-1][0] + rooms_list[-1][2]//2, rooms_list[-1][1] + rooms_list[-1][3]//2)
    
    enemies[:] = []
    for _ in range(2 + current_level):
        while True:
            spawn_x = random.randint(0, GRID_WIDTH - 1)
            spawn_y = random.randint(0, GRID_HEIGHT - 1)
            if dungeon_map[spawn_x][spawn_y] == 0 and (spawn_x, spawn_y) not in hero_segments and (spawn_x, spawn_y) != exit_portal:
                enemies.append((spawn_x, spawn_y, random.choice(["left", "right"])))
                break

def play_sound(sound_name):

    if not is_muted and hasattr(sounds, sound_name):
        getattr(sounds, sound_name).play()

def start_game():
    global level, score, is_game_over
    level, score, is_game_over = 1, 0, False
    generate_dungeon(level)

def reset_to_menu():
    global is_in_menu, is_game_over
    is_in_menu, is_game_over = True, False
    sounds.background_theme.stop()

def on_mouse_down(pos):
    global is_in_menu, is_muted
    if is_in_menu and button_play.collidepoint(pos):
        is_in_menu = False
        if not is_muted:
            try:
                sounds.background_theme.play(-1)
            except:
                print("Music file 'background_theme' not found in sounds folder.")
        start_game()
        return
    if not is_in_menu and mute_button.collidepoint(pos):
        is_muted = not is_muted

        if is_muted:
            sounds.background_theme.stop()
        else:
            sounds.background_theme.play(-1)

clock.schedule_interval(update_enemies, 0.6)
pgzrun.go()