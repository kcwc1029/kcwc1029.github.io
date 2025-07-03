## 1. Process Concept

正在執行中的程式

當你點兩下 .exe 檔案或在 terminal 輸入指令時，系統會把這個程式載入到記憶體並執行，這時它就成為一個 process。

Process 與 Program 的差異：

-   Program 是寫好的程式，儲存在硬碟上
-   Process 是執行中版本的程式，具有活躍狀態與系統資源。
-   一個程式可以對應多個 process（例如你開了兩個 Google Chrome 視窗，每個就是一個 process）。

涵蓋內容：

-   程式計數器（Program Counter）：紀錄下一條要執行的指令位置。
-   記憶體內容：包含程式碼、資料、堆疊、堆積區等。
-   系統資源：如檔案描述器、I/O 裝置等。

### 1.1. Process 結構

-   Text：儲存程式的機器碼，固定不變。
-   Data：全域變數，有些已初始化、有些未初始化。
-   Heap：用 malloc、new 等語法動態配置的記憶體，可擴張縮小。
-   Stack：呼叫函式時會壓入資料（例如參數、return 位置），函式結束後再彈出。

![upgit_20250701_1751375162.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751375162.png)

### 1.2. Process 的狀態（Process States）

每個 process 執行期間都會經歷不同「狀態」：

-   New：剛被建立，尚未執行。
-   Ready：等著 CPU 來執行。
-   Running：目前正在 CPU 上執行。
-   Waiting：暫時被擱置，等待某事件（如 I/O）完成。
-   Terminated：執行完畢，被結束。

![upgit_20250701_1751375393.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751375393.png)

### 1.3. PCB（Process Control Block，行程控制區塊）

系統中每個 process 都會用一個資料結構紀錄它的所有資訊，稱為 PCB，像是 process 的身份證。內容包含：

-   Process 狀態（例如 Running、Waiting）
-   程式計數器（下一步要執行哪行程式）
-   CPU 註冊內容（中斷時需要保存）
-   記憶體相關資訊（如頁表、基底/界限）
-   I/O 狀態（哪些檔案開著、使用哪些裝置）
-   CPU 排程資訊（優先權、排隊指標等）

![upgit_20250701_1751375466.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751375466.png)

## 2. 行程排程(Process Scheduling)

目標：

-   多工（Multiprogramming）：確保 CPU 永遠有事做，提高 CPU 使用率。
-   分時系統（Time Sharing）：讓多個使用者看起來像是同時操作電腦，靠頻繁地切換 process 來實現。

核心任務：

-   使用排程器（scheduler） 從 ready queue（就緒佇列） 選出一個 process，分配給 CPU 執行。
-   每個 CPU 核心同一時間只能執行一個 process。
-   在多核心系統中，每核心可執行一個 process；其餘的就排隊等著。

### 2.1. Scheduling Queues（排程佇列）

系統中有三種主要的佇列：

-   Ready Queue（就緒佇列）：儲存「準備好要執行」的 processes
    -   實作為鏈結串列，佇列頭指向第一個 PCB
-   Wait Queues（等待佇列）：當 process 執行中呼叫 I/O 等操作時，會進入等待狀態。如 I/O wait queue、child termination wait queue 等
-   I/O Queue（輸出入設備佇列）：Process 等待硬碟、滑鼠、鍵盤等設備

![upgit_20250701_1751375752.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751375752.png)

## 3. Context Switch（情境切換 / 上下文切換）

當 process 被中斷或 CPU 要切給別的 process：

1. 要保存目前 process 的狀態 到 PCB（state、registers、memory info）
2. 再載入新 process 的狀態，恢復執行

Context switch 是「額外成本」，因為切換時系統沒有實際做正事

切換速度會受硬體影響（記憶體速度、register 數量、是否有專門指令支援）

![upgit_20250701_1751375902.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751375902.png)

## 4. 行程操作(Operations on Processes)

### 4.1. 行程建立(Process Creation)

父行程（Parent Process）可以建立子行程（Child Process）。子行程也可以建立其他行程，這樣就會形成「行程樹（Process Tree）」。

