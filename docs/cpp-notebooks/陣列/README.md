# 陣列（Array）

## 為什麼需要陣列

若要記錄 3 位學生的成績，我們可以使用 3 個變數：

```cpp
int score1 = 78;
int score2 = 92;
int score3 = 85;
```

但若有 100 位學生，宣告 `score1` 到 `score100` 不但麻煩，也無法方便地用迴圈處理。陣列讓我們用一個名稱管理一批「型態相同、用途相同」且排列連續的資料。

```cpp
int scores[5] = {78, 92, 85, 61, 73};
```

可以把它想成一排有編號的置物櫃：

```text
索引       0       1       2       3       4
        +-------+-------+-------+-------+-------+
數值    |  78   |  92   |  85   |  61   |  73   |
        +-------+-------+-------+-------+-------+
名稱    scores[0]                            scores[4]
```

陣列的核心優點：

- 用單一名稱表示一組相關資料。
- 可利用索引與迴圈批次處理。
- 元素連續存放，存取速度快。
- 是字串、矩陣、影像、查找表與許多資料結構的基礎。

### Problem. 第一個陣列

```cpp
#include <iostream>

using namespace std;  // 使用標準函式庫命名空間

// 主程式：依序完成資料準備、處理與結果輸出。
int main() {
    int scores[5] = {78, 92, 85, 61, 73};

    cout << "第一位學生：" << scores[0] << '\n';
    cout << "最後一位學生：" << scores[4] << '\n';

    scores[3] = 66;
    cout << "補考後第四位學生：" << scores[3] << '\n';
}
```

## 一維原生陣列

```cpp
// 宣告語法
資料型態 陣列名稱[元素個數];

// 例如：
int scores[5];       // 5 個 int
double prices[10];   // 10 個 double
char grades[8];      // 8 個 char
bool passed[30];     // 30 個 bool
```

陣列中的每一格稱為「元素」。存取元素時使用中括號：

```cpp
scores[0] = 80;
scores[1] = 90;
cout << scores[0] << '\n';
```

### 索引可以是運算式

索引不必是寫死的數字，也可以是變數或運算結果：

```cpp
#include <iostream>

using namespace std;  // 使用標準函式庫命名空間

// 主程式：依序完成資料準備、處理與結果輸出。
int main() {
    int data[5] = {10, 20, 30, 40, 50};
    int index = 2;

    cout << data[index] << '\n';      // 30
    cout << data[index + 1] << '\n';  // 40
}
```

索引的型態應為整數型態，而且結果必須落在合法範圍。

### 賦值與讀取

```cpp
#include <iostream>

using namespace std;  // 使用標準函式庫命名空間

int main() {
    constexpr int size = 5;
    int numbers[size]{};

    cout << "請輸入 5 個整數：";
    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int i = 0; i < size; ++i) {
        cin >> numbers[i];
    }

    cout << "你輸入的是：";
    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int i = 0; i < size; ++i) {
        cout << numbers[i] << ' ';
    }
    cout << '\n';
}
```

## 初始化、長度與記憶體

```cpp
// 常見初始化方式
int a[5];                    // 區域陣列：元素值未定，不可直接使用
int b[5]{};                  // 全部初始化為 0
int c[5] = {1, 2, 3, 4, 5}; // 完整初始化
int d[5] = {1, 2};           // 1, 2, 0, 0, 0
int e[] = {4, 8, 15, 16};    // 編譯器推導長度為 4
int f[5] = {};               // 全部為 0
```

沒有初始化的區域陣列含有未定值。讀取它是錯誤的程式行為，不能假設它一定是 0。

```cpp
#include <iostream>

using namespace std;

int main() {
    int values[6] = {7, 9};

    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int value : values) {
        cout << value << ' ';
    }
    cout << '\n';  // 7 9 0 0 0 0
}
```

### 使用 `size` 取得元素個數

