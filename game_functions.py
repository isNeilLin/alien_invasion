import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_events(ai_settings,screen,ship,aliens,bullets,game_stats,play_button,score):
    """ 响应按键和鼠标事件 """
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('score.txt','w') as file:
                    file.write(str(game_stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keydown_events(event,ai_settings,screen,ship,bullets)
            elif event.type == pygame.KEYUP:
                keyup_events(event,ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings,screen,ship,aliens,bullets,game_stats,play_button,score,mouse_x,mouse_y)

def keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        with open('score.txt','w') as file:
            file.write(str(game_stats.high_score))
        sys.exit()

def keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def update_screen(ai_settings,screen,ship,aliens,bullets,play_button,game_stats,score):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    score.show_score()
    if not game_stats.game_active:
        play_button.draw_button()
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets,game_stats,score):
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,game_stats,score)

def check_play_button(ai_settings,screen,ship,aliens,bullets,game_stats,play_button,score,mouse_x,mouse_y):
    """ 在玩家单击Play按钮开始游戏 """
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not game_stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        game_stats.reset_stats()
        game_stats.game_active = True
        # 重置记分牌图像
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ship()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        ai_settings.init_speed()
        # 创建一群新外星人，并让飞船居中
        ship.center_ship()
        create_fleet(ai_settings,screen,ship,aliens)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,game_stats,score):
    # 检查是否有子弹击中了外星人
    # 如果是这样就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            game_stats.score += ai_settings.alien_points
            score.prep_score()
        check_high_score(game_stats,score)
    if len(aliens) == 0 :
        # 删除现有的子弹和外星人,加快游戏节奏,并创建一群新的外星人
        # 如果整群外星人都被消灭,就提高一个等级
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        game_stats.level += 1
        score.prep_level()
        ai_settings.increase_speed()

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    # 创建一个外星人,并计算一行可容纳多少个外星人
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    # 外星人间距为外星人宽度
    number_alien_x = get_number_aliens_x(ai_settings,alien_width)
    number_alien_y = get_number_aliens_y(ai_settings,ship_height,alien_height)
    # 创建外星人群
    for row_number in range(number_alien_y):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,alien_width,row_number)

def get_number_aliens_x(ai_settings,alien_width):
    space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(space_x / (2 * alien_width))
    return number_alien_x

def get_number_aliens_y(ai_settings,ship_height,alien_height):
    space_y = ai_settings.screen_height - 2 * alien_height - ship_height
    number_alien_y = int(space_y / (2 * alien_height))
    return number_alien_y

def create_alien(ai_settings,screen,aliens,alien_number,alien_width,row_number):
    alien = Alien(ai_settings,screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.y = alien.y
    alien.rect.x = alien.x
    aliens.add(alien)
def check_fleet_edges(ai_settings,aliens):
    """ 有外星人到达边缘时采取相应的措施 """
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,ship,aliens,game_stats,screen,bullets,score):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,ship,aliens,game_stats,screen,bullets,score)
    check_aliens_bottom(ai_settings,game_stats,screen,ship,aliens,bullets,score)

def ship_hit(ai_settings,ship,aliens,game_stats,screen,bullets,score):
    """ 响应被外星人撞到的飞船 """
    game_stats.ship_left -= 1
    score.prep_ship()
    if game_stats.ship_left > 0:
        aliens.empty()
        bullets.empty()
        # 创建一群新外星人，并将飞船放在屏幕底端中央
        ship.center_ship()
        create_fleet(ai_settings,screen,ship,aliens)
        # 暂停0.5秒
        sleep(0.5)
    else:
        game_stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,game_stats,screen,ship,aliens,bullets,score):
    """ 检查是否有外星人到达屏幕底端 """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,ship,aliens,game_stats,screen,bullets,score)
            break

def check_high_score(game_stats,score):
    """ 检查是否诞生了新高分 """
    if game_stats.score > game_stats.high_score:
        game_stats.high_score = game_stats.score
        score.prep_high_score()