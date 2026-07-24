# 函數

如果所有工作都塞在 `main()`，程式很快就會變得難讀、難測試、難修改：

```cpp
int main() {
    // 輸入資料
    // 驗證資料
    // 計算統計
    // 排序
    // 顯示報表
    // 儲存檔案……
}
```

函數把工作拆成有名稱的小單位：

```text
main
 ├─ readScores
 ├─ validateScores
 ├─ calculateAverage
 └─ printReport
```

好處：

- **抽象化：** 呼叫者只需知道函數做什麼。
- **重用：** 同一邏輯不必複製多份。
- **可讀性：** 好名稱就是程式文件。
- **可測試：** 每個函數可以獨立驗證。
- **可維護：** 修改集中在單一位置。
- **分工：** 團隊成員可依介面平行開發。

> 函數不是單純把程式碼移到別處。好的函數會建立清楚的輸入、輸出與責任邊界。

## 函數的基本結構

```cpp
回傳型態 函數名稱(參數列表) {
    函數本體
    return 回傳值;
}
```

### Problem. 第一個函數

```cpp
#include <iostream>

using namespace std;

int add(int left, int right) {
    // 函數只負責計算，不處理輸入輸出。
    return left + right;
}

int main() {
    int answer = add(10, 20);
    cout << "答案：" << answer << '\n';
}
```

### void 函數

不需要回傳資料時使用 `void`。

```cpp
#include <iostream>
#include <string>

using namespace std;

void printGreeting(const string& name) {
    // void 函數可以用 return; 提早結束，但不回傳數值。
    if (name.empty()) {
        cout << "姓名不可為空\n";
        return;
    }
    cout << "你好，" << name << "！\n";
}

int main() {
    printGreeting("小華");
}
```

## 宣告、定義與呼叫

編譯器在呼叫函數前必須知道其介面。

```cpp
#include <iostream>

using namespace std;

// 函數宣告：告訴編譯器名稱、參數與回傳型態。
double rectangleArea(double width, double height);

int main() {
    cout << rectangleArea(5.0, 3.0) << '\n';
}

// 函數定義：提供實際運算內容。
double rectangleArea(double width, double height) {
    return width * height;
}
```

### Problem. 呼叫流程與呼叫堆疊

每次呼叫會建立新的函數執行環境，保存參數、區域變數與返回位置。函數結束後，該次呼叫的區域物件會被銷毀。

```cpp
#include <iostream>

using namespace std;

int square(int value) {
    cout << "進入 square\n";
    return value * value;
}

int sumOfSquares(int first, int second) {
    cout << "進入 sumOfSquares\n";
    return square(first) + square(second);
}

int main() {
    cout << "進入 main\n";
    int result = sumOfSquares(3, 4);
    cout << "結果：" << result << '\n';
}
// 進入 main
// 進入 sumOfSquares
// 進入 square
// 進入 square
// 結果：25
```

### `return` 後不再執行

```cpp
bool isValidScore(int score) {
    if (score < 0 || score > 100) {
        return false;
    }
    return true;
}
```

非 `void` 函數的所有可達路徑都應回傳相容的值。

## 參數傳遞

### 傳值：取得副本

適合：

- `int`、`double`、`char`、`bool` 等小型型態。
- 函數本來就需要一份副本。
- 要取得所有權或允許移動的參數。

```cpp
#include <iostream>

using namespace std;

void addTen(int value) {
    // value 是副本，修改不影響呼叫端。
    value += 10;
}

int main() {
    int score = 70;
    addTen(score);
    cout << score << '\n'; // 仍為 70
}
```

### 傳參考：原物件的別名

非 `const` 參考代表函數可能修改呼叫端。函數名稱和文件應明確表達副作用。

```cpp
#include <iostream>

using namespace std;

void addBonus(int& score, int bonus) {
    // score 是呼叫端變數的別名。
    score += bonus;
    if (score > 100) {
        score = 100;
    }
}

int main() {
    int score = 95;
    addBonus(score, 10);
    cout << score << '\n'; // 100
}
```

