## 1. 系統模型（System Model）

一個作業系統包含「有限數量」的資源，要分配給「多個執行緒（threads）」使用。

資源可能會分成幾種類型（resource types），每種類型內有數個相同的實例（instances）。

-   如果同一類資源內部的實例不完全相同，那就代表資源分類不正確

| 資源類型       | 實例數量   | 說明                |
| -------------- | ---------- | ------------------- |
| CPU            | 4 顆       | 有 4 個可用的處理器 |
| 網路卡         | 2 個       | 有兩張網路介面卡    |
| 檔案、I/O 裝置 | 視系統而定 | DVD、硬碟、音效卡等 |

每個鎖通常對應一個特定的資料結構（如佇列、串列等），所以系統會將「每個鎖視為獨立的資源類別」。

### 1.1. 資源使用的流程

每個執行緒使用資源必須遵循：Request → Use → Release

-   Request（請求）：執行緒向系統請求資源。若該資源已被其他執行緒占用，則該執行緒會進入等待狀態。
-   Use（使用）：成功獲得資源後，執行緒可以操作它（例如進入 critical section）。
-   Release（釋放）：使用完畢後，執行緒必須歸還該資源。

## 2. 多執行緒程式中的死結 (Deadlock in Multithreaded Applications)

以 POSIX 的 mutex 鎖（pthread）為例：

-   pthread_mutex_t 是 POSIX 標準的互斥鎖。
-   初始化：pthread_mutex_init(&mutex, NULL)
-   鎖住：pthread_mutex_lock(&mutex)
-   解鎖：pthread_mutex_unlock(&mutex)

### 2.1. 範例：Deadlock Example

{% raw %}

```cpp
// 建立了兩把鎖 first_mutex 和 second_mutex
pthread_mutex_t first_mutex;
pthread_mutex_t second_mutex;

// 建立兩個執行緒 thread_one 和 thread_two
pthread_mutex_init(&first_mutex, NULL);
pthread_mutex_init(&second_mutex, NULL);

// 執行緒函數：
// 執行緒一
void *do_work_one(void *param) {
    pthread_mutex_lock(&first_mutex);       // 鎖住第一把鎖
    pthread_mutex_lock(&second_mutex);      // 嘗試鎖住第二把鎖
    // 做一些工作...
    pthread_mutex_unlock(&second_mutex);    // 釋放第二把鎖
    pthread_mutex_unlock(&first_mutex);     // 釋放第一把鎖
    pthread_exit(0);
}

// 執行緒二
void *do_work_two(void *param) {
    pthread_mutex_lock(&second_mutex);      // 鎖住第二把鎖
    pthread_mutex_lock(&first_mutex);       // 嘗試鎖住第一把鎖
    // 做一些工作...
    pthread_mutex_unlock(&first_mutex);     // 釋放第一把鎖
    pthread_mutex_unlock(&second_mutex);    // 釋放第二把鎖
    pthread_exit(0);
}
```

{% endraw %}

如果發生以下情況，會造成死結（Deadlock）：

-   thread_one 成功鎖住 first_mutex
-   thread_two 成功鎖住 second_mutex
-   兩者都在等待對方的鎖 → 永遠卡住不動。

為何這種死結難以偵測？因為它不是每次都會發生，而是要在某個特定的排程時機（scheduling timing）下才會產生。

![upgit_20250709_1752056381.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752056381.png)

### 2.2. 活結（Livelock）

活結與死結類似，都會讓執行緒無法繼續執行。差別是：

-   死結：執行緒被「阻塞」住，完全卡死。
-   活結：執行緒還在「跑」，但一直重試同一個失敗的動作，沒有實質進展。

{% raw %}

```cpp
if (pthread_mutex_trylock(&second_mutex) != 0) {
    pthread_mutex_unlock(&first_mutex);  // 嘗試失敗就放棄再重試
    continue;
}

// pthread_mutex_trylock不會阻塞，而是馬上回傳：
// - 成功就鎖住
// - 失敗就回傳錯誤值
```

{% endraw %}

活結的發生流程：

