## 1. file system

### 1.1. 如何創建新帳戶

### 1.2. 更改密碼

passwd

### 1.3. 尋找檔案

-   find
-   locate

### 1.4. 硬連結（Hard Link）和軟連結（Soft Link）

-   硬連結是指向文件的物理數據（inode 編號），可以將同一數據與多個文件名關聯。
-   硬連結之間是等價的，刪除任何一個連結，其他連結仍然可以訪問原數據。
-   軟連結是指向另一個文件的路徑（類似於快捷方式）。
-   刪除原文件後，軟連結會變成無效（稱為 "斷開的連結"）。

#### 1.4.1. 建立硬連結

```
touch file.txt
# 創建一個名為 hardlink.txt 的硬連結，與 file.txt 指向同一數據塊。
ln file.txt hardlink.txt
# 查看 inode 編號
ls -li file.txt hardlink.txt #  inode 編號相同
```

#### 1.4.2. 建立軟連結

```
ln -s file.txt softlink.txt

<!-- 562949955470125 -rwxrwxrwx 1 kcwc1029 kcwc1029 0 Dec 24 15:39 file.txt
562949955470126 lrwxrwxrwx 1 kcwc1029 kcwc1029 8 Dec 24 15:42 softlink.txt -> file.txt -->
```

### 1.5. 檔案權限

-   每個文件或目錄的權限由以下三種類型組成：

| 符號 | 權限類型        | 說明                               |
| ---- | --------------- | ---------------------------------- |
| `r`  | 讀取（Read）    | 文件內容可被讀取                   |
| `w`  | 寫入（Write）   | 文件內容可被修改                   |
| `x`  | 執行（Execute） | 文件可被執行（用於程式文件或腳本） |

-   每個文件的權限可以針對以下三個級別的使用者進行設置：

| 符號 | 級別           | 說明                     |
| ---- | -------------- | ------------------------ |
| `u`  | 用戶（User）   | 文件的所有者             |
| `g`  | 群組（Group）  | 與所有者在同一群組的用戶 |
| `o`  | 其他（Others） | 系統中的其他所有用戶     |

-   可以使用 `ls -l` 命令查看文件的權限信息。

```
-rwxr-xr--

`-`：文件類型（`-` 表示普通文件，`d` 表示目錄）。
`rwx`：文件所有者（user）的權限（讀、寫、執行）
`r-x`：文件所在群組（group）的權限（讀、執行）。
`r--`：其他用戶（others）的權限（只有讀權限）。
```

### 1.6. 修改文件權限

-   符號法

```
chmod u+rwx file.txt   # 增加所有者的讀、寫、執行權限
chmod g-w file.txt     # 移除群組的寫權限
chmod o+x file.txt     # 增加其他用戶的執行權限
```

-   數字法（八進位制）

```
`rwx = 7`，`rw- = 6`，`r-- = 4`
chmod 755 file.txt   # 所有者: rwx（7），群組: r-x（5），其他: r-x（5）
chmod 644 file.txt   # 所有者: rw-（6），群組: r--（4），其他: r--（4）
```

### 1.7. 檢查當前用戶的群組

-   groups

### 1.8. 文件所有權（File Ownership）

-   可以使用 ls -l 查看文件的所有權信息

```
-rwxr-x--- 1 alice developers 1024 Nov 23 10:00 file.txt
alice：文件的用戶所有者。
developers：文件的群組所有者。
```

-   修改用戶所有者

```
# 將 file.txt 的所有者更改為 bob
sudo chown bob file.txt

# 一次修改用戶和群組所有者
# sudo chown [新用戶]:[新群組] 文件名
sudo chown bob:admins file.txt
```

-   修改群組所有者

```
# 將 file.txt 的所有者更改為 bob
sudo chown bob file.txt

# 如果需要修改目錄及其所有子目錄和文件的所有權，可以使用 -R
# 將 /path/to/directory 及其子文件的所有者更改為 alice，群組更改為 developers
sudo chown -R alice:developers /path/to/directory

```

### 1.9. 向檔案添加文字

#### 1.9.1. 使用 echo 命令

```
# 覆寫模式
echo "123" > file.txt

# 追加模式
echo "456" >> file.txt

```

#### 1.9.2. 使用 cat 命令

```
# 覆寫模式
cat > file.txt

# 追加模式
cat >> file.txt

```

### 1.10. Pipe

```
# 將 ls 的輸出傳遞給 grep，篩選包含 .txt 的文件：
ls | grep ".txt"

# 使用 wc -l 計算文件或輸出的行數
cat file.txt | wc -l

# 顯示文件內容，按行排序並去重
cat file.txt | sort | uniq

# 查找指定進程：列出所有正在運行的進程，並過濾出包含 apache 的進程
ps aux | grep "apache"

# 列出當前目錄下文件大小，並顯示前 5 個最大文件：
du -h | sort -hr | head -n 5

```

