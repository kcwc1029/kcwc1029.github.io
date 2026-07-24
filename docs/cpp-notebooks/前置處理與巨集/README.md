# 前置處理與巨集

C++ 原始碼送進真正的編譯器之前，會先經過前置處理（preprocessing）。常見工作包括：

- 展開 `#include`。
- 展開 `#define` 巨集。
- 根據 `#if` 等指令保留或移除程式碼。
- 處理部分實作定義的 `#pragma`。

簡化流程：

```text
原始碼 .cpp
   ↓ 前置處理
翻譯單元（巨集已展開、標頭已引入）
   ↓ 編譯
目的檔 .o / .obj
   ↓ 連結
可執行檔
```

前置處理器主要做「token／文字層次轉換」，不了解 C++ 型態、作用域、物件生命週期或運算優先順序。

### Problem. 觀察前置處理結果

```cpp
#include <iostream>

#define MESSAGE "Hello, preprocessor!"

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
    // 編譯前，MESSAGE 會被替換成字串常值。
    cout << MESSAGE << '\n';
}
```

可只執行前置處理：

```text
g++ -std=c++17 -E 01_觀察前置處理結果.cpp
```

輸出通常很長，因為標頭內容也會被展開。可先建立不含標準標頭的小檔案觀察。

### 前置處理指令的形式

指令以 `#` 開頭，通常獨占一行：

```cpp
#include <iostream>
#define BUFFER_SIZE 1024
#if BUFFER_SIZE > 100
#endif
```

指令不是一般 C++ 敘述，結尾通常不加分號。

## #include與標頭檔

```cpp
#include <iostream>
#include "calculator.hpp"
```

- `<...>`：通常用於標準函式庫或設定好的系統引入路徑。
- `"..."`：通常優先搜尋目前檔案附近，再搜尋設定的引入路徑。

實際搜尋順序由編譯器與建置設定決定，不能把「尖括號必定是系統檔」當成語言保證。

### Problem. 宣告放標頭，定義放來源檔

```cpp
// calculator.hpp
#ifndef COURSE_CALCULATOR_HPP
#define COURSE_CALCULATOR_HPP

int add(int left, int right);

#endif
```

```cpp
// calculator.cpp
#include "calculator.hpp"

int add(int left, int right) {
    return left + right;
}
```

```cpp
// 使用自訂標頭.cpp
#include <iostream>
#include "calculator.hpp"

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
    cout << add(10, 20) << '\n';
}
```

編譯：

```text
g++ -std=c++17 02_使用自訂標頭.cpp calculator.cpp -o calculator
```

## 物件式巨集 `#define`

不帶參數的巨集稱為物件式巨集。

慣例使用全大寫，提醒讀者它不是一般變數。

```cpp
#define APP_NAME "Grade Analyzer"
#define MAX_STUDENTS 50
```

```cpp
#include <iostream>

#define APP_NAME "Grade Analyzer"
#define MAX_STUDENTS 50

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
    cout << APP_NAME << '\n';
    cout << "人數上限：" << MAX_STUDENTS << '\n';
}
```

### `#undef`

```cpp
#define TEMP_VALUE 10
#undef TEMP_VALUE
```

`#undef` 之後該名稱不再是巨集。頻繁重新定義通常表示設計混亂。

### 巨集沒有型態與作用域

前置處理器只替換 token，不知道 `PI` 是 `double`。

```cpp
#define PI 3.141592653589793
```

## 函數式巨集

函數式巨集帶有參數：

```cpp
#define SQUARE(x) ((x) * (x))
```

巨集名稱與左括號之間不能插入空白，否則會變成物件式巨集。

```cpp
#include <iostream>

#define SQUARE(x) ((x) * (x))

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
    int value = 5;
    cout << SQUARE(value) << '\n';
    cout << SQUARE(value + 1) << '\n';
    // 展開概念：SQUARE(value + 1) → ((value + 1) * (value + 1))
}
```

### 為什麼每個參數和結果都要加括號

```cpp
// 錯誤：
#define BAD_SQUARE(x) x * x

// BAD_SQUARE(2 + 3)
// → 2 + 3 * 2 + 3
// → 11，不是 25
```

```cpp
// 另一個錯誤：
#define BAD_ADD(a, b) (a) + (b)

// 2 * BAD_ADD(3, 4)
// → 2 * (3) + (4)
// → 10，不是 14
```

## 巨集的重大陷阱

### 重複求值

```cpp
#define SQUARE(x) ((x) * (x))

int value = 3;
int result = SQUARE(value++);
// 展開後 `value++` 出現兩次。這類程式可能具有未定義或非預期行為，絕對不要把有副作用的運算式傳給會重複使用參數的巨集。
```

### 名稱污染

巨集不服從命名空間：

```cpp
#define min(a, b) ...
// 即使程式寫 `std::min`，`min` token 仍可能被巨集干擾。巨集名稱應加上專案前綴：
```

## 條件編譯

### `#if`、`#elif`、`#else`、`#endif`

```cpp
#include <iostream>

#define COURSE_LEVEL 2

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
#if COURSE_LEVEL >= 3
    cout << "進階模式\n";
#elif COURSE_LEVEL == 2
    cout << "中階模式\n";
#else
    cout << "基礎模式\n";
#endif
}
```

未定義識別字在 `#if` 整數常數運算式中通常視為 0，但明確使用 `defined` 更容易閱讀。

### `#ifdef`、`#ifndef` 與 `defined`

```cpp
#ifdef COURSE_DEBUG
    // COURSE_DEBUG 已定義
#endif

#ifndef COURSE_DEBUG
    // COURSE_DEBUG 未定義
#endif

#if defined(COURSE_DEBUG) && !defined(COURSE_RELEASE)
#endif
```

### 除錯程式碼

```cpp
#include <iostream>

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
    int value = 42;

#ifdef COURSE_DEBUG
    cout << "[DEBUG] value=" << value << '\n';
#endif

    cout << "程式完成\n";
}
// 編譯：
// g++ -std=c++17 -DCOURSE_DEBUG 11_除錯模式.cpp

// 沒有 `-DCOURSE_DEBUG` 時，除錯輸出不會進入翻譯單元。
```

### 跨平台條件

```cpp
#if defined(_WIN32)
    // Windows
#elif defined(__linux__)
    // Linux（編譯器慣用巨集，非標準 C++ 保證）
#elif defined(__APPLE__)
    // Apple 平台
#else
    // 未知平台
#endif
```

平台巨集多由編譯器定義，應查閱工具鏈文件，並把平台差異集中在少數抽象層，而非散落整個專案。

## 標準預定義巨集

| 巨集          | 用途               |
| ------------- | ------------------ |
| `__FILE__`    | 目前來源檔名稱字串 |
| `__LINE__`    | 目前來源行號       |
| `__DATE__`    | 翻譯日期字串       |
| `__TIME__`    | 翻譯時間字串       |
| `__cplusplus` | C++ 標準版本數值   |

```cpp
#include <iostream>

using namespace std;

// 主程式：依照範例或題目規格執行，並輸出驗證結果。
int main() {
    cout << "檔案：" << __FILE__ << '\n';
    cout << "行號：" << __LINE__ << '\n';
    cout << "日期：" << __DATE__ << '\n';
    cout << "時間：" << __TIME__ << '\n';
    cout << "C++：" << __cplusplus << '\n';
}
```

`__DATE__`、`__TIME__` 會讓相同原始碼在不同時間產生不同輸出，不利可重現建置。版本資訊通常由建置系統明確注入更好。
