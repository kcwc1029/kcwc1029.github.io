import turtle
import random
import time

# --- 設定區 ---
STAR_COLOR = "#FF0000"     # 鮮紅
GLOW_COLOR = "#FFA500"     # 橘金（能量激發）
SMOKE_COLORS = ["#222222", "#444444", "#666666", "#FF4500"]

def setup_screen():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(800, 800)
    screen.title("至尊黑魔法召喚儀式")
    screen.tracer(0)
    return screen

def draw_star(t, x, y, size, color, width, animate=False):
    """畫出倒五芒星，可選擇是否要有動畫感"""
    t.penup()
    t.goto(x, y)
    t.setheading(180)
    t.pencolor(color)
    t.pensize(width)
    t.pendown()
    
    points = []
    for _ in range(5):
        if animate:
            # 每一條邊拆成 5 段畫，增加流暢感
            for _ in range(5):
                t.forward(size/5)
                turtle.update()
                time.sleep(0.01)
        else:
            t.forward(size)
        points.append(t.pos())
        t.right(144)
    return points

def main():
    screen = setup_screen()
    t = turtle.Turtle()
    t.hideturtle()
    
    while True: # 無限循環開始
        t.clear()
        print("🕯️ 正在刻畫新的召喚陣...")
        
        # 1. 刻畫階段 (從頭開始畫)
        main_pts = draw_star(t, 150, 80, 300, STAR_COLOR, 4, animate=True)
        
        sub_pts_all = []
        for pt in main_pts:
            # 畫子星
            sub_pts = draw_star(t, pt[0]+45, pt[1], 90, GLOW_COLOR, 2, animate=True)
            sub_pts_all.append(sub_pts)
        
        # 2. 持續閃爍與噴發階段 (維持三秒)
        start_time = time.time()
        print("🔥 能量飽和！維持 3 秒中...")
        
        smoke_particles = [] # 儲存煙霧位置 [x, y, size, color]

        while time.time() - start_time < 3:
            t.clear()
            
            # 閃爍切換
            is_bright = (int(time.time() * 10) % 2 == 0)
            current_color = STAR_COLOR if is_bright else "#440000"
            
            # 畫主星與子星 (不帶動畫快速繪製)
            draw_star(t, 150, 80, 300, current_color, 5 if is_bright else 3)
            for pt in main_pts:
                draw_star(t, pt[0]+45, pt[1], 90, GLOW_COLOR, 2)

            # --- 爆酷煙霧粒子系統 ---
            # 在每個尖點產生新煙霧
            for pt in main_pts:
                if random.random() > 0.5:
                    smoke_particles.append([pt[0], pt[1], random.randint(5, 15), random.choice(SMOKE_COLORS)])
            
            # 更新並繪製煙霧
            new_smoke = []
            for p in smoke_particles:
                p[1] += 5  # 向上漂移
                p[2] *= 0.9 # 逐漸變小
                if p[2] > 1: # 如果粒子還沒消失
                    t.penup()
                    t.goto(p[0] + random.randint(-5, 5), p[1])
                    t.dot(p[2], p[3])
                    new_smoke.append(p)
            smoke_particles = new_smoke
            
            screen.update()
            time.sleep(0.03)

        # 3. 爆炸清空感
        print("💥 能量釋放，準備重新召喚...")
        for i in range(10, 0, -1):
            screen.bgcolor((i/10 * 0.3, 0, 0)) # 背景閃紅光
            screen.update()
            time.sleep(0.02)
        screen.bgcolor("black")

# 執行
if __name__ == "__main__":
    try:
        main()
    except turtle.Terminator:
        pass