### 1.11. 比較文件的內容

#### 1.11.1. diff 命令

```
# 比較兩者文件
diff file1.txt file2.txt

# 忽略大小寫
diff -i file1.txt file2.txt

# 只顯示是否不同（不顯示詳細差異）
diff -q file1.txt file2.txt
```

#### 1.11.2. cmp 命令

-   按字節（byte-by-byte）比較兩個文件。
-   更適合用於比較二進制文件。

```
cmp file1.txt file2.txt

```

### 1.12. 打包壓縮

-   tar + gzip 組合

```
# 打包並壓縮
tar -czvf archive.tar.gz file1 file2 dir/

# 解壓 .tar.gz 文件
tar -xzvf archive.tar.gz
```

-   zip 和 unzip

```
# 打包並壓縮
zip -r archive.zip file1 file2 dir/

# 解壓 .tar.gz 文件
unzip archive.zip
```

## 2. System Administration

### 2.1. user accobnt amnagement

```
# 添加新用戶
# useradd [選項] 用戶名
sudo useradd -m -s /bin/bash 用戶名

# 用於創建新組
# sudo groupadd 組名

# 刪除用戶
sudo userdel -r 用戶名

# 用於刪除組
sudo groupdel 組名
```

-   假設要創立一個新的帳戶
    -   名稱：bob
    -   密碼：bob
    -   組別：bob

```
#創建用戶並設置主目錄和 Shell。
sudo useradd -m -s /bin/bash bob
#為用戶設置密碼。
sudo passwd bob
#將用戶添加屬於自己的組
sudo groupadd bob
sudo usermod -g bob bob
#將用戶添加到需要的組，例如 sudo。
# sudo usermod -g 要加入的組 帳號
sudo usermod -g bob sudo
#確保主目錄的所有權和權限正確。
sudo usermod -g sudo bob
#測試用戶環境。
su - bob

# 總體確認
# 查看用戶信息：
id bob
# 查看 /etc/passwd 是否有 bob
cat /etc/passwd | grep bob

# 查看 /etc/group 是否有 bob：
cat /etc/group | grep bob

# 查看主目錄權限：
ls -ld /home/bob

```

### 密碼管理策略

-   /etc/login.defs 文件：定義了全局的密碼策略，主要影響 useradd 創建新用戶時的默認設置。

```
vim /etc/login.defs
```

### 用戶與活動監控

-   who：顯示當前登錄的用戶
-   last：顯示最近登錄的用戶記錄

### Linux 用戶之間的溝通命令

-   三個與用戶溝通相關的命令，分別是 users、wall 和 write，以及它們的用法與功能。

#### users 命令

-   僅列出當前登錄的用戶名，不顯示其他信息。

```
users

```

#### wall 命令

-   向所有當前登錄的用戶廣播消息。

```
echo "系統將於5分鐘後重啟" | wall
```

### 顯示或設置系統的日期和時間

```
data
```

### 顯示系統已運行的時間、當前時間、登錄用戶數以及平均負載

```
uptime
17:22:29 up  6:51,  2 users,  load average: 0.10, 0.11, 0.09
```

### 顯示或設置系統的主機名

```
hostname
kcwc1029-VMware-Virtual-Platform

hostname -I
192.168.44.128
```

-   當前主機名存放路徑：`cat /etc/hostname`
-   更改主機名稱：`hostnamectl set-hostname 新主機名稱`

### systemctl Command

-   systemctl 是管理和控制系統服務（services）的新工具，主要用於管理 systemd 單元（units）

```
# 列出所有單元
systemctl list-units --all

systemctl start <service-name>.service   # 啟動服務
systemctl stop <service-name>.service    # 停止服務
systemctl status <service-name>.service # 檢查服務狀態
systemctl enable <service-name>.service  # 開機自啟動
systemctl disable <service-name>.service # 禁止開機自啟動
systemctl restart <service-name>.service # 重啟服務
systemctl reload <service-name>.service  # 重新加載配置
```

### ps

-   ps 是 Linux 系統中的一個命令，用於顯示有關當前運行中的進程狀態的信息（Process Status）

```
# 僅顯示當前 shell 的進程
ps
# 查看所有進程
ps aux

# 顯示某用戶的所有進程
ps -u <username>

# 與 kill 配合結束進程
ps -e | grep <process_name>
kill <PID>
```

### top

-   top 是一個動態顯示 Linux 系統中正在運行的進程及其資源使用情況的命令。
-   它可以顯示 CPU、內存等資源的實時使用狀況。
-   常見快捷鍵
    -   P：按 CPU 使用率排序。
    -   M：按內存使用率排序。

```
top
```

