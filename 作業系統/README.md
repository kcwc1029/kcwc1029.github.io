## 1. 章節

-   [Overview](./作業系統：Overview.pdf)
-   [Processes](./作業系統：Processes.pdf)
-   [Threads & Concurrency](./作業系統：Threads%20&%20Concurrency.pdf)
-   [CPU Scheduling](./作業系統：CPU%20Scheduling.pdf)
-   [Synchronization Tools](./作業系統：Synchronization%20Tools.pdf)
-   [Deadlock](./作業系統：Deadlock.pdf)
-   [Main Memory](./作業系統：Main%20Memory.pdf)
-   [Virtual Memory](./Virtual%20Memory.md)
-   [Storage Management](./作業系統：Storage%20Management.pdf)
-   [File System](./作業系統：File%20System.pdf)

## 2. 核心（Kernel）

核心（Kernel）是作業系統中最重要、永遠在運作的核心程式，就像是作業系統的大腦，負責管理整台電腦的資源和行程。具體來說，Kernel要負責：

📦 管理記憶體（Memory）
🧮 分配 CPU 資源（CPU scheduling）
📁 控制檔案系統與資料存取
🛜 負責輸入/輸出裝置的協調（像鍵盤、滑鼠、印表機）
🧑‍💻 負責多個程式同時執行的管理（Multitasking）

雖然Kernel得運作是隱藏在幕後，但它與兩種常見的程式類型有密切關係

| 類型                             | 說明                                     | 舉例                          |
| ------------------------------ | -------------------------------------- | --------------------------- |
| ⚙️ 系統程式（System Programs）       | 幫助使用者與作業系統互動，通常提供工具與介面，但不一定屬於核心的一部分。   | 指令列（Command Line）、設定工具、檔案總管 |
| 🖥️ 應用程式（Application Programs） | 使用者執行的程式，與作業系統無直接關係，但需要經過核心協助才能使用電腦資源。 | Word、Chrome、遊戲、音樂播放器        |


