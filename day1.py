import pygame
import sys
# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Onam Snake Boat Race")

# Colors
BLUE = (30, 96, 145)
YELLOW = (255, 209, 102)
GREEN = (6, 214, 160)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()

# Finish line
FINISH_LINE = WIDTH - 100  # slightly before the edge
font = pygame.font.SysFont("arial", 28, bold=True)

# Boat class
class Boat:
    def __init__(self, x, y, color, key, name="Player"):
        self.x = x
        self.y = y
        self.color = color
        self.key = key
        self.name = name
        self.speed = 0
        self.length = 120
        self.height = 30
        self.oar_offset = 0
        self.oar_direction = 1

    def update(self):
        # Move the boat
        self.x += self.speed
        self.speed *= 0.9  # friction

        # Animate oars up/down
        self.oar_offset += self.oar_direction * 2
        if self.oar_offset > 5 or self.oar_offset < -5:
            self.oar_direction *= -1

    def draw(self, surface: "pygame.Surface"):
        # Draw the boat body as a polygon (snake boat shape)
        points = [
            (self.x, self.y + self.height//2),
            (self.x + self.length*0.8, self.y + self.height),
            (self.x + self.length, self.y + self.height//2),
            (self.x + self.length*0.8, self.y),
            (self.x, self.y + self.height//2),
            (self.x + self.length*0.1, self.y + self.height//2)
        ]
        pygame.draw.polygon(surface, self.color, points)

        # Draw rowers
        rower_count = 8
        for i in range(rower_count):
            rower_x = self.x + 10 + i * 12
            rower_y = self.y + self.height//2
            pygame.draw.circle(surface, (255, 200, 150), (int(rower_x), int(rower_y)), 4)

        # Draw animated oars
        for i in range(rower_count):
            oar_x = self.x + 10 + i * 12
            oar_y = self.y + self.height//2
            pygame.draw.line(surface, (150, 75, 0),
                             (oar_x, oar_y),
                             (oar_x + 6, oar_y - 12 + self.oar_offset), 2)

# Initialize boats
p1 = Boat(50, 150, YELLOW, pygame.K_a, "Player 1")
p2 = Boat(50, 300, GREEN, pygame.K_l, "Player 2")
game_over = False

# Functions
def draw_finish_line():
    pygame.draw.line(screen, WHITE, (FINISH_LINE, 0), (FINISH_LINE, HEIGHT), 3)
    text = font.render("Finish 🏁", True, WHITE)
    screen.blit(text, (FINISH_LINE - 50, 10))

def reset_game():
    global p1, p2, game_over
    p1 = Boat(50, 150, YELLOW, pygame.K_a)
    p2 = Boat(50, 300, GREEN, pygame.K_l)
    game_over = False

def show_winner(winner_text):
    text = font.render(winner_text, True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()
            if not game_over:
                if event.key == p1.key:
                    p1.speed += 5
                if event.key == p2.key:
                    p2.speed += 5

    # Update screen
    screen.fill(BLUE)
    draw_finish_line()
    p1.update()
    p2.update()
    p1.draw(screen)
    p2.draw(screen)
    import random


    cheer_sounds= [
        pygame.mixer.Sound(r"C:\Users\Abraham Santhosh\OneDrive\Desktop\onam game\cheer2.wav"),
       ]
    # When player presses key:


    # Check winner
    if not game_over:
        if p1.x + p1.length >= FINISH_LINE:
            game_over = True
            show_winner("🏆 Player 1 Wins! Mahabali approves 🎉")
            cheer_sounds = [
                pygame.mixer.Sound(r"C:\Users\Abraham Santhosh\OneDrive\Desktop\onam game\cheer2.wav"),
            ]
            # When player presses key:
            random.choice(paddle_sounds).play()
        elif p2.x + p2.length >= FINISH_LINE:
            game_over = True
            show_winner("🏆 Player 2 Wins! Extra banana chips 🎉")
        cheer_sounds = [
            pygame.mixer.Sound(r"C:\Users\Abraham Santhosh\OneDrive\Desktop\onam game\cheer2.wav"),
        ]
        # When player presses key:
        random.choice(paddle_sounds).play()
    pygame.display.flip()
    clock.tick(60)
