## 1. Basic Concepts

在單核心系統中，一次只能執行一個 process，其他 process 必須等待。

為什麼需要 CPU 排程（Scheduling）？
- 讓 CPU 不要閒著：當某個程式因 I/O 卡住，就切去跑別的程式。
- 多個程式同時保留在記憶體中，讓 CPU 每次都有事情做 → 提升效能。

### 1.1. CPU–I/O Burst Cycle（爆發週期）

  每個 process 執行的模式：CPU Burst → I/O Burst → CPU Burst → I/O Burst → … 最後結束。其中：
- CPU Burst： 使用 CPU 計算的時間
- I/O Burst： 等待輸入輸出（如：讀檔案、網路請求）的時間
    
針對於CPU Burst這裡面可以細分：
- 多數是**短時間**（exponential 分布），少數是長時間
- I/O-bound 程式：很多小 CPU burst → 等 I/O
- CPU-bound 程式：少量但長 CPU burst → 不太等 I/O
    
![upgit_20250703_1751525596.png|939x655](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250703_1751525596.png)




### 1.2. **Preemptive vs Nonpreemptive Scheduling（可搶佔與不可搶佔）**

  
- Nonpreemptive（不可搶佔）： process 一旦拿到 CPU，除非自願放棄或終止，否則不會被中斷。
- Preemptive（可搶佔）： 現代 OS 幾乎都支援這種排程（像 Linux、Windows）
    


有四種情況會觸發排程決策：
1. Process 從 running → waiting（例如：要 I/O）=> 非搶佔式（Nonpreemptive）
2. Process 從 running → ready（例如：被中斷）=> 搶佔式（Preemptive）
3. Process 從 waiting → ready（I/O 完成）=> 搶佔式（Preemptive）
4. Process 結束=> 非搶佔式（Nonpreemptive）

可搶佔排程可能引發 **race condition（資料競爭）**，需要額外保護機制（像鎖或關中斷）

### 1.3. Dispatcher（派遣器）

主要功能：當 scheduler 選好了要執行的 process，dispatcher 負責交接 CPU 給它。
- 儲存舊 process 的 context 到 PCB => **還原新 process 的 context**
- 切到使用者模式
- 跳至新程式該跑的程式碼位置

**Dispatch Latency（派遣延遲）**：指一次 context switch 所花的時間

## 2. Scheduling Criteria（排程準則）

  
### 2.1. 準則01：CPU Utilization（CPU 利用率）

- 概念：CPU 的**忙碌程度**，越忙表示使用越有效率。
- 查詢方式：使用 top 指令（Linux/macOS）

### 2.2. 準則02：Throughput（吞吐量）

- 概念：每單位時間完成幾個 process。
- 越多代表系統越有效率。


### 2.3. 準則03：Turnaround Time（周轉時間）


- 概念：從程式提交到完成的整體時間
- 包含：等待時間（在 ready queue）、CPU 執行時間、I/O 處理時間
- Turnaround Time ＝ Completion Time - Arrival Time


### 2.4. 準則04：Waiting Time（等待時間）

- 概念：只算在 ready queue 裡乾等的時間    
- 不包含：執行 CPU 的時間、I/O 的時間
- 是 CPU 排程演算法的主要影響範圍

### 2.5. 準則05：Response Time（回應時間）

- 概念：從提出請求到第一次反應出現的時間
- 跟 Turnaround 不同，不是整個完成，只是開始回應（按下 Enter → 等看到第一行輸出）



## 3. Scheduling Algorithms 

CPU 排程的目的是：從 Ready Queue 中選擇一個 Process 執行。

以下演算法皆以「**單核心系統**」為基礎說明。

### 3.1. First-Come, First-Served（FCFS）

特性：
- 最簡單的排程方式，誰先來誰先跑（FIFO）。
- 非搶佔式（nonpreemptive）

缺點：**會出現 Convoy Effect（車隊效應）：長 process 擋住後面所有 process，I/O 效能浪費 

