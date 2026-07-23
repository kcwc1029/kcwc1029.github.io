# 指標與位址

一般變數儲存資料，指標則儲存「某個物件所在的記憶體位址」。

```text
一般變數：保存值
指標變數：保存位址
```

可以把記憶體想成一排有門牌號碼的置物櫃：

```text
變數名稱        num
記憶體位址      0x1000
儲存內容        42

指標名稱        ptr
記憶體位址      0x2000
儲存內容        0x1000  ──────> num
```

## 變數、記憶體與位址

### 使用 `&` 取得位址

```cpp
#include <iostream>

using namespace std;

int main() {
    int number = 42;
    double price = 99.5;

    // &number 代表 number 所在的記憶體位址。
    cout << "number 的值：" << number << '\n';
    cout << "number 的位址：" << &number << '\n';
    cout << "price 的值：" << price << '\n';
    cout << "price 的位址：" << &price << '\n';
}
// 位址通常以十六進位顯示，而且每次執行可能不同。程式不應依賴畫面上看到的固定地址。
```

### 位址也有型態

`&number` 的型態是 `int*`，讀作「指向 `int` 的指標」。`&price` 的型態是 `double*`。

型態告訴編譯器：

- 反參考時，要把該位置解讀成什麼資料。
- 指標移動一格時，應跨越多少位元組。
- 哪些指派與操作是合法的。

### 指標本身也是變數

指標有自己的位址與儲存空間：

```cpp
#include <iostream>

using namespace std;

int main() {
    int number = 42;
    int* ptr = &number;

    // ptr 的內容是 number 的位址；&ptr 才是 ptr 自己的位址。
    cout << "&number：" << &number << '\n';
    cout << "ptr：" << ptr << '\n';
    cout << "&ptr：" << &ptr << '\n';
}
```

## 指標的宣告、初始化與取值

### 宣告指標

```cpp
資料型態* 指標名稱;
```

```cpp
int* intPtr;
double* pricePtr;
char* charPtr;

int* first, second; // first 是指標，second 是 int
int *first, *second; // 兩者都是指標
```

### 初始化與反參考

`&` 取得位址，`*` 透過位址存取目標物件，稱為反參考（dereference）。

```cpp
#include <iostream>

using namespace std;

int main() {
    int score = 80;
    int* scorePtr = &score;

    // scorePtr 保存 score 的位址，*scorePtr 代表 score 本身。
    cout << "score：" << score << '\n';
    cout << "scorePtr：" << scorePtr << '\n';
    cout << "*scorePtr：" << *scorePtr << '\n';

    // 透過指標修改目標，score 也會同步改變。
    *scorePtr = 95;
    cout << "修改後 score：" << score << '\n';
}
```

注意 `*` 的兩種角色：

```cpp
int* ptr;  // 宣告：ptr 是指標
*ptr = 5;  // 運算：反參考 ptr
```

不要用強制轉型掩蓋不相容型態。這可能造成錯誤解讀、對齊問題與未定義行為。

### sizeof 指標

```cpp
#include <iostream>

using namespace std;

int main() {
    int number = 10;
    int* intPtr = &number;
    double* doublePtr = nullptr;

    // 指標大小與它所指向物件的大小是兩件不同的事。
    cout << "sizeof(number)：" << sizeof(number) << '\n';
    cout << "sizeof(intPtr)：" << sizeof(intPtr) << '\n';
    cout << "sizeof(doublePtr)：" << sizeof(doublePtr) << '\n';
}
```

64 位元環境中指標常見為 8 位元組，但標準未保證一定如此。

## `nullptr` 與指標安全

不知道要指向誰時，使用 `nullptr`。

`nullptr` 是 C++11 引入的空指標常值。現代 C++ 優先使用它，不使用 `NULL` 或整數 `0` 表示空指標。

```cpp
int* ptr = nullptr;
```

`nullptr` 的好處是「可明確判斷沒有目標」，不是「可以安全取值」。

## [const與指標](./const與指標.md)

## 指標與函式

### Problem. 用指標修改呼叫端資料

```cpp
#include <iostream>

using namespace std;

void swapValues(int* left, int* right) {
    // 函式需要有效且非空的指標。
    int temporary = *left;
    *left = *right;
    *right = temporary;
}

int main() {
    int first = 10;
    int second = 20;

    swapValues(&first, &second);
    cout << first << ' ' << second << '\n';
}
// 呼叫端傳入地址，函式透過地址修改原物件。
```

### Problem. 可能為空的指標參數

```cpp
#include <iostream>

using namespace std;

bool divide(int dividend, int divisor, int* result) {
    // divisor 為 0 或沒有輸出位置時，回報失敗。
    if (divisor == 0 || result == nullptr) {
        return false;
    }

    *result = dividend / divisor;
    return true;
}

int main() {
    int quotient = 0;

    if (divide(20, 4, &quotient)) {
        cout << "商：" << quotient << '\n';
    } else {
        cout << "無法計算\n";
    }
}
```

## 指標與陣列

大多數運算式中，陣列名稱會退化為指向第一個元素的指標。

```cpp
int values[5] = {10, 20, 30, 40, 50};
int* ptr = values; // 等同 &values[0]
```

```text
values      指向 values[0]
values + 1  指向 values[1]
*(values+2) 取得 values[2]
```

### Problem. 索引與指標等價

