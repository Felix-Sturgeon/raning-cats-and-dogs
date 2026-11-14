from __future__ import annotations
from typing import TYPE_CHECKING

import pygame.font

from resource_game import resource_path

if TYPE_CHECKING:
    from puppy_invasion import PuppyInvasion

class Buttons:
    """按钮相关类"""
    def __init__(self, gamemain: PuppyInvasion, msg):
        # 引入游戏屏幕
        self.screen = gamemain.screen
        self.screen_rect = gamemain.screen.get_rect()
        # 属性
        self.width, self.height = 200, 50
        self.button_color = (150, 150, 150)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font(str(resource_path("AlibabaPuHuiTi-3-45-Light.ttf")), 30)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
