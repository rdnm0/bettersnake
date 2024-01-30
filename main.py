import pygame
import random
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 25
CELL_NUMBER = 30
DISPLAY_SIZE = Vector2(CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER)
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game States
class GameState:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.paused = False

    def reset(self):
        self.score = 0
        self.game_over = False
        self.paused = False

# Snake class
class Snake:
    def __init__(self, game_state):
        self.body = [Vector2(CELL_NUMBER / 2, CELL_NUMBER / 2),
                     Vector2(CELL_NUMBER / 2, CELL_NUMBER / 2 - 1),
                     Vector2(CELL_NUMBER / 2, CELL_NUMBER / 2 - 2)]
        self.direction = Vector2(0, 1)
        self.game_state = game_state

    def move(self):
        if not self.game_state.paused:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def draw(self, screen):
        for block in self.body:
            pygame.draw.rect(screen, WHITE, (block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (block.x * CELL_SIZE + 2, block.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))

    def collide_with_fruit(self, fruit):
        return self.body[0].x == fruit.pos.x and self.body[0].y == fruit.pos.y

    def collide_with_self(self):
        return self.body[0] in self.body[1:]

# Fruit class
class Fruit:
    def __init__(self, snake):
        self.pos = self.generate_random_position(snake)

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.pos.x * CELL_SIZE + CELL_SIZE / 2), int(self.pos.y * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2)

    def generate_random_position(self, snake):
        while True:
            x = random.randint(0, CELL_NUMBER - 1)
            y = random.randint(0, CELL_NUMBER - 1)
            if Vector2(x, y) not in snake.body:
                return Vector2(x, y)

# Game Over Screen
def show_game_over_screen(screen, game_state):
    font = pygame.font.SysFont("8bitwondernominal", int(2 / 3 * CELL_SIZE))
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render("Score: " + str(game_state.score), True, WHITE)
    restart_text = font.render("Press R to restart", True, WHITE)

    screen.blit(game_over_text, (DISPLAY_SIZE.x / 2 - game_over_text.get_width() / 2, DISPLAY_SIZE.y / 3))
    screen.blit(score_text, (DISPLAY_SIZE.x / 2 - score_text.get_width() / 2, DISPLAY_SIZE.y / 2))
    screen.blit(restart_text, (DISPLAY_SIZE.x / 2 - restart_text.get_width() / 2, DISPLAY_SIZE.y / 1.5))






# Main Function
def main():
    # Initialize screen
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # Game State
    game_state = GameState()

    # Snake and Fruit
    snake = Snake(game_state)
    fruit = Fruit(snake)

    # Game Loop
    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction.y != 1:
                    snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and snake.direction.y != -1:
                    snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT and snake.direction.x != 1:
                    snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction.x != -1:
                    snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_r and game_state.game_over:
                    game_state.reset()
                    snake = Snake(game_state)
                    fruit = Fruit(snake)
                elif event.key == pygame.K_p:
                    game_state.paused = not game_state.paused

        # Game Over Logic
        if game_state.game_over:
            screen.fill(BLACK)
            show_game_over_screen(screen, game_state)
        else:
            # Update
            snake.move()
            if snake.collide_with_fruit(fruit):
                game_state.score += 1
                snake.body.append(snake.body[-1])
                fruit = Fruit(snake)

            if snake.body[0].x < 0 or snake.body[0].x >= CELL_NUMBER or snake.body[0].y < 0 or snake.body[0].y >= CELL_NUMBER or snake.collide_with_self():
                play_collision_sound()
                game_state.game_over = True

            # Draw
            screen.fill(BLACK)
            snake.draw(screen)
            fruit.draw(screen)

            # Display Score
            score_font = pygame.font.SysFont("8bitwondernominal", int(2 / 3 * CELL_SIZE))
            score_text = score_font.render("Score: " + str(game_state.score), True, WHITE)
            screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
