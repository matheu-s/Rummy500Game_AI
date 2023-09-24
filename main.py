import pygame, sys
from config.constants import *
from config.messages import Messages
from game.button import Button
from game.board import Board

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
MESSENGER = Messages(SCREEN)
pygame.display.set_caption("RUMMY 500")
BG = pygame.image.load("assets/images/bg.jpg")


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


def play():
    SCREEN.fill(GREEN_TABLE)

    board = Board(screen=SCREEN, messenger=MESSENGER)
    board.start_board()

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not board.check_input(MOUSE_POS):
                    main_menu()

        MESSENGER.check_queue()
        pygame.display.update()


def rules():
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(GREY)

        BTN_OPTIONS_BACK = Button(image=None, pos=(640, 490),
                                  text_input="BACK", font=get_font(80), base_color="White", hovering_color="Green")
        BTN_OPTIONS_BACK.changeColor(MOUSE_POS)
        BTN_OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_OPTIONS_BACK.is_clicked(MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#006400")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(WIDTH / 2, 300),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(WIDTH / 2, 450),
                                text_input="RULES", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(WIDTH / 2, 600),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.is_clicked(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.is_clicked(MENU_MOUSE_POS):
                    rules()
                if QUIT_BUTTON.is_clicked(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
