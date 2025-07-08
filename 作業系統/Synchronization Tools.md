## 1. Background

在現代作業系統中，processes 和 threads 通常「並發（concurrent）」或「平行（parallel）」執行。
- 並發：一顆 CPU 上切換多個 process（快速 context switch）
- 平行：多核心同時執行多個 process

❗ 多個 process 同時存取「共享資料」時，若未加控制，可能導致資料錯誤。

### 1.1. 實例說明：Producer–Consumer 問題

這段程式碼在「單執行緒」下是沒問題的，但在兩個 process 同時執行時，可能會出錯。

{% raw %}
```cpp
// Producer
while (true) {
    while (count == BUFFER_SIZE) ; // 緩衝區滿，等待
    buffer[in] = next_produced;
    in = (in + 1) % BUFFER_SIZE;
    count++;  // 加一個物品
}

// Consumer
while (true) {
    while (count == 0) ; // 緩衝區空，等待
    next_consumed = buffer[out];
    out = (out + 1) % BUFFER_SIZE;
    count--;  // 移除一個物品
}
```
{% endraw %}


原因：count++ 與 count-- 的執行其實包含多個步驟

```
count++ 可能會被 CPU 翻譯成以下三步
- register1 = count          // 把 count 值載入暫存器
- register1 = register1 + 1  // 在暫存器加一
- count = register1          // 把值寫回記憶體

count-- 也是類似的三步
- register2 = count
- register2 = register2 - 1
- count = register2
```

假設 count = 5，producer 做 count++、consumer 做 count--：
1. T0：producer: `register1 = count` → 5
2. T1：producer: `register1 = register1 + 1` → 6
3. T2：consumer: `register2 = count` → 5
4. T3：consumer: `register2 = register2 - 1` → 4
5. T4：producer: `count = register1` → count = 6
6. T5：consumer: `count = register2` → count = 4 ❌ 覆蓋前面的結果

## 2. Race Condition

定義：當兩個或多個 process 並發地存取與修改同一資料，而結果取決於它們交錯執行的順序。

解法：需要同步機制（Synchronization）
- 在某個時間內，只有一個 process 可以修改共享變數（例如 count）
- 這就是我們為什麼需要「臨界區（critical section）」、「鎖（lock）」、「信號量（semaphore）」、「mutex」、「monitor」等等同步工具的根本原因。

## 3. 臨界區問題（The Critical-Section Problem）

當一個 process 要存取「共享資料（shared data）」時，這段會修改共享資源的程式碼就稱為Critical Section（臨界區）。

在任一時刻，最多只能有一個 process 執行在 critical section 中 => 這樣才能確保資料一致、避免 race condition

### 3.1. 每個 process 的結構如下：
![upgit_20250707_1751895313.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250707_1751895313.png)

Critical Section 問題必須同時滿足三個條件：

### 3.2. 三大同步條件

| 條件                    | 說明                                           |
| --------------------- | -------------------------------------------- |
| Mutual Exclusion（互斥）  | 一次只有一個 process 可以在臨界區中（防止 race condition）    |
| Progress（進度）          | 如果沒人處於臨界區，想進入的人必須能選出其中一人進入（不能無限拖延）           |
| Bounded Waiting（有限等待） | 一個 process 等待進入臨界區的次數是有限的，不會被永遠餓著（不能 starve） |

### 3.3. kernel mode中的race condition

即使在 kernel mode，還是可能出現 race condition，像是：
- 檔案列表（open file list）
	- 兩個 process 同時開檔案 → 都要更新 open file list → 可能造成資料錯亂
- fork() 建立新 process：
	- 有個共享變數 next_available_pid（下一個可用的 process ID）→ 如果 P0 和 P1 同時呼叫 `fork()`，可能會拿到一樣的 PID
![upgit_20250707_1751895802.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250707_1751895802.png)


## 4. Peterson’s Solution（彼得森解法）

Peterson’s Solution 是一種只用軟體就能實現兩個 process 的互斥臨界區的演算法。

它是 OS 同步中的經典演算法，儘管在現代硬體上不保證正確，但它非常適合用來：
- 示範如何透過程式邏輯實現臨界區控制
- 解釋三個同步條件：Mutual Exclusion、Progress、Bounded Waiting


適用條件：僅限 兩個 process（P0 與 P1）
- Process 之間會輪流進入 critical section

