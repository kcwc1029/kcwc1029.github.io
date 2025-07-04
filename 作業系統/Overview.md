## 1. 作業系統的角色可分為四個部分：

-   硬體（hardware）：CPU、記憶體與 I/O 裝置，提供資源。
-   作業系統（operating system）：協調硬體與應用程式的使用。
-   應用程式（application programs）：如文字處理器、編譯器、網頁瀏覽器等。
-   使用者（user）：最終使用者。

![upgit_20250630_1751284833.png|527x337](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751284833.png)

### 1.1. User View 使用者觀點

-   一般電腦使用者（如筆電或桌機使用者）習慣使用螢幕、鍵盤、滑鼠。這些系統的設計是給單一使用者獨佔硬體資源。這種情境下，作業系統的設計目標是提升使用方便性（ease of use），其次才考量效能與安全性，不會特別在意資源共享（resource utilization）。
-   隨著科技發展，越來越多人改用行動裝置（如手機、平板），這些設備多使用觸控介面與語音介面（例如 Siri）。
-   某些嵌入式裝置（如家電、車用系統）幾乎沒有使用者介面，只會透過數字鍵盤或燈號顯示狀態。這些系統的作業系統與應用程式多為自動化運行，無需使用者干預。

### 1.2. System View 系統觀點

-   從電腦本身的角度看，作業系統是最貼近硬體的程式。
-   作業系統是資源分配者（resource allocator），負責管理如 CPU 時間、記憶體、儲存空間、I/O 裝置等資源。它必須在多個程式與使用者之間做出資源分配的效率與公平性決策。
-   另一方面，作業系統也是控制程式（control program），負責控制使用者程式的執行，以防錯誤與不當使用，特別是與 I/O 裝置相關的部分。

### 1.3. Defining Operating Systems 作業系統的定義

作業系統是電腦中永遠在運行的程式，通常稱為「核心（kernel）」，可以分為：

-   系統程式（system programs）：輔助作業系統，但不一定屬於核心。
-   應用程式（application programs）：用戶運行的程式，不參與作業系統運作。

## 2. Computer-System Organization 電腦系統組織

現代電腦系統基本構成：

-   包含一個或多個 CPU、多個 裝置控制器（device controller），透過系統匯流排（bus）連接彼此與記憶體（memory）。
-   每個控制器負責一類裝置（如：磁碟、音訊、圖形），有些控制器可同時連接多個裝置（例如 USB hub）。
-   控制器會有緩衝區（local buffer）與特殊暫存器（registers），負責與其裝置間的資料搬移。
-   作業系統為每個控制器提供驅動程式（device driver），這讓 OS 能以一致的方式管理不同裝置。

![upgit_20250630_1751285270.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751285270.png)

## 3. Interrupts 中斷

1. CPU 執行程式
2. 裝置控制器完成任務後發出 interrupt signal（中斷訊號）
3. CPU 接收到中斷後，暫停當前執行，跳到固定位置執行對應的中斷服務程式（ISR）
4. ISR 處理完事件後，恢復先前 CPU 的狀態並繼續原本程式。

> 中斷的技術細節：使用中斷向量表（interrupt vector table）」根據中斷編號快速跳到對應 ISR 的位置。
>
> -   必須保存與還原原本程式的狀態（例如暫存器）。
> -   有兩種中斷線：
>     -   Non-maskable（不可屏蔽）：例如記憶體錯誤，無法忽略。
>     -   Maskable（可屏蔽）：可以暫時忽略，用於一般裝置請求。
> -   若中斷太多，可用「中斷連鎖（interrupt chaining）」機制來處理。

![upgit_20250630_1751285455.png|998x487](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751285455.png)

## 4. Storage Structure 儲存結構

儲存層級（Storage Hierarchy）：由快到慢、由小到大，可分為三類儲存裝置：

-   主儲存（Primary）：快但小，如暫存器、快取、主記憶體（RAM）→ 易失性（volatile）
-   次儲存（Secondary）：大但慢，如硬碟（HDD）、非揮發性記憶體（NVM）→ 非易失性（nonvolatile）
-   三階儲存（Tertiary）：更大更慢，如磁帶、光碟，用於備份

