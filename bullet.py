from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from puppy_invasion import PuppyInvasion
    

class Bullet(Sprite):
    """子弹"""
    def __init__(self, gamemain: PuppyInvasion):
        super().__init__()
        self.screen = gamemain.screen
        self.settings = gamemain.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect\
            (0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = gamemain.headship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """子弹数据更新"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘画子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        
        
