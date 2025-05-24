# main.py
import pygame
from constants import *
from game import Game

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rotate Tetris")
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.rotate_board()
            elif event.key == pygame.K_UP:
                original_blocks = game.current_piece.blocks[:]
                game.current_piece.rotate()
                if game.check_collision():
                    game.current_piece.blocks = original_blocks  # desfaz se colidir

    # Chave para detectar teclas pressionadas continuamente
    keys = pygame.key.get_pressed()
    game.handle_held_keys(keys)

    game.update()

    screen.fill(BLACK)
    game.draw_grid(screen)
    game.draw_piece(screen)
    pygame.display.flip()

pygame.quit()
