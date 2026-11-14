from __future__ import annotations
from typing import TYPE_CHECKING

import pygame.font

from resource_game import resource_path

if TYPE_CHECKING:
    from puppy_invasion import PuppyInvasion

class infoboard:
    """信息面板"""
    #初始化
    def __init__(self, gamemain: PuppyInvasion):
        # 引用
        self.screen = gamemain.screen
        self.screen_rect = gamemain.screen.get_rect()
        self.settings = gamemain.settings
        self.gamestats = gamemain.gamestate

        # 状态属性
        self.state_color = (200, 200, 200)
        self.state_font = pygame.font.Font(str(resource_path("AlibabaPuHuiTi-3-45-Light.ttf")), 26)
        # 事件属性
        self.event_text = ""
        self.event_color = (255, 2, 2)
        self.event_font = pygame.font.Font(str(resource_path("AlibabaPuHuiTi-3-45-Light.ttf")), 40)
        self.event_image = None
        # 准备图像
        self.prep_info()
    #图像
    def prep_info(self):
        self.state_prep_image()
        self.event_prep_imgae()

    def state_prep_image(self):
        state_str = \
        (
            f"郑头等级： {self.gamestats.headship_level}    "
            f"生命值： {self.gamestats.headships_left}  "
            f"剩余子弹： {self.gamestats.bullets_left}  "
            f"分数： {self.gamestats.score}"
        )
        self.state_image = self.state_font.render\
        (

            state_str, True, self.state_color, self.settings.bg_color
        )
        self.state_rect = self.state_image.get_rect()
        self.state_rect.right = self.screen_rect.right - 10
        self.state_rect.top = self.screen_rect.top + 10

    def event_prep_imgae(self):
        current_event = self.gamestats.current_event
        if current_event:
            self.event_image = self.event_font.render\
            (
                current_event, True, self.event_color, self.settings.bg_color 
            )
            self.event_rect = self.event_image.get_rect()
            self.event_rect.midtop = \
            (
                self.screen_rect.centerx, self.state_rect.bottom + 10
            )
        else:
            self.event_image = None 

    def show_info(self, gamemain: PuppyInvasion):
        """展示信息"""
        self.screen.blit(self.state_image, self.state_rect)
        if self.event_image:
            self.screen.blit(self.event_image, self.event_rect)
    
