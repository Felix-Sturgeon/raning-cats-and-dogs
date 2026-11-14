from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from headship import IMAGE_PATH
from setting import Settings
from resource_game import resource_path

if TYPE_CHECKING:
    from puppy_invasion import PuppyInvasion

#IMAGE_PATH = Path(__file__).parent/"images"/"puppy.jpg"
IMAGE_PATH = resource_path("images", "puppy.jpg")

class Puppy(Sprite):
    """小狗"""
    def __init__(self, gamemain: PuppyInvasion):
        super().__init__()
        #引用屏幕
        self.screen = gamemain.screen
        #引用设置
        self.settings = Settings()
        #加载小狗
        self.image = pygame.image.load(IMAGE_PATH).convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        #小狗刷新位置
        screen_x, screen_y = self.screen.get_size()
        image_x, image_y = self.image.get_size()
        spawn_step_x = image_x + self.settings.puppy_interval
        init_position_y = self.settings.puppy_initposition_y
        self.all_position = \
            [(x, init_position_y) for x in range(15, screen_x - 2 * image_x, spawn_step_x)]
        self.available_position = self.all_position.copy()
        position_xy = random.choice(self.available_position)
        self.available_position.remove(position_xy)
        self.rect.x, self.rect.y = position_xy
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.puppy_speed
        self.rect.y = self.y
        
