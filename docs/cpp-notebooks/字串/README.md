# 字串

前面學陣列時，我們把一排資料放在同一個變數名稱底下：

```cpp
int score[5] = {90, 80, 70, 60, 50};
```

字串其實也很像。只是它存的不是整數，而是一串字元。

例如：

```cpp
Hello
Taiwan
C++
Peter Anderson
```

在 C++ 裡面，字串有兩條路可以走：

| 寫法          | 說明                   | 適合什麼時候用               |
| ------------- | ---------------------- | ---------------------------- |
| `char` 陣列   | C 語言留下來的字串寫法 | 想理解底層、記憶體、舊程式碼 |
| `string` 類別 | C++ 更方便的字串寫法   | 大多數日常程式、競賽、專案   |

剛開始學的時候，很多人會卡在這裡：

```cpp
char name[10];
string name;
```

兩個看起來都可以存名字，但本質不太一樣。

`char name[10]` 是「準備 10 格字元空間」。  
`string name` 是「交給 C++ 幫你管理字串」。

工程上，我們通常會優先用 `string`。不過，如果你想成為軟體工程師，還是要知道 `char` 陣列怎麼運作，因為你未來看舊系統、看 C 語言 API、看嵌入式程式時，一定會遇到。

## 字串宣告：C-style 字串

C-style 字串使用 `char` 陣列存放資料。

```cpp
char str[7] = {'S', 'T', 'R', 'I', 'N', 'G', '\0'};
```

這裡最重要的是最後一個 `\0`。

`\0` 叫做「字串結束字元」。它不是數字 0，也不是字元 `'0'`，而是告訴程式：「這個字串到這裡結束」。

所以：

```cpp
char str[] = "STRING";
```

其實會被放成：

```text
S T R I N G \0
```

也就是 6 個看得到的字元，加上 1 個看不到的結束字元。

這就是為什麼 `"STRING"` 的長度是 6，但需要 7 格空間。

### Problem. 觀察字串佔用空間

```cpp
#include <iostream>
using namespace std;

int main()
{
    char str1[] = {'W', 'o', 'r', 'l', 'd', '!'};
    char str2[] = "World!";

    cout << "str1 佔用空間：" << sizeof(str1) << endl;
    cout << "str1 內容：" << str1 << endl;

    cout << "str2 佔用空間：" << sizeof(str2) << endl;
    cout << "str2 內容：" << str2 << endl;

    return 0;
}
// `str1` 沒有放 `\0`，所以 `cout` 不知道哪裡該停，就會一路往後讀，直到剛好遇到某個 `\0` 才停。這就是亂碼來源。
// `str2` 用雙引號宣告，C++ 會自動幫你補 `\0`，所以比較安全。
```

### Problem. 正確宣告 C-style 字串

```cpp

#include <iostream>
using namespace std;

int main()
{
    char word1[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
    char word2[] = "Hello";

    cout << word1 << endl;
    cout << word2 << endl;

    return 0;
}
// 用 `char` 陣列存字串時，空間要多留一格給 `\0`。
```

## 使用 getline() 讀取含空白的字串

`cin` 讀字串時，遇到空白就會停。

```cpp
string name;
cin >> name;
```

如果輸入：

```text
Peter Anderson
```

`name` 只會拿到：

```text
Peter
```

因為空白後面的 `Anderson` 會留在輸入緩衝區。

如果要讀整行，就用 `getline()`。

### Problem. getline() 讀一整行

```cpp

#include <iostream>
#include <string>
using namespace std;

int main()
{
    string sentence;

    cout << "請輸入一句話：";
    getline(cin, sentence);

    cout << "你輸入的是：" << sentence << endl;

    return 0;
}
```

### Problem. cin 與 getline() 混用問題

```cpp

#include <iostream>
#include <string>
using namespace std;

int main()
{
    int age;
    string name;

    cout << "請輸入年齡：";
    cin >> age;

    cout << "請輸入姓名：";
    getline(cin, name);

    cout << "年齡：" << age << endl;
    cout << "姓名：" << name << endl;

    return 0;
}
// 你會發現姓名還沒輸入，程式就結束了。
// 原因是 `cin >> age` 讀完數字後，Enter 仍然留在輸入緩衝區。`getline()` 看到那個 Enter，就以為自己已經讀完一整行。
// 修正方法：在 `getline()` 前加：cin.ignore();
```

