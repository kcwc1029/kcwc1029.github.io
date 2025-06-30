## 1. 作業系統提供的服務（Operating-System Services）

作業系統的主要目的之一，是提供一個方便且高效的環境讓程式得以執行。它對「使用者」與「程式」都提供一組共通的基本服務。這些服務可以分為兩大類：

### 1.1. 種類 01：幫助「使用者」與「應用程式」的服務

| 服務名稱                                       | 說明                                                                                                                                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. 使用者介面 (User Interface)**             | 提供 GUI（圖形介面）、CLI（命令列介面）、或觸控式介面，讓使用者與系統互動。                                                                                              |
| **2. 程式執行 (Program Execution)**            | 載入程式到記憶體並執行它。若程式執行完成或錯誤終止，作業系統要能處理結束程序。                                                                                           |
| **3. 輸入/輸出操作 (I/O Operations)**          | 管理所有 I/O 裝置，例如鍵盤、磁碟、網路等。使用者無法直接操作硬體，因此 OS 提供中介方法來進行 I/O。                                                                      |
| **4. 檔案系統操作 (File-System Manipulation)** | 提供建立、讀寫、搜尋、刪除檔案與資料夾的功能。也包含權限控管（誰可以存取哪個檔案）。                                                                                     |
| **5. 程式間通訊 (Communications)**             | 讓不同程序之間能夠溝通，可透過「共享記憶體」或「訊息傳遞（message passing）」來完成，適用於同一台機器或跨網路的電腦。                                                    |
| **6. 錯誤偵測 (Error Detection)**              | 作業系統要能持續監控錯誤，包括硬體錯誤（如記憶體或網路）、I/O 錯誤（如印表機沒紙）、或程式錯誤（如存取非法記憶體）。有時必須終止程式，有時可回傳錯誤代碼讓程式自行處理。 |

### 1.2. 種類 02：幫助「系統自身運作效率」的服務

| 服務名稱                                    | 說明                                                                                                        |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **1. 資源分配 (Resource Allocation)**       | 當多個程序同時執行，系統要分配 CPU、記憶體、磁碟等資源。使用排程演算法（如 CPU scheduling）與資源管理方法。 |
| **2. 使用記錄與帳務 (Accounting)**          | 系統紀錄每個程式使用了多少資源，例如 CPU 時間、記憶體、磁碟空間等，用來做帳務分析或統計。                   |
| **3. 保護與安全 (Protection and Security)** | 確保不同程序間無法任意干擾彼此，也防止非法使用者入侵系統。包括帳號密碼登入、權限控制、防火牆等。            |

## 2. 系統呼叫（System Calls）

開發者寫程式通常使用的是 API（Application Programming Interface），例如`read(fd, buf, count);`，這其實是「包裝好」的 system call，由作業系統提供的函式庫（如 Linux 的 libc）實作。

-   底層邏輯：呼叫 read() → libc 轉換為 system call → 作業系統幫你做事
-   優點：跨平台、簡單好寫，不用煩惱細節。

![upgit_20250630_1751290161.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751290161.png)

### 2.1. System Calls 種類

| 分類                 | 常見功能                                    | 範例 system call               |
| -------------------- | ------------------------------------------- | ------------------------------ |
| 🧠 Process Control   | 建立、終止程序、等待、記憶體分配等          | `fork()`, `exec()`, `exit()`   |
| 📁 File Management   | 建立、開啟、讀寫、關閉檔案                  | `open()`, `read()`, `write()`  |
| 📦 Device Management | 請求/釋放裝置、讀寫、移動資料               | `ioctl()`, `read()`, `write()` |
| ℹ️ Information       | 時間、日期、系統資訊、屬性查詢與設定        | `gettimeofday()`, `getpid()`   |
| ✉️ Communication     | 進程之間的訊息交換（Message/Shared memory） | `pipe()`, `shm_open()`         |
| 🔐 Protection        | 設定/查詢權限、限制資源使用                 | `chmod()`, `umask()`           |

### 2.2. System Call 的參數怎麼傳？

1. 直接用暫存器 傳參數（少量參數）
2. 用記憶體區塊（table） 傳（參數多時）→ 把所有參數放進記憶體，然後只傳這個位置
3. 用 stack 推入資料

-   Linux 結合以上兩種：少的用暫存器，多的就用 block。

## 3. Linker & Loader

當你寫好一支程式，例如 main.c，你不能直接執行它。它必須經過以下流程：

```
main.c ─→ (Compiler) ─→ main.o ─→ (Linker) ─→ main（執行檔）─→ (Loader) ─→ 放進記憶體執行
```

-   Compiler ：產生「物件檔」
-   Linker ：合併多個物件檔 & 函式庫，生成「可執行檔」→ 兩種連結方式
    -   靜態連結：把函式庫直接寫進執行檔中
    -   動態連結：只留下「之後再載入」的資訊，等真正要跑時再載入（像 Windows 的 .dll）
