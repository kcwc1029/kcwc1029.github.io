
## 1. Monitor

繼 mutex 和 semaphore 之後，用於解決臨界區與程序同步的一種更安全、抽象化程度更高的機制

semaphore 存在的問題：

| 程式錯誤寫法                  | 問題                                    |
| ----------------------------- | --------------------------------------- |
| `signal()` 寫在 `wait()` 前面 | 多人同時進入 critical section，違反互斥 |
| `wait()` 寫兩次               | 卡住不動，造成死結                      |
| 忘記寫 `signal()`             | 鎖永遠不會釋放，其他人無法進入          |

> 錯誤只有在特定時機出現，很難重現、很難 debug

### 1.1. Monitor 是一種「封裝資料 + 同步」的高階結構。可視為：「在高階語言裡自帶互斥鎖的同步物件」

-   Monitor 是「包裹同步的空間」
-   Condition 是「這個空間裡讓人等待與喚醒的機制」。

![upgit_20250708_1751981313.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250708_1751981313.png)

{% raw %}

```cpp
monitor MonitorName {
    // 共享資料
    // 只允許一人進入的函數（自帶鎖）

    void function1(...) { ... }  // 自動加鎖
    void function2(...) { ... }  // 自動加鎖

    initialization() { ... }
}
```

{% endraw %}

Monitor 特點：

| 特點                     | 說明                                                     |
| ------------------------ | -------------------------------------------------------- |
| **自動互斥**             | 一次只有一個程序能進入 Monitor 中的函數                  |
| **變數封裝**             | 外部無法直接存取 monitor 的內部資料，只能透過函數        |
| **有條件變數 condition** | 可支援 `wait()` 與 `signal()` 操作，用來讓程序等待與喚醒 |

### 1.2. Condition 變數：用於等待與通知：

{% raw %}

```cpp
condition x;

x.wait();   // 進入等待，暫停自己
x.signal(); // 喚醒一個在等待 x 的 process
```

{% endraw %}

### 1.3. signal and wait vs signal and continue

![upgit_20250708_1751981562.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250708_1751981562.png)

當 A 執行 x.signal() 喚醒 B 時，兩人不能同時待在 monitor 裡，會怎麼安排？

| 選項                    | 說明                                                     |
| ----------------------- | -------------------------------------------------------- |
| **signal-and-wait**     | A 喚醒 B 之後，A 自己暫停等待                            |
| **signal-and-continue** | A 繼續做事，B 等待 A 離開                                |
| **compromise（折衷）**  | A 呼叫 `signal()` 後立刻離開，B 立刻進來（常見實作方式） |

## 2. Liveness（存活性）

Liveness 意指：「在並行系統中，每一個 process（或 thread）最終都能繼續往下執行，不會卡住不動。」

換句話說，程式不能無限期地卡在某個地方。

如果發生無限等待，會違反：

-   進度條件（Progress）
-   有界等待條件（Bounded Waiting）

### 2.1. 兩種最常見的 Liveness 問題

#### 2.1.1. Deadlock（死結）

所有程序彼此互相等待，沒有人能繼續執行下去。

{% raw %}

```cpp
// P0
wait(S);
wait(Q);

// P1
wait(Q);
wait(S);

// 若：
// P0 拿到 S，P1 拿到 Q，接下來都等對方釋放另一個
// 就形成死結：兩人卡住，互等不放，永遠無法完成工作
```

{% endraw %}

#### 2.1.2. Priority Inversion（優先順序反轉）

高優先權的 process 被低優先權的 process 間接阻擋了，導致高優先權 process 被拖慢，甚至失敗。

範例：

-   有三個 process：L（低）< M（中）< H（高）
-   L 取得了某個資源（如 lock）
-   H 想用這個資源，只好等 L
-   但 M 先跑起來，搶了 CPU 時間，讓 L 永遠沒時間釋放資源
-   導致 H 雖然是高優先權，卻被拖住

解法 → Priority Inheritance（優先權繼承）：

-   L 在使用資源時，暫時繼承 H 的高優先權
-   這樣就能讓它優先完成、釋放資源，讓 H 順利執行

## 3. Bounded-Buffer Problem（有界緩衝區問題）

-   Producer（生產者） 產生資料放進 buffer
-   Consumer（消費者） 從 buffer 拿資料消費
-   buffer 容量有限，需同步兩者避免資料遺失或競爭

使用三個 semaphore：

{% raw %}

```cpp
semaphore mutex = 1;   // 保護 buffer（互斥存取）
semaphore empty = n;   // 可用空格數（初始 n）
semaphore full = 0;    // 已使用格數（初始 0）
```

{% endraw %}

Producer 程式碼：

{% raw %}

```cpp
while (true) {
    produce_item();
    wait(empty);         // 等 buffer 有空間
    wait(mutex);         // 互斥存取
    add_to_buffer();
    signal(mutex);
    signal(full);        // 增加使用格數
}
```

{% endraw %}

Consumer 程式碼：

{% raw %}

```cpp
while (true) {
    wait(full);          // 等 buffer 有資料
    wait(mutex);         // 互斥存取
    remove_from_buffer();
    signal(mutex);
    signal(empty);       // 增加空格
    consume_item();
}
```

{% endraw %}

## 4. Readers–Writers Problem（讀者寫者問題）

-   多個 Reader 可以一起讀資料，不會互相影響
-   Writer 修改資料時，需要獨佔資源，不能和任何人同時進入
-   目標：讓讀者彼此不互斥，但與寫者互斥

變數與 semaphore：

{% raw %}

```cpp
int read_count = 0;
semaphore mutex = 1;      // 保護 read_count
semaphore rw_mutex = 1;   // 保護共享資料（互斥寫入）
```

{% endraw %}

Reader 程式碼：

{% raw %}

```cpp
wait(mutex);
read_count++;
if (read_count == 1)
    wait(rw_mutex);   // 第一個讀者鎖住寫者
signal(mutex);

read_data();

wait(mutex);
read_count--;
if (read_count == 0)
    signal(rw_mutex); // 最後一個讀者釋放寫者鎖
signal(mutex);
```

{% endraw %}

Writer 程式碼：

{% raw %}

```cpp
wait(rw_mutex);
write_data();
signal(rw_mutex);
```

{% endraw %}

## 5. Dining Philosophers Problem（哲學家進餐問題）

-   5 位哲學家，吃飯時需用左右兩隻筷子（共享資源）
-   若大家同時拿起左手的筷子，會造成死結
-   問題：死結

{% raw %}

```cpp
semaphore chopstick[5]; // 每隻筷子代表一個 semaphore

// 每位哲學家
while (true) {
    wait(chopstick[i]);
    wait(chopstick[(i+1)%5]);
    eat();
    signal(chopstick[i]);
    signal(chopstick[(i+1)%5]);
    think();
}
```

{% endraw %}
