## 1. Background





### 1.1. 虛擬記憶體的好處

| 好處                              | 說明                                           |
| --------------------------------- | ---------------------------------------------- |
| 無需受限於實體記憶體容量          | 可撰寫記憶體需求龐大的程式，簡化開發。         |
| 提高 CPU 使用率與同時執行程式數量 | 每個程式只佔用部分記憶體，能同時執行更多程式。 |
| 減少 I/O 操作，加速程式執行       | 無須頻繁讀寫整個程式，加快載入與切換速度。     |

![upgit_20250712_1752323177.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752323177.png)

程式看到的是完整的虛擬地址空間，作業系統與硬體（MMU）會將這些虛擬頁面對應到實體頁框。

### 1.2. 虛擬地址空間（Virtual Address Space）

![upgit_20250712_1752323559.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752323559.png)

### 1.3. 虛擬記憶體支援的共享功能

系統程式庫（如 C 標準庫）可被不同程式共享

程式間也可透過共享記憶體區段（如 mmap()）共享資料。

fork() 呼叫後，子行程會共享父行程的部分頁面，提升建立效率。

![upgit_20250712_1752323647.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752323647.png)

## 2. Demand Paging（需求分頁）

定義：Demand Paging 是一種只在程式執行過程中「需要」用到某頁（Page）時，才將該頁載入實體記憶體的技術。

特性：

| 特性                  | 說明                                                            |
| --------------------- | --------------------------------------------------------------- |
| 延遲加載（Lazy Load） | 程式初始時不載入所有頁面，只有當程式真正「存取」該頁時才載入。  |
| 減少記憶體浪費        | 沒用到的頁永遠不會載入，節省記憶體資源。                        |
| 借助硬體支援          | 透過 **valid-invalid bit（有效位元）** 判斷頁面是否在記憶體中。 |

![upgit_20250712_1752324575.png|598x610](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752324575.png)

### 2.1. 分頁錯誤處理流程（Page Fault Handling）

> 此機制稱為 pure demand paging：初始時不載入任何頁，完全依需求加載。

1. 當程式試圖存取尚未載入的頁時，會觸發 Page Fault（分頁錯誤），由作業系統處理：
2. 陷入（trap）作業系統。
3. 作業系統檢查該記憶體存取是否合法。
    - 若非法 → 終止程序。
    - 若合法但尚未載入 → 繼續以下步驟。
4. 從「自由框架清單（Free Frame List）」中找出一個空閒 frame。
5. 從磁碟（通常是 swap 空間或檔案系統）載入該頁。
6. 更新頁表與內部表格（將 invalid 改成 valid）。
7. 重新執行原本中斷的指令（可從同一位置繼續執行）。

![upgit_20250712_1752325442.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752325442.png)

### 2.2. 指令重啟挑戰與處理方法

例子：三地址指令 `ADD A, B → C`

1. 取出與解碼指令
2. 取出 A
3. 取出 B
4. 相加
5. 寫入 C

若在 C 不在記憶體 → Page Fault

複雜情況：例如 MVC（Move Character）指令

-   會搬移大區塊記憶體，若中途頁錯會導致搬移「一半」。
-   解法：
    -   預先存取所有頁 → 若會出錯先讓頁錯發生。
    -   用暫存區保留原資料 → 若頁錯就回復再重來。

### 2.3. Free-Frame List

當有 page fault 發生，我們就必須：

1. 從硬碟（或其他二級儲存）把資料載入記憶體。
2. 但不能亂放，要放到一個「空抽屜」。
3. 所以就要去 Free-Frame List 裡面撈一格出來用。

框架配置時進行「zero-fill-on-demand」清除記憶體（避免資料洩漏風險）。

如果 Free-Frame List 沒空格了 → Page Replacement（頁面替換）

![upgit_20250712_1752326181.png|524x98](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752326181.png)

## 3. Page Replacement（頁面替換）

Page Replacement（頁面替換） 是指在發生 page fault 而記憶體中已無空 frame 時，必須選擇一個現有的 page 將其淘汰，騰出空間來載入需要的 page。

當 沒有空的 frame 可用時，我們就需要「換掉一頁」，把需要的頁換進來。

頁面替換處理步驟：

1. 發生 page fault。
2. 查詢 secondary storage（例如硬碟）中該頁面的位置。
3. 若有空 frame → 直接載入即可。
4. 若沒有空 frame →
    - 使用 頁面替換演算法（replacement algorithm） 選出 Victim Page（受害者頁）。
    - 若該頁已修改（dirty bit=1） → 先寫回硬碟（Swap Out）。
5. 更新 page table。
6. 恢復中斷指令並繼續執行。

![upgit_20250712_1752327017.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752327017.png)

![upgit_20250712_1752327040.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250712_1752327040.png)

### 3.1. 使用 Dirty Bit（Modify Bit）來優化 I/O：

| 狀況           | 操作                                      |
| -------------- | ----------------------------------------- |
| Modify Bit = 0 | 表示該頁未被改寫 → 可以直接捨棄，不用寫回 |
| Modify Bit = 1 | 表示有改寫 → 需先寫回 swap space 再釋放   |

## 4. 常見的頁面替換演算法

### 4.1. FIFO（First-In-First-Out）

最早載入的 page 最先被替換。

簡單但不聰明，可能把常用頁換掉。

容易出現 Belady's anomaly（增加 frame 反而 page fault 增加）。

![upgit_20250719_1752904756.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752904756.png)

![upgit_20250719_1752904833.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752904833.png)

