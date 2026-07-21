import tkinter as tk
import random
import math

class ParticleArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 互動藝術：模組化管理系統")
        
        self.width = 900
        self.height = 750
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#050510", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.points = 100
        self.current_menu = None 
        
        # 寵物進階屬性
        self.ghost_length = 6 
        self.rainbow_cycle = 0 # 用於彩虹動畫計數
        
        # 物品資料庫
        self.items = {
            # 樹木類
            "gold_tree": {"unlocked": False, "active": False, "price": 50, "name": "黃金之樹", "type": "tree"},
            "aurora_tree": {"unlocked": False, "active": False, "price": 150, "name": "極光之樹", "type": "tree"},
            "rainbow_fruit": {"unlocked": False, "active": False, "price": 100, "name": "彩虹果實", "type": "tree"},
            
            # 寵物形狀 (基礎形狀)
            "shape_circle": {"unlocked": True, "active": True, "price": 0, "name": "經典圓形", "type": "pet", "shape": "circle", "is_effect": False},
            "shape_square": {"unlocked": False, "active": False, "price": 80, "name": "幾何方塊", "type": "pet", "shape": "square", "is_effect": False},
            "shape_diamond": {"unlocked": False, "active": False, "price": 150, "name": "璀璨菱形", "type": "pet", "shape": "diamond", "is_effect": False},
            "shape_triangle": {"unlocked": False, "active": False, "price": 200, "name": "戰鬥三角", "type": "pet", "shape": "triangle", "is_effect": False},
            "shape_star": {"unlocked": False, "active": False, "price": 400, "name": "閃耀星星", "type": "pet", "shape": "star", "is_effect": False},
            "shape_hexagon": {"unlocked": False, "active": False, "price": 600, "name": "蜂巢六角", "type": "pet", "shape": "hexagon", "is_effect": False},
            
            # 寵物特效 (可與形狀疊加)
            "effect_neon": {"unlocked": False, "active": False, "price": 200, "name": "霓虹粉紅", "type": "pet", "is_effect": True, "color": "#FF00FF"},
            "effect_lava": {"unlocked": False, "active": False, "price": 250, "name": "熔岩鮮紅", "type": "pet", "is_effect": True, "color": "#FF4500", "outline": "#FFFF00"},
            "effect_ice": {"unlocked": False, "active": False, "price": 250, "name": "冰晶淺藍", "type": "pet", "is_effect": True, "color": "#E0FFFF", "outline": "#00BFFF"},
            "effect_gold": {"unlocked": False, "active": False, "price": 350, "name": "黃金閃耀", "type": "pet", "is_effect": True, "color": "#FFD700", "outline": "#FFFFFF"},
            "effect_void": {"unlocked": False, "active": False, "price": 500, "name": "虛空陰影", "type": "pet", "is_effect": True, "color": "#111111", "outline": "#00FFFF"},
            "effect_magic": {"unlocked": False, "active": False, "price": 700, "name": "幻彩深紫", "type": "pet", "is_effect": True, "color": "#8A2BE2", "outline": "#DA70D6"},
            "effect_rainbow": {"unlocked": False, "active": False, "price": 2000, "name": "★ 彩虹疊加特效 ★", "type": "pet", "is_effect": True, "is_rainbow": True},

            # 升級與技能
            "ghost_upgrade": {"unlocked": True, "active": False, "price": 300, "name": "幻影長度強化", "type": "pet", "is_upgrade": True},
            "space_bg": {"unlocked": False, "active": False, "price": 120, "name": "宇宙星空", "type": "bg"},
            "matrix_mode": {"unlocked": False, "active": False, "price": 300, "name": "數位矩陣", "type": "bg"},
            "double_pts": {"unlocked": False, "active": False, "price": 250, "name": "雙倍積分", "type": "skill"},
            "auto_feeder": {"unlocked": False, "active": False, "price": 500, "name": "自動餵食", "type": "skill"}
        }
        
        self.particles = []
        self.fruits = []
        self.stars = [(random.randint(0, 2000), random.randint(0, 2000)) for _ in range(100)]
        self.tree_color = (100, 100, 100)
        self.wind_angle = 0
        
        self.pet_min_size = 15
        self.pet_max_size = 45
        self.pet_state = {"x": 450, "y": 600, "size": 15, "ghost_ids": []}
        
        self.mouse_x, self.mouse_y = 450, 375
        self.canvas.bind("<Motion>", self.update_mouse_pos)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_click)

        self.update()

    def update_mouse_pos(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def handle_click(self, event):
        x, y = event.x, event.y
        curr_w = self.canvas.winfo_width()
        curr_h = self.canvas.winfo_height()
        
        if y > curr_h - 70:
            menu_idx = x // (curr_w // 5)
            menus = ["shop", "pet", "tree", "bg", "skill"]
            if menu_idx < len(menus):
                new_menu = menus[menu_idx]
                self.current_menu = None if self.current_menu == new_menu else new_menu
            return

        if self.current_menu:
            self.handle_menu_interaction(x, y, curr_w, curr_h)
            return

        clicked_fruit = False
        for f in self.fruits:
            if math.hypot(x - f["x"], y - f["y"]) < 25:
                f["falling"] = True
                clicked_fruit = True
        
        if not clicked_fruit and y < curr_h - 100:
            self.create_particles(event)
            if y > curr_h * 0.3:
                self.change_tree_color_by_pos(x, y, curr_w, curr_h)

    def handle_menu_interaction(self, x, y, curr_w, curr_h):
        if self.current_menu == "shop":
            target_items = [k for k, v in self.items.items() if not v.get("unlocked") or v.get("is_upgrade")]
        else:
            target_items = [k for k, v in self.items.items() if v.get("unlocked") and (v["type"] == self.current_menu or (self.current_menu == "skill" and v["type"] == "skill"))]

        panel_x_start = curr_w * 0.05
        panel_y_start = 140
        
        for i, key in enumerate(target_items):
            row, col = i // 2, i % 2
            bx = panel_x_start + 40 + col * (curr_w * 0.44)
            by = panel_y_start + row * 52
            
            if bx < x < bx + (curr_w * 0.4) and by < y < by + 45:
                it = self.items[key]
                if self.current_menu == "shop":
                    if self.points >= it["price"]:
                        self.points -= it["price"]
                        if it.get("is_upgrade"):
                            if key == "ghost_upgrade":
                                self.ghost_length += 4
                                it["price"] = int(it["price"] * 1.5)
                        else:
                            it["unlocked"] = True
                            if it["type"] == "pet" and not it.get("is_effect") and not it.get("is_upgrade"):
                                for k, v in self.items.items():
                                    if v["type"] == "pet" and not v.get("is_effect") and not v.get("is_upgrade"): v["active"] = False
                                it["active"] = True
                            elif it.get("is_effect"):
                                for k, v in self.items.items():
                                    if v.get("is_effect"): v["active"] = False
                                it["active"] = True
                else:
                    if it["type"] == "pet" and not it.get("is_effect") and not it.get("is_upgrade"):
                        for k, v in self.items.items():
                            if v["type"] == "pet" and not v.get("is_effect") and not v.get("is_upgrade"): v["active"] = False
                        it["active"] = True
                    elif it.get("is_effect"):
                        current_status = it["active"]
                        for k, v in self.items.items():
                            if v.get("is_effect"): v["active"] = False
                        it["active"] = not current_status
                    else:
                        it["active"] = not it["active"]
                break

    def change_tree_color_by_pos(self, x, y, curr_w, curr_h):
        if self.items["gold_tree"]["active"]:
            self.tree_color = (255, 215, random.randint(0, 50))
        elif self.items["aurora_tree"]["active"]:
            self.tree_color = (0, 255, random.randint(150, 255))
        else:
            self.tree_color = (int((x/curr_w)*255), int((y/curr_h)*255), 200)

    def create_particles(self, event, is_firework=False, pos=None):
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FFFF33"]
        if self.items["matrix_mode"]["active"]: colors = ["#00FF00", "#004400"]
        
        count = 40 if is_firework else 5
        origin_x, origin_y = (pos[0], pos[1]) if pos else (event.x, event.y)
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 15) if is_firework else random.uniform(2, 6)
            p = {
                "x": origin_x, "y": origin_y,
                "vx": math.cos(angle) * speed, "vy": math.sin(angle) * speed,
                "radius": random.uniform(3, 8) if is_firework else random.uniform(2, 4),
                "color": random.choice(colors),
                "life": 1.0, "life_dec": 0.025,
                "id": self.canvas.create_oval(0,0,0,0, fill=random.choice(colors), outline="")
            }
            self.particles.append(p)

    def draw_shape(self, x, y, s, shape, color, outline="white", tags="pet", width=2):
        if shape == "circle":
            return self.canvas.create_oval(x-s, y-s, x+s, y+s, fill=color, outline=outline, width=width, tags=tags)
        elif shape == "square":
            return self.canvas.create_rectangle(x-s, y-s, x+s, y+s, fill=color, outline=outline, width=width, tags=tags)
        elif shape == "diamond":
            pts = [x, y-s, x+s, y, x, y+s, x-s, y]
            return self.canvas.create_polygon(pts, fill=color, outline=outline, width=width, tags=tags)
        elif shape == "triangle":
            pts = [x, y-s, x+s, y+s, x-s, y+s]
            return self.canvas.create_polygon(pts, fill=color, outline=outline, width=width, tags=tags)
        elif shape == "hexagon":
            pts = []
            for i in range(6):
                angle = math.radians(i * 60)
                pts.extend([x + math.cos(angle)*s, y + math.sin(angle)*s])
            return self.canvas.create_polygon(pts, fill=color, outline=outline, width=width, tags=tags)
        elif shape == "star":
            pts = []
            for i in range(10):
                angle = math.radians(i * 36 - 90)
                r = s if i % 2 == 0 else s/2
                pts.extend([x + math.cos(angle)*r, y + math.sin(angle)*r])
            return self.canvas.create_polygon(pts, fill=color, outline=outline, width=width, tags=tags)

    def get_rainbow_color(self, offset=0):
        hue = (self.rainbow_cycle + offset) % 360
        r = int(127 + 127 * math.sin(math.radians(hue)))
        g = int(127 + 127 * math.sin(math.radians(hue + 120)))
        b = int(127 + 127 * math.sin(math.radians(hue + 240)))
        return f'#{r:02x}{g:02x}{b:02x}'

    def draw_ui(self, curr_w, curr_h):
        self.canvas.delete("ui")
        labels = [("🛒 商店", "shop"), ("🐾 寵物", "pet"), ("🌳 樹木", "tree"), ("🖼️ 背景", "bg"), ("⚡ 技能", "skill")]
        w_step = curr_w // 5
        
        for i, (txt, menu_key) in enumerate(labels):
            bg_c = "#222244" if self.current_menu == menu_key else "#111122"
            self.canvas.create_rectangle(i*w_step, curr_h - 70, (i+1)*w_step, curr_h, fill=bg_c, outline="white", tags="ui")
            self.canvas.create_text(i*w_step + w_step//2, curr_h - 35, text=txt, fill="white", font=("Arial", 11, "bold"), tags="ui")

        self.canvas.create_text(20, 30, text=f"💰 積分: {self.points}", fill="gold", font=("Arial", 16, "bold"), anchor="nw", tags="ui")

        if self.current_menu:
            self.canvas.create_rectangle(curr_w*0.05, 80, curr_w*0.95, curr_h-100, fill="#050515", outline="cyan", width=3, tags="ui")
            title = f"--- {next(l[0] for l in labels if l[1] == self.current_menu)} ---"
            self.canvas.create_text(curr_w//2, 110, text=title, fill="cyan", font=("Arial", 16, "bold"), tags="ui")
            
            panel_x_start = curr_w * 0.08
            panel_y_start = 140
            
            if self.current_menu == "shop":
                display_keys = [k for k, v in self.items.items() if not v.get("unlocked") or v.get("is_upgrade")]
            else:
                display_keys = [k for k, v in self.items.items() if v.get("unlocked") and (v["type"] == self.current_menu or (self.current_menu=="skill" and v["type"]=="skill"))]

            for i, key in enumerate(display_keys):
                it = self.items[key]
                row, col = i // 2, i % 2
                bx = panel_x_start + col * (curr_w * 0.43)
                by = panel_y_start + row * 52
                
                btn_c = "#114411" if it.get("active") else "#2A2A4A"
                if self.current_menu == "shop": btn_c = "#1A1A3A"
                
                self.canvas.create_rectangle(bx, by, bx + (curr_w * 0.4), by+42, fill=btn_c, outline="white", tags="ui")
                
                if it.get("is_upgrade") and self.current_menu == "shop":
                    lv = int((self.ghost_length-6)/4)
                    txt = f"{it['name']} (Lv.{lv}) : {it['price']}"
                else:
                    txt = f"{it['name']} [{it['price']}]" if self.current_menu == "shop" else f"{it['name']} {'●' if it['active'] else '○'}"
                
                self.canvas.create_text(bx + (curr_w * 0.2), by+21, text=txt, fill="white", font=("Arial", 9, "bold"), tags="ui")

    def update_pet(self):
        tx, ty = self.mouse_x, self.mouse_y
        fall_f = [f for f in self.fruits if f["falling"]]
        if fall_f: tx, ty = fall_f[0]["x"], fall_f[0]["y"]
        elif self.items["auto_feeder"]["active"] and self.fruits:
            tx, ty = self.fruits[0]["x"], self.fruits[0]["y"]

        self.pet_state["x"] += (tx - self.pet_state["x"]) * 0.1
        self.pet_state["y"] += (ty - self.pet_state["y"]) * 0.1
        
        # 獲取當前形狀
        current_shape_data = next((v for v in self.items.values() if v.get("type") == "pet" and not v.get("is_effect") and not v.get("is_upgrade") and v["active"]), self.items["shape_circle"])
        # 獲取當前特效
        current_effect = next((v for v in self.items.values() if v.get("is_effect") and v["active"]), None)
        
        self.rainbow_cycle = (self.rainbow_cycle + 4) % 360
        
        p_x, p_y = self.pet_state["x"], self.pet_state["y"]
        p_s = self.pet_state["size"]
        p_shape = current_shape_data["shape"]
        
        self.canvas.delete("pet_render")
        self.pet_state["ghost_ids"].append((p_x, p_y))
        if len(self.pet_state["ghost_ids"]) > self.ghost_length: 
            self.pet_state["ghost_ids"].pop(0)
            
        for i, (gx, gy) in enumerate(self.pet_state["ghost_ids"]):
            if i % 2 != 0 and not (current_effect and current_effect.get("is_rainbow")): continue
            
            g_color = "#00AAFF"
            if current_effect:
                if current_effect.get("is_rainbow"): g_color = self.get_rainbow_color(i * 15)
                else: g_color = current_effect.get("color", "#00AAFF")
            
            g_s = p_s * (0.3 + 0.7 * (i / self.ghost_length))
            self.draw_shape(gx, gy, g_s, p_shape, "", outline=g_color, tags="pet_render", width=1)

        # 繪製主體顏色
        p_color = "#00AAFF" 
        p_outline = "white"
        
        if current_effect:
            if current_effect.get("is_rainbow"):
                p_color = self.get_rainbow_color()
                p_outline = self.get_rainbow_color(180)
            else:
                p_color = current_effect.get("color", "#00AAFF")
                p_outline = current_effect.get("outline", "white")

        self.draw_shape(p_x, p_y, p_s, p_shape, p_color, outline=p_outline, tags="pet_render", width=3)
        if p_shape in ["circle", "square", "hexagon"]:
            self.canvas.create_oval(p_x-2, p_y-2, p_x+2, p_y+2, fill="black", tags="pet_render")

    def update(self):
        curr_w = self.canvas.winfo_width()
        curr_h = self.canvas.winfo_height()
        if curr_w <= 1: curr_w, curr_h = 900, 750

        self.wind_angle += 0.05
        self.canvas.delete("bg_effect")
        if self.items["space_bg"]["active"]:
            for x, y in self.stars:
                sx, sy = x % curr_w, y % curr_h
                self.canvas.create_oval(sx, sy, sx+2, sy+2, fill="white", tags="bg_effect")
        
        self.canvas.delete("tree")
        color_hex = f'#{self.tree_color[0]:02x}{self.tree_color[1]:02x}{self.tree_color[2]:02x}'
        sway = math.sin(self.wind_angle) * 2
        
        def draw_branch(x, y, angle, depth):
            if depth > 0:
                x2 = x + int(math.cos(math.radians(angle + sway)) * depth * 8)
                y2 = y + int(math.sin(math.radians(angle + sway)) * depth * 8)
                self.canvas.create_line(x, y, x2, y2, fill=color_hex, width=depth, tags="tree")
                
                if depth == 1 and len(self.fruits) < 30:
                    if random.random() < 0.005:
                        f_c = self.get_rainbow_color() if self.items["rainbow_fruit"]["active"] else "#FF3366"
                        f_id = self.canvas.create_oval(0,0,0,0, fill=f_c, outline="white", tags="fruit")
                        self.fruits.append({"x": x2, "y": y2, "id": f_id, "falling": False, "vy": 0})
                draw_branch(x2, y2, angle-20, depth-1); draw_branch(x2, y2, angle+20, depth-1)
        
        draw_branch(curr_w//2, curr_h - 70, -90, 10)

        active_f = []
        for f in self.fruits:
            if f["falling"]: f["vy"] += 0.5; f["y"] += f["vy"]
            if math.hypot(f["x"]-self.pet_state["x"], f["y"]-self.pet_state["y"]) < self.pet_state["size"]+10:
                self.canvas.delete(f["id"]); self.pet_state["size"] += 4
                if self.pet_state["size"] >= self.pet_max_size:
                    self.create_particles(None, True, (self.pet_state["x"], self.pet_state["y"]))
                    self.points += 50 if not self.items["double_pts"]["active"] else 100
                    self.pet_state["size"] = self.pet_min_size
                continue
            if f["y"] < curr_h - 70:
                self.canvas.coords(f["id"], f["x"]-6, f["y"]-6, f["x"]+6, f["y"]+6)
                active_f.append(f)
            else: self.canvas.delete(f["id"])
        self.fruits = active_f

        new_p = []
        for p in self.particles:
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.2; p["life"] -= p["life_dec"]
            if p["life"] > 0:
                r = p["radius"]*p["life"]
                self.canvas.coords(p["id"], p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r)
                new_p.append(p)
            else: self.canvas.delete(p["id"])
        self.particles = new_p

        self.update_pet()
        self.draw_ui(curr_w, curr_h)
        self.root.after(30, self.update)

if __name__ == "__main__":
    root = tk.Tk(); app = ParticleArtApp(root); root.mainloop()