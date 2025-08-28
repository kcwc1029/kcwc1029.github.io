class Member:
    """
    父類別，提供所有成員的共性
    """
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

class Student(Member):
    """
    子類別，繼承 Member
    """
    def __init__(self, name, member_id, major):
        super().__init__(name, member_id)
        self.major = major

    def display(self):
        return f"Student Record: {self.name}({self.member_id}) - Major: {self.major}"

class Professor(Member):
    """
    子類別，繼承 Member
    """
    def __init__(self, name, member_id, department):
        super().__init__(name, member_id)
        self.department = department

    def display(self):
        return f"Professor Record: {self.name}({self.member_id}) - Department: {self.department}"

# 讀取輸入
member_type = input()
name, member_id, specific_info = input().split()
member_id = int(member_id)

# 根據類型建立對應的物件
if member_type == 'S':
    member = Student(name, member_id, specific_info)
elif member_type == 'P':
    member = Professor(name, member_id, specific_info)

# 呼叫 display 方法並印出
print(member.display())