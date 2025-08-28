class Vehicle:
    """
    最上層的基底類別
    """
    def __init__(self, max_speed):
        self.max_speed = max_speed

class Car(Vehicle):
    """
    中間層的父類別，繼承 Vehicle
    """
    def __init__(self, max_speed, num_doors):
        # 呼叫上一層 Vehicle 的 __init__
        super().__init__(max_speed)
        self.num_doors = num_doors

class ElectricCar(Car):
    """
    最底層的子類別，繼承 Car
    """
    def __init__(self, max_speed, num_doors, battery_capacity):
        # 呼叫上一層 Car 的 __init__，它會再往上呼叫 Vehicle 的 __init__
        super().__init__(max_speed, num_doors)
        self.battery_capacity = battery_capacity

    def display_specs(self):
        # 這個方法可以存取來自三層類別的所有屬性
        print(f"Max Speed: {self.max_speed} km/h")
        print(f"Number of Doors: {self.num_doors}")
        print(f"Battery Capacity: {self.battery_capacity} kWh")

# 讀取輸入並轉換為整數
max_speed, num_doors, battery_capacity = map(int, input().split())

# 建立 ElectricCar 物件
my_ev = ElectricCar(max_speed, num_doors, battery_capacity)

# 呼叫方法印出規格
my_ev.display_specs()