![upgit_20250630_1751285579.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751285579.png)

## 5. I/O 結構（Input/Output Structure）

在電腦中，I/O 裝置（像是鍵盤、滑鼠、磁碟、網路卡等）是讓電腦與外界互動的硬體。作業系統的很大一部分工作，就是管理這些 I/O 裝置的資料傳輸。

### 5.1. 方式 01：中斷驅動 I/O（Interrupt-driven I/O）

> 按下鍵盤 → 裝置控制器會「中斷 CPU」並發出通知 → 告訴作業系統：「欸，我有資料了！」

處理流程：

1. 作業系統先請裝置控制器啟動 I/O（例如讀取硬碟）。
2. 控制器執行後，發出中斷（Interrupt）。
3. CPU 停下手邊的工作，轉去處理這個中斷，並執行「中斷服務程式（Interrupt Service Routine）」來完成後續工作。

問題：

-   每一筆資料都會觸發一次中斷（如每一個字元都要通知 CPU）。
-   如果是要傳輸 大量資料（例如一整張照片），這樣每個 byte 都中斷一次 → 太慢了！

### 5.2. 方式 02：DMA（Direct Memory Access，直接記憶體存取）

概念：由「裝置控制器」自己負責資料搬運 → 不需要 CPU 一筆一筆管

目的：解決大量資料中斷太多的問題

![upgit_20250630_1751286072.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751286072.png)

## 6. 電腦系統架構（Computer-System Architecture）

> 現代電腦系統可能只用一個處理器，也可能有上百個處理器，設計和操作系統的支援方式會有所不同。

### 6.1. 單處理器系統（Single-Processor Systems）

早期電腦大多只有一個 CPU 核心（core）→ CPU 執行所有指令與處理所有任務。

### 6.2. 多處理器系統（Multiprocessor Systems）(現代標準配置)

可以分為：

#### 6.2.1. Symmetric Multiprocessing（SMP 對稱多處理）

-   每個 CPU 都是平等的，可以處理作業系統和應用程式。
-   所有 CPU 共用主記憶體與系統匯流排。
-   運行效率高，N 顆核心最多可同時跑 N 個程序。

問題：當 CPU 太多，會爭搶匯流排，導致效能下降。

![upgit_20250630_1751286385.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751286385.png)

#### 6.2.2. Multicore Systems（多核心系統）

-   一顆實體晶片上面有多個核心（cores）。
-   每個核心有自己的暫存器與 L1 cache，並共享 L2 cache。
-   核心之間溝通快、耗能低，是現今最常見架構（如手機、筆電）。

![upgit_20250630_1751286500.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751286500.png)

#### 6.2.3. NUMA（非一致記憶體存取）

-   每個 CPU 或 CPU 群組有自己的本地記憶體，速度快。
-   透過系統互連線（interconnect）互通資料，共享記憶體空間。
-   適合大量 CPU 的擴充（scalability），多用於伺服器
-   若 CPU0 存取 CPU3 的記憶體，會比較慢（有延遲 latency）→ 需做「CPU 排程」與「記憶體分配」優化來避免延遲

![upgit_20250630_1751286572.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751286572.png)

#### 6.2.4. 叢集系統（Clustered Systems）

-   多台電腦（節點）組成一個群組，透過網路互連（如 LAN 或 InfiniBand）。
-   每台電腦是完整的系統，可有多核心。

功能：

-   高可用性（High Availability）：若有一台電腦掛掉，另一台接管 → 使用者幾乎無感 → 熱備援（hot standby）/ 對等備援（symmetric）
-   高效能（High Performance Computing）：將一個大任務「平行化（parallelization）」，分給多台電腦同時跑。
-   共享儲存（Shared Storage）：用「SAN（Storage Area Network）」讓多台電腦共用資料。→ 系統需使用「分散式鎖定管理（Distributed Lock Manager, DLM）」來避免資料衝突。

