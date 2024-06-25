import flet as ft 
import pygame
import random

window_width = 300
window_height = 600
block_size = 30

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 165, 0)
]

shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 1, 1],
     [1, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 1, 1, 1]],
    
    [[1, 1],
     [1, 1]],
    
    [[0, 1, 0],
     [1, 1, 1]],
    
    [[1, 1, 1],
     [1, 0, 0]]
]

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.game_over = False
        self.figure = None
        self.next_figure = None
        self.new_figure()
    
    def new_figure(self):
        self.figure = self.next_figure if self.next_figure else [random.choice(shapes), 0, self.width // 2 - 2]
        self.next_figure = [random.choice(shapes), 0, self.width // 2 - 2]

    def rotate_figure(self):
        self.figure[0] = [list(row) for row in zip(*self.figure[0][::-1])]
    
    def check_collision(self):
        shape, y, x = self.figure
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] and self.field[y + row][x + col]:
                    return True
        return False
    
    def freeze(self):
        shape, y, x = self.figure
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    self.field[y + row][x + col] = shape[row][col]
        self.clear_lines()
        self.new_figure()
        if self.check_collision():
            self.game_over = True
    
    def clear_lines(self):
        self.field = [row for row in self.field if any(block == 0 for block in row)] + [[0 for _ in range(self.width)] for _ in range(len(self.field) - len(self.field))]
    
    def move(self, dx):
        if not self.game_over:
            self.figure[2] += dx
            if self.check_collision():
                self.figure[2] -= dx
    
    def drop(self):
        if not self.game_over:
            self.figure[1] += 1
            if self.check_collision():
                self.figure[1] -= 1
                self.freeze()
    
    def instant_drop(self):
        while not self.check_collision():
            self.figure[1] += 1
        self.figure[1] -= 1
        self.freeze()

def main():
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Тетрис')
    clock = pygame.time.Clock()
    game = Tetris(window_height // block_size, window_width // block_size)
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_UP:
                    game.rotate_figure()
                elif event.key == pygame.K_SPACE:
                    game.instant_drop()
        game.drop()
        for y in range(game.height):
            for x in range(game.width):
                pygame.draw.rect(screen, colors[game.field[y][x]], (x * block_size, y * block_size, block_size, block_size))
        for y in range(len(game.figure[0])):
            for x in range(len(game.figure[0][y])):
                if game.figure[0][y][x]:
                    pygame.draw.rect(screen, colors[game.figure[0][y][x]], ((game.figure[2] + x) * block_size, (game.figure[1] + y) * block_size, block_size, block_size))
        pygame.display.flip()
        clock.tick(10)

if name == "__main__":
    main()