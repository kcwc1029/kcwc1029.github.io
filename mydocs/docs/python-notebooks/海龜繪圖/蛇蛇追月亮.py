import turtle
import math
import random
import time
import colorsys

def setup_canvas():
    screen = turtle.Screen()
    screen.bgcolor("#01020A")
    screen.setup(1100, 900)
    screen.tracer(0, 0)
    return screen

def draw_moon(t):
    """金黃月牙"""
    t.penup(); t.goto(380, 320)
    t.pencolor("#FFFACD"); t.fillcolor("#FFFACD")
    t.begin_fill(); t.circle(50); t.end_fill()
    t.penup(); t.goto(400, 330)
    t.pencolor("#01020A"); t.fillcolor("#01020A")
    t.begin_fill(); t.circle(50); t.end_fill()

def draw_dragon_part(t, x, y, size, hue, is_head, is_tail, step, angle):
    t.penup(); t.goto(x, y); t.setheading(angle)
    
    if is_head:
        # 銀白龍頭與長角
        t.pencolor("#FFFFFF"); t.pensize(2); t.pendown()
        for s in [-1, 1]:
            t.penup(); t.goto(x, y); t.setheading(angle + s * 35)
            t.pendown(); t.circle(s * 45, 85)
        
        # --- 靈動小眼 ---
        for s in [-1, 1]:
            ex = x + math.cos(math.radians(angle + s * 45)) * 18
            ey = y + math.sin(math.radians(angle + s * 45)) * 18
            t.penup(); t.goto(ex, ey); t.dot(6, "#00FFFF")
        
        # --- 飄逸長鬚 (流體律動) ---
        for s in [-1, 1]:
            t.penup(); t.goto(x, y); t.setheading(angle + 180 + s * 30)
            t.pensize(1); t.pencolor("#FFFFFF")
            for j in range(12):
                t.pendown()
                # 鬍鬚隨飛行速度與時間產生波浪
                whisker_wave = math.sin(step * 0.15 - j * 0.5) * 6
                t.left(whisker_wave); t.forward(8)
        
        # 主眼
        t.penup(); t.goto(x, y); t.dot(14, "#00FFFF"); t.dot(5, "white")
    
    elif is_tail:
        # 尾部流光火球
        glow = 25 + math.sin(step * 0.3) * 12
        t.dot(glow + 15, "#FF4500"); t.dot(glow, "#FFD700")
    
    else:
        # 龍身鱗片
        col = colorsys.hsv_to_rgb(hue, 0.6, 0.7)
        t.dot(size, col)

def main():
    screen = setup_canvas()
    t_drag = turtle.Turtle(); t_drag.hideturtle()
    t_env = turtle.Turtle(); t_env.hideturtle()
    t_smoke = turtle.Turtle(); t_smoke.hideturtle()
    
    # 星空資料 [x, y, 閃爍偏移, 大小]
    stars = [[random.randint(-550, 550), random.randint(-450, 450), random.uniform(0, 6.28), random.randint(2, 5)] for _ in range(80)]
    # 亂流線資料 [x, y, 長度, 角度偏移]
    wind_lines = [[random.randint(-600, 600), random.randint(-500, 500), random.randint(30, 60), random.uniform(0, 6.28)] for _ in range(12)]
    smoke_particles = []

    while True:
        nodes = []
        curr_x, curr_y = 0, 0
        angle = random.randint(0, 360)
        start_time = time.time()
        step = 0

        while time.time() - start_time < 20:
            t_drag.clear(); t_env.clear(); t_smoke.clear()
            step += 1
            
            # 1. 繪製閃爍星空與月亮
            draw_moon(t_env)
            for s in stars:
                twinkle = (math.sin(step * 0.1 + s[2]) + 1) / 2
                t_env.penup(); t_env.goto(s[0], s[1])
                t_env.dot(s[3] * twinkle, "#FFFFFF")

            # 2. 繪製不規則亂流 (動態風場)
            t_env.pensize(1)
            for wl in wind_lines:
                # 風的角度隨時間小幅漂移
                drift_angle = math.sin(step * 0.05 + wl[3]) * 45
                t_env.pencolor("#1A2A44")
                t_env.penup(); t_env.goto(wl[0], wl[1])
                t_env.setheading(drift_angle)
                t_env.pendown(); t_env.forward(wl[2])
                # 風跡移動
                wl[0] += 5; wl[1] += math.sin(step*0.02)*2
                if wl[0] > 600: wl[0] = -600

            # 3. 邊界導航
            if abs(curr_x) > 480 or abs(curr_y) > 380:
                target_angle = math.degrees(math.atan2(-curr_y, -curr_x))
                angle += ((target_angle - angle + 180) % 360 - 180) * 0.1
            else:
                angle += math.sin(step * 0.04) * 4

            speed = 6 + math.sin(step * 0.03) * 2
            curr_x += math.cos(math.radians(angle)) * speed
            curr_y += math.sin(math.radians(angle)) * speed
            
            nodes.append((curr_x, curr_y, angle))
            if len(nodes) > 75: nodes.pop(0)

            # 4. 尾部煙霧
            tx, ty = nodes[0][0], nodes[0][1]
            if step % 3 == 0: smoke_particles.append([tx, ty, 25])
            new_smoke = []
            for p in smoke_particles:
                p[1] += 1.5; p[2] -= 1 # 向上飄與消散
                if p[2] > 0:
                    t_smoke.penup(); t_smoke.goto(p[0], p[1])
                    t_smoke.dot(p[2] * 0.7, "#222222")
                    new_smoke.append(p)
            smoke_particles = new_smoke

            # 5. 繪製龍身
            for i, (nx, ny, na) in enumerate(nodes):
                hue = (0.6 + i * 0.002) % 1.0
                size = 12 + (i / len(nodes)) * 28
                draw_dragon_part(t_drag, nx, ny, size, hue, (i == len(nodes)-1), (i == 0), step, na)

            screen.update()
            time.sleep(0.01)

        t_drag.clear(); t_env.clear(); t_smoke.clear(); smoke_particles = []
        screen.update(); time.sleep(1)

if __name__ == "__main__":
    try: main()
    except: pass