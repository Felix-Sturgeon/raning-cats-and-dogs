from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from resource_game import resource_path

if TYPE_CHECKING:
    from puppy_invasion import PuppyInvasion
    from setting import Settings

#IMAGE_PATH = Path(__file__).parent/"images"/"headship.jpg"
IMAGE_PATH = resource_path("images", "headship.jpg")

class HeadShip:
    """飞船设置"""
    def __init__(self, gamemain: PuppyInvasion):
        #导入设置
        self.settings: Settings = gamemain.settings
        #飞船图片加载及尺寸调整
        self.image = pygame.image.load(IMAGE_PATH).convert()
        self.image = pygame.transform.scale(self.image, (90, 110))
        self.rect = self.image.get_rect()
        #游戏屏幕
        self.screen = gamemain.screen
        self.screen_rect = gamemain.screen.get_rect()
        #飞船位置
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """对飞船数据更新"""
        #飞船位置调整
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.headship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.headship_speed
        self.rect.x = self.x

    def blitme(self, gamemain: PuppyInvasion):
        """粘贴飞船图标"""
        if gamemain.gamestate.game_active:
            self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """重置飞船位置"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
