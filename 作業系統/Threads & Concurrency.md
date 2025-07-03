
執行緒（thread）是 CPU 利用的最基本單位。

每個執行緒包含以下元素：
- Thread ID：唯一識別編號
- Program Counter：程式計數器，記錄下一個執行的指令
- Register Set：暫存器組（CPU 狀態）
- Stack：堆疊（函式呼叫、區域變數）

### 0.1. 單一執行緒 vs 多執行緒

![upgit_20250702_1751458685.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751458685.png)


### 0.2. 好處（Benefits）
- 反應速度（Responsiveness）：使用者操作不中斷，程式更即時互動，例如按下按鈕還能繼續使用介面
- 資源共享（Resource Sharing）：同一個 process 中的 threads 天生就能共享資料、變數與資源
- 經濟效益（Economy）：thread 比 process 更輕便，建立與切換成本更低
- 可擴展性（Scalability）：在多核心系統上，執行緒可平行運作，效能提升更明顯


## 1. 多核心程式設計（Multicore Programming）

- Concurrency（併發）：多個任務能交錯執行，看起來同時在跑（單核心也可以達成）
- Parallelism（平行）：多個任務真的同時在跑（多核心才能實現）

![upgit_20250702_1751458853.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751458853.png)

![upgit_20250702_1751458860.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751458860.png)


### 1.1. 多核心程式設計（Multicore Programming）挑戰

- 任務分解（Identifying Tasks）：要把程式切成可以「獨立」執行的部分。
	- 理想情況：每個任務彼此獨立（無依賴），才能真正平行執行。
- 工作平衡（Balance）：各個執行緒要做「差不多份量」的事。
- 資料切分（Data Splitting）：和任務一樣，資料也要切給每個核心自己處理。
- 資料相依（Data Dependency）：如果 thread A 要用 thread B 的資料，就要「同步」
- 測試與除錯（Testing & Debugging）

### 1.2. AMDAHL’SLAW

![upgit_20250702_1751459057.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751459057.png)

- S：不能平行的部分（serial）
- N：核心數量

![upgit_20250702_1751459068.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751459068.png)


假設一個程式：
- 75% 可平行（0.75）
- 25% 必須串行執行（0.25）

如果用：
- 2 顆核心 → 最快提升 ≈ 1.6 倍
- 4 顆核心 → 最快提升 ≈ 2.28 倍
- ∞ 顆核心 → 最大速度 = 1 / 0.25 = 4 倍
- 重點：即使有 100 顆核心，若程式裡面有 25% 不能平行，最大速度也只能提升 4 倍！


## 2. 多執行緒模型（Multithreading Models）

- 使用者執行緒（User Thread）：由應用程式與**執行緒函式庫**控制，在**使用者空間中管理**
- 核心執行緒（Kernel Thread）：由**作業系統內核**直接支援與管理

### 2.1. Many-to-One 模型（多對一）

- 定義：多個使用者執行緒 → 對應到 一個 核心執行緒
- 優點：快速建立、上下文切換成本低
- 缺點：無法發揮多核心效能
- 現況：幾乎已被淘汰，因為無法發揮多核心的平行能力

![upgit_20250702_1751459305.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751459305.png)

### 2.2. One-to-One 模型（一對一）
- 定義：每個使用者執行緒 → 對應到 一個 核心執行緒
- 特徵：真正支援平行執行（可利用多核心）
- 阻塞（Blocking）不會影響其他執行緒
- 缺點：建立大量執行緒 = 建立大量核心執行緒 → 系統負擔大



![upgit_20250702_1751459323.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751459323.png)

### 2.3. Many-to-Many 模型（多對多）
- 定義：多個使用者執行緒 ↔ 映射到一群（較少或等量）核心執行緒
- 可以建立「很多使用者執行緒」，核心只處理部分執行緒（核心與效能平衡）
- 支援平行處理，不會因為一個 thread 阻塞整個 process


![upgit_20250702_1751459378.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751459378.png)


## 3. Implicit Threading（隱式多執行緒）

隨著多核心 CPU 普及，程式可能需要數百甚至上千個執行緒。為了簡化開發，隱式多執行緒（Implicit Threading）出現了。


- 傳統方式：程式設計師要明確建立、管理 thread
- 隱式方式：
	- 程式設計師只需定義「任務」（task），
	- 由系統的函式庫或編譯器自動轉成 thread 並執行

四種隱式多執行緒：

### 3.1. Thread Pool（執行緒池）

1. 預先建立一群執行緒（例如 10 個）
2. 當有任務來時 → 從池中取出 thread 來執行
3. 執行完 → 回收進池