### Problem. cin 與 getline() 混用問題 -- 修正版

```cpp

#include <iostream>
#include <string>
using namespace std;

int main()
{
    int age;
    string name;

    cout << "請輸入年齡：";
    cin >> age;
    cin.ignore();

    cout << "請輸入姓名：";
    getline(cin, name);

    cout << "年齡：" << age << endl;
    cout << "姓名：" << name << endl;

    return 0;
}
```

## 字串陣列

如果要存很多個名字，可以用字串陣列。

C-style 寫法會長這樣：

```cpp
char names[5][20] = {
    "John",
    "Mary",
    "Wilson",
    "Candy",
    "Allen"
};
```

這代表有 5 個字串，每個字串最多放 19 個看得到的字元，最後 1 格要留給 `\0`。

不過在 C++ 裡，通常會寫成：

```cpp
string names[5] = {
    "John",
    "Mary",
    "Wilson",
    "Candy",
    "Allen"
};
```

這樣乾淨很多。

### Problem. 輸出字串陣列

```cpp

#include <iostream>
#include <string>
using namespace std;

int main()
{
    string names[5] = {
        "John",
        "Mary",
        "Wilson",
        "Candy",
        "Allen"};

    for (int i = 0; i < 5; i++)
    {
        cout << names[i] << endl;
    }

    return 0;
}
```

### Problem. 輸入 5 位學生姓名

```cpp

#include <iostream>
#include <string>
using namespace std;

int main()
{
    string names[5];

    for (int i = 0; i < 5; i++)
    {
        cout << "請輸入第 " << i + 1 << " 位學生姓名：";
        getline(cin, names[i]);
    }

    cout << "\n學生名單如下：" << endl;

    for (int i = 0; i < 5; i++)
    {
        cout << i + 1 << ". " << names[i] << endl;
    }

    return 0;
}
```

## string 類別

`string` 是 C++ 提供的字串類別。使用它之前，要引用標頭檔：

```cpp
#include <string>
```

```cpp
// 宣告方式：
string name;
string city = "Tainan";
string message("Hello");
```

`string` 最大的好處是：你不用自己管 `\0`，也不用擔心字串長度固定死。

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // 三種宣告方式
    string name;
    string city = "Tainan";
    string message("Hello");

    // 指派字串
    name = "Kevin";

    // 輸出結果
    cout << "name = " << name << endl;
    cout << "city = " << city << endl;
    cout << "message = " << message << endl;

    return 0;
}
```

### 字串運算子

`string` 可以直接用一些運算子處理，這點比 `char` 陣列舒服很多。

| 運算子    | 功能           | 範例                   |
| --------- | -------------- | ---------------------- |
| `=`       | 指定字串       | `name = "Peter";`      |
| `+`       | 字串串接       | `full = first + last;` |
| `+=`      | 接到原字串後面 | `name += "!";`         |
| `==`      | 判斷是否相等   | `a == b`               |
| `!=`      | 判斷是否不相等 | `a != b`               |
| `<`       | 字典順序比較   | `a < b`                |
| `>`       | 字典順序比較   | `a > b`                |
| `[]`      | 取出單一字元   | `name[0]`              |
| `cin >>`  | 輸入字串       | `cin >> name;`         |
| `cout <<` | 輸出字串       | `cout << name;`        |

### Problem. 字串串接

```cpp

#include <iostream>
#include <string>
using namespace std;

int main()
{
    string firstName = "Peter";
    string lastName = "Anderson";
    string fullName;

    fullName = firstName + " " + lastName;

    cout << "全名：" << fullName << endl;

    return 0;
}
```

### Problem. 用[]讀取每個字元

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string word;

    cout << "請輸入一個單字：";
    cin >> word;

    for (int i = 0; i < word.length(); i++)
    {
        cout << "第 " << i << " 格是：" << word[i] << endl;
    }

    return 0;
}
```

### [string成員函數](./string成員函數.md)

### [練習題目](./練習題目.md)

### ZeroJudge -- 字串 (18 題)

- a021
- a022
- a040
- a042
- a044
- a095
- a147
- a148
- e024
- e051
- e128
- e156
- d186
- c258
- c260
- c265
- c268
- c269