![upgit_20250719_1752904777.png|582x376](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752904777.png)

### 4.2. Optimal Page Replacemen

換掉「未來最久不會用到的 page」

是理論上最少 page fault 的最佳演算法。

無法實作（需預知未來），僅作為比較標準。

![upgit_20250719_1752904848.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752904848.png)

### 4.3. LRU（Least Recently Used）

換掉「最久沒被使用的 page」。

是 OPT 的實際近似解。

實作困難，需要額外硬體支援（記錄最近使用時間）。

實作方法：

-   計數器法（counter）：每次 memory access 更新 time stamp。
-   堆疊法（stack）：最近用的 page 放頂端，最久未用放底層（使用雙向鏈結串列）。

![upgit_20250719_1752904880.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752904880.png)

![upgit_20250719_1752904894.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752904894.png)

### 4.4. LRU Approximation

由於 LRU 太耗資源，實務上使用近似 LRU 的方法：

#### 4.4.1. Reference Bit（參考位元）

每個 page 有一個參考位元（由硬體設定），有被訪問過設為 1。

無法得知時間順序，但可判斷是否被使用。

#### 4.4.2. Additional-Reference-Bits Algorithm

每隔一段時間（如 100ms），將 reference bit shift 到 8-bit register。

越小的值代表越久沒使用。

可看成 page 使用的時間序列紀錄。

#### 4.4.3. Second-Chance Algorithm（Clock Algorithm）

基於 FIFO，但加入參考位元判斷。

若 reference bit = 1 → 不替換，給它第二次機會並清為 0。

像時鐘一樣繞一圈，直到找到 reference bit = 0 為止。

## 5. Frame Allocation（框架分配）

系統記憶體被分為許多固定大小的「frame」（頁框），每個程式被分成「page」（頁面）。

問題： 如果有 m 個 frame，如何把它們分配給 n 個程式？

通常作業系統會預留一些 frame 給自己，其餘供使用者程序分配。

如果系統有 128 個 frame，其中 OS 使用 35 個，剩下 93 個可以給使用者程序使用。

### 5.1. 最小 frame 數量限制（Minimum Number of Frames）

為了讓一條指令可以執行完成，每個程序需要至少幾個 frame。

根據架構不同而異，例子：
一條 load 指令可能需要：
- 1 frame 放指令
- 1 frame 放資料
- 1 frame 放間接參考 → 共 3 個 frame

電腦架構會定義每個程序最少需要的 frame 數量，不能低於這個數。

## 6. Thrashing（抖動）

當系統為某個程序分配的 page frame 數量太少，不足以容納它當前正在使用的所有頁面（locality），就會發生：

1. 頁面不斷被替換出去
2. 下一條指令馬上又需要剛剛被替換出去的頁面 → 再次 page fault。
3. 不斷 page-in 與 page-out，程式花大量時間在 I/O，而不是執行。

當程序花費更多時間在分頁（paging）而不是執行真正的指令，稱為 thrashing（抖動）。



### 6.1. Thrashing 的成因：系統誤以為 CPU 利用率低，增加多工處理數量

1. 系統偵測到 CPU 利用率下降 → 嘗試「新增程序」以提升利用率。
2. 新程序加入 → 分掉原本就不足的 frame。
3. 所有程序都因記憶體不足而產生大量 page fault。
4. Page fault → 需要 I/O → 程序等待 → CPU idle 更久。
5. 系統錯誤地再新增更多程序（想解決 idle 問題）。
6. 最終結果是系統進入「thrashing」狀態，效率崩潰。

![upgit_20250719_1752916009.png|500x338](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752916009.png)

### 6.2. Page-Fault Frequency (PFF) 策略

直接以「page-fault rate」作為控制參數。

設定一個上限與下限，若超出上限 → 加 frame，低於下限 → 減 frame。

![upgit_20250719_1752916076.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250719_1752916076.png)

優點：
- 更直接、更簡潔。
- 避免需要複雜的 working set 計算與紀錄。


## 7. Memory Compression（記憶體壓縮）

當系統記憶體不足時，將多個頁面壓縮後存進一個 frame 中，而非直接 swap 到磁碟。

傳統分頁與壓縮比較：

|項目|傳統分頁|記憶體壓縮|
|---|---|---|
|作法|將 page 寫到磁碟 (swap)|將 page 壓縮後保留在 RAM|
|效能|慢（I/O 成本高）|較快（壓縮成本低於 I/O）|
|適用場景|桌面系統、傳統伺服器|手機、筆電、現代 OS|

## 8. Prepaging（預先載入）

問題：初次啟動一個程式時，會產生大量 page fault，因為沒有頁面在記憶體中。

解法：Prepaging
- 在程式開始或恢復時，預先將可能會用到的頁面載入記憶體。

### 8.1. 成本 vs. 效益分析：

- 假設載入 `s` 頁，有 `α` 比例實際被使用：
    - 成本 = 載入沒用到的頁 `s*(1–α)`
    - 效益 = 避免 `s*α` 次 page fault
    - 若 `α → 1` → 預載效益高；`α → 0` → 預載浪費資源。

## 9. Page Size（頁面大小）

|考量因素|小頁面較佳|大頁面較佳|
|---|---|---|
|Page table 大小|❌ 增加|✅ 減少|
|Internal fragmentation|✅ 減少浪費|❌ 增加浪費|
|I/O 傳輸效率|❌ 較慢|✅ 較快|
|Locality 精準度|✅ 提高|❌ 降低|
|Page fault 次數|❌ 增加|✅ 減少|

