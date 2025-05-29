import pygame
from constants import *
from game import Game

pygame.init()
#define o tamanho da janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rotate Tetris")
#contados de Frames por segundo, aonde controla o tempo e a taxa de frames
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    #Define a taxa de frames por segundo
    clock.tick(FPS)
    #Captura eventos como as teclas pressionadas ou o fechamento da janela
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
                    game.current_piece.blocks = original_blocks  # desfaz os se colidir
    #Adiciona a lógica de pressionamento das teclas ao invês de apenas clique único
    keys = pygame.key.get_pressed()
    game.handle_held_keys(keys)

    game.update()

    screen.fill(BLACK)
    game.draw_grid(screen)
    game.draw_piece(screen)
    pygame.display.flip()

pygame.quit()