### 唯讀參考

大型唯讀物件通常使用 `const T&`；小型基本型態通常直接傳值。

```cpp
#include <iostream>
#include <string>

using namespace std;

void printStudent(const string& name, int score) {
    // const& 避免複製，也禁止函數修改 name。
    cout << name << "：" << score << '\n';
}

int main() {
    string name = "王小明";
    printStudent(name, 88);
}
```

### 指標參數

當「沒有物件」是合法狀態，使用指標。

```cpp
#include <iostream>

using namespace std;

bool tryDivide(double left, double right, double* result) {
    if (right == 0.0 || result == nullptr) {
        return false;
    }
    *result = left / right;
    return true;
}

int main() {
    double result = 0.0;
    if (tryDivide(10.0, 4.0, &result)) {
        cout << result << '\n';
    }
}
```

---

## 回傳值與錯誤表示

### Problem. 優先按值回傳

```cpp
#include <string>

using namespace std;

string makeFullName(const string& family, const string& given) {
    // 現代 C++ 會進行回傳值最佳化或移動，不必回傳區域物件參考。
    return family + given;
}

int main() {
    string name = makeFullName("王", "小明");
}
```

絕對不要回傳區域變數的參考或指標：

```cpp
const string& dangerous() {
    string local = "temporary";
    return local; // 函數結束後 local 已不存在
}
```

### Problem. 同時回傳多個值

可用 `struct` 表達具名結果。

```cpp
#include <iostream>

using namespace std;

struct DivisionResult {
    int quotient;
    int remainder;
};

DivisionResult divide(int dividend, int divisor) {
    return {dividend / divisor, dividend % divisor};
}

int main() {
    DivisionResult result = divide(17, 5);
    cout << result.quotient << ' ' << result.remainder << '\n';
}
```

## 陣列、字串與容器參數

```cpp
int sum(const int values[], size_t size);
```

參數中的 `int values[]` 實際上是 `const int*`，函數不知道長度，必須額外傳入 `size`。

```cpp
#include <cstddef>
#include <iostream>

using namespace std;

int sum(const int* values, size_t size) {
    int result = 0;
    for (size_t i = 0; i < size; ++i) {
        result += values[i];
    }
    return result;
}

int main() {
    int values[] = {1, 2, 3, 4, 5};
    cout << sum(values, 5) << '\n';
}
```

## 作用域

變數應在最小需要範圍內宣告。

```cpp
// 區域作用域
void example() {
    int outer = 10;
    if (outer > 0) {
        int inner = 20;
    }
    // inner 在此不可見，而且已結束生命週期。
}
```

## 靜態區域變數 static

`static` 狀態會讓測試和併行程式更難推理，應有明確理由才使用。

```cpp
#include <iostream>

using namespace std;

int nextId() {
    // 只初始化一次，並在多次呼叫之間保留值。
    static int id = 0;
    return ++id;
}

int main() {
    cout << nextId() << '\n';
    cout << nextId() << '\n';
    cout << nextId() << '\n';
}
```

## 預設參數

規則：

- 預設值通常只寫在宣告，不在定義重複。
- 有預設值後，右側參數也必須有預設值。
- 呼叫時只能從右側省略參數。

```cpp
#include <iostream>
#include <string>

using namespace std;

void printMessage(
    const string& message,
    int repeat = 1,
    const string& separator = "\n"
) {
    for (int i = 0; i < repeat; ++i) {
        cout << message;
        if (i + 1 < repeat) {
            cout << separator;
        }
    }
    cout << '\n';
}

int main() {
    printMessage("Hello");
    printMessage("Hi", 3, " | ");
}
```

## 函數多載

