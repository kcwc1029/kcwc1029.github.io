## 1. Background

一段程式要執行，必須放進主記憶體中。這雖然合理，但也產生了兩個限制：
- 程式大小受限於實體記憶體大小
- 記憶體的使用效率低落


### 1.1. 虛擬記憶體的好處

| 好處                  | 說明                      |
| ------------------- | ----------------------- |
| 無需受限於實體記憶體容量        | 可撰寫記憶體需求龐大的程式，簡化開發。     |
| 提高 CPU 使用率與同時執行程式數量 | 每個程式只佔用部分記憶體，能同時執行更多程式。 |
| 減少 I/O 操作，加速程式執行    | 無須頻繁讀寫整個程式，加快載入與切換速度。   |

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

| 特性              | 說明                                          |
| --------------- | ------------------------------------------- |
| 延遲加載（Lazy Load） | 程式初始時不載入所有頁面，只有當程式真正「存取」該頁時才載入。             |
| 減少記憶體浪費         | 沒用到的頁永遠不會載入，節省記憶體資源。                        |
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
- 會搬移大區塊記憶體，若中途頁錯會導致搬移「一半」。
- 解法：
	- 預先存取所有頁 → 若會出錯先讓頁錯發生。
	- 用暫存區保留原資料 → 若頁錯就回復再重來。

### 2.3. Free-Frame List



當有 page fault 發生，我們就必須：
1. 從硬碟（或其他二級儲存）把資料載入記憶體。
2. 但不能亂放，要放到一個「空抽屜」。
3. 所以就要去 Free-Frame List 裡面撈一格出來用。

框架配置時進行「zero-fill-on-demand」清除記憶體（避免資料洩漏風險）。

如果Free-Frame List沒空格了 → Page Replacement（頁面替換）

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

| 狀況             | 操作                          |
| -------------- | --------------------------- |
| Modify Bit = 0 | 表示該頁未被改寫 → 可以直接捨棄，不用寫回      |
| Modify Bit = 1 | 表示有改寫 → 需先寫回 swap space 再釋放 |

## 4. 常見的頁面替換演算法

