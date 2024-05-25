import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Algorithm Selection")

# Load and scale background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

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

def algorithm_selection():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button is clicked and launch the corresponding algorithm visualization
                if dijkstra_button.collidepoint(event.pos):
                    subprocess.Popen(["python", "dijkstra.py"])
                    pygame.quit()
                    sys.exit()
                elif bellman_ford_button.collidepoint(event.pos):
                    subprocess.Popen(["python", "bellman_ford.py"])
                    pygame.quit()
                    sys.exit()
                elif floyd_warshall_button.collidepoint(event.pos):
                    subprocess.Popen(["python", "floyd_warshall.py"])
                    pygame.quit()
                    sys.exit()

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Draw elements on top of the background
        draw_text("Select Algorithm", font, WHITE, screen, screen_width // 2, 100)

        # Draw Dijkstra button
        dijkstra_button = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(screen, GRAY, dijkstra_button)
        draw_text("Dijkstra", font, WHITE, screen, dijkstra_button.centerx, dijkstra_button.centery)

        # Change button color on hover
        if dijkstra_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (180, 180, 180), dijkstra_button)
            draw_text("Dijkstra", font, WHITE, screen, dijkstra_button.centerx, dijkstra_button.centery)

        # Draw Bellman-Ford button
        bellman_ford_button = pygame.Rect(275, 300, 250, 50)
        pygame.draw.rect(screen, GRAY, bellman_ford_button)
        draw_text("Bellman-Ford", font, WHITE, screen, bellman_ford_button.centerx, bellman_ford_button.centery)

        # Change button color on hover
        if bellman_ford_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (180, 180, 180), bellman_ford_button)
            draw_text("Bellman-Ford", font, WHITE, screen, bellman_ford_button.centerx, bellman_ford_button.centery)

        # Draw Floyd-Warshall button
        floyd_warshall_button = pygame.Rect(250, 400, 300, 50)
        pygame.draw.rect(screen, GRAY, floyd_warshall_button)
        draw_text("Floyd-Warshall", font, WHITE, screen, floyd_warshall_button.centerx, floyd_warshall_button.centery)

        # Change button color on hover
        if floyd_warshall_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (180, 180, 180), floyd_warshall_button)
            draw_text("Floyd-Warshall", font, WHITE, screen, floyd_warshall_button.centerx, floyd_warshall_button.centery)

        pygame.display.flip()

algorithm_selection()