1. thread_one 鎖住 first_mutex
2. thread_two 鎖住 second_mutex
   然後：
3. thread_one 嘗試 trylock(second_mutex) → 失敗 → 解鎖 first_mutex → 重試
4. thread_two 嘗試 trylock(first_mutex) → 失敗 → 解鎖 second_mutex → 重試
   他們彼此一直重試又碰撞，就像走廊中兩人互相閃避卻擋住對方。

活結的解法：在重試之間加入隨機延遲（random backoff）來避免無限碰撞。

## 3. 死結的四個必要條件(Necessary Conditions)

如果同時滿足以下四個條件，系統就可能發生死結（Deadlock）：

| 條件名稱                    | 說明                                                                       |
| --------------------------- | -------------------------------------------------------------------------- |
| 互斥（Mutual Exclusion）    | 資源**一次只能被一個執行緒佔用**，不可共享。例如：鎖。                     |
| 保持並等待（Hold and Wait） | 執行緒持有一部分資源的同時，還在**等待其他資源**。                         |
| 不可搶佔（No Preemption）   | 資源**不能被強制奪回**，只能由持有者主動釋放。                             |
| 循環等待（Circular Wait）   | 存在一個執行緒集合 `{T0, T1, ..., Tn}`，彼此**環狀等待對方所持有的資源**。 |

### 3.1. 資源配置圖（Resource-Allocation Graph，RAG）

資源配置圖是一種用來可視化死結情況的有向圖，圖中的循環可以幫助我們判斷是否有死結。

|             |                                                                |
| ----------- | -------------------------------------------------------------- |
| 執行緒 Ti   | 圓圈表示                                                       |
| 資源類型 Rj | 用矩形表示                                                     |
| `Ti → Rj`   | **請求邊（Request Edge）**，表示執行緒 Ti 正在等待 Rj          |
| `Rj → Ti`   | **分配邊（Assignment Edge）**，表示資源 Rj 的某個實例分配給 Ti |

### 3.2. 範例說明：Figure 8.4

執行緒集合：T = {T1, T2, T3}

資源集合：R = {R1, R2, R3, R4}

資源實例數量：

-   R1、R3 各有 1 個
-   R2 有 2 個
-   R4 有 3 個

資源配置情形：

-   T1：擁有 R2，等待 R1
-   T2：擁有 R1 和 R2，等待 R3
-   T3：擁有 R3

![upgit_20250709_1752056395.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752056395.png)

若此時 T3 又請求 R2，但沒資源，就新增 T3 → R2 請求邊 → 死結就形成了（如 Figure 8.5）

![upgit_20250709_1752056489.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752056489.png)

無死結的循環案例（Figure 8.6）

-   圖中有循環 T1 → R1 → T3 → R2 → T1
-   但：T4 正在使用 R2，有可能釋放 R2，解開循環
-   結論：雖然有循環，但沒有死結

![upgit_20250709_1752056662.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752056662.png)

## 4. 死結預防（Deadlock Prevention）

死結的四個必要條件：

1. Mutual Exclusion（互斥）
2. Hold and Wait（保有並等待）
3. No Preemption（不可搶佔）
4. Circular Wait（循環等待）

### 4.1. 互斥（Mutual Exclusion）

若資源是可共用的，就不需要鎖定，也不會產生死結

可行度：

-   可共用：如唯讀檔案（read-only file），多個執行緒可以同時讀取。
-   但大多數資源（如 mutex、I/O 裝置）是天生不可共用的，因此這條通常無法被破壞。

### 4.2. 保有並等待（Hold and Wait）

方法一（全部一次請完）：

-   規定執行緒必須在開始執行前，一次請求全部資源。
-   如果有任何資源還沒拿到，就不能開始。

方法二（只能在沒持有時請求）：

-   如果一個程式已經持有某些資源，它不能直接再要求新資源
-   如果它真的想請求新的，就必須先把目前拿到的資源釋放掉。

問題：

-   資源利用率低（可能先佔著不用）
-   容易飢餓（一直請不到一整組資源）