![upgit_20250630_1751286813.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751286813.png)

## 7. 作業系統的基本運作（OS Operations）

### 7.1. 開機流程（Bootstrap Process）

1. 電腦開機時（power on 或 reboot）：
    1. 執行 bootstrap program（啟動程式）→ 儲存在 firmware（如 ROM）→ 負責初始化 CPU、記憶體與裝置控制器，然後載入作業系統核心（kernel）
2. Kernel 開始執行後：載入系統程式（稱為 daemon，常駐程式）
    1. Linux 中第一個系統程式是 systemd
    2. 系統完成開機後，就等待「事件」（例如：鍵盤輸入、網路請求）

### 7.2. 中斷與系統呼叫（Interrupt & System Call）

> 事件大多透過中斷（interrupt）來通知 OS

Interrupt 可以分為

-   硬體中斷（如滑鼠移動、磁碟完成）
-   陷阱 Trap / Exception（例如：除以零錯誤、記憶體違規存取）

System call（系統呼叫） 也是一種「軟體中斷」：用來請求 OS 幫忙執行特權任務（例如存檔）

| 特徵       | 系統呼叫（System Call）          | 中斷（Interrupt）              |
| ---------- | -------------------------------- | ------------------------------ |
| 誰觸發     | 程式主動請求                     | 硬體或裝置主動發出             |
| 時機       | 程式需要作業系統幫忙時           | 例如鍵盤輸入、網路封包到達時   |
| 控制權轉移 | 使用者程式請求進入核心           | 當前執行單元被「打斷」進入核心 |
| 是否可預期 | 可預期                           | 多半不可預期                   |
| 範例       | `read()`, `write()`, `open()` 等 | 鍵盤輸入中斷、計時器中斷等     |

## 8. 多工與多工處理（Multiprogramming & Multitasking）

-   Multiprogramming：多個程式在記憶體，CPU 一次執行一個，等待時切換
-   Multitasking：Multiprogramming + 快速切換

## 9. 雙模式（Dual-Mode ）

目的：避免惡意或錯誤程式傷害系統

區分

-   User mode（使用者模式）：執行使用者程式，受限、無法執行危險指令
-   Kernel mode（核心模式）：執行作業系統程式，有最高權限，可直接操控硬體

切換流程：

1. 使用者程式呼叫 system call → Trap → 進入 kernel mode
2. 執行完系統任務 → 回到 user mode，繼續程式執行

![upgit_20250630_1751287477.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751287477.png)

```
[ 開機 ]
   ↓
[ bootstrap 程式（firmware）]
   ↓
[ 載入作業系統核心 kernel（進入 kernel mode）]
   ↓
[ 載入 daemon（系統常駐程式）]
   ↓
[ 切換到 user mode，執行使用者程式 ]
   ↓
       ┌──────────────┐
       │ user 執行錯誤 │────→ [ Trap → 回到 kernel mode → 錯誤處理 ]
       └──────────────┘
       ┌─────────────────────┐
       │ user 呼叫系統服務（system call）│────→ [ 進入 kernel mode → 執行服務 ]
       └─────────────────────┘
```

## 10. 計時器（Timer）

-   定時中斷 → 強迫程式交出 CPU 控制權
-   目的：避免程式無限迴圈或長時間佔用 CPU

## 11. 作業系統的運算環境（Computing Environments）

-   傳統桌機與辦公室環境：辦公室的電腦通常是 PC 接在內部網路上，透過伺服器提供檔案與印表機服務。
-   行動裝置（ iOS 和 Android）
    -   優點：行動裝置現在的功能很強大，能上網、拍照、導航、看影片、玩遊戲、處理文件等。
    -   配備：有 GPS、加速度計、陀螺儀等感測器（可偵測位置、傾斜、搖動等）。
    -   限制：雖然功能接近筆電，但處理器較小、耗電受限、記憶體與儲存容量較低（例如 256GB 對上 8TB）。
