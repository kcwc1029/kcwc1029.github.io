# Conditional Statement(條件判斷)

## 關聯運算子 (Relational Operators)

![upgit_20260420_1776667080.png|329x184](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260420_1776667080.png)

## Python 邏輯運算子

邏輯運算子通常會用在「判斷條件」裡面。

例如：

你想判斷一個學生：

- 分數是否及格
- 是否同時符合兩個條件
- 是否只要符合其中一個條件就可以
- 是否不是某種狀態

這時候就會用到邏輯運算子。

| 運算子 | 意思 | 說明                   |
| ------ | ---- | ---------------------- |
| `and`  | 而且 | 兩個條件都要成立       |
| `or`   | 或者 | 其中一個條件成立就可以 |
| `not`  | 不是 | 將結果反轉             |

- [範例：兩個條件都要成立](./Conditional_Statement_src/and_operator_demo.py)
- [範例：是否可以通過課程](./Conditional_Statement_src/course_pass_demo.py)
- [範例：其中一個條件成立就可以](./Conditional_Statement_src/or_operator_demo.py)
- [範例：是否可以享有優惠](./Conditional_Statement_src/discount_demo.py)
- [範例：把結果反過來](./Conditional_Statement_src/not_operator_demo.py)
- [範例：登入判斷](./Conditional_Statement_src/login_demo.py)

## 判斷式(if / else)

在寫程式時，我們常常會遇到一種情況：根據不同條件，執行不同動作。

例如：

- 成績及格才能通過
- 年齡滿 18 才能註冊
- 餘額不足不能買東西
- 下雨就帶傘

這時候就會用到「判斷式」。

### if：如果條件成立，就執行

```py
score = 80

if score >= 60:
    print("及格")
```

- [範例：年齡判斷](./Conditional_Statement_src/age_check_demo.py)

### if else：二選一判斷

有時候我們希望：

- 條件成立做一件事
- 條件不成立做另一件事

```py
score = 40

if score >= 60:
    print("及格")
else:
    print("不及格")
```

- [範例：餘額判斷](./Conditional_Statement_src/money_check_demo.py)

### if elif else：多條件判斷

如果有很多種情況。

例如：

- 90 分以上：A
- 80 分以上：B
- 60 分以上：C
- 其他：不及格

```py
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 60:
    print("C")
else:
    print("不及格")
```

- [範例：基於gradio做電影票價計算](./Conditional_Statement_src/Movie_ticket_fee_calculator.py)

## 補充：尚未設定的變數值 None

```py
x = None
print(x) # None
print(type(x)) # <class 'NoneType'>
```

## 練習

- [練習題目](./Conditional_Statement_practices/練習題目.ipynb)
- [Problem. 基於gradio做Discord 身分組驗證](./Conditional_Statement_practices/discord_role_check_gradio.py)
- [Problem. 基於gradio做Discord 校園 Wi-Fi 登入](./Conditional_Statement_practices/campus_wifi_login_gradio.py)
- [Problem. 基於gradio做手機充電提醒](./Conditional_Statement_practices/battery_warning_gradio.py)
- [Problem. 基於gradio做電商優惠券判斷](./Conditional_Statement_practices/coupon_checker_gradio.py)