優點
- 效率高：省去頻繁建立與銷毀 thread 的開銷
- 控制數量：可限制 thread 數，避免耗盡資源
- 彈性排程：支援延遲執行、週期執行等策略

### 3.2. Fork-Join 模型（分叉-合併）

- 適用於「分而治之」的演算法（Divide and Conquer）
- 主 thread 把工作切割成多個子任務 → fork
- 等待子任務完成 → join → 整合結果


![upgit_20250702_1751459811.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250702_1751459811.png)


### 3.3. OpenMP（適用於 C/C++/Fortran ）

只要在 for 迴圈上面加一句「魔法註解 `#pragma omp parallel for`」，編譯器就會幫你自動把迴圈切開，讓不同核心處理不同段落。

{% raw %}
```cpp
/*
假設你有 4 位工人要搬 100 箱貨物
這句話的意思就是：「請幫我自動分配這 100 箱工作，分給不同的工人（CPU 核心）一起做！」
/*
#pragma omp parallel for
for (int i = 0; i < 100; i++) {
    c[i] = a[i] + b[i];  // 每一箱做一次加法
}

```
{% endraw %}

### 3.4. Grand Central Dispatch (GCD)（Apple 專用）
GCD 是 Apple 發明的一種「任務派送中心」，你只要把任務丟到「佇列」（queue），它會幫你找空閒的核心來執行。

{% raw %}
```cpp
// 請幫我找一個空的核心，幫我執行這段任務，等一下可以印出 'This is a concurrent task.'
let queue = DispatchQueue.global(qos: .userInitiated)
queue.async {
    print("This is a concurrent task.")
}
```
{% endraw %}

GCD 中的兩種 queue：
- Serial Queue：任務一個一個來，順序執行（像排隊）
- Concurrent Queue：任務可以同時跑（像排一排人然後一起搬貨）

### 3.5. Intel TBB（Thread Building Blocks）

你只要告訴我你有一堆工作，我來幫你分配給 CPU 跑，跑得快還自動幫你調整

它是 C++ 的一個函式庫，幫你自動做平行處理。

{% raw %}
```cpp
parallel_for(size_t(0), n, [=](size_t i) {
    apply(v[i]);
});
```
{% endraw %}


## 4. 多執行緒相關問題（Threading Issues）


### 4.1. 問題01：fork() 和 exec() 的多執行緒語意

> 如果多執行緒程式中某個 thread 呼叫 fork()，那新產生的 process 是？
> - 只有那個 thread 被複製？
> - 還是所有 thread 一起被複製？

### 4.2. 問題02：Signal Handling（訊號處理）

UNIX 的 Signal 三步驟：
1. 某事件發生 → 產生 signal
2. 系統傳送 signal 到 process
3. 被指定的 signal handler 處理該 signal

Signal 類型：
- 同步（synchronous）：process 自己引發 e.g. 除以 0、存取非法記憶體
- 非同步（asynchronous）：外部事件引發 e.g. Ctrl+C、時間到期

### 4.3. 多執行緒中該把 signal 傳給誰
- 傳給觸發該 signal 的 thread
- 傳給所有 thread(如 Ctrl+C，要終止整個 process)
- 傳給部分 thread(像特定監控 thread)
- 指定某個 thread 接收全部 signal(最常見、安全設計方式)

### 4.4. 問題03：Thread Cancellation（執行緒取消）
Thread Cancellation：中斷某個正在執行的 thread（例如：搜尋完成就取消其他還在查資料的 thread）

兩種取消模式：
- 非同步（Asynchronous） (不推薦)：馬上強制終止 target thread
- 延遲（Deferred）(較安全)：target thread 自己定期檢查是否要中止

### 4.5. 問題04：Thread-Local Storage（執行緒區域儲存）

> 多個 thread 共用資料好棒棒？但有時候....有些資料要每個 thread 一份！不能共享！

TLS：每個 thread 都有自己私有的一份資料（像是自己的小白板）


### 4.6. 問題05：Scheduler Activations（排程啟動通知）

在 many-to-many 模型下，我們需要讓「使用者執行緒程式庫」和「核心」協調合作（例如：什麼時候有資源？哪個 thread block 掉？）

解法：Scheduler Activations：一種雙向溝通機制，核心透過「upcall」通知使用者程式庫重要事件，像是：
- 有 thread 要 block → 核心通知程式庫「嘿你得讓其他 thread 上場！」
- thread 回來了 → 核心說「這個 thread 可以再跑了！」





















