from __future__ import annotations

import sys
import io
import os
from time import sleep

import pygame
from pygame.sprite import Group

from setting import Settings
from gamestate import Gamestate
from headship import HeadShip
from bullet import Bullet
from puppy import Puppy
from buttons import Buttons
from infoboard import infoboard

if sys.stdout is not None and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
else:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")

class PuppyInvasion:
    """小狗入侵"""
    # ---------------------------------------------------------------------------- #
    #                                      控制层                                     #
    # ---------------------------------------------------------------------------- #
    def __init__(self):
        """初始化游戏，创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode\
        (
                (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("felix sturgeon's mini-game之郑头大冒险")
        # 飞船
        self.headship = HeadShip(self)
        # 子弹
        self.bullets: Group[Bullet] = pygame.sprite.Group()
        # 小狗
        self.puppy = Puppy(self)
        self.puppys: Group[Puppy] = pygame.sprite.Group()
        # 按键
        self.play_button = Buttons(self, "Play")
        # 游戏开始
        self.gamestate = Gamestate(self)
        # 记分
        self.infoboard = infoboard(self)

    # ------------------------------------ 流程层 ----------------------------------- #
    def run_game(self):
        """开始游戏循环"""
        while True:
            self._check_event()

            if self.gamestate.game_active == True:
                self.headship.update()
                self._update_bullet()
                self._update_puppys()

            self._update_screen()
            self.clock.tick(60)

    # ---------------------------------------------------------------------------- #
    #                                      实体层                                     #
    # ---------------------------------------------------------------------------- #

    # ------------------------------------ 子弹 ------------------------------------ #
    def _fire_bullet(self):
        """创建新子弹， 加入编组bullets"""
        if not self.gamestate.game_active:
            return
        if len(self.bullets) < self.settings.bullet_num_allowed:
            self.gamestate.bullets_left = \
                self.settings.bullet_num_allowed - len(self.bullets) -1
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _bullet_delete(self):
        """删除已消失的子弹"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                self.gamestate.bullets_left += 1
        # print(f"bullet:{len(self.bullets)}")
        #bullet_left = self.settings.bullet_num_allowed - len(self.bullets)
        #self.gamestate.current_event = f"剩余子弹： {bullet_left}"
        #self.infoboard.prep_info(self)              

    def _update_bullet(self):
        self.bullets.update()
        self._bullet_delete()
        self._check_b_p_collision()

    # ------------------------------------ 小狗 ------------------------------------ #
    def _update_puppys(self):
        """超多小狗及其事件"""
        self._creat_puppys()
        self._check_puppy_bottom()
        self._puppy_delete()
        self._check_b_p_collision()
        self._check_h_p_collision()
        # print(f"puppy_num: {len(self.puppys)}")

    def _creat_puppys(self):
        """生成小狗"""
        now = pygame.time.get_ticks()
        if \
            (
                (now - self.settings.puppy_last_spawn_time >= self.settings.puppy_spawn_interval)
                and
                (len(self.puppys) < self.settings.puppy_num_limit)
            ):
            puppy = Puppy(self)
            self.puppys.add(puppy)
            self.puppy_last_spawn_time = now
        self.puppys.update()

    def _puppy_delete(self):
        """删除消失小狗"""
        for puppy in self.puppys.copy():
            if puppy.rect.top >= self.settings.screen_height:
                self.puppys.remove(puppy)

    def _check_puppy_bottom(self):
        """响应小狗达到事件"""
        for puppy in self.puppys.sprites():
            if puppy.rect.bottom >= self.settings.screen_height:
                self._head_hit()
                if self.gamestate.headships_left >= 1:
                    self.gamestate.score -= 100
                    text = "你被小狗咬伤了。"
                    self.gamestate.sent_event(text)
                break

    # ----------------------------------- 实体事件 ----------------------------------- #
    def _check_b_p_collision(self):
        """检测子弹与小狗的碰撞事件，并执行碰撞结果"""
        b_p_collisions = pygame.sprite.groupcollide\
        (
            self.bullets, self.puppys, True, True
        )
        if b_p_collisions:
            self.gamestate.kill_num += 1
            self.gamestate.score += self.settings.puppy_point
            
            text = \
            (
                f"killpuppy: 坏种郑腾旭，残忍杀害了{self.gamestate.kill_num}只可爱的小狗。"
            )
            self.gamestate.sent_event(text)
            self.gamestate.update_headship_level()


    def _check_h_p_collision(self):
        """检测郑头与小狗的碰撞事件, 并执行碰撞结果"""
        h_p_collision = pygame.sprite.spritecollideany\
        (
            self.headship, self.puppys
        )
        if h_p_collision:
            self._head_hit()
            if self.gamestate.game_active:
                self.gamestate.score -= 50
                text = \
f"""
郑头被小狗咬伤了！！！
I'm suffering from an excruciating headache.
头痛至极
剩余生命： {self.gamestate.headships_left}
 """

                print\
                (
                   text, flush=True
                )
                self.gamestate.sent_event("郑头被小狗咬伤了！！！头痛至极")

    def _head_hit(self):
        """响应郑头和小狗的碰撞"""
        self.gamestate.headships_left -= 1
        if self.gamestate.headships_left >= 1:
            self.puppys.empty()
            self.headship.center_ship()
            # 暂停
            sleep(1)
        else:
            self.gamestate.game_active = False
            pygame.mouse.set_visible(True)
            self.bullets.empty()
            self.puppys.empty()        
            print("你被小狗咬死了！！！", flush=True)
            text = "你被小狗咬死了！！！"
            self.gamestate.sent_event(text)


    # ---------------------------------------------------------------------------- #
    #                                      交互层                                     #
    # ---------------------------------------------------------------------------- #

    # ---------------------------------- menu交互 ---------------------------------- #
    def _check_play_button(self, mouse_pos):
        if \
        (
            (self.play_button.rect.collidepoint(mouse_pos))
            and
            (not self.gamestate.game_active)
        ):
            self.gamestate.reset_starts(self)
            self.gamestate.game_active = True
            pygame.mouse.set_visible(False)

    # ----------------------------------- 键鼠交互 ----------------------------------- #
    def _check_keydown(self, event):
        """响应按下"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.headship.moving_right = True
            if event.key == pygame.K_LEFT:
                self.headship.moving_left = True
            if event.key == pygame.K_SPACE:
                self._fire_bullet()

    def _check_keyup(self, event):
        """响应释放"""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.headship.moving_right = False
            if event.key == pygame.K_LEFT:
                self.headship.moving_left = False

    def _check_mousedown(self,event):
        """响应鼠标按下事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)

    # ----------------------------------- 总交互层 ----------------------------------- #
    def _check_event(self):
        """侦听游戏事件,并执行相应程序"""
        for event in pygame.event.get():
            self._check_mousedown(event)
            self._check_quit(event)
            self._check_keydown(event)
            self._check_keyup(event)

    # ------------------------------------ 退出 ------------------------------------ #
    def _quit(self):
        pygame.quit()
        sys.exit()

    def _check_quit(self, event):
        """执行退出事件"""
        if (
            (event.type == pygame.QUIT)
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
        ):
            self._quit()

    # ---------------------------------------------------------------------------- #
    #                                      渲染层                                     #
    # ---------------------------------------------------------------------------- #
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if not self.gamestate.game_active:
            self.play_button.draw_button()
        self.headship.blitme(self)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.puppys.draw(self.screen)
        self.infoboard.prep_info()
        self.infoboard.show_info(self)    
        # 刷新屏幕
        pygame.display.flip()


if __name__ == "__main__":
    gamemain = PuppyInvasion()
    gamemain.run_game()