```cpp
#include <iostream>

using namespace std;

int main() {
    int values[] = {10, 20, 30, 40, 50};
    int* ptr = values;

    // arr[i] 在語意上等價於 *(arr + i)。
    for (int i = 0; i < 5; ++i) {
        cout << values[i] << ' '
             << *(values + i) << ' '
             << ptr[i] << ' '
             << *(ptr + i) << '\n';
    }
}
```

### Problem. 指標不知道陣列長度

```cpp
void print(const int* data, size_t size);
```

`data` 只保存起點，不知道結尾。函式必須另收長度，或採用「起點與終點」。

```cpp
#include <cstddef>
#include <iostream>

using namespace std;

int sum(const int* data, size_t size) {
    int result = 0;

    // data 指向第一個元素，size 決定合法範圍。
    for (size_t i = 0; i < size; ++i) {
        result += data[i];
    }
    return result;
}

int main() {
    int values[] = {3, 1, 4, 1, 5};
    cout << sum(values, 5) << '\n';
}
```

### 二維陣列的指標型態

```cpp
int matrix[3][4]{};
int (*rowPtr)[4] = matrix;
```

`rowPtr` 是「指向含有 4 個 `int` 之陣列的指標」。括號不可省略；`int* rowPtr[4]` 會變成含 4 個 `int*` 的指標陣列。

### Problem. 二維陣列指標

```cpp
#include <iostream>

using namespace std;

int main() {
    int matrix[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    int (*rowPtr)[3] = matrix;

    // 先移動到指定列，再移動到指定欄。
    for (int row = 0; row < 2; ++row) {
        for (int col = 0; col < 3; ++col) {
            cout << *(*(rowPtr + row) + col) << ' ';
        }
        cout << '\n';
    }
}
```

## 指標運算

可在同一陣列範圍內進行：

- `ptr + n`、`ptr - n`
- `++ptr`、`--ptr`
- 同陣列兩指標相減
- 比較同陣列內的位置

### Problem. 指標移動與距離

```cpp
#include <cstddef>
#include <iostream>

using namespace std;

int main() {
    int values[] = {10, 20, 30, 40, 50};
    int* first = &values[1];
    int* last = &values[4];

    // 指標相減得到元素距離，不是位元組差。
    ptrdiff_t distance = last - first;

    cout << "*first：" << *first << '\n';
    cout << "*(first + 2)：" << *(first + 2) << '\n';
    cout << "距離：" << distance << '\n';
}
```

重要限制：

- 只能在同一陣列物件及其「尾端下一格」範圍內運算。
- 尾端下一格可比較，但不可反參考。
- 不相關物件的指標相減或順序比較沒有一般可攜意義。
- 不可讓指標任意跨越記憶體。

## 多重指標

```cpp
int number = 10;
int* ptr = &number;
int** ptrToPtr = &ptr;
```

```text
ptrToPtr ──> ptr ──> number
 **ptrToPtr == 10
```

```cpp
#include <iostream>

using namespace std;

int main() {
    int number = 10;
    int* ptr = &number;
    int** ptrToPtr = &ptr;

    // 兩次反參考後才到達 number。
    **ptrToPtr = 99;
    cout << number << '\n';
}
```

## 指標陣列

```cpp
const char* names[] = {"Ada", "Bjarne", "Linus"};
// `names` 是陣列，每個元素都是 `const char*`。
```

```cpp
#include <iostream>

using namespace std;

int main() {
    const char* languages[] = {"C", "C++", "Rust", "Python"};

    // 每個元素指向一個字串常值。
    for (const char* language : languages) {
        cout << language << '\n';
    }
}
```

## 函式指標

函式也有位址，可用函式指標實作回呼（callback）。

```cpp
#include <iostream>

using namespace std;

int add(int left, int right) {
    return left + right;
}

int multiply(int left, int right) {
    return left * right;
}

int calculate(int left, int right, int (*operation)(int, int)) {
    return operation(left, right);
}

int main() {
    // operation 的型態是：接收兩個 int、回傳 int 的函式指標。
    int (*operation)(int, int) = add;
    cout << calculate(3, 4, operation) << '\n';

    operation = multiply;
    cout << calculate(3, 4, operation) << '\n';
}
```

現代 C++ 也常使用 lambda、模板或 `function`，可讀性通常更好。

## 動態記憶體與 `new`、`delete`

### new與delete

```cpp
#include <iostream>

using namespace std;

int main() {
    int* number = new int{42};

    // new 建立物件並回傳其位址。
    cout << *number << '\n';

    // 每次成功的 new 都必須有且只有一次對應 delete。
    delete number;
    number = nullptr;
}
```

### 動態陣列

```cpp
#include <cstddef>
#include <iostream>

using namespace std;

int main() {
    size_t size;
    cin >> size;

    int* values = new int[size]{};

    // values 的合法索引為 0 到 size - 1。
    for (size_t i = 0; i < size; ++i) {
        cin >> values[i];
    }

    int sum = 0;
    for (size_t i = 0; i < size; ++i) {
        sum += values[i];
    }
    cout << sum << '\n';

    // new[] 必須搭配 delete[]。
    delete[] values;
    values = nullptr;
}
```

```cpp
// 配對規則：
new T       <──> delete
new T[n]    <──> delete[]
// 不可混用，也不可重複釋放。
```

## 生命週期、所有權與常見災難

### 記憶體洩漏

```cpp
void leak() {
    int* ptr = new int{42};
    // 忘記 delete，位址離開作用域後再也無法釋放
}
```

## 補充：[RAII與智慧指標](./RAII與智慧指標.md)

### [練習題目](./練習題目.md)
