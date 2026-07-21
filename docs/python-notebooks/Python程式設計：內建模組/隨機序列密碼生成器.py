### 隨機序列密碼生成器
# 💡 開發動機
# 在密碼學中，「隨機性」是安全的重要指標。若密碼總是遵循「先字母、再符號、後數字」的規律，駭客就能縮小暴力破解的範圍。本程式透過「洗牌演算法」確保密碼的每一位字元出現的類別都是隨機的。

# 🛠 邏輯流程
# 初始化：準備字母、數字、符號三個獨立的資源池。
# 採集：根據使用者設定的數量，從資源池中「抽樣」放入暫存列表。此時列表順序仍是整齊的。
# 亂序：調用 random.shuffle() 函數對列表進行原地洗牌（In-place Shuffle），打亂所有索引位置。
# 聚合：將打亂後的字元列表合併為最終密碼字串。

import random

# 定義可用字元集
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_hard_password():
    print("歡迎使用 PyPassword 密碼生成器！")
    
    # 1. 取得使用者需求數量
    try:
        nr_letters = int(input("您希望密碼中包含多少個字母？\n"))
        nr_symbols = int(input("您希望密碼中包含多少個符號？\n"))
        nr_numbers = int(input("您希望密碼中包含多少個數字？\n"))
    except ValueError:
        print("請輸入有效的整數數字！")
        return

    # 2. 收集字元到暫存清單 (password_list)
    # 使用 random.choice 從字元集中隨機選取，並加入清單
    password_list = []

    for _ in range(nr_letters):
        password_list.append(random.choice(letters))

    for _ in range(nr_symbols):
        password_list.append(random.choice(symbols))

    for _ in range(nr_numbers):
        password_list.append(random.choice(numbers))

    # 3. 核心步驟：原地打亂順序 (Shuffle)
    # 這一步讓密碼結構從 [字母...符號...數字] 變成完全混亂
    random.shuffle(password_list)

    # 4. 組合成字串並輸出
    # 使用 join 效率比 += 字串相加更高
    password = "".join(password_list)
    
    print(f"您的密碼是：{password}")

if __name__ == "__main__":
    generate_hard_password()
