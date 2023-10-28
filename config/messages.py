import pygame
from config.constants import *


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


class Messages:
    screen = None
    message_queue = None

    def __init__(self, screen):
        self.screen = screen
        self.message_queue = []

    def add_message(self, text, milliseconds=None):
        start_time = pygame.time.get_ticks()
        erase_time = None
        if milliseconds:
            erase_time = start_time + milliseconds
        message = {
            'text': text,
            'erase_time': erase_time
        }
        self.message_queue.append(message)

    def check_queue(self):
        if not len(self.message_queue):
            return

        current_time = pygame.time.get_ticks()
        message = self.message_queue[0]

        if current_time < message['erase_time']:
            font = get_font(24)
            text = font.render(message['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT - 225))
            self.screen.blit(text, text_rect)
        else:
            pygame.draw.rect(self.screen, GREEN_TABLE, pygame.Rect((WIDTH/2)-300, (HEIGHT -250), 700, 50))
            pygame.display.flip()
            self.message_queue.pop(0)