-   用戶端與伺服器系統(Client–Server Computing)：是一種分散式系統架構
    -   Client 發出需求（像是查資料）
    -   Server 回應需求（查完回傳）
-   點對點系統（Peer-to-Peer Computing, P2P）：
    -   不再區分 client 或 server，每個節點都是 peer（同儕）。
    -   集中式註冊：像 Napster，一個中央伺服器記錄誰有什麼檔案。
    -   分散式查找：像 Gnutella，節點之間廣播查詢誰有某個檔案。
-   雲端運算(Cloud Computing)：架構包含：虛擬機（VM）、雲管理工具（如 VMware vCloud、Eucalyptus）、防火牆保護等。
-   即時嵌入式系統(Real-Time Embedded Systems)：
    -   最常見的電腦裝置，像微波爐、汽車引擎、工廠機器等。
    -   有些使用簡單 OS（如嵌入式 Linux）、有些則是 ASIC 晶片。
    -   幾乎所有都需要 即時性（Real-time）：必須在嚴格時間內完成任務，否則系統會失敗（例如：機械手臂來不及停止會撞壞物品）。

![upgit_20250630_1751288119.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751288119.png)

## 12. 練習：

### 12.1. Q01：

Q：What are the three main purposes of an operating system?

A：作業系統有三大主要目的

1. 提供介面：讓使用者能夠與電腦互動（例如：透過 GUI 或命令列）。
2. 資源管理：管理 CPU、記憶體、儲存裝置、I/O 等硬體資源。
3. 作業控制與執行環境：讓應用程式可以安全、有效率地執行。

### 12.2. Q02：

Q：When is it appropriate for the OS to ‘waste’ resources? Why is such a system not really wasteful?

A：當使用者體驗（UX）或可用性比效能更重要 時，"浪費資源" 是合理的 → GUI 系統浪費更多記憶體，但操作更直覺

### 12.3. Q03：

Q：What is the main difficulty in writing an OS for real-time environment?

A：必須保證每個任務在「嚴格的時間限制內完成」

-   任務延遲會造成系統失敗（例如：飛機控制系統、車用感測） → 必須設計可預測的排程與中斷管理機制

### 12.4. Q04：

Q：Should the OS include applications like browsers or mail clients? Argue both sides.
A：

-   正面:
    -   提供更完整的「作業體驗」
    -   減少額外安裝與整合問題（像 Windows 的 IE）
-   反面：
    -   OS 應該聚焦在資源與硬體管理，不應與應用程式混在一起
    -   不利於模組化與安全性（ex: 攻擊瀏覽器可能影響整個系統）

### 12.5. Q05：

Q：How does kernel mode vs user mode function as a basic protection?

A：隔離機制防止惡意或錯誤的程式傷害系統，形成基本的保護層。

### 12.6. Q06：

Q：Which of the following instructions should be privileged?

A：

| 指令                                     | 是否為特權指令 | 原因                                     |
| ---------------------------------------- | -------------- | ---------------------------------------- |
| a. Set value of timer                    | ✅             | 防止程式修改系統排程                     |
| b. Read the clock                        | ❌             | 只是讀取資料                             |
| c. Clear memory                          | ✅             | 可能刪除系統資料                         |
| d. Issue a trap instruction              | ❌             | Trap 是從 user mode 呼叫系統 call 的機制 |
| e. Turn off interrupts                   | ✅             | 關掉中斷可能讓系統無法應變               |
| f. Modify entries in device-status table | ✅             | 影響 I/O 控制                            |
| g. Switch from user to kernel mode       | ✅             | 只能由 OS 控制進入核心模式               |
| h. Access I/O device                     | ✅             | 防止亂存設備造成損壞                     |

### 12.7. Q07：

Q：What difficulties arise if OS is placed in protected memory that cannot be changed at all (even by OS itself)?

A：問題：

-   系統無法動態更新核心模組（如：驅動程式）
-   錯誤修補變困難，無法即時修正漏洞或異常

### 12.8. Q08：

Q：What are two uses of CPUs with more than two modes?

A：