每個行程都有一個 pid（process ID）

![upgit_20250701_1751376045.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751376045.png)

### 4.2. fork() 與 exec()（UNIX 系統）

-   `fork()`：複製一個行程（父行程被複製，變成一模一樣的子行程）
-   `exec()`：把目前行程的程式碼，換成別的程式（例如 ls）

{% raw %}

```c
pid = fork();
if (pid == 0) {
    // 子行程，pid 回傳為 0
    execlp("/bin/ls", "ls", NULL);  // 換成 ls 程式
} else {
    // 父行程，pid 是子行程的 pid
    wait(NULL);  // 等待子行程結束
    printf("Child Complete\n");
}
```

{% endraw %}

### 4.3. 行程終止(Process Termination)

行程結束會呼叫 exit() 系統呼叫，並通知父行程：

父行程怎麼得知子行程結束 → 使用 wait() 系統呼叫

{% raw %}

```c
int status;
pid_t pid = wait(&status);  // status 儲存子行程的結束狀態
```

{% endraw %}

### 4.4. 殭屍行程(Zombie Process)

行程結束後，如果父行程沒有呼叫 wait()，它就變成 Zombie → 它還會佔用 process table 的空間。

解法是由 init 或 systemd 接手「孤兒行程」來進行回收。

## 5. 行程間通訊(Interprocess Communication, IPC)

在一個系統中，有很多行程（process）同時執行，這些行程可能需要：

-   獨立行程（Independent）：各做各的，互不干涉
-   合作行程（Cooperating）：互相合作，分享資料

動機：

1. 資訊共享：多個應用程式可能要共用資料（例如：剪貼簿內容）
2. 加速計算：把大任務分成小任務，讓多核心同時執行（平行處理）
3. 模組化設計：系統設計時，把功能拆分成多個行程或模組

### 5.1. IPC 方式方式：

1. Shared Memory（共享記憶體）：建立一塊記憶體區塊，讓多個行程能同時存取那塊記憶體
2. Message Passing（訊息傳遞）：行程之間用「傳送訊息」的方式來溝通，就像傳紙條
   ![upgit_20250701_1751376555.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/07/upgit_20250701_1751376555.png)

### 5.2. Message Passing（訊息傳遞）

透過 send() 和 receive() 這兩個動作來傳遞資料 → 適合分散式系統（例如不同電腦之間的行程）

```
send(message);    // 傳送訊息
receive(message); // 接收訊息
```

訊息可以是：

-   固定大小（簡單實作但限制多）
-   變動大小（程式好寫但系統要多處理）

三大設計層面要考慮

#### 5.2.1. 考慮層面 01：Naming（命名方式）

行程之間怎麼「知道要傳給誰」

1. Direct Communication（直接命名）：
    - 一對一通訊（每一個 link 只給一對行程）→ 傳送和接收者必須知道對方的名字

```
send(P, msg)：傳訊息給 P
receive(Q, msg)：從 Q 收訊息
```

2. Indirect Communication（間接命名）：使用「Mailbox / Port（信箱）」作為中介物件：
    - 多個行程可以共用一個 mailbox
    - Mailbox 可以由 process 擁有（會隨 process 終止）或由作業系統管理（獨立存在）

```
send(A, msg)：傳送給信箱 A
receive(A, msg)：從信箱 A 收訊息
```

#### 5.2.2. 考慮層面 02：Synchronization（同步方式）

當 send() 和 receive() 呼叫時，會不會「等對方」

當 send() 和 receive() 都是 blocking，稱為 rendezvous（會合點） → 雙方等彼此，成功才繼續。

|         | Blocking                     | Non-blocking                            |
| ------- | ---------------------------- | --------------------------------------- |
| Send    | 傳送後卡住，等對方收到才繼續 | 傳送後就繼續跑，不管對方有沒有收到      |
| Receive | 沒收到就卡住，一直等         | 嘗試接收，有的話就收，沒有就回傳 null\| |

#### 5.2.3. 考慮層面 03：Buffering（緩衝區設計）

即使是 message passing，訊息在「送達之前」也要有地方暫存——這叫 buffer（緩衝區）