-   也可以使用 htop 替代

```
sudo apt install htop
htop
```

### kill

-   kill 命令用於向進程發送信號，最常見的用途是終止進程。
-   通過指定進程 ID (PID) 和信號，系統可以執行特定的操作，例如終止進程或發送其他信號。

```
# 列出所有信號
kill -l

# 終止進程
kill 1234

# 強制終止進程 如果進程無法正常關閉
kill -9 1234

# 重啟進程 通過 SIGHUP 信號重啟進程
kill -1 1234

```

### 查找系統資訊

-   `uname -a`：顯示系統的核心資訊，包括主機名稱、核心版本、操作系統名稱
-   `sudo dmidecode`：更詳細的資訊
-   `arch`：查詢系統架構

### 環境變數

-   `env`：查看所有環境變數
-   `echo $LC_TIME`：查看單個環境變數

#### 永久設置用戶級環境變數

```
vim ~/.bashrc
export TEST='123'
source ~/.bashrc
echo $TEST
```

#### 永久設置全局環境變數

```
sudo vim /etc/profile
export TEST='123'
source /etc/profile
echo $TEST

```

## screen 指令

-   是一個終端多工工具，可以讓你在一個終端會話中運行多個進程，並允許你在斷開連線（例如 VPN 中斷或網絡故障）後重新連接到這些進程。
-   就是類似在原本的終端機中，在開終端機的感覺。
-   電源問題 (Power Issues)： 如果你的設備意外斷電，未保存的進程會被終止。使用 screen，進程仍會在後台運行，重啟後可以重新連接。
-   VPN 中斷 (VPN Drop)： 如果你使用遠程連線操作伺服器，VPN 或網絡中斷會導致進程終止。screen 可以確保進程不受影響。
-   網絡問題 (Network Issues)： 在遠端伺服器運行長時間任務時，網絡不穩定可能導致你失去連線。screen 可以在你斷開連線時保持進程運行。

```
# 使否安裝
screen --version

# 安裝方式
sudo apt update
sudo apt install screen

# 開啟一個會話(session)
screen
screen -S session_name # 自己定義會話名稱

# 斷開會話但保持進程運行
使用快捷鍵Ctrl + A + D
```

```
# 查詢所有會話
screen -ls

# 會輸出
# There are screens on:
#         48895.session_name      (12/26/24 15:43:07)     (Detached)
#         48871.pts-1.kcwc1029-VMware-Virtual-Platform    (12/26/24 15:42:42)     (Detached)
# 2 Sockets in /run/screen/S-kcwc1029.
#
# 前面48895是會話ID
# 後面是會話名稱

# 要返回該會話
screen -r session_name(就是48895.session_name這全部)

# 要終止當前對話：
exit

# 刪除會話：如果不再需要某個會話
screen -S 48555 -X quit

```

```
# 共享會話： 允許多個用戶連接到同一會話，適用於協作。
screen -x session_name
```

## linux kernal

![upgit_20241226_1735201986.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/12/upgit_20241226_1735201986.png)

### Shell 是什麼

-   Shell 是一種介面 (Interface)，作為使用者與作業系統核心 (Kernel/OS) 的橋樑。
-   它提供了一個容器 (Container)，使用者可以透過它與作業系統進行互動。
-   命令列介面 (Command Line Interface, CLI) 就是一種 Shell。

```
# 查找自己的shell
echo $0

# 查看你的預設 Shell
cat /etc/passwd

# 檢查系統中可用的 Shell
cat /etc/shells
```

### 什麼是 Shell Script

-   Shell Script 是一種可執行的文件，其中包含多個 shell 命令，這些命令按照順序執行。
-   它作為一種腳本語言，適合自動化日常任務，例如文件操作、系統管理、批量處理。

### Shell Script 的結構

-   Shell: 每個 Shell script 都需要在文件開頭指定解釋器。通常用 `#!/bin/bash`。
-   註解: 使用 # 來添加註解，幫助其他人或自己未來理解腳本的邏輯。
-   命令: 常見的命令包括 echo (打印信息)、cp (複製文件)、grep (搜尋文本) 等。
-   語句: 可以包含條件語句 (if)、迴圈 (for, while) 來實現邏輯控制。
-   會需要添加執行權限：chmod 755 script01

-   超級簡單腳本：輸出 hello linux

```bash
#!/bin/bash
# 這是一個範例 Shell script

echo "Hello, linux!"  # 打印信息
```

### 腳本：輸出一些小資訊

```bash
#!/bin/bash
# 定義一些小任務

whoami
echo
pwd
echo
hostname
echo
ls -al
echo
```

### 腳本：練習使用變數

```bash
#!/bin/bash
# 練習使用變數
a=TA1
b=TA2
c="TA 3"

echo "我的助教是$a "
echo "$a 是最可愛的"
echo "$a 是最帥氣的"
```

