# const與指標

> const 修飾的是它右邊的東西。

```cpp
int* ptr;
// ptr：指標
// *ptr：指向的資料
```

因此可以把它想成：

```text
ptr -----> number
            10
```

有兩個東西可以改：

- 改資料：`*ptr = 20`
- 改指向：`ptr = &other`

```cpp
const int* ptr = &number;
// const修飾右邊的int -> int 不能動 -> 資料不能改，但指標本身可以改指向
```

```cpp
int* const ptr = &number;
// const修飾右邊的ptr -> ptr 不能動 -> 指標指向不能改，但可以藉由指標修改資料
```

```cpp
const int * const ptr
// 啥都不能動
```

```cpp
#include <iostream>

using namespace std;

int main() {
    int first = 10;
    int second = 20;

    const int* readOnly = &first;
    cout << *readOnly << '\n';
    readOnly = &second; // 可改指向

    int* const fixed = &first;
    *fixed = 99;        // 可改目標

    const int* const fixedReadOnly = &second;
    cout << *fixedReadOnly << '\n';
}
```

記憶技巧：從變數名稱往外讀。

```text
const int* p       p 可變，*p 唯讀
int* const p       p 固定，*p 可變
const int* const p p 固定，*p 唯讀
```