{% raw %}
```cpp
// 共享兩個變數
int turn;          // 輪到誰（0 或 1）
bool flag[2];      // flag[i] 表示 Pi 想要進入臨界區

// 演算法流程（Process Pi 的程式碼）
while (true) {
    flag[i] = true;        // 宣告自己要進入 CS
    turn = j;              // 禮讓對方先選
    while (flag[j] && turn == j){} // 忍耐等待

    // 🔐 Critical Section
    ...

    flag[i] = false;       // 我執行完畢，退出 CS

    // 🧘 Remainder Section
}


state 初始：flag[0] = flag[1] = false

P0 想進入：
flag[0] = true
turn = 1

P1 想進入：
flag[1] = true
turn = 0

while 條件：
P0: flag[1] && turn==1 → ❌ 不滿足（turn = 0）
P1: flag[0] && turn==0 → ✅ 卡住

➡ P0 可以進入

```
{% endraw %}




### 4.1. 三大同步條件

| 條件                    | 說明                                     |
| --------------------- | -------------------------------------- |
| Mutual Exclusion（互斥）  | 同時最多只會有一個人成功通過 `while` 條件              |
| Progress（進度）          | 沒有 process 在 critical section 時，不會無限等待 |
| Bounded Waiting（有限等待） | 最多只會等一次對方執行完臨界區，不會無限 starve            |


## 5. Hardware Support for Synchronization（硬體支援的同步工具）

> 為什麼靠軟體實現互斥（如 Peterson's Solution）不夠安全？如何透過硬體指令來保障「原子操作」？

## 6. Memory Barriers（記憶體障壁）

一種 CPU 指令，用來 阻止編譯器或處理器對指令順序的重新排序。

它會強迫先前的讀寫操作一定要完成後，後續的操作才能開始。

### 6.1. 記憶體模型（Memory Model）：

| 類型                   | 說明                           |
| -------------------- | ---------------------------- |
| **Strongly Ordered** | 一個處理器的記憶體變化 **馬上能被其他處理器看到**。 |
| **Weakly Ordered**   | 記憶體變化可能 **不馬上可見**，會延遲更新。     |

範例：

{% raw %}
```cpp
// Thread 1
while (!flag)
    memory_barrier();  // 確保讀 flag 之前不會偷跑去讀 x
print x;
```
{% endraw %}


{% raw %}
```cpp
// Thread 2
x = 100;
memory_barrier();     // 確保 x = 100 寫入後，flag 才會設為 true
flag = true;
```
{% endraw %}


## 7. Hardware Instructions（硬體原子指令）
現代 CPU 提供兩種常見原子操作，解決同步問題：
### 7.1. test-and-set（測試並設定）

定義test-and-set：

{% raw %}
```cpp
bool test_and_set(bool* target) {
    bool rv = *target;
    *target = true;
    return rv;
}
```
{% endraw %}


使用test-and-set：（這段操作是「原子」進行，兩個核心同時執行也不會競爭失敗）

{% raw %}
```cpp
bool lock = false;

while (test_and_set(&lock)) ;  // busy-wait

// critical section
lock = false;  // 解鎖
```
{% endraw %}

### 7.2. compare-and-swap（比較並交換，CAS）
定義CAS：

{% raw %}
```cpp
int compare_and_swap(int* value, int expected, int new_value) {
    int temp = *value;
    if (*value == expected)
        *value = new_value;
    return temp;
}
```
{% endraw %}


使用CAS：（這段操作是「原子」進行，兩個核心同時執行也不會競爭失敗）

{% raw %}
```cpp
int lock = 0;

while (compare_and_swap(&lock, 0, 1) != 0) ;  // busy-wait

// critical section
lock = 0;  // 解鎖
```
{% endraw %}


然而，test-and-set跟CAS都不滿足 Bounded Waiting：
- 可能有某個 process 一直搶不到鎖（饑餓現象）。


### 7.3. 改良版 CAS：加入 waiting 陣列實現「有界等待」

保證了：每個 process 最多等待 n-1 次就可以進入 critical section。

{% raw %}
```cpp
bool waiting[n];
int lock = 0;
int key;

waiting[i] = true;
key = 1;

while (waiting[i] && key == 1)
    key = compare_and_swap(&lock, 0, 1);

waiting[i] = false;

// critical section

int j = (i + 1) % n;
while (j != i && !waiting[j]) j = (j + 1) % n;
if (j == i)
    lock = 0;
else
    waiting[j] = false;

```
{% endraw %}


## 8. Mutex Locks（互斥鎖）

硬體原子操作（test-and-set、CAS）很底層、難用、不友善於應用程式開發者

為此，作業系統提供「軟體層級」的工具 → mutex 鎖（Mutual Exclusion Lock）

