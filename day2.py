import pygame
import sys
import random
import math
import numpy as np

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Onam Snake Boat Race – Power Up Edition")

# Colors
BLUE = (30, 96, 145)
LIGHT_BLUE = (50, 130, 200)
YELLOW = (255, 209, 102)
GREEN = (6, 214, 160)
WHITE = (255, 255, 255)
BROWN = (150, 75, 0)
DARK_BROWN = (100, 50, 0)
RED = (255, 50, 50)
ORANGE = (255, 140, 0)
CYAN = (0, 255, 255)
SKIN_COLOR = (255, 200, 150)
CLOTH_COLOR = (240, 240, 240)
HEAD_CLOTH_COLOR = (200, 200, 200)

# New Power-up Colors
BANANA_SLIP_COLOR = (255, 255, 0)
PAYASAM_COLOR = (255, 255, 255)
SLIP_RED = (255, 100, 100)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Finish line
FINISH_LINE = WIDTH - 100
font = pygame.font.SysFont("arial", 28, bold=True)

# Winning Quotes
WINNER_QUOTES = [
    "A legendary victory! Onam is here!",
    "🏆 The spirit of Onam shines through! You won!",
    "Mahabali approves! A magnificent race!",
    "A stunning finish! The champions of the river!",
    "Extra banana chips for you! You earned it!"
]


# --- Classes ---