### 腳本：script 寫入

```bash
#!/bin/bash
# 練習輸入輸出
a=$(hostname)  # 設置變數 a 為主機名
echo "Hello, my name is $a."
echo "What are your first name and last name?"  # 提示用戶輸入
read first_name last_name  # 讀取兩個參數，分別存到 first_name 和 last_name
echo "Hello, $first_name $last_name!"
```

### 腳本：if else

-   -gt：大於（greater than）
-   -lt：小於（less than）
-   -ge：大於或等於（greater than or equal）
-   -le：小於或等於（less than or equal）

```bash
#!/bin/bash
# 檢查輸入的數字
echo "請輸入一個數字："
read number  # 讀取用戶輸入

if [ $number -gt 0 ]
then
    echo "$number 是正數"
elif [ $number -lt 0 ]
then
    echo "$number 是負數"
else
    echo "$number 是零"
fi
```

### 腳本：for

```bash
#!/bin/bash
# 輸出數字迴圈
for i in 1 2 3 4 5  # 定義數字序列
do
    echo "Welcome $i times"  # 對每個數字輸出歡迎語
done
```

```bash
#!/bin/bash
# 輸出數字迴圈
for i in {1..5}  # 使用範圍表示法
do
    echo "Welcome $i times"  # 對每個數字輸出歡迎語
done
```

```bash
#!/bin/bash
# 輸出字串迴圈
for i in eat run jump play  # 定義字串序列
do
    echo "See Imran $i"  # 對每個字串執行操作
done
```

### 腳本：case

```bash
#!/bin/bash
# 使用者選擇操作
echo "請輸入一個選項："
echo "1) 啟動服務"
echo "2) 停止服務"
echo "3) 重啟服務"
echo "4) 退出"
read choice  # 讀取使用者輸入

case $choice in
    1)
        echo "正在啟動服務..." ;;
    2)
        echo "正在停止服務..." ;;
    3)
        echo "正在重啟服務..." ;;
    4)
        echo "退出程式"
        exit 0 ;;
    *)
        echo "無效的選項，請重新輸入" ;;
esac
```

```bash
#!/bin/bash
# 實現簡單的計算器
echo "選擇操作："
echo "add) 加法"
echo "sub) 減法"
echo "mul) 乘法"
echo "div) 除法"
read operation

case $operation in
    add)
        echo "輸入兩個數字："
        read a b
        echo "結果：$((a + b))" ;;
    sub)
        echo "輸入兩個數字："
        read a b
        echo "結果：$((a - b))" ;;
    mul)
        echo "輸入兩個數字："
        read a b
        echo "結果：$((a * b))" ;;
    div)
        echo "輸入兩個數字："
        read a b
        if [ $b -eq 0 ]; then
            echo "錯誤：除數不能為 0"
        else
            echo "結果：$((a / b))"
        fi ;;
    *)
        echo "無效的操作" ;;
esac
```

### 腳本：單個 IP 地址檢測

```bash
#!/bin/bash
# 單個 IP 地址檢測
echo 請輸入要檢測的ip
read hosts
ping -c1 $hosts &> /dev/null  # 發送一個 ICMP 請求到指定的 IP 地址，不顯示輸出
if [ $? -eq 0 ]  # 判斷上一條命令是否成功，$? 表示上一條命令的返回值
# 0 表示成功，非 0 表示失敗
then
    echo "OK"  # 如果成功，輸出 OK
else
    echo "NOT OK"  # 如果失敗，輸出 NOT OK
fi

```

### 腳本：檢測多個 IP 地址

-   先建立一個 txt，裡面要要檢測的 IP

```
192.168.1.1
192.168.1.2
192.168.1.3
192.168.1.235
```

```bash
#!/bin/bash
# 檢測多個 IP 地址
IPLIST="path_to_the_Ip_list_file"  # 定義包含多個 IP 地址的文件路徑

for ip in $(cat $IPLIST)  # 逐行讀取文件中的 IP 地址
do
   ping -c1 $ip &> /dev/null  # 對每個 IP 發送一次 ping 請求
   if [ $? -eq 0 ]
   then
       echo "$ip ping passed"  # 如果成功，輸出通過
   else
       echo "$ip ping failed"  # 如果失敗，輸出失敗
   fi
done
```

## history 指令

-   history 指令用於顯示當前終端中的指令歷史紀錄。

```
#  顯示歷史命令
history

# 顯示最近的 N 條命令
history N

# 執行特定編號的命令
!<編號>

# 使用 grep 搜索
history | grep <關鍵字>

# 清除歷史紀錄（僅當前 session）
history -c

# 保存歷史紀錄(將當前 session 的命令歷史寫入 .bash_history 文件。)
history -w

# 查看 .bash_history 文件
cat ~/.bash_history

# 手動查看歷史命令記錄文件
cat ~/.bash_history

```

