# 判斷式

判斷式就是讓程式「看情況做事」。  
你可以把它想成軟體裡的路口：使用者輸入不同、資料狀態不同、系統條件不同，程式就要走不同的路。

## 比較運算子

- 在學 `if` 之前，先認識用來構成條件的**比較運算子（Relational Operators）**：
- ⚠️ **超級常見的 Bug**：`=` 是**賦值**（assignment），`==` 才是**比較**（comparison）！

| 運算子 | 意義     | 範例     | 結果    |
| ------ | -------- | -------- | ------- |
| `==`   | 等於     | `5 == 5` | `true`  |
| `!=`   | 不等於   | `5 != 3` | `true`  |
| `<`    | 小於     | `3 < 5`  | `true`  |
| `>`    | 大於     | `5 > 3`  | `true`  |
| `<=`   | 小於等於 | `5 <= 5` | `true`  |
| `>=`   | 大於等於 | `3 >= 5` | `false` |

## if：條件成立才做

```cpp
#include <iostream>
using namespace std;

int main() {
    int score = 0; // 宣告 score，用來存放使用者輸入的成績。
    cout << "請輸入成績："; // 提示使用者輸入資料。
    cin >> score;     // 從鍵盤讀入一個整數，放進 score。

    if (score >= 60) { // 如果 score 大於等於 60，代表及格。
        cout << "及格，這科先過關。" << endl;
    }


    cout << "程式結束。" << endl; // 這行不在 if 裡面，所以不管條件成不成立都會執行。
    return 0;
}
```

## `if...else`：二選一

```cpp
#include <iostream>
using namespace std;

int main() {
    // number 用來存放使用者輸入的整數。
    int number = 0;

    cout << "請輸入一個整數：";
    cin >> number;

    // % 是取餘數。任何整數除以 2，餘數是 0 就是偶數。
    if (number % 2 == 0) {
        cout << number << " 是偶數。" << endl;
    } else {
        // 如果上面的條件不成立，就代表餘數不是 0，也就是奇數。
        cout << number << " 是奇數。" << endl;
    }

    return 0;
}
```

## `else if`：多種情況

```cpp
#include <iostream>
using namespace std;

int main() {
    int score = 0;

    cout << "請輸入 0 到 100 的成績：";
    cin >> score;

    // 先處理不合理資料，避免後面分級被亂輸入影響。
    if (score < 0 || score > 100) {
        cout << "成績範圍錯誤。" << endl;
    } else if (score >= 90) {
        cout << "等第 A" << endl;
    } else if (score >= 80) {
        cout << "等第 B" << endl;
    } else if (score >= 70) {
        cout << "等第 C" << endl;
    } else if (score >= 60) {
        cout << "等第 D" << endl;
    } else {
        cout << "等第 F" << endl;
    }

    return 0;
}
```

### Problem. 登入帳密

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // string 可以存文字，例如帳號與密碼。
    string username;
    string password;

    // bool 適合存是/否狀態。
    bool isBanned = false;

    cout << "帳號：";
    cin >> username;

    cout << "密碼：";
    cin >> password;

    // && 代表所有條件都要成立。
    // !isBanned 代表「不是被停權」。
    if (username == "admin" && password == "1234" && !isBanned) {
        cout << "登入成功。" << endl;
    } else {
        cout << "登入失敗。" << endl;
    }

    return 0;
}
```

### Problem. 先判斷年齡，再判斷會員

```cpp
#include <iostream>
using namespace std;

int main() {
    int age = 0;
    char isMember = 'n';
    int price = 300;

    cout << "請輸入年齡：";
    cin >> age;

    cout << "是否為會員？(y/n)：";
    cin >> isMember;

    // 第一層：先判斷年齡票種。
    if (age < 0) {
        cout << "年齡不可小於 0。" << endl;
        return 0;
    } else if (age < 12) {
        price = 150;
    } else if (age >= 65) {
        price = 180;
    } else {
        price = 300;
    }

    // 第二層：在票價算出來後，再判斷會員折扣。
    if (isMember == 'y' || isMember == 'Y') {
        price = price - 30;
        cout << "會員折扣 30 元。" << endl;
    }

    cout << "應付票價：" << price << " 元" << endl;
    return 0;
}
```

## 三元運算子

- 三元運算子適合用在很短的二選一。
- 如果邏輯開始變複雜，請回去用 `if...else`。可讀性比炫技重要。

```cpp
格式：
條件 ? 條件成立的值 : 條件不成立的值

例如：
string result = score >= 60 ? "及格" : "不及格";
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int amount = 0;

    cout << "請輸入購物金額：";
    cin >> amount;

    // 三元運算子適合簡短的二選一。
    // 金額滿 1000 免運，否則運費 80。
    int shippingFee = amount >= 1000 ? 0 : 80;

    cout << "商品金額：" << amount << " 元" << endl;
    cout << "運費：" << shippingFee << " 元" << endl;
    cout << "總金額：" << amount + shippingFee << " 元" << endl;

    return 0;
}
```

### [練習題目](./練習題目.md)

### ZeroJudge -- 判斷式

| 知識點           | 題號 |
| ---------------- | ---- |
| if 基本判斷      | a002 |
| 大小比較         | a003 |
| 奇偶判斷         | a038 |
| 閏年判斷         | a004 |
| 三角形判斷       | a006 |
| 成績等第         | d460 |
| 多重 if-else     | a053 |
| 區間判斷         | a058 |
| 最大值           | d070 |
| 最小值           | d071 |
| 絕對值           | d072 |
| 三數排序(判斷版) | d073 |
| BMI 判斷         | d074 |
| 是否倍數         | d478 |
| 優惠計算         | d490 |
| 條件分類         | e339 |
| 綜合判斷         | e343 |
| APCS 入門判斷    | c149 |