-   Loader 載入器：把程式載入記憶體，準備執行 → OS 會
    -   呼叫 fork() 建立一個新行程（process）
    -   呼叫 exec() 載入 main 進記憶體並執行

![upgit_20250630_1751290750.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751290750.png)

## 4. 作業系統的結構（Operating-System Structure）

### 4.1. Monolithic Structure（單體式結構）

核心（Kernel）什麼都做：所有功能都在同一個程式裡，像 UNIX 最早期的設計。

-   優點：效率高，因為功能之間可以直接互相呼叫。
-   缺點：難以維護與擴充，改動一部分可能會影響其他部分。

![upgit_20250630_1751290971.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751290971.png)

![upgit_20250630_1751291011.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751291011.png)

### 4.2. Layered Approach（層次式結構）

將作業系統分為一層層（Layer 0 是硬體，最上層是使用者界面）。每一層只依賴比自己低的層。

-   優點：容易除錯與驗證，每層都可以獨立測試。
-   缺點：效能較差，需要逐層呼叫才可完成任務。

![upgit_20250630_1751291023.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751291023.png)

### 4.3. Modules（模組化核心）

只保留最基本功能在核心裡（例如記憶體管理、排程、IPC(程序間通訊)）。
其他功能（像裝置驅動程式、檔案系統）則跑在使用者空間，透過訊息傳遞（Message Passing）與核心溝通。

-   優點：
    -   更安全可靠（失敗的模組不會當掉整個系統）
    -   更容易移植（不同硬體改很少）
-   缺點：效能較差，因為訊息傳遞需要複製資料與切換行程

![upgit_20250630_1751291060.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751291060.png)

### 4.4. Modules（模組化核心）(Linux、Windows )

類似 Layered + Microkernel 的混合體。

使用 Loadable Kernel Modules (LKM)：例如插上 USB 時，自動載入驅動模組。

好處：

-   效能接近 monolithic
-   又具備可動態擴充模組的彈性（不需重新編譯整個核心）

### 4.5. Hybrid Systems（混合型系統）

#### 4.5.1. macOS/iOS：

-   內核叫做 Darwin，採用 Mach 微核心 + BSD 核心混合
-   提供雙系統呼叫介面（Mach + POSIX）
-   大部分模組仍在同一個核心空間，減少傳訊 overhead
    ![upgit_20250630_1751291286.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751291286.png)

![upgit_20250630_1751291295.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751291295.png)

#### 4.5.2. Android

-   基於 Linux 核心。
-   Java 程式執行在 ART（Android Runtime）虛擬機上，支援 AOT 編譯與低功耗設計。
-   使用 HAL（硬體抽象層），讓開發者不用管手機硬體細節。

![upgit_20250630_1751291307.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/06/upgit_20250630_1751291307.png)

#### 4.5.3. Windows WSL（Windows Subsystem for Linux）：

-   讓 Linux 程式可在 Windows 中執行。
-   使用特殊的「Pico Process」與 LXSS/LXCore 模組翻譯 Linux system call 到 Windows 的呼叫。

## 5. 練習：

### 5.1. Q01：

Q：What is the purpose of system calls?

A：System call 是使用者程式與作業系統核心之間的溝通介面，它的目的是讓應用程式可以請求作業系統執行某些操作，例如：開檔案、讀取資料、建立新程序（使用者無法直接存取硬體，必須透過 system call）

### 5.2. Q02：

Q：What is the purpose of the command interpreter? Why is it usually separate from the kernel?

A：

Command interpreter（命令直譯器） 也稱為 shell。像是 UNIX 中的 bash、zsh；windows 中的 cmd、powerShell。

功能：

-   讓使用者可以輸入指令
-   解譯指令後呼叫適當的 system call 去執行程式或操作系統功能

為什麼要和 kernel 分開;

-   Shell 是使用者空間的程式，不需要在核心中運行
-   保持 kernel 簡潔、穩定與安全
-   允許用戶自由更換不同的 shell(像是 vscode 中的 terminal)

### 5.3. Q03：

Q：What system calls have to be executed by a command interpreter or shell in order to start a new process on a UNIX system?

A：

在 UNIX 系統中，shell 執行新程式時會呼叫兩個核心 system call：

-   fork()：建立一個新的子程序（process）
-   exec()：在子程序中載入新程式（用新程式碼取代原來的程式）

有時也會搭配：

-   wait()：等待子程序結束
-   exit()：終止程序

### 5.4. Q04：

Q：What is the purpose of system programs?

A：System programs 是提供給使用者或其他程式使用的實用工具程式，不屬於 kernel，但與 OS 緊密合作。

像是:

