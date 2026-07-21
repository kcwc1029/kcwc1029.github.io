# 集合（set）

集合（set）是一種 無序、不重複的元素集合，常用於需要唯一性檢查的情境。其主要特性如下：

- 無序性：集合中的元素沒有固定順序，不能透過索引（如 set[0]）存取。
- 不重複性：集合會自動過濾重複元素，新增已存在的元素時會被忽略。
- 可變性：集合本身是可變的，可以新增或刪除元素。
- 元素限制：集合中的元素必須是不可變（immutable）的資料型態，例如數字、字串、元組（tuple）；像列表（list）、字典（dict）則不能作為集合元素。

![upgit_20260420_1776668811.png|329x184](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260420_1776668811.png)

## [定義集合](./Set_src/定義集合.py)

你可以用 {} 或 set() 函數來建立集合。

## 集合的常用方法

- [add()：新增元素](./Set_src/新增元素.py)
- [remove()：刪除元素](./Set_src/刪除元素.py)
- [pop()：隨機刪除元素](./Set_src/隨機刪除元素.py)
- [update()：合併多個集合](./Set_src/合併多個集合.py)

## 集合的數學運算

![upgit_20260420_1776668949.png|329x184](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260420_1776668949.png)

- [union() 或 |：聯集](./Set_src/聯集.py)
- [intersection() 或 &：交集](./Set_src/交集.py)
- [difference() 或 -：差集](./Set_src/差集.py)
- [union() 或 |：聯集](./Set_src/聯集.py)
- [union() 或 |：聯集](./Set_src/聯集.py)

* Zerojudge連結：https://drive.google.com/file/d/1Qn5bAbSHvagnq0D6C0h9QFpOajSahr57/view?usp=sharing

## [練習](./Set_practices/練習題目.ipynb)
