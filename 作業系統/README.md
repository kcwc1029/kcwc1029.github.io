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

| 比較面向     | PCS（行程層級競爭）                                | SCS（系統層級競爭）            |
| ------------ | -------------------------------------------------- | ------------------------------ |
| 控制彈性     | 高（使用者程式控制）                               | 低（kernel 控制）              |
| 效能         | 高（context switch 少）                            | 較低（kernel 介入多）          |
| 相容性       | 需配合使用者程式排程策略                           | 與作業系統一致，穩定性好       |
| 搶不到 CPU？ | 可能造成整個 process 被餓死（因為 process 不被排） | 不會（每個 thread 都公平競爭） |
