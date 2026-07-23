# 迴圈

迴圈就是讓程式「重複做事」。

你可以把它想成：如果一件事要做 100 次，你不會真的複製貼上 100 行程式碼，而是寫一個規則，讓電腦自己跑完。

### 為什麼需要迴圈？

想像一個情境：你要印出 1 到 100 的所有數字。

如果沒有迴圈，你必須寫 100 行 `cout`：

```cpp
cout << 1 << endl;
cout << 2 << endl;
cout << 3 << endl;
// ... 一直到 100
cout << 100 << endl;
```

這顯然既費時又容易出錯。**迴圈**讓我們只需寫一段程式，讓電腦重複執行：

```cpp
for (int i = 1; i <= 100; i++) {
    cout << i << endl;
}
```

迴圈是程式設計中最重要的概念之一，幾乎所有實際應用都離不開它。

### 迴圈可以幹嘛

你會用迴圈做這些事：

- 跑固定次數：印出 1 到 10、產生 100 筆測試資料。
- 跑到條件滿足：一直要求輸入密碼，直到正確。
- 處理一串資料：把每筆成績加總，算平均。
- 做互動選單：使用者選功能，直到選擇離開。
- 畫圖形：用星號印三角形、九九乘法表。
- 跳過或中止：遇到不合法資料跳過，找到答案就停止。

## `while`：條件成立就一直做

```
while (條件式) {
    // 迴圈主體（重複執行的程式碼）
}
```

- `while` 適合「不知道會跑幾次，但知道停止條件」的情境。
- `while` 裡面通常要改變條件相關的變數，不然很容易變成無限迴圈。

### Problem. while迴圈倒數計時

```cpp
#include <iostream>
using namespace std;

int main() {
    // count 是計數器，負責記錄目前倒數到幾。
    int count = 5;

    // 只要 count 大於 0，就繼續執行迴圈。
    while (count > 0) {
        // 印出目前的 count。
        cout << count << endl;
        // count 每次減 1，讓迴圈最後可以結束。
        count--;
    }

    // while 結束後才會執行這一行。
    cout << "發射！" << endl;
    return 0;
}
```

### Problem. while迴圈計算1至100

```cpp
#include <iostream>
using namespace std;

int main() {
    int i = 1;
    int sum = 0;

    while (i <= 100) {
        sum += i;   // sum = sum + i
        i++;
    }

    cout << "1 到 100 的總和為：" << sum << endl;

    return 0;
}
```

### Problem. while迴圈猜數字遊戲

```cpp
#include <iostream>
using namespace std;

int main() {
    int secret = 42;    // 秘密數字
    int guess;
    int attempts = 0;

    cout << "=== 猜數字遊戲 ===" << endl;
    cout << "請猜一個 1 到 100 之間的數字：" << endl;

    cin >> guess;
    attempts++;

    while (guess != secret) {
        if (guess < secret) {
            cout << "太小了！再猜一次：";
        } else {
            cout << "太大了！再猜一次：";
        }
        cin >> guess;
        attempts++;
    }

    cout << "恭喜！答對了！" << endl;
    cout << "你共猜了 " << attempts << " 次" << endl;

    return 0;
}
```

## `for`：固定次數很順手

- `for` 適合「很清楚要跑幾次」的情境。

### Problem. 基本計數

```cpp
#include <iostream>
using namespace std;

int main() {
    // 正向計數
    cout << "正向計數：";
    for (int i = 1; i <= 5; i++) {
        cout << i << " ";
    }
    cout << endl;

    // 反向計數
    cout << "反向計數：";
    for (int i = 5; i >= 1; i--) {
        cout << i << " ";
    }
    cout << endl;

    // 間隔計數（每次加 2）
    cout << "偶數：";
    for (int i = 2; i <= 10; i += 2) {
        cout << i << " ";
    }
    cout << endl;

    return 0;
}

```

### Problem. for迴圈累加

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 0;

    // sum 是累加器，負責存目前加總。
    int sum = 0;

    cout << "請輸入 n：";
    cin >> n;

    // i 從 1 開始，每次加 1，直到 i 大於 n 為止。
    for (int i = 1; i <= n; i++) {
        // 把目前的 i 加進 sum。
        sum = sum + i;
    }

    cout << "1 加到 " << n << " 的總和是：" << sum << endl;
    return 0;
}
```

### Problem. 找出最大值與最小值

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "請輸入數字個數：";
    cin >> n;

    int num;
    cout << "請輸入第 1 個數字：";
    cin >> num;

    int maxVal = num;
    int minVal = num;

    for (int i = 2; i <= n; i++) {
        cout << "請輸入第 " << i << " 個數字：";
        cin >> num;

        if (num > maxVal) maxVal = num;
        if (num < minVal) minVal = num;
    }

    cout << "最大值：" << maxVal << endl;
    cout << "最小值：" << minVal << endl;

    return 0;
}
```

