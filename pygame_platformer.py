import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fromage Finder')

# Load and scale custom font
font_path = 'fonts/Jersey10-Regular.ttf'
font = pygame.font.Font(font_path, 30)
title_font = pygame.font.Font(font_path, 40)
score_font = pygame.font.Font(font_path, 40)
congrats_font = pygame.font.Font(font_path, 35)

# Load and scale images for title screen and gameplay
background_image = pygame.image.load('images/louvre.png')  # Custom title screen background
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) 

level_1_background = pygame.image.load('images/louvre_2.png')  # Custom background for level 1
level_1_background = pygame.transform.scale(level_1_background, (WIDTH, HEIGHT))

level_2_background = pygame.image.load('images/louvre_2.png')  # Custom background for level 1
level_2_background = pygame.transform.scale(level_2_background, (WIDTH, HEIGHT))

start_button_image = pygame.image.load('images/start.png')  # Custom start button image
start_button_image = pygame.transform.scale(start_button_image, (150, 100)) 

player_image = pygame.image.load('images/rat.png')  # Custom player image
player_image = pygame.transform.scale(player_image, (50, 50))

cheese_image = pygame.image.load('images/cheese.png') # Custom cheese image
cheese_image = pygame.transform.scale(cheese_image, (30, 30)) 

pizza_image = pygame.image.load('images/pizza.png') # Custom pizza image
pizza_image = pygame.transform.scale(pizza_image, (42, 42))

donut_image = pygame.image.load('images/donut.png') # Custom pizza image
donut_image = pygame.transform.scale(donut_image, (46, 46))

candy_image = pygame.image.load('images/candy.png') # Custom candy image
candy_image = pygame.transform.scale(candy_image, (32, 62)) 

restart_button_image = pygame.image.load('images/restart.png')  # Custom restart button image
restart_button_image = pygame.transform.scale(restart_button_image, (100, 100)) 

# Load sound effects
start_button_sound = pygame.mixer.Sound('audio/point_2.mp3')
replay_button_sound = pygame.mixer.Sound('audio/point_2.mp3')
cheese_collect_sound = pygame.mixer.Sound('audio/point_2.mp3')
pizza_collect_sound = pygame.mixer.Sound('audio/point_2.mp3')
donut_collect_sound = pygame.mixer.Sound('audio/point_2.mp3')
candy_collect_sound = pygame.mixer.Sound('audio/point_3.mp3')


# Define colors
WHITE = (255, 255, 255)

# # Fonts
# font = pygame.font.SysFont("Jersey10-Regular", 40)

# Game variables
clock = pygame.time.Clock()
FPS = 60

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  # Set player image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 100
        self.velocity_y = 0
        self.score = 0
        self.jump_boost = 1 # Jump boost

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.y == HEIGHT - 100:
            self.velocity_y = -15 * self.jump_boost # Apply jump boost
        
        # Apply gravity
        self.velocity_y += 1
        self.rect.y += self.velocity_y
        
        # Prevent the player from falling through the ground
        if self.rect.y > HEIGHT - 100:
            self.rect.y = HEIGHT - 100
            self.velocity_y = 0
        
    def collect_point(self, points):
        self.score += points

    def apply_jump_boost(self):
        self.jump_boost = 1.5  # Increase jump height when candy is collected

    def reset_jump_boost(self):
        self.jump_boost = 1  # Reset jump boost after a period