## 讓 VM 虛擬機可以被外部其他裝置訪問到

-   動機：在成大實驗室的電腦，IP 是靜態 IP，那我希望我的虛擬機也可以讓外部去訪問到。
-   如果您的伺服器需要被外部設備訪問，您可以選擇以下兩種方法：
    -   使用 Bridged 模式(但我在猜想，可能是網路管制之類的，他這邊我只要一選擇 bridge，虛擬機網路就直接死給你看)
    -   如果您仍想使用 NAT 模式，也可以通過配置端口轉發（Port Forwarding）來實現外部設備訪問虛擬機內的伺服器。

### 配置端口轉發（Port Forwarding）

-   打開 Virtual Network Editor，選擇 NAT 網絡（如 VMnet8）。
-   點擊 NAT Settings，進入端口轉發設置。
-   添加一條端口映射規則：
    -   協議：選擇 TCP 或 UDP。
    -   主機端口（Host Port）：設置主機上的對外端口，例如 8080。
    -   虛擬機 IP（Virtual Machine IP）：填寫虛擬機的 IP 地址（例如 192.168.44.128）。
    -   虛擬機端口（Virtual Machine Port）：設置虛擬機伺服器的端口，例如 80。
-   保存設置並重啟虛擬機。

![upgit_20250101_1735716951.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250101_1735716951.png)

![upgit_20250101_1735717044.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250101_1735717044.png)

### 測試

-   在虛擬機內啟動終端，下指令`sudo python3 -m http.server 80
`
-   在虛擬機內執行以下命令，確認伺服器是否正常運行`curl http://localhost:80`
-   從 PC 或其他裝置測試主機能否通過端口轉發訪問虛擬機內的伺服器`curl http://192.168.44.128:8080`

## Network service

### Network Components

#### IP (Internet Protocol Address)

-   IP 是用來標識網絡上的每個設備的唯一地址，分為 IPv4 和 IPv6 兩種類型。
    -   IPv4: 格式為 192.168.1.1，由四段數字組成（32 位）。
    -   IPv6: 格式為 2001:0db8:85a3:0000:0000:8a2e:0370:7334（128 位），用於解決 IPv4 地址枯竭問題。
-   如何查詢 IP 地址：
    -   Windows: 在命令提示符輸入 ipconfig。
    -   Linux/Unix: 在終端輸入 ip addr 或 ifconfig。

#### Subnet Mask

-   子網掩碼用來劃分網絡和主機部分，幫助確定設備是否在同一網段中。
-   例如，子網掩碼 255.255.255.0 表示網段中的最後一段用於標識主機。

![upgit_20250101_1735717440.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250101_1735717440.png)

#### Gateway

-   網關是設備連接到其他網段（如互聯網）的出口。
-   在一個本地網絡中，默認網關通常是路由器的 IP 地址（如 192.168.1.1）。
-   查詢默認網關：
    -   Windows: 在 ipconfig 輸出中找到 Default Gateway。
    -   Linux: 使用 route -n 或 ip route。

### 常見的網絡命令

```bash
# 測試主機之間的連通性，驗證目標設備是否可以到達
ping <目標IP地址或域名>
ping 8.8.8.8   # 測試與 Google DNS 的連通性
ping www.google.com   # 測試與 Google 網站的連通性

# -c <次數>：指定發送的數據包次數
ping -c 4 8.8.8.8
```

```bash
# 顯示網絡連接、路由表、接口統計等信息（舊工具，部分功能已被 ss 取代）
netstat -a       # 查看所有網絡連接
netstat -tuln    # 查看所有正在監聽的端口
netstat -r       # 查看路由表

# -t：顯示 TCP 連接。
# -u：顯示 UDP 連接。
# -l：顯示正在監聽的端口。
# -n：以數字形式顯示地址和端口。
```

```bash
# 捕獲和分析網絡流量（非常強大的網絡調試工具）
sudo tcpdump    # 捕獲所有網絡流量
sudo tcpdump -i eth0    # 捕獲指定接口 eth0 的流量

# 捕獲特定主機的流量
sudo tcpdump host 192.168.1.1

# 捕獲特定端口的流量
sudo tcpdump port 80
```

```bash
# 用於跟蹤數據包從本地主機到目標主機的路徑
traceroute 8.8.8.8

```

```bash
# 用於測試 DNS 查詢：dig 或 nslookup
dig www.google.com
nslookup www.google.com

```

### Interface Configuration Files（網絡接口配置文件）