範例：

![upgit_20250704_1751566558.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751566558.png)


![upgit_20250704_1751566573.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751566573.png)

![upgit_20250704_1751566588.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751566588.png)


若順序為 P1, P2, P3：等待時間變為(0 + 24 + 27)/3 = **17ms**

若順序為 P2, P3, P1：等待時間變為 (0 + 3 + 6)/3 = **3ms**


### 3.2. Shortest-Job-First（SJF）

特性：

- 執行下一個 CPU burst 最短的 process
- 可為 **preemptive**（Shortest Remaining Time First, SRTF）或 **nonpreemptive**

優點： 最小平均等待時間（理論上最佳）

缺點： 很難準確預測 CPU burst 時間

  
範例：非搶佔 SJF
- 假設P1=6, P2=8, P3=7, P4=3
- 平均等待時間 = **7ms**

![upgit_20250704_1751566932.png|939x134](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751566932.png)


範例：搶佔 SJF


|**Process**|**Arrival**|**Burst**|
|---|---|---|
|P1|0|8|
|P2|1|4|
|P3|2|9|
|P4|3|5|

- 假設P1=6, P2=8, P3=7, P4=3
- 平均等待時間 ≈ **6.5ms**

![upgit_20250704_1751567064.png|711x103](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751567064.png)



### 3.3. Round-Robin（RR）

  特性：
- 為 FCFS 加上 搶佔（Preemption）
- 每個 process 分得一段固定的時間 → Time Quantum

範例：
- P1=24, P2=3, P3=3，time quantum = 4
- 平均等待時間 ≈ 5.66ms

![upgit_20250704_1751567228.png|939x131](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751567228.png)

  


Time Quantum 設定關鍵：
- 太大 → 變成 FCFS
- 太小 → 過多 context switch，浪費效能

### 3.4. Priority Scheduling

特性：
- 每個 process 有一個「優先順序」
- 數字越小，優先度越高

搶佔與否： 可為 preemptive 或 nonpreemptive

缺點：可能造成 **Starvation（飢餓）**：低優先程式永遠等不到
- 解法：Aging（等待越久，優先度逐漸提高）

範例：

|**Process**|**Burst**|**Priority**|
|---|---|---|
|P1|10|3|
|P2|1|1|
|P3|2|4|
|P4|1|5|
|P5|5|2|

- 執行順序：P2 → P5 → P1 → P3 → P4
- 平均等待時間 = **8.2ms**


### 3.5. Multilevel Queue Scheduling

  特性：根據「process 類型」分成多個隊列，例如：
1. Real-time processes
2. System processes
3. Interactive processes
4. Batch processes


特徵：
- 每個 queue 有**獨立的排程策略**（如前面提到的 FCFS 或 RR）
- Queue 之間的排程通常採用 **Fixed-Priority Preemptive Scheduling**  
- 低優先 queue 會被高優先 queue 抢走 CPU

可設計：每個 queue 分配不同 **CPU 時間比例**（Time Slicing）



![upgit_20250704_1751567648.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751567648.png)

![upgit_20250704_1751567669.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751567669.png)


### 3.6. Multilevel Feedback Queue Scheduling

  特性：
- 與 Multilevel Queue 最大不同 → **允許 process 在 queue 之間移動**
- 移動規則根據：
    - CPU burst 長度
    - 等待時間（防止飢餓）
        
常見設計：三層 queue：
- Queue 0（優先）: RR，quantum=8
- Queue 1：RR，quantum=16
- Queue 2：FCFS

邏輯：
- 新進程 → Queue 0
- 若跑超過 quantum，降級至下一層
- 若長時間沒被執行 → **升級（aging）**
    

 優點：
- 綜合各家排程策略優點
- 適應性強，適合**混合型系統**
    
缺點：複雜度高，參數多


![upgit_20250704_1751567759.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250704_1751567759.png)

