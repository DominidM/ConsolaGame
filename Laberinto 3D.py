import pygame
import math
import random

# Configuración básica
WIDTH, HEIGHT = 1600, 900
TILE_SIZE = 40
FPS = 60
FOV = math.pi / 3  # Campo de visión
HALF_FOV = FOV / 2
MAX_DEPTH = 800  # Profundidad máxima del rayo
NUM_RAYS = WIDTH // 2  # Número de rayos lanzados
DELTA_ANGLE = FOV / NUM_RAYS
SCREEN_DIST = WIDTH // (2 * math.tan(HALF_FOV))
COLLISION_OFFSET = 10  # Margen para evitar que el jugador se acerque demasiado a la pared
MOUSE_SENSITIVITY = 0.010 # Sensibilidad del ratón

# Colores
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_LIGHT = (0, 255, 100)
GREEN_DARK = (0, 150, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (150, 150, 150)
CONCRETE_COLOR = (255, 0, 0)  # Color del piso concreto
SKY_COLOR = (135, 206, 235)  # Color del cielo

# Tiempo máximo para encontrar el cuadro (en segundos)
TIME_LIMIT = 600

# Definir múltiples laberintos para los niveles
MAPS = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # Puedes añadir más laberintos aquí
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
]

# Variables para el control de niveles
current_level = 0
MAP = MAPS[current_level]

MAP_SCALE = 5  # Escala del minimapa
VISIBILITY_RADIUS = 150  # Radio en el que el cuadro es visible

# Inicializar Pygame
pygame.init()

# Cargar efectos de sonido
sound_move = pygame.mixer.Sound("sound_move.wav")
sound_collision = pygame.mixer.Sound("sound_collision.wav")
sound_win = pygame.mixer.Sound("sound_win.wav")

# Función para avanzar al siguiente nivel
def next_level():
    global current_level, MAP, player, square_pos, show_square, message_displayed, start_ticks
    current_level += 1
    if current_level < len(MAPS):
        MAP = MAPS[current_level]
        player = Player()  # Reiniciar jugador
        square_pos = generate_square_position()  # Generar nueva posición para el cuadro
        show_square = True
        message_displayed = False
        start_ticks = pygame.time.get_ticks()  # Reiniciar el temporizador
    else:
        # Juego completado
        print("¡Felicitaciones! Has completado todos los niveles.")
        pygame.quit()
        exit()