class Boat:
    def __init__(self, x, y, color, control_keys, name="Player"):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.control_keys = control_keys
        self.name = name
        self.horizontal_speed = 0.0
        self.vertical_speed = 0.0
        self.length = 200
        self.height = 40
        self.oar_animation_time = 0.0
        self.rower_lean_offset = 0
        self.distance = 0.0
        self.rower_count = 12
        self.boost_timer = 0
        self.shield_timer = 0
        self.is_slipping = False
        self.slip_timer = 0
        self.slip_counter = 0
        self.slip_recovery_needed = 15

    def update(self):
        # Handle slipping state
        if self.is_slipping:
            self.horizontal_speed = -2.5
            self.slip_timer -= 1
            if self.slip_timer <= 0 or self.slip_counter >= self.slip_recovery_needed:
                self.is_slipping = False
                self.slip_counter = 0
                self.horizontal_speed = 0

        self.x += self.horizontal_speed
        self.y += self.vertical_speed
        self.distance = self.x

        # Friction
        self.horizontal_speed *= 0.92
        self.vertical_speed *= 0.9

        if self.boost_timer > 0:
            self.horizontal_speed += 1.5
            self.boost_timer -= 1
        if self.shield_timer > 0:
            self.shield_timer -= 1

        self.oar_animation_time = (self.oar_animation_time + abs(self.horizontal_speed) * 0.05 + 0.5) % (2 * math.pi)
        self.rower_lean_offset = int(5 * math.sin(self.oar_animation_time))

    def draw(self, surface: "pygame.Surface"):
        # Draw special effects first
        if self.is_slipping:
            # Fix: Ensure color values are capped at 255
            slip_color = tuple(min(c + 50, 255) for c in self.color)
            pygame.draw.rect(surface, slip_color,
                             (int(self.x) - 5, int(self.y) - 5, self.length + 10, self.height + 10), 3, border_radius=5)

        if self.shield_timer > 0:
            pygame.draw.rect(surface, CYAN, (int(self.x) - 5, int(self.y) - 5, self.length + 10, self.height + 10), 3,
                             border_radius=5)

        if self.boost_timer > 0:
            pygame.draw.circle(surface, ORANGE, (int(self.x), int(self.y + self.height // 2)), 10)

        # Draw boat body
        body_points = [
            (int(self.x), int(self.y + self.height * 0.75)),
            (int(self.x + 20), int(self.y + self.height * 0.9)),
            (int(self.x + self.length * 0.8), int(self.y + self.height)),
            (int(self.x + self.length * 0.95), int(self.y + self.height * 0.75)),
            (int(self.x + self.length * 0.9), int(self.y + self.height * 0.25)),
            (int(self.x + self.length * 0.7), int(self.y)),
            (int(self.x + 10), int(self.y + self.height * 0.1)),
        ]
        pygame.draw.polygon(surface, self.color, body_points)

        # Draw the raised stern decoration
        stern_height = 80
        stern_tip_x = int(self.x + self.length - 5)
        stern_tip_y = int(self.y + self.height / 2 - stern_height)
        stern_points = [
            (stern_tip_x, stern_tip_y),
            (int(self.x + self.length * 0.8), int(self.y + self.height)),
            (int(self.x + self.length * 0.75), int(self.y + self.height * 0.9)),
            (int(stern_tip_x - 5), int(self.y + self.height / 2 - stern_height * 0.8))
        ]
        pygame.draw.polygon(surface, BROWN, stern_points)
        pygame.draw.line(surface, YELLOW, (stern_tip_x, stern_tip_y), (stern_tip_x, int(self.y + self.height / 2)), 3)

        for i in range(self.rower_count):
            rower_base_x = int(self.x + 40 + i * (self.length - 60) / (self.rower_count - 1))
            rower_base_y = int(self.y + self.height * 0.6)
            seat_width = 15
            seat_height = 5
            pygame.draw.rect(surface, DARK_BROWN,
                             (rower_base_x - seat_width // 2, rower_base_y - seat_height, seat_width, seat_height))
            body_width = 8
            body_height = 15
            body_x = rower_base_x - body_width // 2
            body_y = rower_base_y - seat_height - body_height + self.rower_lean_offset
            pygame.draw.rect(surface, CLOTH_COLOR, (body_x, body_y, body_width, body_height))
            head_radius = 5
            head_x = rower_base_x
            head_y = body_y - head_radius
            pygame.draw.circle(surface, SKIN_COLOR, (head_x, head_y), head_radius)
            pygame.draw.rect(surface, HEAD_CLOTH_COLOR,
                             (head_x - head_radius, head_y - head_radius, head_radius * 2, head_radius * 1.5))
            oar_length = 30
            oar_angle_base = math.radians(20)
            oar_swing_amplitude = math.radians(60)
            oar_phase = self.oar_animation_time + (i * 0.1 * math.pi)
            oar_angle = oar_angle_base + oar_swing_amplitude * ((math.sin(oar_phase) + 1) / 2)
            oar_start_x = rower_base_x + body_width // 2 - 2
            oar_start_y = rower_base_y - seat_height - 5
            oar_end_x = oar_start_x + oar_length * math.cos(oar_angle)
            oar_end_y = oar_start_y - oar_length * math.sin(oar_angle)
            blade_width = 3
            blade_height = 8
            if math.degrees(oar_angle) > 50:
                blade_points = [
                    (oar_end_x - blade_width * math.sin(oar_angle), oar_end_y - blade_width * math.cos(oar_angle)),
                    (oar_end_x + blade_height * math.cos(oar_angle), oar_end_y - blade_height * math.sin(oar_angle)),
                    (oar_end_x + blade_width * math.sin(oar_angle), oar_end_y + blade_width * math.cos(oar_angle)),
                    (oar_end_x - blade_height * math.cos(oar_angle), oar_end_y + blade_height * math.sin(oar_angle))
                ]
                pygame.draw.polygon(surface, DARK_BROWN, blade_points)
            pygame.draw.line(surface, BROWN, (oar_start_x, oar_start_y), (oar_end_x, oar_end_y), 2)


class Obstacle:
    def __init__(self):
        self.x = random.randint(400, WIDTH - 200)
        self.y = random.randint(50, HEIGHT - 50)
        self.width = 40
        self.height = 20
        self.color = RED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class PowerUp:
    def __init__(self):
        self.x = random.randint(400, WIDTH - 200)
        self.y = random.randint(50, HEIGHT - 50)
        self.radius = 15
        self.type = random.choice(['speed_boost', 'shield', 'banana_slip', 'payasam_boost'])
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, surface):
        if self.type == 'speed_boost':
            color = ORANGE
        elif self.type == 'shield':
            color = CYAN
        elif self.type == 'banana_slip':
            color = BANANA_SLIP_COLOR
        else:
            color = PAYASAM_COLOR
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)


class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
        self.size = 5.0
        self.lifetime = 60

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))


# --- Sound Loading ---
try:
    # This line loads the sound from a WAV file.
    cheering_sound = pygame.mixer.Sound("cheer2.wav")
except pygame.error:
    print("Warning: Could not load cheer2.wav. Check if the file exists.")
    # Create a simple placeholder sound if the file is not found
    cheering_sound = None


# --- Functions ---

def create_particles(x, y, color, count=10):
    global particles
    for _ in range(count):
        particles.append(Particle(x, y, color))


def draw_water(surface, time_counter):
    surface.fill(BLUE)
    for y in range(0, HEIGHT, 20):
        for x in range(0, WIDTH, 20):
            wave = int(5 * math.sin(0.05 * x + time_counter * 0.1))
            pygame.draw.circle(surface, LIGHT_BLUE, (x, y + wave), 3)


def draw_finish_line():
    pygame.draw.line(screen, WHITE, (FINISH_LINE, 0), (FINISH_LINE, HEIGHT), 3)
    text = font.render("Finish 🏁", True, WHITE)
    screen.blit(text, (FINISH_LINE - 50, 10))


def draw_scoreboard():
    p1_text = font.render(
        f"P1 Dist: {int(p1.distance)} | Boost: {p1.boost_timer // 60}s | Shield: {p1.shield_timer // 60}s", True, WHITE)
    p2_text = font.render(
        f"P2 Dist: {int(p2.distance)} | Boost: {p2.boost_timer // 60}s | Shield: {p2.shield_timer // 60}s", True, WHITE)
    screen.blit(p1_text, (10, 10))
    screen.blit(p2_text, (10, 40))


def handle_boat_movement(boat, key_pressed):
    if key_pressed in boat.control_keys:
        if boat.is_slipping:
            boat.slip_counter += 1
            return

        if key_pressed in [pygame.K_RIGHT, pygame.K_d]:
            boat.horizontal_speed = 5
        elif key_pressed in [pygame.K_LEFT, pygame.K_a]:
            boat.horizontal_speed = -5

        if key_pressed in [pygame.K_UP, pygame.K_w]:
            boat.vertical_speed = -5
        elif key_pressed in [pygame.K_DOWN, pygame.K_s]:
            boat.vertical_speed = 5


def check_collision_obstacles(boat, obstacles):
    remaining_obstacles = []
    boat_rect = pygame.Rect(boat.x, boat.y, boat.length, boat.height)
    for obs in obstacles:
        if boat_rect.colliderect(obs.rect):
            if boat.shield_timer > 0:
                create_particles(obs.rect.centerx, obs.rect.centery, CYAN, 15)
            else:
                boat.horizontal_speed *= 0.5
                create_particles(obs.rect.centerx, obs.rect.centery, RED, 15)
        else:
            remaining_obstacles.append(obs)
    return remaining_obstacles


def check_collision_powerups(boat, powerups):
    remaining_powerups = []
    boat_rect = pygame.Rect(boat.x, boat.y, boat.length, boat.height)
    for pu in powerups:
        if boat_rect.colliderect(pu.rect):
            if pu.type == 'speed_boost':
                boat.boost_timer = FPS * 5
                create_particles(pu.rect.centerx, pu.rect.centery, ORANGE, 20)
            elif pu.type == 'shield':
                boat.shield_timer = FPS * 5
                create_particles(pu.rect.centerx, pu.rect.centery, CYAN, 20)
            elif pu.type == 'banana_slip':
                boat.is_slipping = True
                boat.slip_timer = FPS * 3
                create_particles(pu.rect.centerx, pu.rect.centery, BANANA_SLIP_COLOR, 20)
            elif pu.type == 'payasam_boost':
                boat.horizontal_speed += 50
                create_particles(pu.rect.centerx, pu.rect.centery, PAYASAM_COLOR, 20)
        else:
            remaining_powerups.append(pu)
    return remaining_powerups


def reset_game():
    global p1, p2, game_over, obstacles, powerups, particles, time_counter
    p1 = Boat(50, 150, YELLOW, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], "Player 1")
    p2 = Boat(50, 300, GREEN, [pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d], "Player 2")
    game_over = False
    obstacles = [Obstacle() for _ in range(6)]
    powerups = []
    particles = []
    time_counter = 0