| 類型                           | 說明                                                            |
| ------------------------------ | --------------------------------------------------------------- |
| 0 容量（Zero Capacity）        | 緩衝區不能存訊息 → `send()` 會卡住，直到 `receive()` 把訊息收走 |
| 有限容量（Bounded Capacity）   | 緩衝區最多可存 `n` 筆訊息，如果滿了 → `send()` 會等             |
| 無限容量（Unbounded Capacity） | 想送幾筆就送幾筆，`send()` 永遠不會卡住（理論上）               |

#### 5.2.4. Producer/Consumer

{% raw %}

```cpp
// producer.c
#include <stdio.h>
#include <stdlib.h>
#include <mqueue.h>
#include <string.h>
#include <unistd.h>

#define QUEUE_NAME "/myqueue"
#define MAX_SIZE 256

int main() {
    mqd_t mq;
    char buffer[MAX_SIZE];

    // 建立 message queue（只要建立一次）
    mq = mq_open(QUEUE_NAME, O_CREAT | O_WRONLY, 0644, NULL);
    if (mq == -1) {
        perror("mq_open (producer)");
        exit(1);
    }

    while (1) {
        // 模擬資料產生
        printf("輸入資料給消費者（輸入 exit 結束）：");
        fgets(buffer, MAX_SIZE, stdin);
        buffer[strcspn(buffer, "\n")] = 0; // 移除換行

        // 傳送訊息
        if (mq_send(mq, buffer, strlen(buffer) + 1, 0) == -1) {
            perror("mq_send");
            exit(1);
        }

        if (strcmp(buffer, "exit") == 0) break;
    }

    mq_close(mq);
    return 0;
}
```

{% endraw %}

{% raw %}

```cpp
// consumer.c
#include <stdio.h>
#include <stdlib.h>
#include <mqueue.h>
#include <string.h>
#include <unistd.h>

#define QUEUE_NAME "/myqueue"
#define MAX_SIZE 256

int main() {
    mqd_t mq;
    char buffer[MAX_SIZE];

    // 開啟既有 message queue
    mq = mq_open(QUEUE_NAME, O_RDONLY);
    if (mq == -1) {
        perror("mq_open (consumer)");
        exit(1);
    }

    while (1) {
        // 接收訊息（blocking）
        ssize_t bytes_read = mq_receive(mq, buffer, MAX_SIZE, NULL);
        if (bytes_read < 0) {
            perror("mq_receive");
            exit(1);
        }

        buffer[bytes_read] = '\0'; // 結尾補上字串結束符
        printf("消費者收到資料：%s\n", buffer);

        if (strcmp(buffer, "exit") == 0) break;
    }

    mq_close(mq);
    mq_unlink(QUEUE_NAME); // 清除 queue（只有一方做）
    return 0;
}
```

{% endraw %}

```
// 編譯方式
gcc producer.c -o producer -lrt
gcc consumer.c -o consumer -lrt


// 開兩個終端
// 終端機 A：啟動消費者：./consumer
// 終端機 B：啟動生產者：./producer

// 輸入 exit 可以結束通訊
```

## 6. 練習

### 6.1. Q01：

Q：Using the program shown in Figure 3.30, explain what the output will be at LINE A.

{% raw %}

```cpp
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>

int value = 5;

int main() {
    pid_t pid;
    pid = fork();

    if (pid == 0) { /* child process */
        value += 15;
        return 0;
    }
    else if (pid > 0) { /* parent process */
        wait(NULL);
        printf("PARENT: value = %d", value); /* LINE A */
        return 0;
    }
}
```

{% endraw %}

A：

1. 程式中有一個 value 變數被初始化為 5。
2. 呼叫 fork() 後，會創造一個新的子程序（child process）
3. 子程序會將 value 增加 15，但這只發生在子程序中
4. 父程序使用 wait(NULL); 等待子程序結束，然後在 LINE A 印出 value

### 6.2. Q02

Q：Including the initial parent process, how many processes are created by the program shown in Figure 3.31?

{% raw %}

