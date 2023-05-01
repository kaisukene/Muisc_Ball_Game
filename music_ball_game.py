import pygame
import random

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Music ball Game")

# Set up the clock
clock = pygame.time.Clock()

# Define the Circle class
class Circle:
    def __init__(self, x, y, color, note):
        self.x = x
        self.y = y
        self.color = color
        self.note = note

    def move(self):
        self.y += 5

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 25)
        font = pygame.font.SysFont("arial", 18)
        text = font.render(self.note, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

def start_screen():
    font_title = pygame.font.SysFont("arial", 48)
    font_instructions = pygame.font.SysFont("arial", 24)
    title_text = font_title.render("Music Tiles Game", True, WHITE)
    instructions_text = font_instructions.render("Press SPACE to start", True, WHITE)
    title_text_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
    instructions_text_rect = instructions_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
    screen.blit(title_text, title_text_rect)
    screen.blit(instructions_text, instructions_text_rect)
    pygame.display.update()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def create_game(root):
    """Create the game."""
    # Set the title of the window.
    root.title("My Game")

    # Create the felt for the game and add it to the root window.
    felt = Frame(root, bg="green")
    felt.pack(fill="both", expand=True)

    # Create the labels for the game and add them to the felt.
    label_1 = Label(felt, text="Label 1", font=("Arial", 24), bg="yellow")
    label_1.pack(padx=10, pady=10)

    label_2 = Label(felt, text="Label 2", font=("Arial", 24), bg="yellow")
    label_2.pack(padx=10, pady=10)

    # Create the frame for the buttons and add it to the felt.
    button_frame = Frame(felt)
    button_frame.pack(side="bottom", pady=10)

    # Create the buttons for the game.
    create_buttons(button_frame)

    # Set the focus to the root window so that keyboard events are handled properly.
    root.focus_set()

    # Start the game loop.

    root.mainloop()


# Define the game loop
def game_loop():
    start_screen()

    # Initialize game variables
    circles = []
    score = 0
    missed = 0
    font = pygame.font.SysFont("arial", 24)
    last_circle_time = pygame.time.get_ticks()
    game_running = True

    while game_running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for circle in circles:
                    if ((mouse_x - circle.x) ** 2 + (mouse_y - circle.y) ** 2) ** 0.5 <= 25:
                        circles.remove(circle)
                        score += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = False

        # Generate new circle
        current_time = pygame.time.get_ticks()
        time_since_last_circle = current_time - last_circle_time
        if time_since_last_circle > random.randint(500, 1500):
            colors = ["red", "blue", "green", "yellow","white","brown","pink","purple","gray","beige"]
            color = random.choice(colors)
            notes = ["Cis", "D", "E", "Fis", "G", "A", "B"]
            note = random.choice(notes)
            circle = Circle(random.randint(25, screen_width - 25), 0, color, note)
            circles.append(circle)
            last_circle_time = current_time

        # Move and draw the circles
        screen.fill(BLACK)
        for circle in circles:
            circle.move()
            circle.draw()

        # Update the score and missed count
        score_text = font.render("Score: " + str(score), True, WHITE)
        missed_text = font.render("Missed: " + str(missed), True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(missed_text, (10, 40))

        # Check for missed circles

        for circle in circles:
            if circle.y > screen_height:
                circles.remove(circle)
                missed += 1

        # Update the display
        pygame.display.update()

        # Check for game over
        if missed >=10:
            game_over()

        # Set the frame rate
        clock.tick(60)



# Define the game over function
def game_over():
    font = pygame.font.SysFont("arial", 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)

    # Create the start again button
    start_button = pygame.Rect(screen_width / 4, screen_height / 2 + 50, screen_width / 4, 50)
    pygame.draw.rect(screen, WHITE, start_button)
    start_text = font.render("Start Again", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    # Create the quit button
    quit_button = pygame.Rect(screen_width / 2 + screen_width / 4, screen_height / 2 + 50, screen_width / 4, 50)
    pygame.draw.rect(screen, WHITE, quit_button)
    quit_text = font.render("Quit", True, BLACK)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

    # Update the display
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    game_loop()
                elif quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    quit()
game_loop()