-   配置網絡設置的核心文件，用於管理主機名、DNS、子網掩碼等信息
-   `/etc/nsswitch.conf`：控制系統如何解析主機名（如通過 DNS、文件或其他服務）
-   `/etc/resolv.conf`：配置 DNS 服務器地址。
-   `/etc/hostname`：儲存系統的主機名。

```
// 編輯主機名
sudo nano /etc/hostname

// 修改後重啟生效
sudo systemctl restart systemd-hostnamed
```

-   `/etc/sysconfig/network`：配置全局網絡設置（僅適用於部分 Linux 發行版，如 CentOS）
-   `/etc/sysconfig/network-scripts/ifcfg-nic`：管理特定網絡接口的設置（例如 ifcfg-eth0）

### 網絡介面卡（NIC, Network Interface Card）

-   網絡介面卡是計算機用於連接網絡的硬件設備，它負責設備和網絡之間的數據傳輸。

```bash
(base) kcwc1029@kcwc1029-VMware-Virtual-Platform:~$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:0d:47:65 brd ff:ff:ff:ff:ff:ff
    altname enp2s1
    inet 192.168.153.128/24 brd 192.168.153.255 scope global dynamic noprefixroute ens33
       valid_lft 1704sec preferred_lft 1704sec
    inet6 fe80::fd2b:bd4a:14f9:2742/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

-   ens33 就是一個實際的網路介面，用於連接到局域網或外部網路
    -   它有一個 IPv4 地址：192.168.153.128/24，並且顯示此地址是動態分配的(DHCP)。
    -   還有一個 IPv6 地址：fe80::fd2b:bd4a:14f9:2742/64，這是連接範圍內的鏈路本地地址。
    -   使用 ethtool 檢查和管理網卡屬性：`ethtool ens33`

```bash
(base) kcwc1029@kcwc1029-VMware-Virtual-Platform:~$ ethtool ens33
Settings for ens33:
	Supported ports: [ TP ] # 網卡支持的端口類型。TP代表 Twisted Pair（雙絞線），即網線
	Supported link modes:   10baseT/Half 10baseT/Full # 支援的鏈路模式
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Full
	Supported pause frame use: No
	Supports auto-negotiation: Yes
	Supported FEC modes: Not reported
	Advertised link modes:  10baseT/Half 10baseT/Full
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Full
	Advertised pause frame use: No
	Advertised auto-negotiation: Yes
	Advertised FEC modes: Not reported
	Speed: 1000Mb/s # 當前鏈路速率為 1000 Mbps（1 Gbps）。
	Duplex: Full # 當前鏈路是全雙工模式（Full Duplex）
	Auto-negotiation: on
	Port: Twisted Pair
	PHYAD: 0
	Transceiver: internal
	MDI-X: off (auto)
netlink error: Operation not permitted
        Current message level: 0x00000007 (7)
                               drv probe link
	Link detected: yes # 表示網卡目前檢測到有效的網絡連接
```

-   lo (Loopback Device)
    -   是一個特殊的虛擬網絡接口，稱為 迴環設備。它的作用是讓設備可以與自己進行通信
    -   用於本地測試和診斷（不經過實體網卡）。
    -   本地服務（如 Web 伺服器）可以通過 127.0.0.1 訪問。
-   Virtual Bridge：
-   是一個虛擬橋接接口，通常由虛擬化軟件（如 VirtualBox、VMware 或 KVM）創建。
-   用於 NAT（網絡地址轉換） 模式，幫助虛擬機連接到外部網絡。

![upgit_20250101_1735719508.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250101_1735719508.png)

-   在虛擬化環境中，VMnet0、VMnet1 和 VMnet8 是 VMware 提供的三種常見虛擬網絡類型，用於幫助虛擬機器與主機或外部網絡進行通信。
-   VMnet0 (Bridged Mode - 橋接模式)
    -   橋接模式讓虛擬機直接與主機的物理網絡（實體網卡）進行通信。
    -   虛擬機就像是局域網中的一個獨立設備，擁有自己的 IP 地址（與主機的網絡相同）
    -   虛擬機作為 Web 伺服器
-   VMnet1 (Host-Only Mode - 主機專用模式)
    -   主機專用模式將虛擬機與主機連接在一個私有的虛擬網絡中。
    -   虛擬機之間可以通信，且可以與主機通信，但無法直接連接到外部網絡。
-   VMnet8 (NAT Mode - 網絡地址轉換模式)
    -   NAT 模式允許虛擬機通過主機的網絡接口與外部網絡通信。
    -   主機作為虛擬機的網關，負責將虛擬機的流量轉發到外部網絡。
    -   虛擬機可以訪問外部網絡，但外部設備無法直接訪問虛擬機。
    -   支持端口轉發，允許外部設備通過主機的 IP 和指定端口訪問虛擬機。

### curl 指令

-   用於向網絡服務發送請求並接收數據，常用於調試 API、下載文件或檢查網絡連接。

```bash
# 發送 GET 請求：獲取 URL 的內容（默認為 GET 請求）
curl https://example.com