def show_winner(winner_text):
    if cheering_sound:
        cheering_sound.play()
    quote = random.choice(WINNER_QUOTES)
    text = font.render(winner_text, True, WHITE)
    quote_text = font.render(quote, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(quote_text, (WIDTH // 2 - quote_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)


# --- Initialize game ---
p1 = Boat(50, 150, YELLOW, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], "Player 1")
p2 = Boat(50, 300, GREEN, [pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d], "Player 2")
obstacles = [Obstacle() for _ in range(6)]
powerups = []
particles = []
game_over = False
time_counter = 0

# --- Main loop ---
while True:
    time_counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()
            if not game_over:
                handle_boat_movement(p1, event.key)
                handle_boat_movement(p2, event.key)

    if not game_over:
        if random.randint(1, 150) == 1:
            obstacles.append(Obstacle())
        if random.randint(1, 400) == 1:
            powerups.append(PowerUp())

    p1.update()
    p2.update()

    for particle in particles:
        particle.update()
    particles = [p for p in particles if p.lifetime > 0]

    if not game_over:
        obstacles = check_collision_obstacles(p1, obstacles)
        obstacles = check_collision_obstacles(p2, obstacles)
        powerups = check_collision_powerups(p1, powerups)
        powerups = check_collision_powerups(p2, powerups)

    draw_water(screen, time_counter)
    draw_finish_line()
    for obs in obstacles:
        obs.draw(screen)
    for pu in powerups:
        pu.draw(screen)
    p1.draw(screen)
    p2.draw(screen)
    for particle in particles:
        particle.draw(screen)
    draw_scoreboard()

    if not game_over:
        if p1.x + p1.length >= FINISH_LINE:
            game_over = True
            show_winner("🏆 Player 1 Wins!")
        elif p2.x + p2.length >= FINISH_LINE:
            game_over = True
            show_winner("🏆 Player 2 Wins!")

    pygame.display.flip()
    clock.tick(FPS)