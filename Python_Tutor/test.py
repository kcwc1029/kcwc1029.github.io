# 檔案: ch12_9_7.py
class Pizza:
    # 這是靜態方法
    @staticmethod
    def demo():
        print("I like Pizza")

# 不需要建立 Pizza 物件，直接用類別名稱呼叫
Pizza.demo()