### Problem. 計算階乘

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "請輸入 n：";
    cin >> n;

    long long factorial = 1;    // 用 long long 避免溢位

    for (int i = 1; i <= n; i++) {
        factorial *= i;          // factorial = factorial * i
    }

    cout << n << "! = " << factorial << endl;

    return 0;
}

```

### Problem. 九九乘法表

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    for (int i = 1; i <= 9; i++) {          // 外層：被乘數
        for (int j = 1; j <= 9; j++) {      // 內層：乘數
            cout << i << "×" << j << "="
                 << setw(2) << i * j << "  ";  // setw(2) 對齊
        }
        cout << endl;    // 換行（每個被乘數一行）
    }

    return 0;
}
```

### Problem. 印出矩形星號

```cpp
#include <iostream>
using namespace std;

int main() {
    int rows, cols;
    cout << "請輸入列數和行數：";
    cin >> rows >> cols;

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cout << "* ";
        }
        cout << endl;
    }

    return 0;
}
```

### Problem. 印出直角三角形

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "請輸入層數：";
    cin >> n;

    cout << "\n左下直角三角形：" << endl;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {    // 第 i 行印 i 個星號
            cout << "* ";
        }
        cout << endl;
    }

    cout << "\n右下直角三角形：" << endl;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i; j++) {    // 先印空格
            cout << "  ";
        }
        for (int j = 1; j <= i; j++) {        // 再印星號
            cout << "* ";
        }
        cout << endl;
    }

    return 0;
}
```

### Problem. 印出等腰三角形

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int rows = 3, cols = 4;

    cout << "一個 " << rows << "×" << cols << " 的乘法矩陣：" << endl;

    for (int i = 1; i <= rows; i++) {
        for (int j = 1; j <= cols; j++) {
            cout << setw(4) << i * j;
        }
        cout << endl;
    }

    return 0;
}
```

## `break`：提早離開迴圈

- `break` 適合「已經找到答案了，不需要再跑」。

### Problem. 搜尋第一個符合條件的數

```cpp
#include <iostream>
using namespace std;

int main() {
    int target;
    cout << "請輸入要搜尋的數字：";
    cin >> target;

    bool found = false;

    for (int i = 1; i <= 100; i++) {
        if (i % target == 0 && i != target) {
            cout << target << " 的第一個大於自身的倍數是：" << i << endl;
            found = true;
            break;    // 找到後立即停止
        }
    }

    if (!found) {
        cout << "在 1-100 範圍內找不到" << endl;
    }

    return 0;
}
```

## continue：跳過這一輪

- `continue` 適合「這筆資料不要處理，但下一筆還要繼續」。
- [範例：跳過不合法數字](./迴圈_src/跳過不合法數字.cpp)
- [範例：跳過特定數字](./迴圈_src/跳過特定數字.cpp)
- [範例：忽略負數](./迴圈_src/忽略負數.cpp)

### Problem. 跳過不合法數字

```cpp
#include <iostream>
using namespace std;

int main() {
    int score = 0;
    int sum = 0;
    int validCount = 0;

    for (int i = 1; i <= 5; i++) {
        cout << "請輸入第 " << i << " 筆成績：";
        cin >> score;

        // 如果資料不合法，就跳過這一輪後面的程式。
        if (score < 0 || score > 100) {
            cout << "不合法資料，這筆跳過。" << endl;
            continue;
        }

        // 只有合法資料才會走到這裡。
        sum = sum + score;
        validCount++;
    }

    cout << "合法筆數：" << validCount << endl;
    cout << "合法總分：" << sum << endl;
    return 0;
}
```

### Problem. 忽略負數

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "請輸入 5 個正整數（負數會被忽略，直到收集夠 5 個）：" << endl;

    int count = 0;
    int sum = 0;

    while (count < 5) {
        int x;
        cin >> x;

        if (x < 0) {
            cout << "  忽略負數 " << x << endl;
            continue;    // 跳過本次，不計入
        }

        sum += x;
        count++;
        cout << "  已收集 " << count << " 個" << endl;
    }

    cout << "5 個正整數的總和：" << sum << endl;
    cout << "平均：" << (double)sum / 5 << endl;

    return 0;
}
```

### [練習題目](./練習題目.md)

### ZeroJudge -- 迴圈 (20 題)

- d049
- d050
- d051
- d058
- d063
- d064
- d065
- d066
- d067
- d068
- d069
- d086
- d115
- d122
- d244
- d277
- d299
- e357
- e358
- e359
