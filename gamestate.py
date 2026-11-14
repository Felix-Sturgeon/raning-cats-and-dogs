from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from puppy_invasion import PuppyInvasion

class Gamestate:
    """游戏信息"""
    def __init__(self, gamemain: PuppyInvasion):
        """初始化游戏信息"""
        self.settings = gamemain.settings        
        self.reset_starts(gamemain)

    def reset_starts(self, gamemain: PuppyInvasion):
        """重置与初始化信息"""
        self.game_active = False
        self.headship_level = self.settings.headship_init_level
        self.score = 0
        self.kill_num = 0
        self.headships_left = self.settings.ships_limit
        self.bullets_left = self.settings.bullet_num_allowed
        self.settings.__init__()
        self.clear_event()
        gamemain.headship.center_ship()

    # 信息
    def sent_event(self, text: str, duration_ms: int = 2000):
        """显示信息， duration_ms毫秒后消失"""
        self.event_text = text
        self.event_until = pygame.time.get_ticks() + duration_ms

    def clear_event(self):
        """清空当前显示事件"""
        self.event_text = ""
        self.event_until = 0

    @property
    def current_event(self) -> str:
        """显示当前事件"""
        if self.event_text and pygame.time.get_ticks() >= self.event_until:
            self.event_text = ""
        return self.event_text

    def update_headship_level(self):
        #等级2
        if self.kill_num == 10:
            self.headship_level += 1
            self.sent_event("郑头成功升级")
            self.headships_left += 1
            self.settings.bullet_width += 1
        #等级3
        if self.kill_num == 30:
            self.headship_level += 1
            self.sent_event("郑头成功升级")
            self.headships_left += 1
            self.settings.headship_speed += 1
            self.settings.bullet_width += 1
        #等级4
        if self.kill_num == 60:
            self.headship_level += 1
            self.sent_event("郑头成功升级")
            self.headships_left += 1
            self.settings.bullet_width += 1
        #等级5
        if self.kill_num == 100:
            self.headship_level += 1
            self.sent_event("郑头成功升级")
            self.headships_left += 1
            self.settings.headship_speed += 1
            self.settings.bullet_width += 1
            self.settings.bullet_num_allowed += 1

    def update_puppy_state(self):
        if self.kill_num % 10 == 0:
            self.settings.puppy_speed += 0.01
        if self.kill_num % 20 == 0:
            self.settings.puppy_num_limit += 1