C++17 起可以使用 `size`。`sizeof(values)` 是整個陣列的位元組數，`sizeof(values[0])` 是一個元素的位元組數。兩者相除得到元素個數。現代 C++ 優先使用 `size`，意圖更清楚。

```cpp
#include <iostream>
#include <iterator>

using namespace std;

int main() {
    int values[] = {10, 20, 30, 40, 50};
    cout << "元素個數：" << size(values) << '\n';
}
```

### 補充：sizeof陷阱

陣列傳入一般函式參數後，通常會退化（decay）成指標。此時 `sizeof(parameter)` 得到的是指標大小，而非原陣列大小。

因此函式通常要同時接收長度，或使用 `array`、`span` 等保留範圍資訊的工具。

```cpp
void wrongSize(int values[]) {
    // 此處 values 實際上是 int*
    cout << sizeof(values) << '\n'; // 不是陣列總大小
}
```

### 連續記憶體

原生陣列的元素會連續存放。若 `int` 佔 4 位元組，元素位址可能如下：

```text
values[0]  0x1000
values[1]  0x1004
values[2]  0x1008
values[3]  0x100C
```

```cpp
#include <iostream>

using namespace std;  // 使用標準函式庫命名空間

int main() {
    int values[4] = {10, 20, 30, 40};
    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int i = 0; i < 4; ++i) {
        cout << "&values[" << i << "] = "
                  << static_cast<const void*>(&values[i]) << '\n';
    }
}
```

。

## 陣列與迴圈

### 索引式 `for`

需要索引、要比較相鄰元素或反向走訪時，索引式迴圈最合適：

```cpp
// 依序走訪需要處理的元素，並確保索引不超出範圍。
for (size_t i = 0; i < size(values); ++i) {
    cout << "values[" << i << "] = " << values[i] << '\n';
}
```

### 範圍式 `for`

只需逐一讀取元素時，範圍式 `for` 更簡潔：

```cpp
// 依序走訪需要處理的元素，並確保索引不超出範圍。
for (int value : values) {
    cout << value << ' ';
}
```

若要修改原陣列，必須使用參考 `&`：

**建議檔名：`07_範圍式for與參考.cpp`**

```cpp
#include <iostream>

using namespace std;

int main() {
    int scores[] = {55, 68, 79, 91};

    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int score : scores) {
        score += 5;
        if (score > 100) {
            score = 100;
        }
    }

    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int score : scores) {
        cout << score << ' ';
    }
    cout << '\n';
}
```

## 陣列搭配常用陣列演算法

演算法不是死背程式碼，而是辨認「狀態如何更新」。

### 總和與平均

```cpp
#include <iostream>

using namespace std;

int main() {
    int scores[] = {78, 92, 85, 61, 73};
    int sum = 0;

    for (int score : scores) {
        sum += score;
    }

    double average = sum / size(scores);
    cout << "總分：" << sum << '\n'
              << "平均：" << average << '\n';
}
```

### 最大值、最小值與索引

```cpp
#include <iostream>

using namespace std;
int main() {
    int values[] = {-8, -3, -12, -1, -6};
    int maxValue = values[0];
    int maxIndex = 0;

    for (int i = 1; i < size(values); ++i) {
        if (values[i] > maxValue) {
            maxValue = values[i];
            maxIndex = i;
        }
    }

    cout << "最大值：" << maxValue << "，索引：" << maxIndex << '\n';
}
```

### 計數與條件篩選

```cpp
#include <iostream>

using namespace std;

int main() {
    int scores[] = {48, 60, 77, 59, 95, 61};
    int passed = 0;

    for (int score : scores) {
        if (score >= 60) {
            passed++;
        }
    }

    cout << "及格人數：" << passed << '\n';
}
```

### 線性搜尋

從頭逐一比較，時間複雜度為 `O(n)`。

