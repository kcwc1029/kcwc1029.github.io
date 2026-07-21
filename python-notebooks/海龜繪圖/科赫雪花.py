import turtle

# 設置繪圖視窗
screen = turtle.Screen()
screen.title("科赫雪花 (Koch Snowflake)")
screen.bgcolor("black")  # 設定背景顏色

# 設置海龜
t = turtle.Turtle()
t.speed(0)  # 設定最快速度
t.color("cyan") # 設定畫筆顏色
t.pensize(2)

def koch_curve(t, order, length):
    """
    遞迴繪製科赫曲線
    :param t: turtle 物件
    :param order: 遞迴階數
    :param length: 線段長度
    """
    if order == 0:
        t.forward(length)
    else:
        # 新的線段長度
        new_length = length / 3.0
        
        # 遞迴繪製四段線，中間凸起
        koch_curve(t, order - 1, new_length)
        t.left(60)
        koch_curve(t, order - 1, new_length)
        t.right(120)
        koch_curve(t, order - 1, new_length)
        t.left(60)
        koch_curve(t, order - 1, new_length)

def draw_koch_snowflake(t, order, length):
    """
    繪製科赫雪花
    :param t: turtle 物件
    :param order: 遞迴階數
    :param length: 初始三角形邊長
    """
    # 隱藏海龜，使繪圖過程更流暢
    t.hideturtle()
    
    # 繪製三條科赫曲線，每條曲線之間轉 120 度
    for _ in range(3):
        koch_curve(t, order, length)
        t.right(120)

# --- 主程式執行區 ---
if __name__ == "__main__":
    # 繪製前先將海龜移動到起始位置
    t.penup()
    t.goto(-200, 150)
    t.pendown()

    # 設置繪製的階數和邊長
    # 階數越大，圖案越複雜，繪圖時間越長
    # 建議從 order = 1, 2, 3 開始嘗試
    order = 5
    length = 400

    draw_koch_snowflake(t, order, length)
    
    # 保持視窗開啟
    screen.mainloop()