# Función para generar la posición del cuadro
def generate_square_position():
    while True:
        x = random.randint(0, len(MAP[0]) - 1) * TILE_SIZE + TILE_SIZE // 2
        y = random.randint(0, len(MAP) - 1) * TILE_SIZE + TILE_SIZE // 2
        if MAP[y // TILE_SIZE][x // TILE_SIZE] == 0:
            return x, y

# Verificación si el cuadro está visible
def is_square_visible(player_pos, square_pos, player_angle):
    player_x, player_y = player_pos
    square_x, square_y = square_pos
    distance = math.hypot(player_x - square_x, player_y - square_y)
    if distance > VISIBILITY_RADIUS:
        return False
    angle_to_square = math.atan2(square_y - player_y, square_x - player_x)
    angle_diff = player_angle - angle_to_square
    angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi
    return -HALF_FOV <= angle_diff <= HALF_FOV

# Función para verificar si el cuadro está en el campo de visión
def is_square_visible(player_pos, square_pos, player_angle):
    player_x, player_y = player_pos
    square_x, square_y = square_pos
    distance = math.hypot(player_x - square_x, player_y - square_y)
    if distance > VISIBILITY_RADIUS:
        return False
    angle_to_square = math.atan2(square_y - player_y, square_x - player_x)
    angle_diff = player_angle - angle_to_square
    angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi
    return -HALF_FOV <= angle_diff <= HALF_FOV

# Función para lanzar rayos y detectar colisiones
def cast_rays(screen, player_pos, player_angle, square_pos, show_square):
    start_x, start_y = player_pos
    current_angle = player_angle - HALF_FOV
    # Dibujar el cielo
    pygame.draw.rect(screen, SKY_COLOR, (0, 0, WIDTH, HEIGHT // 2))
    for ray in range(NUM_RAYS):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)

        for depth in range(1, MAX_DEPTH):
            x = start_x + depth * cos_a
            y = start_y + depth * sin_a

            map_x, map_y = int(x // TILE_SIZE), int(y // TILE_SIZE)

            if MAP[map_y][map_x] == 1:
                depth *= math.cos(player_angle - current_angle)  # Evitar distorsión
                wall_height = SCREEN_DIST / (depth + 0.0001)
                color = (255 / (1 + depth * depth * 0.0001), 0, 0)
                pygame.draw.rect(screen, CONCRETE_COLOR, (ray * 2, HEIGHT // 2 - wall_height // 2, 2, wall_height))
                break

        current_angle += DELTA_ANGLE
    if show_square:
        square_x, square_y = square_pos
        depth = math.hypot(player_pos[0] - square_x, player_pos[1] - square_y)
        if depth < MAX_DEPTH:
            square_height = SCREEN_DIST / (depth + 0.0001)
            square_color = GREEN_LIGHT if pygame.time.get_ticks() % 1000 < 500 else GREEN_DARK
            pygame.draw.rect(screen, square_color, (WIDTH // 2 - 20, HEIGHT // 2 - square_height // 2, 40, square_height))

# Clase Jugador
class Player:
    def __init__(self):
        self.x = TILE_SIZE * 1.5
        self.y = TILE_SIZE * 1.5
        self.angle = 0
        self.speed = 1

    def move(self):
        keys = pygame.key.get_pressed()
        moved = False
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        if keys[pygame.K_w]:
            if not self.check_collision(dx, dy):
                self.x += dx
                self.y += dy
                moved = True
            else:
                if not pygame.mixer.get_busy():
                    sound_collision.play()
        if keys[pygame.K_s]:
            if not self.check_collision(-dx, -dy):
                self.x -= dx
                self.y -= dy
                moved = True
            else:
                if not pygame.mixer.get_busy():
                    sound_collision.play()
        side_dx = self.speed * math.sin(self.angle)
        side_dy = self.speed * math.cos(self.angle)
        if keys[pygame.K_d]:
            if not self.check_collision(-side_dx, side_dy):
                self.x -= side_dx
                self.y += side_dy
                moved = True
            else:
                if not pygame.mixer.get_busy():
                    sound_collision.play()
        if keys[pygame.K_a]:
            if not self.check_collision(side_dx, -side_dy):
                self.x += side_dx
                self.y -= side_dy
                moved = True
            else:
                if not pygame.mixer.get_busy():
                    sound_collision.play()

        if moved and not pygame.mixer.get_busy():
            sound_move.play()

    def check_collision(self, dx, dy):
        future_x = self.x + dx
        future_y = self.y + dy
        map_x = int(future_x // TILE_SIZE)
        map_y = int(future_y // TILE_SIZE)
        if MAP[map_y][map_x] == 1:
            return True
        return False

    @property
    def pos(self):
        return self.x, self.y

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value % (2 * math.pi)

# Función para dibujar el minimapa
def draw_minimap(screen, player):
    map_width, map_height = len(MAP[0]), len(MAP)
    minimap_size = TILE_SIZE // MAP_SCALE
    for y in range(map_height):
        for x in range(map_width):
            color = WHITE if MAP[y][x] == 1 else BLACK
            pygame.draw.rect(screen, color, (WIDTH - map_width * minimap_size + x * minimap_size,
                                             HEIGHT - map_height * minimap_size + y * minimap_size,
                                             minimap_size, minimap_size))
    player_map_x = int(player.x // TILE_SIZE * minimap_size)
    player_map_y = int(player.y // TILE_SIZE * minimap_size)
    pygame.draw.circle(screen, RED, (WIDTH - map_width * minimap_size + player_map_x,
                                     HEIGHT - map_height * minimap_size + player_map_y), 5)
    player_dir_x = player_map_x + 10 * math.cos(player.angle)
    player_dir_y = player_map_y + 10 * math.sin(player.angle)
    pygame.draw.line(screen, BLUE, (WIDTH - map_width * minimap_size + player_map_x,
                                    HEIGHT - map_height * minimap_size + player_map_y),
                     (WIDTH - map_width * minimap_size + player_dir_x,
                      HEIGHT - map_height * minimap_size + player_dir_y), 2)

# Función para dibujar el temporizador
def draw_timer(screen, time_left):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Tiempo restante: {int(time_left)} s", True, YELLOW)
    screen.blit(timer_text, (20, 20))

# Función para dibujar un indicador que apunte hacia el cuadro verde
def draw_direction_indicator(screen, player_pos, square_pos):
    player_x, player_y = player_pos
    square_x, square_y = square_pos
    angle_to_square = math.atan2(square_y - player_y, square_x - player_x)

    # Calcular el color del indicador según la distancia
    distance = math.hypot(player_x - square_x, player_y - square_y)
    intensity = max(0, min(255, int(255 - (distance / VISIBILITY_RADIUS) * 255)))
    color = (255, 255 - intensity, 255 - intensity)  # De blanco a rojo según la distancia

    # Dibujar una flecha en la parte superior de la pantalla apuntando hacia el cuadro
    arrow_length = 50
    arrow_x = WIDTH // 2 + arrow_length * math.cos(angle_to_square)
    arrow_y = 50 + arrow_length * math.sin(angle_to_square)
    pygame.draw.line(screen, color, (WIDTH // 2, 50), (arrow_x, arrow_y), 5)
    pygame.draw.circle(screen, color, (int(arrow_x), int(arrow_y)), 5)

# Generar una posición fija para el cuadro dentro del laberinto
def generate_square_position():
    while True:
        x = random.randint(1, len(MAP[0]) - 2) * TILE_SIZE + TILE_SIZE // 2
        y = random.randint(1, len(MAP) - 2) * TILE_SIZE + TILE_SIZE // 2
        if MAP[y // TILE_SIZE][x // TILE_SIZE] == 0:
            return x, y

# Inicializar Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Crear al jugador
player = Player()

# Generar la posición del cuadro
square_pos = generate_square_position()

# Variables para la lógica del cuadro
show_square = True
message_displayed = False
start_ticks = pygame.time.get_ticks()  # Tiempo inicial

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcular el tiempo restante
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = TIME_LIMIT - seconds_passed

    # Verificar si se acabó el tiempo
    if time_left <= 0:
        pygame.mixer.stop()
        font = pygame.font.Font(None, 36)
        lose_text = font.render("¡Tiempo agotado! Has perdido.", True, RED)
        screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - lose_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Obtener movimiento del mouse para rotar al jugador
    mouse_x, mouse_y = pygame.mouse.get_rel()
    player.angle += mouse_x * MOUSE_SENSITIVITY

    # Actualizar la posición del jugador
    player.move()

    # Verificar colisión con el cuadro
    if show_square:
        square_x, square_y = square_pos
        if (square_x - COLLISION_OFFSET < player.x < square_x + COLLISION_OFFSET and
                square_y - COLLISION_OFFSET < player.y < square_y + COLLISION_OFFSET):
            message_displayed = True
            show_square = False
            pygame.mixer.stop()
            sound_win.play()
            font = pygame.font.Font(None, 36)
            level_text = font.render(f"Nivel {current_level + 1} completado. Pasas al siguiente nivel.", True, YELLOW)
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - level_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            next_level()

    # Limpiar pantalla
    screen.fill(BLACK)

    # Verificar si el cuadro es visible
    show_square = is_square_visible(player.pos, square_pos, player.angle)

    # Lógica de raycasting
    cast_rays(screen, player.pos, player.angle, square_pos, show_square)

    # Dibujar el minimapa
    draw_minimap(screen, player)

    # Dibujar el temporizador
    draw_timer(screen, time_left)

    # Dibujar el indicador de dirección que cambia de color según la distancia
    draw_direction_indicator(screen, player.pos, square_pos)

    pygame.display.flip()
    clock.tick(FPS)

# Finalizar Pygame
pygame.quit()