情境：你想用影印機，但發現有人在用。你怎麼做？
- 你說：「好，我先去喝咖啡，等有人用完再叫我回來。」
- 這就像 Mutex，你進入睡眠狀態（block），等別人釋放鎖再喚醒你


優點：不浪費資源（你去做別的事）

缺點：喚醒需要時間（切換 context）


使用方式：

{% raw %}
```cpp
while (true) {
    acquire();        // 嘗試鎖定，若失敗就等待（忙等）
    // critical section // 共享資源的區域，只能同一時間一人進入
    release();        // 解鎖，讓其他人能進入臨界區
    // remainder section
}
```
{% endraw %}


Mutex 的實作核心：
{% raw %}
```cpp
bool available = true;

void acquire() {
    while (!available) ;  // busy-wait
    available = false;
}

void release() {
    available = true;
}

// 這樣的操作若不是原子性的，就會有競爭問題。
// 實物上的acquire() 和 release()會由CAS來實作
```
{% endraw %}

### 8.1. Contention

當很多 thread 同時搶鎖時，我們稱這種鎖為「有爭用的（contended）」

| 類型                   | 說明                                       |
| -------------------- | ---------------------------------------- |
| **uncontended lock** | 沒有人競爭，直接取得鎖                              |
| **contended lock**   | 有人搶鎖，可能會進入等待（busy-wait 或 context switch） |

### 8.2. Spinlock（自旋鎖）

因為上面 while (!available); 是一直重複檢查 → 稱為 Spinlock。

當一個執行緒無法取得鎖時，它會不斷重複嘗試（自旋），而不會讓出 CPU 控制權（不會 context switch）。

情境：你想用影印機，但發現有人在用。你怎麼做？
- 你站在影印機門口，一直看：「好了沒？好了沒？好了沒？」
- 你不去做其他事情，只是不停地看 —— 這就是 Spinlock。

優點：影印機很快用完：你立刻搶到

缺點：如果那個人很久都不出來：你站那邊啥事都做不了，浪費時間

### 8.3. Spinlock vs Mutex

| 比較項目 | Spinlock                | Mutex                   |
| ---- | ----------------------- | ----------------------- |
| 等待方式 | busy wait（不讓出 CPU）      | block（會 context switch） |
| 效率   | 鎖定時間短時快                 | 鎖定時間長時較穩定               |
| 適用場景 | 多核心、短臨界區                | 單核心、長臨界區                |
| 實作原理 | CAS / Test-and-Set + 自旋 | 系統呼叫 + 睡眠機制             |
| 資源使用 | 高（浪費 CPU）               | 低（讓出 CPU）               |

## 9. Semaphore

Semaphore 是一個整數變數 + 兩個操作（wait() 和 signal()）組成的同步工具。

核心原則：只有透過 wait() 和 signal() 可以存取這個變數，而且這兩個操作 必須原子性（atomic）

| 操作名稱        | 舊名             | 功能                         |
| ----------- | -------------- | -------------------------- |
| `wait(S)`   | P 操作（proberen） | 嘗試取得資源，若無則等待（ 試著進去，沒得進就睡覺） |
| `signal(S)` | V 操作（verhogen） | 表示釋放資源或完成某件事（通知外面的人可以進來）   |



 優點：
- 支援「資源共享」與「程序間通知」
- 可以排隊（不 busy-wait）
- 適用範圍廣：互斥、同步、資源限制都能做

限制：
- 要小心用法錯誤，可能死鎖
- wait() 和 signal() 必須確保原子性（需要底層支援）

定義：
{% raw %}
```cpp
wait(S) {
    while (S <= 0)
        ;  // busy-wait
    S--;
}

signal(S) {
    S++;
}
// 初始版本會造成 busy-wait（一直繞圈圈等資源），後面會改進。
```
{% endraw %}

### 9.1. 常見應用 1：互斥（Mutual Exclusion）（binary semaphore）
若你有一個共享區域（critical section）只允許一人使用：

{% raw %}
```cpp
semaphore mutex = 1;

wait(mutex);   // 鎖住
// critical section
signal(mutex); // 解鎖

// binary semaphore其行為就跟 mutex lock 一樣！
```
{% endraw %}

### 9.2. 常見應用 2：控制資源數量（counting semaphore）

假設你有 3 台影印機，5 個人要用：

{% raw %}
```cpp
semaphore printers = 3;

wait(printers);   // 有資源才可以用
// 使用影印機
signal(printers); // 用完歸還

// S 初始值代表「可用資源數」。
```
{% endraw %}

### 9.3. 常見應用 3：順序控制
假設你希望 P1 執行完 S1 之後，P2 才能執行 S2

