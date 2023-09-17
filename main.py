import pygame, sys
from config.constants import *
from game.button import Button
from game.board import Board

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUMMY 500")
BG = pygame.image.load("assets/images/bg.jpg")


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


def play():
    SCREEN.fill(GREEN_TABLE)

    board = Board()
    board.start_board(screen=SCREEN)

    BTN_PLAY_BACK = Button(image=None, pos=(WIDTH - 275, 660),
                           text_input="BACK", font=get_font(30), base_color="White", hovering_color="Blue")
    BTN_PLAY_BACK.update(SCREEN)

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_PLAY_BACK.isClicked(MOUSE_POS):
                    main_menu()
                board.check_input(MOUSE_POS)
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
                if BTN_OPTIONS_BACK.isClicked(MOUSE_POS):
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
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(640, 400),
                                text_input="RULES", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(640, 550),
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
                if PLAY_BUTTON.isClicked(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.isClicked(MENU_MOUSE_POS):
                    rules()
                if QUIT_BUTTON.isClicked(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
