# RAII與智慧指標

RAII（Resource Acquisition Is Initialization）把資源生命週期綁定到物件生命週期。物件離開作用域時，解構函式自動釋放資源。

### 13.1 `unique_ptr`

表示唯一所有權，不能複製，但可以移動。

**建議檔名：`21_unique_ptr.cpp`**

```cpp
#include <iostream>
#include <memory>
#include <utility>

using namespace std;

int main() {
    unique_ptr<int> owner = make_unique<int>(42);
    cout << *owner << '\n';

    // move 將所有權交給 next，owner 之後變成空。
    unique_ptr<int> next = move(owner);

    if (!owner) {
        cout << "owner 已不再擁有物件\n";
    }
    cout << *next << '\n';
} // next 自動釋放物件
```

### 13.2 `unique_ptr` 管理物件

**建議檔名：`22_unique_ptr管理類別.cpp`**

```cpp
#include <iostream>
#include <memory>
#include <string>

using namespace std;

class Student {
public:
    Student(string name, int score)
        : name_(name), score_(score) {
    }

    void print() const {
        cout << name_ << "：" << score_ << '\n';
    }

private:
    string name_;
    int score_;
};

int main() {
    // make_unique 同時建立物件與唯一所有權。
    auto student = make_unique<Student>("小華", 90);
    student->print();
}
```

### 13.3 `shared_ptr`

多個擁有者共同延長物件生命週期，最後一位擁有者消失時才釋放。

**建議檔名：`23_shared_ptr.cpp`**

```cpp
#include <iostream>
#include <memory>

using namespace std;

int main() {
    auto first = make_shared<int>(100);
    cout << "擁有者數量：" << first.use_count() << '\n';

    {
        shared_ptr<int> second = first;
        cout << "擁有者數量：" << first.use_count() << '\n';
    }

    cout << "擁有者數量：" << first.use_count() << '\n';
}
```

不要因為「怕物件消失」就全面使用 `shared_ptr`。共享所有權較難推理，也有額外成本。所有權明確時優先 `unique_ptr`。

### 13.4 `weak_ptr` 與循環參考

兩個 `shared_ptr` 互相擁有會形成循環，引用計數永遠不會歸零。非擁有方向應使用 `weak_ptr`。

**建議檔名：`24_weak_ptr.cpp`**

```cpp
#include <iostream>
#include <memory>

using namespace std;

int main() {
    auto owner = make_shared<int>(88);
    weak_ptr<int> observer = owner;

    // lock 成功才取得暫時的 shared_ptr。
    if (auto value = observer.lock()) {
        cout << *value << '\n';
    }

    owner.reset();

    if (observer.expired()) {
        cout << "被觀察物件已不存在\n";
    }
}
```

### 13.5 `->` 成員存取

指標指向物件時：

```cpp
student->print();
```

等價於：

```cpp
(*student).print();
```

`->` 可讀性更好。