```cpp
#include <iostream>
#include <string>

using namespace std;

int maximum(int left, int right) {
    return left > right ? left : right;
}

double maximum(double left, double right) {
    return left > right ? left : right;
}

const string& maximum(const string& left, const string& right) {
    return left > right ? left : right;
}

int main() {
    cout << maximum(3, 8) << '\n';
    cout << maximum(2.5, 1.8) << '\n';
}
```

不能只靠回傳型態多載：

```cpp
// int convert(string);
// double convert(string); // 錯：參數列表完全相同
```

若不同多載的行為語意不一致，應改用不同名稱。

## 遞迴

遞迴函數直接或間接呼叫自己，必須具備：

1. 終止條件：不再遞迴。
2. 縮小問題：每次更接近終止條件。

### Problem. 階乘

```cpp
#include <iostream>

using namespace std;

unsigned long long factorial(unsigned int n) {
    // 0! 與 1! 都是 1。
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    cout << factorial(5) << '\n';
}
```

呼叫展開：

```text
factorial(5)
= 5 * factorial(4)
= 5 * 4 * factorial(3)
= 5 * 4 * 3 * 2 * 1
= 120
```

### Problem. 遞迴二分搜尋

```cpp
#include <vector>

using namespace std;

int binarySearch(
    const vector<int>& values,
    int target,
    int left,
    int right
) {
    if (left > right) {
        return -1;
    }

    int middle = left + (right - left) / 2;
    if (values[middle] == target) {
        return middle;
    }
    if (target < values[middle]) {
        return binarySearch(values, target, left, middle - 1);
    }
    return binarySearch(values, target, middle + 1, right);
}
```

### 遞迴風險

- 忘記終止條件會造成堆疊溢位。
- 問題縮小方向錯誤，永遠到不了終點。
- 重複計算可能造成極差效能。
- 深度過大時，迴圈通常更安全。
- 整數結果可能在堆疊溢位之前就先算術溢位。

## 函數指標

```cpp
#include <iostream>

using namespace std;

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }

int calculate(int a, int b, int (*operation)(int, int)) {
    return operation(a, b);
}

int main() {
    cout << calculate(3, 4, add) << '\n';
    cout << calculate(3, 4, multiply) << '\n';
}
```

## lambda

lambda 是可在使用位置定義的匿名函數，常搭配排序使用。

```cpp
// lambda 基本形式：
[捕獲列表](參數列表) -> 回傳型態 {
    函數本體
}
```

```cpp
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> values{3, -8, 2, -1, 5};

    // 依絕對值由小到大排序。
    sort(values.begin(), values.end(), [](int left, int right) {
        return abs(left) < abs(right);
    });

    for (int value : values) {
        cout << value << ' ';
    }
}
```

## 多檔案程式與標頭檔

實務專案不會把所有函數放在一個檔案。原則：

- `.hpp` 放公開宣告。
- `.cpp` 放非模板函數定義。
- 標頭檔應可獨立被引入。
- 不要在標頭檔寫 `using namespace std;`，避免污染使用者命名空間。
- 標頭中的非 `inline` 函數定義可能違反單一定義規則。

```text
├── calculator.hpp  宣告公開介面
├── calculator.cpp  定義實作
└── main.cpp        使用介面
```

```cpp
// calculator.hpp
#ifndef CALCULATOR_HPP
#define CALCULATOR_HPP

int add(int left, int right);
int subtract(int left, int right);

#endif
```

```cpp
// calculator.cpp
#include "calculator.hpp"

int add(int left, int right) {
    return left + right;
}

int subtract(int left, int right) {
    return left - right;
}
```

```cpp
// 多檔案主程式.cpp
#include <iostream>
#include "calculator.hpp"

using namespace std;

int main() {
    cout << add(10, 3) << '\n';
    cout << subtract(10, 3) << '\n';
}
```

編譯：

```text
g++ -std=c++17 main.cpp calculator.cpp -o calculator
```

### [練習題目](./練習題目.md)