-   檔案處理：cp, mv, rm
-   程序管理：ps, kill
-   編譯工具：gcc, make
-   文字處理：vim, cat, more

### 5.5. Q05：

Q：What is the main advantage of the layered approach to system design? What are the disadvantages?

A：

-   優點：
    -   模組化設計：每一層只處理自己的職責。
    -   安全性較高：下層被錯誤影響的機會減少。
    -   維護與除錯更容易：錯誤容易定位在哪一層。
-   缺點：
    -   效能可能變差：要「逐層呼叫」，有額外開銷
    -   設計困難：要正確切分層次與定義介面很麻煩

### 5.6. Q06：

Q：List five services provided by an operating system, and explain how each creates convenience for users. In which cases would it be impossible for user-level programs to provide these services?

A： 個常見的 OS 服務

| 服務              | 功能說明             | 使用者便利性               | 為什麼不能在 user-level 實作？   |
| ----------------- | -------------------- | -------------------------- | -------------------------------- |
| 1. 程序管理       | 建立、終止與切換程序 | 支援多工與控制             | 需要控制 CPU 分配                |
| 2. 記憶體管理     | 分配與回收 RAM       | 自動分配空間、避免衝突     | 使用者程式無法直接操作記憶體     |
| 3. 檔案系統管理   | 儲存、存取與刪除檔案 | 提供一致檔案介面           | 需要存取磁碟裝置與權限管理       |
| 4. I/O 系統       | 控制輸入輸出裝置     | 操作滑鼠、鍵盤、網路等硬體 | 必須控制硬體與中斷處理           |
| 5. 安全與存取控制 | 帳號登入、權限管理   | 防止資料外洩與未授權使用   | 只有 kernel 能安全地控制整個系統 |

### 5.7. Q07：

Q： Why do some systems store the operating system in firmware, while others store it on disk?

A：

Firmware 儲存 OS 的例子：嵌入式系統（如：路由器、微波爐）

-   好處：開機快速、不需要硬碟
-   壞處：更新不方便、儲存空間小
    磁碟儲存 OS 的例子：一般電腦（Windows、Linux）
-   好處：容易更新、彈性高
-   壞處：需要啟動程序（boot loader）載入 OS

### 5.8. Q08：

Q：The services and functions provided by an operating system can be divided into two main categories. Briefly describe the two categories, and discuss how they differ.

A：作業系統提供的服務主要分為兩大類

-   User Services（使用者導向服務）：
    -   直接支援使用者與應用程式的運作，例如程式執行、檔案操作、I/O 操作、UI 介面等。
    -   提供便利的操作與使用經驗。
-   System Services（系統導向服務 / 資源管理）：
    -   負責系統資源管理，如 CPU 排程、記憶體管理、裝置控制、安全性等。
    -   目的是維持整體系統的穩定性與效率。

### 5.9. Q09：

Q：Describe three general methods for passing parameters to the operating system.

A：

1. Registers（暫存器）： 將參數直接放入 CPU 的暫存器中，快速但數量有限。
2. Memory Block（記憶體區塊）： 將參數放入記憶體，然後把指標傳給作業系統。
3. Stack（堆疊）： 把參數壓入程式堆疊，適合參數數量不固定的情況。

### 5.10. Q10：

Q：Would it be possible for the user to develop a new command interpreter using the system-call interface provided by the operating system?

A：是的，使用者可以自行開發命令直譯器（command interpreter / shell），因為作業系統提供的 system call（例如 exec()、fork()、read()、write()）允許程式：接收輸入、解譯命令字串、建立新程序執行指令

### 5.11. Q11：

Q：Why is the separation of mechanism and policy desirable?

A：

-   機制（Mechanism）： 如何達成某件事的實作方法（例如：提供 CPU 排程功能）。
-   政策（Policy）： 做決策的規則（例如：使用 FCFS 還是 RR 排程）。

### 5.12. Q12：

Q：It is sometimes difficult to achieve a layered approach if two components of the operating system are dependent on each other. Identify a scenario in which it is unclear how to layer two system components that require tight coupling of their functionalities.

A：I/O buffer 管理與記憶體管理

-   I/O 系統可能需要記憶體管理來配置緩衝區。
-   記憶體系統又可能依賴 I/O 來進行虛擬記憶體的換頁（paging）

### 5.13. Q13：

Q：What is the main advantage of the microkernel approach to system design? How do user programs and system services interact in a microkernel architecture? What are the disadvantages of using the microkernel approach?

A：

互動方式：

-   所有服務透過 IPC（訊息傳遞）與核心溝通
    優點：
-   將非核心功能（如檔案系統、網路）移出 kernel，減少出錯風險。
-   增強模組化與穩定性，系統當掉不會一併影響核心。
    缺點：效能開銷大： 多次上下文切換與訊息交換增加延遲。