# Define Cheese class for collecting cheese items
class Cheese(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = cheese_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define Pizza class for collecting pizza items
class Pizza(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pizza_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define Donut class for collecting donut items
class Donut(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = donut_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define Candy class for collecting candy items
class Candy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = candy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Title screen with custom background and start button
def show_title_screen():
    screen.fill(WHITE)  # Fallback fill (white), in case background loading fails
    screen.blit(background_image, (0, 0))  # Display the custom title screen background

    # Define the position for the start button
    start_button_rect = start_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Display start button image
    screen.blit(start_button_image, start_button_rect)

    # Display the title text
    title_text = title_font.render('Fromage Finder', True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    pygame.display.update()

    # Wait for start button click
    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_button_sound.play()
                    start_game = True

# Level 1 with cheese items
def level_1(player):
    player.rect.x = 100
    player.rect.y = HEIGHT - 100
    player.score = 0
    running = True

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    cheeses = pygame.sprite.Group()
    
    # Add 10 cheese items to the level, in random positions within jumping distance
    for _ in range(10):
        x = random.randint(150, WIDTH - 50)
        y = random.randint(HEIGHT - 230, HEIGHT - 100)  # Ensure within jumping distance. Original settings were HEIGHT - 150, HEIGHT - 50
        cheese = Cheese(x, y)
        all_sprites.add(cheese)
        cheeses.add(cheese)

    while running:
        screen.fill(WHITE)  # Fill the screen with a solid color before rendering the background
        screen.blit(level_1_background, (0, 0))  # Display the custom level 1 background

        player.update()
        screen.blit(player.image, player.rect)  # Draw player with custom image

        # Display score
        score_text = score_font.render(f'Score: {player.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display level 1 text
        title_text = font.render('Jump to collect the cheese!', True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Check for collisions with cheese items
        for cheese in cheeses:
            if player.rect.colliderect(cheese.rect):
                player.collect_point(10)  # Each cheese is worth 10 points
                cheese.kill()  # Remove the cheese item once collected

                # Play the cheese collection sound
                cheese_collect_sound.play()

        # Draw all sprites (player and cheeses)
        all_sprites.update()  # Update all sprite groups
        cheeses.draw(screen)  # Draw all cheeses on the screen

        # Level 1 condition
        if player.score >= 100:
            return True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Level 2 with pizza items
def level_2(player):
    player.rect.x = 100
    player.rect.y = HEIGHT - 100
    player.score = 0
    running = True

    all_sprites = pygame.sprite.Group()
    pizzas = pygame.sprite.Group()

    for _ in range(15):
        x = random.randint(150, WIDTH - 50)
        y = random.randint(HEIGHT - 230, HEIGHT - 100)
        pizza = Pizza(x, y)
        all_sprites.add(pizza)
        pizzas.add(pizza)

    while running:
        screen.fill(WHITE)
        screen.blit(level_2_background, (0, 0))

        player.update()
        screen.blit(player.image, player.rect)

        score_text = score_font.render(f'Score: {player.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        for pizza in pizzas:
            if player.rect.colliderect(pizza.rect):
                player.collect_point(10)
                pizza.kill()
                pizza_collect_sound.play()

        all_sprites.update()
        pizzas.draw(screen)

        if player.score >= 150:
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Level 3 with donut items, and candy items with jump boost
def level_3(player):
    player.rect.x = 100
    player.rect.y = HEIGHT - 100
    player.score = 0
    running = True

    all_sprites = pygame.sprite.Group()
    donuts = pygame.sprite.Group()
    candies = pygame.sprite.Group()

    for _ in range(20):
        x = random.randint(150, WIDTH - 50)
        y = random.randint(HEIGHT - 300, HEIGHT - 150)  # Donuts are scattered higher
        donut = Donut(x, y)
        all_sprites.add(donut)
        donuts.add(donut)

    for _ in range(1):
        x = random.randint(150, WIDTH - 50)
        y = random.randint(HEIGHT - 230, HEIGHT - 100)  # Ensure within jumping distance
        candy = Candy(x, y)
        all_sprites.add(candy)
        candies.add(candy)

    while running:
        screen.fill(WHITE)
        screen.blit(level_2_background, (0, 0))

        player.update()
        screen.blit(player.image, player.rect)

        score_text = score_font.render(f'Score: {player.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display the jump hint text
        hint_text = font.render('Collect the lollipop to jump higher!', True, WHITE)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 6))
       
        for donut in donuts:
            if player.rect.colliderect(donut.rect):
                player.collect_point(10)
                donut.kill()
                donut_collect_sound.play()

        for candy in candies:
            if player.rect.colliderect(candy.rect):
                player.apply_jump_boost()  # Apply jump boost when candy is collected
                candy.kill()
                candy_collect_sound.play()

        all_sprites.update()
        donuts.draw(screen)
        candies.draw(screen)

        if player.score >= 200:
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Win screen with restart button
def win_screen():
    screen.blit(level_1_background, (0, 0))  # Win screen has the same background as level 1

    # Display win text
    win_text = congrats_font.render('Great job! You collected all of the delicious foods.', True, WHITE)

    # Display win text centered at top of screen
    win_x = (WIDTH - win_text.get_width()) // 2  # Center horizontally
    screen.blit(win_text, (win_x, 60)) 
    
    # Display restart button
    restart_button_rect = restart_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    restart_button_image_x = (WIDTH - restart_button_image.get_width()) // 2  # Center horizontally
    screen.blit(restart_button_image, (restart_button_image_x, 280))

    # Display restart text
    restart_text = font.render('Play Again', True, WHITE)
    # Display restart text at bottom of screen
    restart_x = (WIDTH - restart_text.get_width()) // 2  # Center horizontally
    screen.blit(restart_text, (restart_x, 245)) 

    pygame.display.update()

    # Wait for restart button click
    restart_game = False
    while not restart_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    restart_game = True
                    replay_button_sound.play()
                    return True  # Return to restart the game

# Main Game Loop
def game():
    player = Player()
    show_title_screen()
    if level_1(player):
        if level_2(player):  # Proceed to level 2
            if level_3(player): # Proceed to level 3
                if win_screen():
                    game()  # Restart the game


# Run the game
if __name__ == '__main__':
    game()


