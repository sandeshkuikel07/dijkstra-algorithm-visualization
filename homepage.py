import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dijkstra Algorithm Visualization")

# Load background image
background_image = pygame.image.load("background.jpg")

# Colors
NAVY_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Fonts
font_size = 36
font_bold = True
font_name = "times"  # Times Roman font

font = pygame.font.SysFont(font_name, font_size, bold=font_bold)
small_font_size = 24
small_font_bold = True
small_font_name = "times"  # Times Roman font
small_font = pygame.font.SysFont(small_font_name, small_font_size, bold=small_font_bold)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
def homepage():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If user clicks on "Start", launch the dijkstra.py game
                if start_button.collidepoint(event.pos):
                    subprocess.Popen(["python", "algorithmselection.py"])
                    pygame.quit()
                    sys.exit()

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Draw elements on top of the background
        draw_text("Dijkstra Algorithm Visualization", font, WHITE, screen, screen_width // 2, 150)

        # Draw Start button
        start_button = pygame.Rect(300, 250, 200, 50)
        pygame.draw.rect(screen, GRAY, start_button)
        draw_text("Start", font, WHITE, screen, start_button.centerx, start_button.centery)

        # Change button color on hover
        if start_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (180, 180, 180), start_button)
            draw_text("Start", font, WHITE, screen, start_button.centerx, start_button.centery)
            

        # Draw instructions
        draw_text("BY", small_font, WHITE, screen, screen_width // 2, screen_height * 0.60)
        draw_text("Sandesh Kuikel", small_font, WHITE, screen, screen_width // 2, screen_height * 0.65)


        pygame.display.flip()

homepage()

