#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from setting import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
def run_game():
    # 初始化游戏，并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('外星人入侵——Alien Invasion')
    # 创建一艘飞船,一个子弹的编组和外星人编组
    ship = Ship(ai_settings,screen)
    aliens = Group()
    bullets = Group()
    game_stats = GameStats(ai_settings)
    score = ScoreBoard(ai_settings,screen,game_stats)
    # 创建Play按钮
    play_button = Button(ai_settings,screen,'Play',ship)
    # 创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    # 开始游戏的主循环
    while True:
        # 监听键盘和鼠标事件
        gf.check_events(ai_settings,screen,ship,aliens,bullets,game_stats,play_button,score)
        if game_stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets,game_stats,score)
            gf.update_aliens(ai_settings,ship,aliens,game_stats,screen,bullets,score)
        # 每次循环时都重绘屏幕
        gf.update_screen(ai_settings,screen,ship,aliens,bullets,play_button,game_stats,score)
        # 让最近绘制的屏幕可见
        pygame.display.flip()
        
run_game()