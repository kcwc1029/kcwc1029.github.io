> 學習來源：https://www.youtube.com/watch?v=byHcYRpMgI4&t=4541s

## 建立(連線)資料庫

```python
import sqlite3
# NOTE: 建立資料庫
conn = sqlite3.connect("customer.db")
# conn = sqlite3.connect(":memory:") # 暫時性建立
```

## 建立資料表

主要的資料類型：

-   NULL
-   INTEGER
-   REAL：儲存浮點數
-   TEXT：儲存文字字串
-   BLOB：儲存二進位數據

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫
c = conn.cursor() # 建立 cursor

# 建立資料表
c.execute("""
CREATE TABLE customers(
    first_name text,
    last_name text,
    email text
)
""")

conn.commit() # 執行
conn.close()
```

## 新增資料

### 插入單筆數據

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫
c = conn.cursor() # 建立 cursor
customer_data = ("Tim", "Smith", "john@codemy.com")
c.execute("INSERT INTO customers VALUES (?, ?, ?)", customer_data)

conn.commit()
print("資料插入成功！")
conn.close()

```

### 一次插入多筆數據

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫
c = conn.cursor() # 建立 cursor

customer_list = [
    ("Alice", "Johnson", "alice@example.com"),
    ("Bob", "Brown", "bob@example.com")
]
c.executemany("INSERT INTO customers VALUES (?, ?, ?)", customer_list)
conn.commit()
conn.close()
print("資料插入成功！")
```

## 查詢

-   fetchone()
-   fetchall()
-   fetchmany(size)

```python
# TODO: 獲取查詢結果中的第一條記錄
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT * FROM customers")
row = c.fetchone()  # 獲取第一條記錄

# 獲取下一條記錄
while row:
    print(row)
    row = c.fetchone()

conn.close()
```

```python
# TODO: 獲取查詢結果中的所有記錄
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT * FROM customers")
rows = c.fetchall()  # 獲取所有記錄

# 打印每條記錄
for row in rows:
    print(row)

conn.close()
```

```python
# TODO: 獲取指定數量的記錄
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT * FROM customers")
rows = c.fetchmany(2)  # 每次獲取 2 條記錄

# 打印每條記錄
for row in rows:
    print(row)

conn.close()
```

實也可以直接迭代 Cursor 本身

高效且簡潔，適合逐行處理數據

```python
# TODO: 迭代Cursor本身
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT * FROM customers")
for row in c:  # 直接遍歷 Cursor
    print(*row)

conn.close()
```

## 排序資料

```python
# TODO: 獲取查詢結果中的所有記錄
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT rowid, * FROM customers ORDER BY rowid")
rows = c.fetchall()  # 獲取所有記錄

# 打印每條記錄
for row in rows:
    print(row)

conn.close()
```

## 限制查詢筆數

```python
# TODO: 獲取查詢結果中的所有記錄
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT rowid, * FROM customers ORDER BY rowid DESC LIMIT 2")
rows = c.fetchall()  # 獲取所有記錄

# 打印每條記錄
for row in rows:
    print(row)

conn.close()
```

## Primary key

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT rowid, * FROM customers")
for row in c:  # 直接遍歷 Cursor
    print(*row)

conn.close()
```

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

c = conn.cursor() # 建立 cursor
c.execute("SELECT rowid, * FROM customers WHERE first_name = 'Tim'")
for row in c:  # 直接遍歷 Cursor
    print(*row)

conn.close()
```

## 更新資料

### 更新單筆記錄

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

data = ('Bob', 'Elder')

c = conn.cursor() # 建立 cursor
c.execute("""
    UPDATE customers SET first_name = ? WHERE last_name = ?
""", data)

conn.commit()
conn.close()

```

### 更新多筆記錄

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

data = [
    ('Alice', 'Smith'),
    ('Charlie', 'Brown')
]

c = conn.cursor() # 建立 cursor
c.executemany("""
    UPDATE customers SET first_name = ? WHERE last_name = ?
""", data)

conn.commit()
conn.close()
```

## 刪除資料

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫

data = ('Alice',)

c = conn.cursor() # 建立 cursor

# 查詢資料以驗證刪除
c.execute("SELECT * FROM customers")
c.execute("""
    DELETE FROM customers WHERE first_name = ?
""", data)

conn.commit()
conn.close()
```

## 刪除整張資料表

```python
import sqlite3
conn = sqlite3.connect("customer.db") # 連線資料庫
c = conn.cursor() # 建立 cursor
c.execute("DROP TABLE customers")

conn.commit()
conn.close()
```