```cpp
#include <stdio.h>
#include <unistd.h>

int main() {
    /* fork a child process */
    fork();
    /* fork another child process */
    fork();
    /* and fork another */
    fork();
    return 0;
}
```

{% endraw %}

A：2 的 3 次方個

### 6.3. Q03

Q：Including the initial parent process, how many processes are created by the program shown in Figure 3.32?

{% raw %}

```cpp
#include <stdio.h>
#include <unistd.h>

int main() {
    int i;
    for (i = 0; i < 4; i++)
        fork();
    return 0;
}

```

{% endraw %}

A：2 的 4 次方個

### 6.4. Q04

Q：Original versions of Apple’s mobile iOS operating system provided no means of concurrent processing.  
Discuss three major complications that concurrent processing adds to an operating system.

A：

定義：Concurrent Processing（並行處理）：是指系統同時執行多個程序或執行緒的能力。雖然它能讓系統效率更高，但會帶來一系列新的問題與挑戰。

1. Race Conditions：當多個程序或執行緒**同時存取共享資源**（如變數、記憶體、檔案）時，可能會發生「誰先誰後」影響結果的情況，這稱為 Race Condition。
    - 兩個執行緒同時更新同一個計數器，可能導致計數錯誤。
    - 必須使用鎖（locks）、互斥（mutex）等同步機制保護資源。
2. Deadlocks：當程序互相等待對方釋放資源時，可能會造成系統永遠卡住，這種情況稱為 Deadlock。
    - 序 A 拿到資源 1，等待資源 2；而程序 B 拿到資源 2，也在等待資源 1。
3. 同步與一致性（Synchronization and Data Consistency）：並行處理讓系統更難確保資料的一致性與正確的執行順序。
    - 同程序執行順序改變可能導致結果不同。
    - 使用條件變數（condition variables）、信號量（semaphores）等同步方法，確保程式按正確順序執行。

### 6.5. Q05

Q：Some computer systems provide multiple register sets.  
Describe what happens when a context switch occurs if the new context is already loaded into one of the register sets.  
What happens if the new context is in memory rather than in a register set and all the register sets are in use?

A：

1. 情況一：新的上下文已經在某組暫存器中
    - 作業系統只需「切換指向那組暫存器」。
    - 不需要把舊的暫存器值儲存到記憶體，也不需要從記憶體重新載入新的 context。
2. 情況二：新的上下文還在記憶體中，且所有 register set 都在使用
    - 代表系統無法直接使用任何 register set
    1. 作業系統必須將某一組現有的暫存器內容存回記憶體（稱為 register spilling）。
    2. 然後將新的上下文從記憶體載入到這組暫存器中（register loading）。
    3. 再開始執行新的 process。

### 6.6. Q06

Q：When a process creates a new process using the `fork()` operation, which of the following states is shared between the parent process and the child process?

1. Stack
2. Heap
3. Shared memory segments

A：

1. Stack：❌ 不會共享 → 父子程序在 `fork()` 後會各自有**獨立的 stack**，修改變數互不影響。
2. Heap：❌ 不會共享 → heap 區的資料，如 `malloc()` 分配的記憶體，也會複製到子程序中。彼此獨立。
3. Shared memory segments（共享記憶體區段）：✅ 共享：

### 6.7. Q07

Q：Describe the actions taken by a kernel to context-switch between processes.
A：

1. 儲存目前執行程序的上下文（Context）：將目前 CPU 使用的暫存器（registers）內容儲存起來(儲存位置通常在 程序控制區 PCB)
2. 更新該程序的狀態：例如將它從 Running 更新為 Ready 或 Waiting 狀態
3. 選出下一個要執行的程序：根據某種排程策略（如 Round Robin、Priority Scheduling）從 Ready Queue 中選擇下一個程序
4. 載入新程序的上下文（Context）：從新的程序 PCB 中，讀取先前儲存的暫存器內容
5. 開始執行新的程序

### 6.8. Q8

Q：Using the program in Figure 3.34, identify the values of pid at lines A, B, C, and D. (Assume that the actual pids of the parent and child are 2600 and 2603, respectively.)

{% raw %}

