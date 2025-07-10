## 1. Background

記憶體是電腦系統的核心，CPU 要從記憶體抓指令與資料。

執行指令流程如下：

1. **從記憶體抓指令**
2. **解碼**
3. **抓取操作數**
4. **執行後可能寫回記憶體**

CPU 只能直接操作暫存器與主記憶體（不能直接操作硬碟）。

主記憶體存取速度慢 → 引入 快取 (Cache) 來加速。

### 1.1. Basic Hardware（基本硬體與保護機制）

每個 CPU 只能直接操作暫存器和主記憶體（例如寄存器的速度通常為一個 CPU 時脈週期）。

若主記憶體資料尚未完成存取，CPU 會「停滯（stall）」，除非使用快取或多執行緒技術來減少等待。

系統需保護：

-   作業系統不可被使用者程式讀寫
-   使用者程式不可互相干擾

#### 1.1.1. 解法：基底暫存器（base）+ 限制暫存器（limit）

每個 process 的記憶體限制由這兩個暫存器定義：

-   base：起始位址
-   limit：可使用的記憶體範圍

若 user 程式違規 → 產生 **trap** 給作業系統

只有作業系統（kernel mode）可以修改 base/limit 暫存器

![upgit_20250709_1752068345.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752068345.png)

![upgit_20250709_1752068707.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752068707.png)


### 1.2. Address Binding（位址繫結）

「位址繫結」是將變數名稱（symbolic address）變成實際位址的過程。

有三種繫結方式：

#### 1.2.1. 編譯時（Compile time）：
- 程式位址在編譯時就固定（例如：從位址 100 開始）
- 缺點：若位置改變，必須重新編譯

#### 1.2.2. 載入時（Load time）：
- 編譯產生「可重定位（relocatable）」程式碼
- 真正的實體位址延後到載入到記憶體時決定

#### 1.2.3. 執行時（Execution time）
- 現今最常見
- 程式執行過程中可以搬動到不同位置
- 需要硬體支援，例如：MMU

![upgit_20250709_1752068737.png|447x707](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752068737.png)


### 1.3. Logical vs Physical Address Space（邏輯位址 vs 實體位址）

邏輯位址（Logical / Virtual Address）：程式內看到的地址（例如你寫 `arr[3]`）

實體位址（Physical Address）：真正送進記憶體的位址（經過硬體轉換）

使用 **MMU（Memory Management Unit）** 做地址轉換：
-   user 程式產生邏輯位址
-   MMU 使用「重定位暫存器（relocation register）」轉成實體位址


![upgit_20250709_1752068826.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752068826.png)


範例：

```
重定位暫存器 = 14000
user 想存位置 346
→ 實體位址 = 14346
```

![upgit_20250709_1752068856.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752068856.png)





### 1.4. Dynamic Loading（動態載入）


> 這是 **程式設計層面**的技巧，不一定需要作業系統支援。

平常：整個程式都先載入記憶體

動態載入：只載入主程式，其他函式直到呼叫時才載入

好處：
-   減少記憶體使用
-   稀少使用的函式（如錯誤處理）不用一直佔記憶體


### 1.5. Dynamic Linking and Shared Libraries（動態連結與共享函式庫）

靜態連結：每個程式都內嵌一份函式庫（浪費空間）

動態連結（DLL）：
-   程式執行時才連結共享函式庫
-   多個程式可共用一份程式碼（記憶體節省）

## 2. Contiguous Memory Allocation（連續記憶體配置）

每個 process 都會被分配到一段「連續的」記憶體區塊。

整體記憶體空間會分成兩部分：
- 一部分保留給作業系統（通常放在高位址）
- 一部分給使用者程式

### 2.1. Memory Protection（記憶體保護）

核心概念：防止一個 process 去存取不屬於它的記憶體

解法：使用 relocation register（基底暫存器）與 limit register（範圍限制）
- Relocation Register：process 可存取的最小物理位址（也就是它的起點）
- Limit Register：可存取的邏輯記憶體長度

![upgit_20250709_1752069262.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250709_1752069262.png)


操作流程：
1. 使用者程式產生邏輯位址（例如 100）
2. MMU 幫它加上 relocation（如 100040 + 100 = 100140）
3. 判斷是否超出 limit（否則觸發 trap）

Context switch 時，OS 會重新載入新的 relocation 與 limit。

### 2.2. Memory Allocation（記憶體分配）

一開始：整個記憶體是個大洞（hole），只有 OS 的部分是固定的，其餘可以被分配給使用者 process。

當 process 進入記憶體時：
1. OS 找到一個夠大的洞（hole）
2. 分出一塊給這個 process，其餘保留成新的洞
3. 當 process 結束，釋放記憶體 → 成為新的洞
4. 如果相鄰的洞可以合併 → merge 成一個大洞

#### 2.2.1. 三種洞的分配策略（hole selection）

|策略|說明|優缺點|
|---|---|---|
|**First Fit**|找到第一個夠大的洞就用|快速但會留下很多小碎塊|
|**Best Fit**|找最剛剛好的小洞|節省空間但要全部掃過，慢|
|**Worst Fit**|找最大洞|剩下最大空間，但容易浪費|

### 2.3. Fragmentation（碎裂）

#### 2.3.1. External Fragmentation（外部碎裂）

記憶體被切成很多小塊，總量夠但無法連續分配
- 最壞情況：每兩個 process 間都有一小段無法使用
- 有個 50% 規則：當有 N 個已分配區塊時，會產生額外約 0.5N 個無法使用的小碎塊 → 約三分之一記憶體浪費

#### 2.3.2. Internal Fragmentation（內部碎裂）
分配比需求稍大的記憶體區塊時，造成內部浪費
- 例如：洞有 18464 bytes，process 只要 18462 bytes → 剩 2 bytes 難再利用

#### 2.3.3. 解法一：Compaction（壓縮）
針對External Fragmentation（外部碎裂）

把記憶體中的資料集中到一邊，空洞集中成一大塊。
- 需配合 動態位址重配置（dynamic relocation）
- 把所有 process 往一側搬，更新 relocation register
缺點：成本高、效率差

#### 2.3.4. 解法二：非連續分配（noncontiguous allocation）
解決外部碎裂問題

採用 paging（分頁），是下一節的主角。

不需要把整個 process 放在連續區域。可以把 process 分散放在不同記憶體空間中