```cpp
#include <iostream>

using namespace std;

int main() {
    int values[] = {42, 18, 73, 9, 55};
    int target;
    cin >> target;

    int foundIndex = -1;
    // 依序走訪需要處理的元素，並確保索引不超出範圍。
    for (int i = 0; i < size(values); ++i) {
        if (values[i] == target) {
            foundIndex = static_cast<int>(i);
            break;
        }
    }

    if (foundIndex == -1) {
        cout << "找不到\n";
    } else {
        cout << "位於索引 " << foundIndex << '\n';
    }
}
```

### 排序

實務上應先熟悉標準函式庫的 `sort`：

```cpp
#include <algorithm>
#include <iostream>

using namespace std;

int main() {
    int values[] = {42, 18, 73, 9, 55};

    sort(begin(values), end(values));
    for (int value : values) {
        cout << value << ' ';
    }
    cout << '\n';

    sort(begin(values), end(values), greater<int>{});
    for (int value : values) {
        cout << value << ' ';
    }
    cout << '\n';
}
```

## 二維與多維陣列

二維陣列像一張表格：

```cpp
int matrix[3][4];
```

它有 3 列（row）、每列 4 欄（column），共 `3 × 4 = 12` 個元素。

```text
             欄 0       欄 1       欄 2       欄 3
列 0      [0][0]      [0][1]      [0][2]      [0][3]
列 1      [1][0]      [1][1]      [1][2]      [1][3]
列 2      [2][0]      [2][1]      [2][2]      [2][3]
```

第一個索引是列，第二個索引是欄：`matrix[row][column]`。

### 初始化與走訪

```cpp
#include <iostream>

using namespace std;

int main() {
    int rows = 3;
    int cols = 4;

    int matrix[rows][cols] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };


    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            cout << matrix[row][col] << '\t';
        }
        cout << '\n';
    }
}
```

若部分初始化，其餘元素補 0：

```cpp
int matrix[2][4] = {
    {1, 2},
    {3}
};
// 實際為 {{1, 2, 0, 0}, {3, 0, 0, 0}}
```

### Problem. 每列與每欄總和

```cpp
// 外層迴圈決定「目前統計誰」，內層迴圈負責把相關元素累加。
#include <iostream>

using namespace std;

int main() {
    int students = 3;
    int subjects = 4;
    int scores[students][subjects] = {
        {80, 72, 91, 85},
        {65, 59, 73, 70},
        {94, 88, 90, 96}
    };

    for (int student = 0; student < students; ++student) {
        int sum = 0;
        for (int subject = 0; subject < subjects; ++subject) {
            sum += scores[student][subject];
        }
        cout << "學生 " << student + 1 << " 平均：" << sum/subjects << '\n';
    }

    for (int subject = 0; subject < subjects; ++subject) {
        int sum = 0;

        for (int student = 0; student < students; ++student) {
            sum += scores[student][subject];
        }
        cout << "科目 " << subject + 1  << " 平均：" <<  sum/subjects << '\n';
    }
}
```

### 記憶體排列

C++ 二維原生陣列採列優先（row-major）連續存放：

```text
matrix[0][0], matrix[0][1], matrix[0][2],
matrix[1][0], matrix[1][1], matrix[1][2], ...
```

因此通常以列為外層、欄為內層走訪，對快取較友善。

### 三維陣列

```cpp
int cube[2][3][4]{};
```

可理解為 2 層、每層 3 列、每列 4 欄，共 24 個元素。

```cpp
#include <iostream>

using namespace std;

int main() {
    int data[2][3][4]{};
    int next = 1;

    for (int layer = 0; layer < 2; ++layer) {
        for (int row = 0; row < 3; ++row) {
            for (int col = 0; col < 4; ++col) {
                data[layer][row][col] = next++;
            }
        }
    }
    cout << data[1][2][3] << '\n'; // 24
}
```

### ZeroJudge -- 陣列 (18 題)

- a149
- c315
- c316
- c317
- c318
- c350
- c356
- c364
- c381
- c382
- c418
- c419
- c420
- c431
- c435
- c440
- c488
