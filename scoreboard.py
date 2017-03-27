import pygame.font
from pygame.sprite import Group
from ship import Ship
class ScoreBoard():
    """ 显示得分信息的类 """
    def __init__(self,ai_settings,screen,game_stats):
        """ 初始化显示得分信息涉及的属性 """
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.stats = game_stats
        self.ai_settings = ai_settings
        # 显示得分信息使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,36)
        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        """ 将得分转换为渲染的一幅图像 """
        roundedscore = round(self.stats.score,-1)
        score_str = "score:" + "{:,}".format(roundedscore)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
        # 将得分放在屏幕右上角
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 10
    def prep_high_score(self):
        """ 将最高得分转换为渲染的一幅图像 """
        highscore = round(self.stats.high_score,-1)
        highscorestr = "HighScore:" + "{:,}".format(highscore)
        self.highscore_image = self.font.render(highscorestr,True,self.text_color,self.ai_settings.bg_color)
        # 将最高得分放在屏幕顶部中央
        self.highscore_image_rect = self.highscore_image.get_rect()
        self.highscore_image_rect.centerx = self.screen_rect.centerx
        self.highscore_image_rect.top = self.screen_rect.top
    def prep_level(self):
        """ 将等级换为渲染的一幅图像 """
        levelstr = "level:" + str(self.stats.level)
        self.level_image = self.font.render(levelstr,True,self.text_color,self.ai_settings.bg_color)
        # 将等级放在得分下方
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.screen_rect.right - 10
        self.level_image_rect.top = self.score_image_rect.bottom + 10
    def prep_ship(self):
        """ 显示还余下多少艘飞船 """
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image,self.score_image_rect)
        self.screen.blit(self.highscore_image,self.highscore_image_rect)
        self.screen.blit(self.level_image,self.level_image_rect)
        self.ships.draw(self.screen)