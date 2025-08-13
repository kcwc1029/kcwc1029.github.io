# a.sh
#!/bin/bash

# 定義一個函式，用於處理 USR1 訊號
do_log_usr1() {
    echo "$(date): user1 signal received" >> /tmp/pa.log
}

# 定義一個函式，用於處理 USR2 訊號
do_log_usr2() {
    echo "$(date): user2 signal received" >> /tmp/pa.log
}

# trap 指令：當收到 USR1 訊號時，執行 do_log_usr1 函式
trap do_log_usr1 USR1

# trap 指令：當收到 USR2 訊號時，執行 do_log_usr2 函式
trap do_log_usr2 USR2

# 無限迴圈，讓腳本持續運行
while true; do
    sleep 1
done