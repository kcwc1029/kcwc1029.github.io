## 前言
obesidan在增加圖片的方式是用本地儲存

### 一 在github新增一個Repositories

先新增一個新的Repositorie
![upgit_20240403_1712129302.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712129302.png)



### 二 新增github token

因為你是要用
![upgit_20240403_1712129486.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712129486.png)

接這到settings/ Develop Settings/ Personal access tokens (classic)，點選【generate new tokin】
![upgit_20240403_1712129703.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712129703.png)

填上token的註記、時效、權限
![upgit_20240403_1712129970.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712129970.png)



### 三 下載upgit

upgit有Windows、macOS與Linux等不同平台的版本。
upgit其實是一個通用的圖檔上傳工具，只要用一個命令就能把圖檔上傳到GitHub，並且直接取得GitHub的圖片鏈接網址，方便在筆記或Blog裡引用。

1 到upgit的github [upgit](https://github.com/pluveto/upgit/tree/main)
（接下來的部分，來源為官方文件，所以也不一定要看我這邊）
2 下载：从[Release](https://github.com/pluveto/upgit/releases) 下载.
下载后将其重命名为`upgit`（对于Windows用户，`upgit.exe`），保存到可以全局訪問的地方。
	1.1 `ㄎ` 確認shell是哪一種
	1.2 我是mac，那gpt是叫我存在`~/bin` 中，同時依照官方文件指示，在同資歷夾內新增 `config.toml` 文件。內容按照如下配寫
	

```shell
# =============================================================================
# UPGIT 配置
# =============================================================================

# 默认上传器
default_uploader = "github"

# 上传文件名的格式模板（仅特定上传器适配）
#   / 目录分隔符, 作用: 是区分目录
#   {year} 年份, 例如: 2022
#   {month} 月份, 例如: 02
#   {day} 天, 例如: 01
#   {unix_ts} 时间戳, 例如: 1643617626
#   {fname} 原始文件名，如 logo (不含后缀名)
#   {fname_hash} {fname}的 MD5 散列值
#   {ext} 文件后缀名, 例如.png
#   下面的例子生成的文件名预览: 2022/01/upgit_20220131_1643617626.png
#   如果目录不存在将会被程序自动创建
rename = "{year}/{month}/upgit_{year}{month}{day}_{unix_ts}{ext}"


# -----------------------------------------------------------------------------
# 自定义输出格式
# -----------------------------------------------------------------------------
#   {url} 图片文件的网络URL地址
[output_formats]
"bbcode" = "[img]{url}[/img]"
"html" = '<img src="{url}" />'
"markdown-simple" = "![|700]({url})"

# -----------------------------------------------------------------------------
# 直链替换规则 RawUrl -[replace]-> Url
# -----------------------------------------------------------------------------

# 如果您的网络访问Github异常或者缓慢，您可以尝试下面的配置以开启CDN加速
# [replacements]
# "raw.githubusercontent.com" = "cdn.jsdelivr.net/gh"
# "/master" = "@master"

# =============================================================================
# 以下为各个上传器的配置示例. 用不到的留空即可
# =============================================================================

# Github 上传器
[uploaders.github]
# 保存文件的分支，例如 master 或 main
branch = "main<填寫要上傳的分支>"

# 您的拥有"repo"权限的 Github 令牌
# 获取Github Token连接: https://github.com/settings/tokens
pat = "<填寫token>"

# 您的公共Github存储库的名称
# 注意: 为了让您和他人可以访问到图片资源, 您的Github仓库一定要是公开的,
#       在私有仓库中Github会拦截未授权的请求,你将会得到一个404.
repo = "obsidian-upgit-image<填寫Repositorie>"

# 您的 Gtihub 用户名
username = "kcwc1029<填寫Gtihub 用户名>"
```

![upgit_20240403_1712130928.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712130928.png)

3 將upgit放置全局變量
```
// 如果是bash shell
vim ~/.bash_profile
// 在文件的末尾添加以下行：
export PATH="$HOME/bin:$PATH"
// 重新加载您的 shell 配置文件，以使更改生效
source ~/.bash_profile



// 如果是bash zsh
vim ~/.zshrc
// 在文件的末尾添加以下行：
export PATH="$HOME/bin:$PATH"
// 重新加载您的 shell 配置文件，以使更改生效
source ~/.zshrc



// 如果不確定可以下此指令確認
`echo $0`
```

4 測試：能否將圖片git push
```
upgit <image_path> -f markdown //-f markdown 以markdown方式回傳
upgit Colorful\ \ Simple\ \ World\ Art\ Day\ -\ Poster.png -f markdown

成功的話會回傳githup 上傳後的圖片http 路徑
```



## 四 回到obsidian
到第三方庫安裝 shell commands，安裝好後進入。點選【選項】：
![upgit_20240403_1712132741.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712132741.png)
![upgit_20240403_1712132923.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712132923.png)
![upgit_20240403_1712133087.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2024/04/upgit_20240403_1712133087.png)





## 五 實際測試
先截一張圖，mac記得要把圖片打開再做複製（反正就是要讓剪貼簿有這張圖片就對了）
然後再由標處按下快捷鍵。


## 參考資料
-  [upgit 官方文件](https://github.com/pluveto/upgit/blob/main/docs/README.zh-CN.md)
- [(631) [Obs＃67] upgit－使用GitHub圖床：快速上傳圖檔到GitHub並插入圖片網址到Obsidian - YouTube](https://www.youtube.com/watch?v=nGII-khqm2o&t=955s)
- [yt付的中文教學](http://jdev.tw/blog/6982)