# 指定 HTTP 方法
# - GET 請求
curl -X GET https://example.com

# - POST 請求
curl -X POST https://example.com

# 用於 POST 或 PUT 請求時，傳遞 JSON 或表單數據
curl -X POST https://example.com -d "key1=value1&key2=value2"

# 模擬表單提交
curl -X POST https://example.com/login \
-d "username=user&password=pass"


# 下載文件：將內容保存到文件中
curl -o filename.html https://example.com

# 上傳文件
curl -X POST https://example.com/upload \
-F "file=@path/to/file.txt"

# 將 API 的 JSON 響應保存到文件中
curl -X GET https://api.example.com/data -o result.json

```

### wget 指令

-   用於從網絡下載文件或資源。它支持 HTTP、HTTPS 和 FTP 協議
-   特別適合於自動化下載或大批量下載任務。

```bash
# 下載單個文件：下載指定 URL 的文件到當前目錄
wget http://example.com/file.txt

# 將下載的文件保存到特定目錄
wget -P /path/to/directory http://example.com/file.txt

# 如果下載過程中斷，可以使用 -c 繼續下載
wget -c http://example.com/largefile.zip
```

## FTP - 檔案傳輸協定

-   誰需要接收文件，誰就需要安裝並配置適合的服務來實現文件傳輸
-   主要需求是 win 傳輸給 ubuntu，因此要在 ubuntu 上裝 FTP 服務

### 在 Ubuntu 上安裝 vsftpd

```bash
# 打開終端並安裝 vsftpd
sudo apt update
sudo apt install vsftpd -y

# 啟動 vsftpd 服務
sudo systemctl start vsftpd
sudo systemctl enable vsftpd

# 檢查服務狀態
sudo systemctl status vsftpd

# 配置 vsftpd
sudo vim /etc/vsftpd.conf
```

### 在 Windows 上配置 FTP 客戶端

-   port：21
-   https://filezilla-project.org/download.php?type=client

![upgit_20250101_1735728672.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250101_1735728672.png)
![upgit_20250102_1735805799.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250102_1735805799.png)

## SCP(Secure Copy Protocol)協定

-   用於在本地和遠程主機之間安全地傳輸文件
-   默認使用 SSH 協議的端口 22

### 在 Ubuntu 虛擬機上，安裝並啟動 SSH 服務

```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl start ssh
sudo systemctl enable ssh

# 確認SSH服務正在運行
sudo systemctl status ssh

# 查找Ubuntu虛擬機的IP地址
ip addr # 192.168.153.128
```

### 從 Windows 複製文件到 Ubuntu 虛擬機

-   使用內建的 scp 命令：打開 PowerShell 或 CMD，測試是否能使用 scp
-   將本地文件複製到虛擬機

```bash
scp .\scp_send_file.pdf kcwc1029@192.168.153.128:/home/kcwc1029/Desktop
```

### 從 Ubuntu 虛擬機複製文件到 Windows

```bash
scp kcwc1029@192.168.153.128:/home/kcwc1029/Desktop/scp_send_file.pdf  .\
```

![upgit_20250102_1735808785.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/01/upgit_20250102_1735808785.png)

### 小總結

-   SSH(Secure Shell)：遠程操作、管理伺服器。
-   SCP(Secure Copy Protocol)：適用場景：需要一次性、安全地傳輸文件或目錄。通過 SSH 加密通道傳輸，快速且安全性高。
-   FTP(File Transfer Protocol)：傳輸大量文件，提供圖形界面、批量操作的支持

## DNS

-   將域名（例如 www.google.com）轉換為對應的IP 地址（例如 142.250.190.78）的系統。
-   就像互聯網的電話簿，讓人們用容易記住的名字（域名）訪問網站，而不需要記住難以記憶的 IP 地址。

### DNS 記錄類型

-   PTR Record（Pointer Record）：IP to hostname
    -   使用場景：反向 DNS 查詢（Reverse DNS Lookup）。
    -   例子：192.168.1.1 → server.example.com
-   A Record（Address Record）
    -   hostname to IP
    -   例子：www.example.com → 192.168.1.1
-   CNAME Record（Canonical Name Record）
    -   功能：將 主機名稱 映射到另一個 主機名稱。
    -   使用場景：設置別名。例如，www 可能是 example.com 的別名。
    -   例子：www.example.com → alias.example.com

### 安裝和確認 DNS 伺服器軟體 Bind9

-   太難了拉，偶不會

### DNS 查詢工具 nslookup

```bash
(openai) PS D:\github\blog> nslookup www.es.ncku.edu.tw
伺服器:  apple.tnrc.edu.tw # 這個DNS伺服器接收你的請求，並查詢www.es.ncku.edu.tw 的對應 IP 地址
Address:  163.28.113.1

