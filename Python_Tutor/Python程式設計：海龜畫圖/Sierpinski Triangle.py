import turtle

def draw_triangle(t, points, color):
    """
    繪製一個實心三角形
    :param t: turtle 物件
    :param points: 包含三個頂點座標的列表，例如 [[x1, y1], [x2, y2], [x3, y3]]
    :param color: 三角形的填充顏色
    """
    t.fillcolor(color)
    t.penup()
    t.goto(points[0][0], points[0][1])
    t.pendown()
    t.begin_fill()
    t.goto(points[1][0], points[1][1])
    t.goto(points[2][0], points[2][1])
    t.goto(points[0][0], points[0][1])
    t.end_fill()

def get_mid(p1, p2):
    """
    計算兩點的中點座標
    :param p1: 點1座標
    :param p2: 點2座標
    :return: 中點座標
    """
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def sierpinski(t, points, degree):
    """
    遞迴繪製謝爾賓斯基三角形
    :param t: turtle 物件
    :param points: 目前三角形的三個頂點座標
    :param degree: 遞迴階數
    """
    colors = ['blue', 'red', 'green', 'white', 'yellow', 'violet', 'orange']
    
    # 繪製當前階數的三角形
    draw_triangle(t, points, colors[degree % len(colors)])
    
    # 遞迴步驟
    if degree > 0:
        # 繪製左下方的小三角形
        sierpinski(t, 
                   [points[0],
                    get_mid(points[0], points[1]),
                    get_mid(points[0], points[2])],
                   degree - 1)
                   
        # 繪製上方的小三角形
        sierpinski(t,
                   [points[1],
                    get_mid(points[0], points[1]),
                    get_mid(points[1], points[2])],
                   degree - 1)
                   
        # 繪製右下方的小三角形
        sierpinski(t,
                   [points[2],
                    get_mid(points[2], points[1]),
                    get_mid(points[0], points[2])],
                   degree - 1)

# --- 主程式執行區 ---
if __name__ == "__main__":
    # 設置繪圖視窗
    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.title("謝爾賓斯基三角形 (Sierpinski Triangle)")
    
    t = turtle.Turtle()
    t.speed(0)  # 設定最快速度
    t.hideturtle() # 隱藏海龜

    # 設定繪圖初始三角形的頂點座標
    my_points = [[-200, -100], [0, 200], [200, -100]]
    
    # 設置繪製的階數，可以修改此數字來觀察不同階數的圖案
    degree = 3
    
    sierpinski(t, my_points, degree)
    
    # 保持視窗開啟
    screen.mainloop()