-   分開使用者應用程式、核心模組、驅動程式的權限（多層安全）
    -   支援虛擬化環境（讓 guest OS 只能執行在較低等級）

### 12.9. Q09：

Q：How can timers be used to compute the current time?

A：如果每 1 秒產生一個中斷，則`current_time = boot_time + interrupt_count × timer_interval`

### 12.10. Q10：

Q：Why are caches useful? What do they solve? What problems do they cause?

A：

-   好處：
    -   提高效能：加速資料存取
    -   減少主記憶體或硬碟的存取次數
-   問題：
    -   一致性問題（Cache 與實際資料不同步）
    -   增加複雜性（需設計一致性協定）
    -   成本問題：若 cache = 裝置大小？會太昂貴、不符效益（像硬碟的 cache）

### 12.11. Q11：

Q：Client–Server vs Peer-to-Peer Model

A：Client–Server 架構清楚但依賴中心節點；P2P 沒有中心節點，因此更彈性但難以管理。

| 項目     | Client–Server         | Peer-to-Peer      |
| -------- | --------------------- | ----------------- |
| 架構     | 中央伺服器            | 每個節點都是 peer |
| 節點角色 | 固定：client / server | 角色可互換        |
| 可擴展性 | 中心可能成為瓶頸      | 容易擴展          |
| 範例     | Web, Email            | BitTorrent, Skype |

### 12.12. Q11：

Q：How do clustered systems differ from multiprocessor systems? What is required for two machines belonging to a cluster to cooperate to provide a highly available service?

A：

-   Clustered systems 是由多台獨立的電腦組成，透過網路連線共同執行工作。
-   Multiprocessor systems 是單一機器中有多個處理器，共用記憶體和其他硬體資源。

### 12.13. Q12：

Q：Consider a computing cluster consisting of two nodes running a database. Describe two ways in which the cluster software can manage access to the data on the disk. Discuss the benefits and disadvantages of each.

A：

-   Shared Disk： 兩台機器共同存取同一個磁碟。透過鎖機制避免資料衝突。
    -   優點：資料一致性高，快速轉移任務。
    -   缺點：需嚴格同步，容易造成 bottleneck。
-   Shared Nothing： 每台機器有自己磁碟，各自處理部分資料。
    -   優點：擴展性佳。
    -   缺點：資料同步困難，容錯較複雜。

### 12.14. Q13：

Q：What is the purpose of interrupts? How does an interrupt differ from a trap? Can traps be generated intentionally by a user program?

A：

-   Interrupt 是由硬體產生，表示需要 CPU 注意，如鍵盤按下。
-   Trap 是軟體產生的異常或請求，如除以零或系統呼叫。
-   使用者程式可以透過 系統呼叫 主動產生 trap，例如存取檔案。

### 12.15. Q14：

Q：Direct memory access is used for high-speed I/O devices in order to avoid increasing the CPU’s execution load.

1. How does the CPU interface with the device to coordinate the transfer?
2. How does the CPU know when the memory operations are complete?
3. The CPU is allowed to execute other programs while the DMA controller is transferring data. Does this process interfere with the execution of the user programs? If so, describe what forms of interference are caused.

### 12.16. Q15：

Q：Some computer systems do not provide a privileged mode of operation in hardware. Is it possible to construct a secure operating system for these computer systems? Give arguments both that it is and that it is not possible.

A：

-   不安全： 缺乏硬體層級保護，程式可能直接操作敏感資源。
-   可能安全： 透過軟體層面（如 sandbox、虛擬機）進行限制

### 12.17. Q16：

Q：Many SMP systems have different levels of caches; one level is local to each processing core, and another level is shared among all processing cores. Why are caching systems designed this way?

A：

-   Local cache：提供每個核心快速存取資料。
-   Shared cache：讓多核心共享資訊，避免不一致。

### 12.18. Q17：

Q：What are some advantages of peer-to-peer systems over client–server systems?

A：

-   優勢：分散資源、不需中央伺服器、容錯能力高
-   缺點：安全與控制難、同步與資料一致性麻煩