### 4.3. 不可搶佔（No Preemption）

預防方法：若某個執行緒請求的資源無法立即取得，則把它持有的資源通通搶回來（preempted），讓它重新排隊。

類似機制：被搶回的資源會加入等待佇列，執行緒等到它原本的資源與新請求的資源全部都能取得時才繼續執行。

限制：

-   ✅ 適用於可保存狀態的資源（如 CPU 資源、資料庫交易）
-   ❌ 不適用於 mutex、semaphore（狀態難保存、難回復）

### 4.4. 循環等待（Circular Wait）

解法：資源編號 + 遞增順序請求

-   先給所有資源設定一個「唯一整數編號」F(Ri)。
-   規定執行緒請求資源時只能照編號遞增順序請求：
-   若要請 Rj，必須釋放所有 Ri 且 F(Ri) ≥ F(Rj)
    -   可以先請 R1 再請 R5，但不能先請 R5 再請 R1。

## 5. Deadlock Avoidance

與其像 Deadlock Prevention 一開始就限制資源請求方式，Deadlock Avoidance 的策略是：在執行緒每次請求資源時，動態判斷分配這筆資源會不會導致未來進入死結。

### 5.1. Safe State（安全狀態）

安全狀態（safe state）代表：存在一個執行緒的順序 <T1, T2, ..., Tn>，讓每個執行緒在資源可用時最終都能成功完成並釋放資源。

![upgit_20250709_1752066375.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752066375.png)

安全狀態 ≠ 死結狀態

-   安全 → 絕不會死結
-   不安全 → 不一定死結，但有可能進入死結
-   死結狀態 → 已經死結，是不安全狀態的一種

相關演算法

-   資源配置圖演算法（只有一個資源實例時可用）
-   銀行家演算法（Banker’s Algorithm）
-   安全狀態演算法（Safety Algorithm）

## 6. 死結復原(Recovery from Deadlock

### 6.1. 方法 01：終止程序（Process Termination）

#### 6.1.1. 終止方式 01：全部終止

-   把所有死結相關的執行緒都終止。
-   ✅ 簡單有效，一定會解除死結
-   ❌ 缺點：計算結果全丟失，損失很大。

#### 6.1.2. 終止方式 02：逐一終止（partial termination）

-   一次只殺掉一個執行緒，並每次都重新檢查是否還有死結。
-   ✅ 節省資源損失
-   ❌ 缺點：檢查次數多，效率差

#### 6.1.3. 執行緒選擇策略（誰該被終止？）

這屬於 policy decision（策略判斷），可依下列因素選擇成本最低的受害者：

| 考慮因素                    | 說明                               |
| --------------------------- | ---------------------------------- |
| 1️⃣ 優先權                   | 優先權低者優先終止                 |
| 2️⃣ 已經執行多久？還剩多久？ | 越早終止代價越小                   |
| 3️⃣ 佔用了多少資源？         | 資源越多 → 成本越高                |
| 4️⃣ 還需要多少資源？         | 需求大者可能更難完成任務           |
| 5️⃣ 需要終止多少人？         | 若終止一人即可解決，最好別動太多人 |

### 6.2. 方法 02：Resource Preemption（資源搶回）

這是另一種選擇：不殺執行緒，而是搶資源

三個關鍵問題：

#### 6.2.1. 選擇受害者（Select a victim）

-   要決定從誰那裡搶哪些資源。
-   依照成本考量，選擇「損失最小」的犧牲者。

#### 6.2.2. 回滾（Rollback）

搶走資源後，該執行緒不能繼續跑，必須回到某個安全狀態（Safe State）重來。

-   ✅ 最簡方法：完全重啟該執行緒
-   ✅ 進階做法：只回滾到「剛好打破死結的地方」，但需儲存更多狀態資訊

#### 6.2.3. 避免飢餓（Avoid Starvation）

若一直搶某個執行緒的資源，它可能永遠無法完成工作 ⇒ 飢餓（Starvation）

-   解法：限制該執行緒被選為犧牲者的次數（例如：超過 3 次就優先保護它）
