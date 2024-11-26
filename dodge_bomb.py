import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたrectが画面内か画面外か判定
    引数：こうかとんrectか爆弾rect
    戻り値：真理値タプル（横方向判定結果,　縦方向判定結果）画面内ならTrue, 画面外ならFalse
    """
    x = True
    y = True
    if rct.left < 0 or rct.right > WIDTH:
        x = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        y = False
    return (x, y)


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面上に「Game Over」と表示し、
    泣いているこうかとん画像を貼り付ける関数
    """
    black = pg.Surface((1100,650))  #ブラックアウト背景surface生成
    pg.draw.rect(black, (0,0,0), pg.Rect(0,0,1100,650))
    black.set_alpha(200)  #背景の透過度設定
    go_kk_img = pg.image.load("fig/8.png")  #泣いているこうかとん読みこみ
    fonto = pg.font.Font(None, 100)  #文字surface生成
    go_txt = fonto.render("Game Over", True, (255, 255, 255))  #文字をGame Over,色を白に設定
    go_txt_rct = go_txt.get_rect()
    go_txt_rct.center = (WIDTH/2, HEIGHT/2)
    screen.blit(black, [0,0])
    screen.blit(go_kk_img, [WIDTH/2+200, HEIGHT/2-30])
    screen.blit(go_kk_img, [WIDTH/2-240, HEIGHT/2-30])
    screen.blit(go_txt, go_txt_rct)
    pg.display.update()


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20))  #爆弾surface
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)  #半径10の赤色の円を中心座標(10,10)に描画
    bb_img.set_colorkey((0,0,0))  #黒色を透過させる
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()  #爆弾rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  #爆弾速度ベクトル
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            time.sleep(5)
            return
        # if tmr % 100 == 0:
        #     vx -= 1
        #     vy -= 1
        screen.blit(bg_img, [0, 0])
        DELTA = {pg.K_UP:(0,-5), pg.K_DOWN:(0,+5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(+5,0), }
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #辞書を作成したので、for文で書ける。
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key, tpl in DELTA.items():
            if key_lst[key] == True:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip([-sum_mv[0], -sum_mv[1]])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  #爆弾動く
        x, y = check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
