### 終端機剪刀石頭布

# 這是一個基於 Python 開發的命令列小遊戲。玩家透過輸入代碼與電腦進行對決，程式會透過 ASCII Art 視覺化呈現雙方的出拳結果。

# 🕹️ 遊戲規則
# 程式依據標準的剪刀石頭布規則進行判定：
# 石頭 (0) 勝 剪刀 (2)
# 布 (1) 勝 石頭 (0)
# 剪刀 (2) 勝 布 (1)

# 📋 輸入說明
# 執行程式後，請依照提示輸入：
# 0：石頭
# 1：布
# 2：剪刀

import random

# 定義 ASCII 圖形
rock = """
    _______
---'    ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper = """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

scissors = """
    _______
---'    ____)____
           ______)
        __________)
      (____)
---.__(___)
"""

# 將圖形存入清單，方便索引呼叫
game_images = [rock, paper, scissors]

def play_game():
    try:
        # 1. 取得使用者輸入
        user_input = input("請出拳！輸入 0 代表石頭, 1 代表布, 2 代表剪刀：\n")
        user_choice = int(user_input)

        # 2. 檢查數字範圍
        if user_choice < 0 or user_choice > 2:
            print("輸入無效的數字，你輸了！")
            return

        # 3. 顯示玩家選擇
        print("\n你出的拳是：")
        print(game_images[user_choice])

        # 4. 電腦隨機出拳
        computer_choice = random.randint(0, 2)
        print("電腦出的拳是：")
        print(game_images[computer_choice])

        # 5. 勝負邏輯判斷
        # 平手
        if user_choice == computer_choice:
            print("平手！")
        # 玩家勝利條件：(0>2), (1>0), (2>1)
        elif (user_choice == 0 and computer_choice == 2) or \
             (user_choice == 1 and computer_choice == 0) or \
             (user_choice == 2 and computer_choice == 1):
            print("你贏了！")
        # 其餘情況皆為電腦勝
        else:
            print("你輸了！")

    except ValueError:
        # 處理非整數輸入的異常
        print("請輸入數字！你因為輸入錯誤而輸了！")

if __name__ == "__main__":
    play_game()