{% raw %}
```cpp
semaphore sync = 0;

// P1
S1;
signal(sync);   // 表示事情做完了

// P2
wait(sync);     // 等待 P1 做完
S2;
```
{% endraw %}

### 9.4. 改進：不要再 busy-wait（用 queue 排隊）

改進方式：排隊等待，睡著（sleep），等 signal() 叫醒

{% raw %}
```cpp
wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        add this process to S->list;
        sleep();   // 睡著，讓出 CPU
    }
}


signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        P = remove a process from S->list;
        wakeup(P);   // 喚醒一個等待者
    }
}
```
{% endraw %}

## 10. Monitor

繼 mutex 和 semaphore 之後，用於解決臨界區與程序同步的一種更安全、抽象化程度更高的機制


semaphore存在的問題：

| 程式錯誤寫法                    | 問題                           |
| ------------------------- | ---------------------------- |
| `signal()` 寫在 `wait()` 前面 | 多人同時進入 critical section，違反互斥 |
| `wait()` 寫兩次              | 卡住不動，造成死結                    |
| 忘記寫 `signal()`            | 鎖永遠不會釋放，其他人無法進入              |

>  錯誤只有在特定時機出現，很難重現、很難 debug


### 10.1. Monitor 是一種「封裝資料 + 同步」的高階結構。可視為：「在高階語言裡自帶互斥鎖的同步物件」
- Monitor 是「包裹同步的空間」
- Condition 是「這個空間裡讓人等待與喚醒的機制」。


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

Monitor特點：

|特點|說明|
|---|---|
|**自動互斥**|一次只有一個程序能進入 Monitor 中的函數|
|**變數封裝**|外部無法直接存取 monitor 的內部資料，只能透過函數|
|**有條件變數 condition**|可支援 `wait()` 與 `signal()` 操作，用來讓程序等待與喚醒|


### 10.2. Condition 變數：用於等待與通知：

{% raw %}
```cpp
condition x;

x.wait();   // 進入等待，暫停自己
x.signal(); // 喚醒一個在等待 x 的 process
```
{% endraw %}

### 10.3. signal and wait vs signal and continue

![upgit_20250708_1751981562.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250708_1751981562.png)


當 A 執行 x.signal() 喚醒 B 時，兩人不能同時待在 monitor 裡，會怎麼安排？

|選項|說明|
|---|---|
|**signal-and-wait**|A 喚醒 B 之後，A 自己暫停等待|
|**signal-and-continue**|A 繼續做事，B 等待 A 離開|
|**compromise（折衷）**|A 呼叫 `signal()` 後立刻離開，B 立刻進來（常見實作方式）|



## 11. Liveness（存活性）



Liveness 意指：「在並行系統中，每一個 process（或 thread）最終都能繼續往下執行，不會卡住不動。」


換句話說，程式不能無限期地卡在某個地方。

如果發生無限等待，會違反：
- 進度條件（Progress）
- 有界等待條件（Bounded Waiting）

### 11.1. 兩種最常見的 Liveness 問題
#### 11.1.1. Deadlock（死結）
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

#### 11.1.2. Priority Inversion（優先順序反轉）

高優先權的 process 被低優先權的 process 間接阻擋了，導致高優先權 process 被拖慢，甚至失敗。

範例：
- 有三個 process：L（低）< M（中）< H（高）
- L 取得了某個資源（如 lock）
- H 想用這個資源，只好等 L
- 但 M 先跑起來，搶了 CPU 時間，讓 L 永遠沒時間釋放資源
- 導致 H 雖然是高優先權，卻被拖住

解法 → Priority Inheritance（優先權繼承）：
- L 在使用資源時，暫時繼承 H 的高優先權
- 這樣就能讓它優先完成、釋放資源，讓 H 順利執行

## 12. Bounded-Buffer Problem（有界緩衝區問題）

- Producer（生產者） 產生資料放進 buffer
- Consumer（消費者） 從 buffer 拿資料消費
- buffer 容量有限，需同步兩者避免資料遺失或競爭

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
## 13. Readers–Writers Problem（讀者寫者問題）

- 多個 Reader 可以一起讀資料，不會互相影響
- Writer 修改資料時，需要獨佔資源，不能和任何人同時進入
- 目標：讓讀者彼此不互斥，但與寫者互斥

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

## 14. Dining Philosophers Problem（哲學家進餐問題）

- 5 位哲學家，吃飯時需用左右兩隻筷子（共享資源）
- 若大家同時拿起左手的筷子，會造成死結
- 問題：死結

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