未經授權的回答:             # 表示該回應來自快取 DNS 伺服器，而不是權威 DNS 伺服器
名稱:    www.es.ncku.edu.tw # 你查詢的完整域名 www.es.ncku.edu.tw
Address:  140.116.78.118    # 對應的 IPv4 地址 140.116.78.118
```

## NTP - 時間同步的協議

-   NTP (Network Time Protocol) 是一種用於時間同步的協議，主要功能是使電腦的時鐘與網路上的伺服器保持一致。
-   定期向一個可信的「時間伺服器」（例如 Google 的 NTP 伺服器 time.google.com）請求精準的時間。
-   調整本地機器的時間，讓它與時間伺服器保持一致。
-   應用在分布式系統中的正確時間標記。
-   這個我現在也不太懂，未來有碰到分布式系統再來看看好了 XD

```bash
sudo apt-get update
sudo apt-get install ntp

# 編輯配置文件 /etc/ntp.conf
sudo nano /etc/ntp.conf


# 在文件中添加或確認以下內容
# 指定 NTP 伺服器
server 0.ubuntu.pool.ntp.org iburst
server 1.ubuntu.pool.ntp.org iburst
server 2.ubuntu.pool.ntp.org iburst
server 3.ubuntu.pool.ntp.org iburst

# 重啟服務以應用更改
sudo systemctl restart ntp

# 檢查 NTP 同步狀態
ntpq -p
```

## Mail Transfer Agent 郵件傳輸代理

-   Mail Transfer Agent (MTA)：又稱為郵件傳輸代理，是電子郵件系統中的核心組件，負責在不同的電子郵件伺服器之間傳輸電子郵件。
-   MTA 是處理郵件傳輸的專門軟體，它確保電子郵件能從發送者傳輸到接收者的郵件伺服器。
-   MTA 使用 SMTP（簡單郵件傳輸協議）在不同伺服器之間傳輸郵件，SMTP 是 MTA 傳輸郵件的標準協議。

### MTA 的基本功能

1. 接收郵件：從用戶的郵件客戶端（如 Outlook、Gmail 等）或其他郵件伺服器接收電子郵件。
2. 路由郵件：根據郵件地址解析規則，將郵件轉發至下一個 MTA 或目標伺服器。
3. 投遞郵件：將郵件送達最終的目標郵件伺服器，供收件人檢索。
4. 錯誤處理：當郵件無法送達時，生成錯誤回報或通知。

### MTA 的工作流程

-   用戶撰寫一封郵件，並透過郵件客戶端（如 Thunderbird 或 Gmail）發送
-   郵件客戶端將郵件發送到本地的 MTA（如 Postfix）
-   本地 MTA 檢查目標郵件地址，並根據 DNS（域名系統）查找接收方的郵件伺服器（使用 MX 記錄）。
-   本地 MTA 通過 SMTP 協議將郵件傳輸到接收方的 MTA。
-   接收方的 MTA 將郵件存儲到郵件存儲系統（如 Mailbox），供用戶檢索。

### 在 Ubuntu 上安裝 Postfix、s-nail(未來有使用到在學即可)

## Web 伺服器 httpd

-   Apache HTTP Server 通常被稱為 httpd
-   配置文件：/etc/httpd/conf/httpd.conf
-   默認網頁目錄：/var/www/html/index.html

```
# 安裝 Apache（httpd）
sudo apt update
sudo apt install apache2 -y

# 啟動 Apache
sudo systemctl start apache2
sudo systemctl enable apache2

# 測試 Web Server
# 打開瀏覽器，訪問 http://localhost 或伺服器 IP 地址。
# 如果顯示 Apache 的默認網頁，說明服務正常運行。

# 修改主頁文件
# 編輯默認主頁文件：
sudo nano /var/www/html/index.html
```

## Nginx

-   是一款高性能的 Web 伺服器和反向代理伺服器
-   能處理大量的 HTTP 請求，適合高流量網站。
-   以高效處理靜態資源（如 HTML、圖片、CSS 等）著稱。
-   提供標準的 HTTP 網頁服務
-   Nginx 的主要配置文件位於 /etc/nginx/nginx.conf
-   網站相關的配置文件通常位於 /etc/nginx/sites-available/ 和 /etc/nginx/sites-enabled/。

```
# 安裝 Nginx
sudo apt update
sudo apt install nginx -y

# 啟動 Nginx 服務
sudo systemctl start nginx
sudo systemctl enable nginx

# 測試 Nginx 是否正常運行
# 打開瀏覽器，訪問 http://localhost 或伺服器的 IP 地址。如果看到 Nginx 的默認頁面，說明安裝成功。
```
