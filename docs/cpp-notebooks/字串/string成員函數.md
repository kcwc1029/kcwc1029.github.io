`string` 除了可以用運算子，也有很多好用的成員函數。

| 函數        | 功能             | 範例                    |
| ----------- | ---------------- | ----------------------- |
| `length()`  | 取得字串長度     | `s.length()`            |
| `size()`    | 取得字串長度     | `s.size()`              |
| `empty()`   | 判斷是否為空字串 | `s.empty()`             |
| `find()`    | 尋找子字串       | `s.find("abc")`         |
| `substr()`  | 擷取子字串       | `s.substr(0, 3)`        |
| `append()`  | 接上字串         | `s.append("abc")`       |
| `insert()`  | 插入字串         | `s.insert(2, "xx")`     |
| `erase()`   | 刪除字串         | `s.erase(1, 3)`         |
| `replace()` | 取代字串         | `s.replace(0, 3, "Hi")` |
| `at()`      | 取得指定位置字元 | `s.at(0)`               |

以下都依照你的教材風格，採用 **`### Problem.` + 完整程式**，難度維持初學者程度。

### Problem. length() 取得長度 -- 計算字串有幾個字元

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string text;

    cout << "請輸入一段文字：";
    cin >> text;

    cout << "字串長度：" << text.length() << endl;

    return 0;
}
```

### Problem. find() 尋找字串 -- 判斷是否包含指定文字

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string sentence;

    cout << "請輸入一句話：";
    getline(cin, sentence);

    if (sentence.find("AI") != string::npos)
    {
        cout << "找到 AI！" << endl;
    }
    else
    {
        cout << "沒有找到 AI。" << endl;
    }

    return 0;
}
```

### Problem. substr() 擷取字串 -- 擷取前四個字元

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string id;

    cout << "請輸入學號：";
    cin >> id;

    cout << "前四個字元：" << id.substr(0, 4) << endl;

    return 0;
}
```

### Problem. append() 與 += -- 將兩個字串接在一起

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string first = "Hello";
    string second = " World";

    first.append(second);

    cout << first << endl;

    first += "!!!";

    cout << first << endl;

    return 0;
}
```

### Problem. insert() 插入字串 -- 在指定位置插入文字

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string text = "Helo";

    text.insert(2, "l");

    cout << text << endl;

    return 0;
}
```

### Problem. erase() 刪除字串 -- 刪除指定範圍的文字

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string text = "Hello World";

    text.erase(5, 1);

    cout << text << endl;

    return 0;
}
```

### Problem. replace() 取代字串 -- 將指定文字換成新的文字

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string text = "I like Java";

    text.replace(7, 4, "C++");

    cout << text << endl;

    return 0;
}
```

### Problem. 反轉字串 -- 將輸入的字串反轉

```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main()
{
    string word;

    cout << "請輸入一個單字：";
    cin >> word;

    reverse(word.begin(), word.end());

    cout << "反轉後：" << word << endl;

    return 0;
}
```

### Problem. 簡單關鍵字過濾 -- 判斷是否包含禁止字詞

```cpp
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string message;

    cout << "請輸入留言：";
    getline(cin, message);

    if (message.find("垃圾") != string::npos)
    {
        cout << "偵測到禁止字詞！" << endl;
    }
    else
    {
        cout << "留言正常。" << endl;
    }

    return 0;
}
```