```cpp
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pid, pid1;

    /* fork a child process */
    pid = fork();

    if (pid < 0) {  /* 發生錯誤 */
        fprintf(stderr, "Fork Failed");
        return 1;
    }
    else if (pid == 0) {  /* 子程序 */
        pid1 = getpid();
        printf("child: pid = %d\n", pid);   // A
        printf("child: pid1 = %d\n", pid1); // B
    }
    else {  /* 父程序 */
        pid1 = getpid();
        printf("parent: pid = %d\n", pid);  // C
        printf("parent: pid1 = %d\n", pid1); // D
        wait(NULL);
    }
    return 0;
}
```

{% endraw %}

A：

程式邏輯回顧

-   pid = fork(); 會創造一個子程序。
-   在子程序中，fork() 會回傳 0，所以 pid == 0
-   在父程序中，fork() 會回傳子程序的 pid（此處為 2603）

| 行號 | 說明                     | 顯示內容              | 值     |
| ---- | ------------------------ | --------------------- | ------ |
| A    | 子程序的 `pid` 值        | `child: pid = 0`      | `0`    |
| B    | 子程序自己的 pid         | `child: pid1 = 2603`  | `2603` |
| C    | 父程序中 `pid`（子 pid） | `parent: pid = 2603`  | `2603` |
| D    | 父程序自己的 pid         | `parent: pid1 = 2600` | `2600` |

### 6.9. Q10

Q：What are the benefits and the disadvantages of each of the following? Consider both the system level and the programmer level.

-   Synchronous and asynchronous communication
-   Automatic and explicit buffering
-   Send by copy and send by reference
-   Fixed-sized and variable-sized messages

A：

Synchronous vs. Asynchronous Communication

| 比較項目     | 同步通訊 (Synchronous)                           | 非同步通訊 (Asynchronous)                        |
| ------------ | ------------------------------------------------ | ------------------------------------------------ |
| **系統層級** | 兩端必須同步（送方等收方）較易保證資料正確與順序 | 可提高效率，傳送端不必等待，但需額外資源管理佇列 |
| **程式設計** | 編程較簡單，流程清楚                             | 較複雜，需考慮回呼、通知機制與非同步事件處理     |
| **優點**     | 資料一致性高、易同步                             | 效能高、可以重疊處理工作                         |
| **缺點**     | 容易阻塞（blocking）                             | 難以除錯，狀態管理複雜                           |

Automatic vs. Explicit Buffering

| 比較項目     | 自動緩衝 (Automatic)           | 明確緩衝 (Explicit)                |
| ------------ | ------------------------------ | ---------------------------------- |
| **系統層級** | 系統自動決定何時傳輸效能最佳化 | 開發者控制緩衝與傳送時機           |
| **程式設計** | 開發簡單，不需手動管理         | 可精細調整效能與行為               |
| **優點**     | 使用簡便、不需擔心緩衝溢出     | 可提升效率，適合高效能應用         |
| **缺點**     | 難以預測傳送時機與延遲         | 編寫程式時容易出錯，需小心管理資源 |

Send by Copy vs. Send by Reference

| 比較項目     | 傳值 (Copy)            | 傳參考 (Reference)         |
| ------------ | ---------------------- | -------------------------- |
| **系統層級** | 複製資料造成負擔       | 較省資源，但需同步控制     |
| **程式設計** | 安全，避免共用資料錯誤 | 易出現同步問題與資料競爭   |
| **優點**     | 無副作用，資料獨立     | 效能佳，避免大量資料複製   |
| **缺點**     | 效率低，浪費記憶體     | 需小心共享資料同步與一致性 |

Fixed-sized vs. Variable-sized Messages

| 比較項目     | 固定大小訊息       | 可變大小訊息                     |
| ------------ | ------------------ | -------------------------------- |
| **系統層級** | 實作簡單、效率穩定 | 支援彈性應用，但需額外標記與管理 |
| **程式設計** | 編碼容易，不易出錯 | 需額外考慮長度標記與切割方式     |
| **優點**     | 可預測、快         | 彈性高、適用範圍廣               |
| **缺點**     | 可能浪費空間       | 易發生記憶體錯誤或資料截斷問題   |



