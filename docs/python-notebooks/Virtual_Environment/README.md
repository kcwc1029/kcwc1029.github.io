# 虛擬環境

在程式開發或 Python 生態系中，這個詞通常指獨立的環境，用來安裝套件、避免不同專案之間的衝突。

想像你家有許多獨立的實驗室。如果你在「蛋糕實驗室」裡放了大量麵粉（特定版本的套件），這堆麵粉絕對不會跑進隔壁的「炸雞實驗室」，這樣你研發炸雞時就不會被麵粉干擾配方。這就是隔離。

> 如果你今天要在同一個廚房（你的電腦）裡，同時準備『麻辣鍋』跟『草莓蛋糕』，如果不小心把麻辣醬沾到蛋糕上，是不是就毀了？
> 在寫程式時也一樣！我們未來會寫很多不同的專案（例如：記帳程式、AI 機器人）。如果我們把所有的工具和材料（套件）都丟在電腦的同一個大空間裡，它們的版本可能會『互相打架、互相干擾』
> 所以，Python 提供了一個超棒的功能叫做『虛擬環境』，它就像是幫你的每一個專案免費蓋一間『專屬的獨立廚房』，確保不同專案的材料完全分開，乾乾淨淨！

## UV

uv 是一個由 Astral 公司開發、用 Rust 編寫的高效 Python 套件管理工具，旨在取代傳統的 pip，提供更快的速度和現代化的管理方式。它支援 pyproject.toml（符合 PEP 621 標準）以及自動生成 uv.lock 鎖檔，確保依賴版本一致性。

uv 的安裝速度比 pip 快數倍（例如安裝 Flask：pip 約 19.2 秒，uv 僅 0.02 秒），且支援現代化專案管理。

- [用uv管理Python的一切！](https://www.youtube.com/watch?v=aVXs8lb7i9U)
- [从pip到uv：一口气梳理现代Python项目管理全流程！](https://www.youtube.com/watch?v=jd1aRE5pJWc&t=68s)

### 安裝 uv

```shell=
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 建立虛擬環境

```shell=
# 初始化專案：運行以下命令，uv 會自動生成專案設定檔 pyproject.toml 和其他必要檔案
uv init

# 建立虛擬環境
uv venv # 這會在專案資料夾內創建 .venv 虛擬環境
```

(補充)BUG：如果跑出

```
.venv\Scripts\activate : 因為這個系統上已停用指令碼執行，所以無法載入 E:\維誠\uv_python_file\.venv\Scripts\activate.ps1
 檔案。如需詳細資訊，請參閱 about_Execution_Policies，網址為 https:/go.microsoft.com/fwlink/?LinkID=135170。
位於 線路:1 字元:1
+ .venv\Scripts\activate
+ ~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException -> Windows 的安全鎖沒打開。
    + FullyQualifiedErrorId : UnauthorizedAccess
```

你需要打開安全鎖：

```shell=
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# 在這次開啟視窗的期間，允許我執行自己電腦上的腳本。
```

執行後重啟。

### 啟動虛擬環境

啟動後，命令列提示符會顯示虛擬環境名稱，表示已進入虛擬環境。

```shell=
# 在 macOS/Linux 上
source .venv/bin/activate

# Windows 上：
.\.venv\Scripts\activate
```

### (補充)要在ipynb上使用虛擬環境

```
# 必須先確保虛擬環境裡有 ipykernel。
uv add ipykernel

# 註冊核心至ipynb
python -m ipykernel install --user --name uv-env --display-name venv[這個就是你環境要選擇的名稱]

# 執行完畢後，回到 JupyterLab 介面，在右上角的 Kernel 選項中就能看到 "venv(剛剛寫的名稱)"。
```

### 離開虛擬環境

```shell=
deactivate
```

### 安裝套件

用 uv add 安裝套件，會自動更新 pyproject.toml 和 uv.lock：

```shell=
# 安裝正式環境套件（例如 Django）
uv add django

# 安裝開發環境套件（例如 pytest，不會部署到正式環境）
uv add --dev pytest
```

安裝後，pyproject.toml 會更新

### 與其他開發者共享專案

當其他開發者下載你的專案時，他們只需執行以下步驟即可重現環境：

```shell=
# 同步套件（根據 pyproject.toml 和 uv.lock 安裝所有依賴）：
uv sync

# 啟動虛擬環境
.\.venv\Scripts\activate
```

## venv

venv 是一個 Python 內建的標準函式庫，專門用來建立輕量級的虛擬環境。它不需依賴外部安裝，能夠為每個專案提供獨立的 Python 執行環境，確保不同專案之間的套件版本不會互相干擾。

venv 的環境建置速度與現代工具相比稍慢，但具有極高的系統相容性，是許多開發者與導生在學習基礎專案管理時的首選。

## Conda

conda 是一個開源的跨平台套件管理與環境管理系統，最初為 Python 資料科學與機器學習領域設計。它不僅能管理 Python 套件，還能處理包含 C/C++ 等底層依賴的複雜函式庫，非常適合用於開發人工智慧模型或處理需要大量運算資源的專案。

conda 的環境建置雖然較佔用磁碟空間，但它能獨立安裝並切換不同版本的 Python 直譯器，擁有極龐大且穩定的科學運算生態系，在帶領導生進行進階專案開發時非常實用。

- [15分钟彻底搞懂！Anaconda Miniconda conda-forge miniforge Mamba](https://www.youtube.com/watch?v=-MSLJKjH8U0)
