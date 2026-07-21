import turtle
import colorsys
import time
import math
import random

def setup_screen():
    screen = turtle.Screen()
    screen.bgcolor("#000000")
    screen.setup(1000, 1000)
    screen.tracer(0)
    return screen

def draw_branch(t, length, angle, noise, depth, hue):
    """遞迴生成分形分支，帶有動態噪點"""
    if depth == 0:
        return

    # 計算顏色：隨深度變亮，隨時間偏移色彩
    color = colorsys.hsv_to_rgb(hue, 0.8, 1.0 - (depth * 0.05))
    t.pencolor(color)
    t.pensize(depth * 1.5)

    # 繪製主幹
    t.forward(length)

    # 紀錄當前座標與角度
    pos = t.pos()
    heading = t.heading()

    # 右分支：加入隨機擾動 (Noise)
    t.right(angle + noise)
    draw_branch(t, length * 0.75, angle, noise, depth - 1, (hue + 0.02) % 1.0)

    # 回到分叉點繪製左分支
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()
    
    t.left(angle - noise)
    draw_branch(t, length * 0.75, angle, noise, depth - 1, (hue + 0.02) % 1.0)

def main():
    screen = setup_screen()
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    
    step = 0
    while True:
        t.clear()
        step += 1
        
        # 核心參數：隨時間擺動的角度與噪點
        # 這裡創造了如同在水中搖曳或呼吸的律動感
        oscillation = math.sin(step * 0.05) * 20 + 30
        noise = math.cos(step * 0.08) * 10
        current_hue = (step * 0.005) % 1.0
        
        # 從中心向六個方向輻射生長
        for i in range(6):
            t.penup()
            t.goto(0, 0)
            t.setheading(i * 60 + step * 0.5) # 整體緩慢旋轉
            t.pendown()
            draw_branch(t, 120, oscillation, noise, 8, current_hue)
            
        # 加上中央發光核心
        t.penup(); t.goto(0, 0); t.dot(20, "white")
        
        screen.update()
        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except:
        pass