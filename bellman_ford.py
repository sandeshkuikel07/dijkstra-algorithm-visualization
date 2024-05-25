import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bellman-Ford Algorithm Visualization")

# Load and scale background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Fonts
font_size = 24
font_bold = True
font_name = "times"

font = pygame.font.SysFont(font_name, font_size, bold=font_bold)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def bellman_ford_visualization():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_image, (0, 0))
        draw_text("Sorry, we don't have this visualization available right now", font, WHITE, screen, screen_width // 2, screen_height // 2)
        pygame.display.flip()

bellman_ford_visualization()

