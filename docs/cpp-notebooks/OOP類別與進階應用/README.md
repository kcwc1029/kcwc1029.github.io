# C++ OOP 類別與進階應用

## 為什麼需要物件導向？

## 開場問題

問學生：「一個遊戲角色只有名字嗎？」

學生通常會回答：還有血量、等級、攻擊力、裝備，而且角色可以攻擊、補血、升級。

## 可直接照讀的講稿

「傳統程式常把資料和函式分開。角色名字放一個變數、血量放另一個變數，攻擊是一個函式、補血又是另一個函式。程式小時沒問題；角色一多，函式可能收到錯的資料，任何地方也都能直接把血量改成負一萬。」

「物件導向做的第一件事，是把描述同一件東西的資料與行為放在一起。角色物件自己保存名字和血量，也提供受傷與補血的操作。外界不必知道血量怎麼保存，只需照規則使用角色。」

## 三個核心名詞

| 名詞        | 高中程度解釋         | 程式例子              |
| ----------- | -------------------- | --------------------- |
| 類別 class  | 設計圖、規格書       | `class GameCharacter` |
| 物件 object | 依設計圖做出的實體   | `GameCharacter may;`  |
| 成員 member | 物件擁有的資料或能力 | `hp`、`takeDamage()`  |

## 類別不是物件

同一張手機規格可以生產很多支手機；同一個類別也能建立很多個物件。每個物件通常各有自己的普通資料成員。

```text
GameCharacter 類別（藍圖）
    ├── May 物件：HP 80
    ├── John 物件：HP 35
    └── Amy 物件：HP 100
```

## 與 struct 的關係

C++ 的 `struct` 也能有函式、建構子與存取控制。主要語法差異是：

- `class` 預設成員為 `private`。
- `struct` 預設成員為 `public`。

教學慣例：單純資料集合常用 struct；具有規則與行為、希望強調封裝時常用 class。這是慣例，不是硬性限制。

## 第一個示範

檔名：`01_social_profile_class.cpp`

執行前提問：

1. `SocialProfile` 是帳號本身，還是帳號藍圖？
2. `profile` 建立後，`followers` 初始值是多少？
3. 為何不直接公開 followers？

### 延伸修改

加入 `unfollow()`。追蹤者為 0 時不能再減。學生會立刻看見：把規則寫在類別裡，所有使用者都得到同一套保護。

---

# 2. 資料成員、成員函式與封裝

## 類別基本骨架

```cpp
class 類別名稱 {
private:
    // 私有資料：類別內部細節
public:
    // 公開操作：提供外界使用
};
```

類別結尾的分號不能漏掉。

## 封裝不是「全部藏起來」

封裝的意思是：物件自己保管狀態，外界透過清楚的操作使用它。像提款機不讓使用者打開機器直接改帳戶餘額，而是提供存款、提款與查詢按鈕。

## private、public、protected

### private

- 本類別的成員函式可以存取。
- 外部程式不能直接存取。
- class 的預設權限。
- 適合必須維持規則的資料。

### public

- 外界可呼叫或存取。
- 是類別提供給使用者的操作介面。
- 通常公開行為，不直接公開可任意破壞的資料。

### protected

- 外界不能直接存取。
- 本類別及衍生類別可使用。
- 主要與繼承有關；本單元先建立概念，繼承章再深入。

## 共鳴案例：遊戲血量

檔名：`02_game_character_access.cpp`

如果 hp 是 public：

```cpp
player.hp = -500;
player.hp = 999999;
```

語法合法，但遊戲規則已壞。改由 `takeDamage()` 與 `heal()` 控制後，類別可保證 0 ≤ hp ≤ 100。

## Getter 與 Setter 不是必須成對

不要機械式地替每個 private 成員建立可任意讀寫的 get/set。若 `setHp(-500)` 仍完全接受，封裝只是換了寫法，沒有保護規則。

較好的問題是：使用者真正想做的是「設定血量」，還是「受到傷害／使用補包」？以行為命名通常更接近真實需求。

## 成員函式最後的 const

```cpp
int getHp() const;
void show() const;
```

這個 `const` 表示函式承諾不改變物件的可觀察狀態。讀取與顯示函式通常應標 const。好處包括：

- 編譯器協助防止誤改。
- const 物件也能呼叫。
- 閱讀介面時立刻知道函式是否會改資料。

## 課堂練習

檔名：`practice_01_battery.cpp`

設計 `PhoneBattery`：

- private：`percent`。
- public：`charge(int)`、`use(int)`、`show() const`。
- 電量不得低於 0 或高於 100。

### 討論題

1. 直接把 percent 設 public 有什麼後果？
2. `show()` 為何應加 const？
3. 使用負數 charge 應忽略、報錯還是拋出例外？不同選擇代表不同介面設計。

---

# 3. 成員函式：類內與類外定義

## 類內定義

函式直接寫在 class 大括號中，適合很短、很清楚的函式。

```cpp
int total() const { return price * quantity; }
```

## 類外定義與範圍解析運算子

```cpp
class FoodOrder {
public:
    int total() const;
};

int FoodOrder::total() const {
    return price * quantity;
}
```

`FoodOrder::` 表示「接下來這個 total 屬於 FoodOrder」。`::` 像完整地址，避免全域函式與其他類別的同名函式混淆。

## 為何要分開？

大型專案通常把介面放 `.h`，實作放 `.cpp`：

```text
FoodOrder.h    → 使用者需要知道有哪些操作
FoodOrder.cpp  → 操作內部怎麼完成
main.cpp       → 使用 FoodOrder
```

這能降低閱讀負擔與編譯耦合，但初學單檔示範可先寫在一起。

## 示範

檔名：`03_food_order_methods.cpp`

### 逐行問題

- 建構子為何沒有回傳型別？
- `total()` 能直接使用 private 的 price 嗎？可以，因為它是成員。
- `showReceipt()` 呼叫 `total()` 時為何不需傳入 order？因為它處理目前物件。

## 練習

檔名：`practice_02_ride_fare.cpp`

建立共享機車租借類別：分鐘數、解鎖費、每分鐘費率；把 `calculateFare()` 與 `showReceipt()` 寫在類別外。

---

# 4. 建立物件與物件指標

```cpp
FoodOrder order("雞排便當", 110, 2);
order.showReceipt();              // 物件用 .

FoodOrder* p = &order;
p->showReceipt();                 // 指標用 ->
```

## 心智模型

- 物件變數保存物件本身。
- 指標保存物件位址。
- `.`：直接進入手上的物件。
- `->`：先沿位址找到物件，再進入它。

## 常見錯誤

```cpp
order->showReceipt(); // 錯：order 不是指標
p.showReceipt();      // 錯：p 是指標
```

## 何時需要指標？

- 物件可能不存在，以 nullptr 表示。
- 動態生命週期。
- 多型與執行期選擇。
- 資料結構需要互相連結。

不應只為了「看起來進階」而使用指標。

---

# 5. 建構子：讓物件出生時就合理

## 生活比喻

辦學生證時不能只拿到一張完全空白、甚至有亂碼的卡。建立物件也是一樣：物件一出生就應處於可使用狀態。建構子就是物件的出生流程。

## 四項特性

1. 名稱與類別相同。
2. 沒有回傳型別，連 void 都不能寫。
3. 建立物件時自動呼叫。
4. 可以多載。

## 成員初始化串列

```cpp
StreamingAccount(string name, string plan, int screens)
    : owner(name), plan(plan), screens(screens) {}
```

冒號後不是「先指定再覆蓋」，而是在成員建立時直接初始化。對 const 成員、參考成員與沒有預設建構子的成員尤其必要，也通常比在函式本體賦值更清楚。

## 預設建構子是否一定存在？

如果完全沒有宣告任何建構子，編譯器可能生成預設建構子。但一旦自行宣告其他建構子，無參數版本不會必然自動存在；需要就明確寫出或使用 `= default`。

## 示範 1

`04_streaming_constructor.cpp`

問學生：`guest` 與 `may` 分別呼叫哪個版本？為什麼建立後不需再逐欄設定？

## 建構子多載

同一類別可以有同名建構子，只要參數列不同。編譯器依實際參數選擇版本。

示範：`05_concert_constructor_overload.cpp`

### 委派建構

```cpp
ConcertTicket(string event)
    : ConcertTicket(event, "一般區", 1800) {}
```

短版把初始化交給完整版，避免三個建構子各複製一份規則。

## explicit

只有一個參數的建構子有時會造成意外隱式轉換。加 `explicit` 表示必須清楚寫出建立物件的意圖。

## 練習

檔名：`practice_03_gym_membership.cpp`

設計健身房會員：姓名、方案、月費。提供訪客、學生方案、完整自訂三種建構方式，使用委派建構避免重複。

---

# 6. 解構子與物件生命週期

## 生活比喻

建構子像入住旅館時領房卡；解構子像退房時歸還房卡、結清費用。物件取得檔案、網路連線或記憶體等資源後，生命結束時需要釋放。

```cpp
~ClassName() {
    // 清理工作
}
```

## 解構子特性

- 名稱是 `~` 加類別名稱。
- 沒有回傳型別。
- 沒有參數。
- 不能多載；一個類別只有一個解構子。
- 自動物件離開作用域時自動執行。

## 解構順序

同一作用域內，通常後建立者先解構，像疊盤子：最後放上去的先拿走。

示範：`06_study_timer_destructor.cpp`

請學生先畫：

```text
建立 math
建立 cpp
離開內層：解構 cpp
離開 main：解構 math
```

## RAII

RAII 是 C++ 很重要的思想：資源綁定物件生命週期。建構時取得，解構時釋放。即使中途 return 或發生例外，也可依物件生命週期清理。

## 不能只看「有沒有 delete」

如果類別自己管理裸資源，就必須考慮複製、指定與解構，容易發生重複釋放或記憶體洩漏。現代 C++ 優先使用 `string`、`vector`、`unique_ptr` 等會自行管理資源的類型。

---

# 7. 動態物件：new/delete 與現代寫法

圖片教材示範：

```cpp
Student* student = new Student;
student->input();
delete student;
```

這是理解堆積區與手動生命週期的重要語法，但實務風險包括：

- 忘記 delete，造成洩漏。
- delete 後繼續使用，成為懸空指標。
- 同一地址 delete 兩次。
- 中途 return 或例外導致清理沒執行。

## 現代 C++ 優先方案

```cpp
auto player = std::make_unique<Player>("May");
player->play();
```

`unique_ptr` 表示單一擁有權，離開作用域自動 delete。

示範檔：

- `07_dynamic_game_player.cpp`
- `15_smart_pointer_pet_adoption.cpp`

## 教學對照

| 問題   | 裸指標             | unique_ptr         |
| ------ | ------------------ | ------------------ |
| 建立   | `new T`            | `make_unique<T>()` |
| 釋放   | 手動 `delete`      | 自動               |
| 可複製 | 位址可被隨意複製   | 不可複製擁有權     |
| 適合   | 舊介面、非擁有觀察 | 單一擁有動態物件   |

## 練習

檔名：`practice_04_download_task.cpp`

建立下載任務物件，在建構子輸出「開始」、解構子輸出「清理暫存」。分別用區域物件與 unique_ptr 觀察生命週期。

---

# 8. 物件陣列

物件陣列不是「一個物件有很多欄位」，而是很多個同型別物件排在一起。

```cpp
Song playlist[] {
    {"歌 A", 200},
    {"歌 B", 180}
};
```

每個元素建立時都會呼叫建構子，陣列結束生命時每個元素都會被解構，順序與建立相反。

示範：`08_playlist_object_array.cpp`

## 圖片棒球案例的現代轉化

原圖以三位打者計算打擊率。可改成學生較熟悉的遊戲戰績：玩家名稱、出賽場數、勝場，成員函式計算勝率。核心仍是物件陣列與逐一呼叫成員函式。

## 練習

檔名：`practice_05_game_team.cpp`

建立五位玩家物件，輸出勝率最高者。要求處理出賽 0 場，避免除以 0。

---

# 9. 朋友函式與朋友類別

## 先說結論

friend 是封裝的「受控例外」，不是一般成員，也不是繼承。它讓指定函式或類別存取 private/protected 成員。

## 朋友函式

```cpp
class Wallet {
    friend void splitDinner(const Wallet&, const Wallet&, int);
};
```

它在類別中被宣告為 friend，但呼叫時仍是普通函式：

```cpp
splitDinner(a, b, 700);
```

不是 `a.splitDinner()`。

示範：`09_friend_split_bill.cpp`

## 朋友類別

```cpp
friend class DeliveryPlatform;
```

這會讓對方所有成員函式都能存取 private，權限很大。示範：`10_friend_class_delivery.cpp`。

## friend 的規則

- 不是雙向：A 把 B 當朋友，不代表 B 也把 A 當朋友。
- 不會自動傳遞：A 的朋友的朋友不是 A 的朋友。
- 不會自動繼承。
- 宣告位置不改變其 friend 本質，但通常放 private 區附近便於閱讀。

## 何時不用 friend？

如果普通 public 成員函式已能完成需求，就不需打開 private 權限。大量 friend 會增加類別間耦合，使內部修改影響更多程式。

## 課堂辯論

題目：「外送平台是否應看得到店家的秘密配方？」

讓學生理解技術上做得到，不代表設計上應授權。權限設計與真實世界的最小權限原則相同。

---

# 10. this 指標

## 高中程度解釋

同一份成員函式會被很多物件使用。當 `cartA.add(60)` 執行時，函式怎麼知道要修改 cartA 而不是 cartB？編譯器暗中提供 `this`，它指向「目前呼叫此函式的物件」。

```text
cartA.add(60) → this 指向 cartA
cartB.add(60) → this 指向 cartB
```

## 兩種成員寫法

```cpp
this->totalPrice += price;
(*this).totalPrice += price;
```

兩者概念相同；`.` 優先於 `*`，所以第二種一定要括號。一般成員函式通常可省略 `this->`。

## 參數與成員同名

```cpp
void setPrice(int price) {
    this->price = price;
}
```

左側是目前物件的成員，右側是參數。

## 回傳 \*this 與鏈式呼叫

```cpp
ShoppingCart& add(int price) {
    totalPrice += price;
    return *this;
}
```

因回傳目前物件的參考，可以寫：

```cpp
cart.add(60).add(35).checkout();
```

示範：`11_this_shopping_cart.cpp`

## this 的限制

- 只能在非 static 成員函式中使用。
- static 函式不屬於某一特定物件，所以沒有 this。
- `return this;` 回傳指標；`return *this;` 回傳物件或參考，需配合函式回傳型別。

## 練習

檔名：`practice_06_video_settings.cpp`

建立影片播放器設定，支援：

```cpp
settings.setVolume(70).setSpeed(1.25).enableSubtitle().show();
```

---

# 11. static 靜態資料成員

## 普通成員與 static 成員

普通成員每個物件各有一份；static 成員屬於整個類別，所有物件共用一份。

```text
Viewer May  ─┐
Viewer John ─┼──→ Viewer::onlineCount
Viewer Amy  ─┘
```

## 常見用途

- 計算目前或累計建立多少物件。
- 共用設定。
- 發號器。
- 類別層級常數。

示範：`12_static_live_stream.cpp`

## 初始化與存取

傳統常見寫法：

```cpp
int Viewer::onlineCount = 0;
```

存取可用：

```cpp
Viewer::getOnlineCount();
```

比透過某個物件呼叫更能表達「這屬於類別整體」。C++17 也可用 `inline static int onlineCount = 0;` 放在類別內。

## static 成員函式限制

它沒有 this，不能直接讀取某一物件的普通成員；除非另外取得該物件參考或指標。

## 計數器陷阱

若建構子加一、解構子減一，還要思考複製建構：複製物件是否也算新在線者？真正專案必須明確定義語意，而不只是機械加減。

## 練習

檔名：`practice_07_queue_number.cpp`

設計飲料店訂單，每張單自動取得 101、102、103……取餐號。static 保存下一號，普通成員保存每張單自己的號碼。

---

# 12. 巢狀類別

巢狀類別是在某類別內宣告另一類別。它適合表達「內層概念主要只服務外層概念」。

```cpp
class Course {
public:
    class Enrollment { ... };
};
```

完整名稱是 `Course::Enrollment`。

示範：`13_nested_course_registration.cpp`

## 與一般包含物件的差別

- 巢狀類別：型別名稱被放進外層類別作用域。
- 組合：外層物件擁有內層物件作為資料成員。

兩者可同時存在，但概念不同。內層類別也不會因為「住在裡面」就自動擁有外層某個物件；若需要操作外層物件，仍要有參考或指標。

## 原圖書架案例的安全改寫

原圖以 `new char[]`、物件指標陣列及巢狀 Book 實作書架。現代版本可使用：

```cpp
class Bookshelf {
    class Book { std::string title; int price; };
    std::vector<Book> books;
};
```

由 string 和 vector 自動管理資源，可避免缺少解構子、複製控制與容量越界。

## 練習

檔名：`practice_08_chat_room.cpp`

外層 ChatRoom、內層 Message；Message 保存發言者與文字，ChatRoom 保存訊息清單並顯示紀錄。

---

# 13. 函式與物件傳遞

這一節可用「交作業」比喻。

## 傳值：交影印本

```cpp
void byValue(PhonePlan plan);
```

函式拿到副本；修改副本不影響原物件。大型物件會有複製成本。

## 傳址：交地址

```cpp
void byPointer(PhonePlan* plan);
```

可以修改原物件，也可以傳 nullptr，所以函式通常要檢查。成員用 `->`。

## 傳參考：替原件取別名

```cpp
void byReference(PhonePlan& plan);
```

修改會影響原物件；語法像普通物件，不需解參考。

## const 參考：借原件看，不准塗改

```cpp
void readOnly(const PhonePlan& plan);
```

這是唯讀大型物件常用方式：不複製、不修改、也沒有一般空參考問題。

示範：`14_object_passing_phone_plan.cpp`

## 比較表

| 參數                 | 是否複製 | 可改原物件 | 可表達沒有物件 | 成員語法 |
| -------------------- | -------: | ---------: | -------------: | -------- |
| `T value`            |       是 |         否 |             否 | `.`      |
| `T* pointer`         |       否 |         是 |    是，nullptr | `->`     |
| `T& reference`       |       否 |         是 |         一般否 | `.`      |
| `const T& reference` |       否 |         否 |         一般否 | `.`      |

## 選擇口訣

- 要副本：傳值。
- 只讀且物件一定存在：const 參考。
- 要修改且物件一定存在：參考。
- 物件可能不存在：指標或更能表達語意的型別。

## 練習

檔名：`practice_09_trade_game_item.cpp`

兩位玩家交換道具。先用傳值故意失敗，再改成參考；說明為何交換必須改原物件。

---

# 14. 綜合實作：校園訂餐 App

示範：`16_capstone_campus_food_app.cpp`

## 技術對照

| 需求                         | 技術           |
| ---------------------------- | -------------- |
| 每張訂單保存自己的學生與品項 | 普通資料成員   |
| 取餐號全班共用遞增           | static         |
| 訂單狀態有限                 | enum class     |
| 加品項後繼續操作             | `return *this` |
| total 不修改訂單             | const 成員函式 |
| 多個價格                     | vector         |

## 分階段改造

1. 加入餐點名稱與價格。
2. 拒絕負價格。
3. 顯示 preparing、ready、completed 中文狀態。
4. completed 後禁止新增品項。
5. 支援折價券，但總價不得小於 0。
6. 建立多張訂單，依取餐號查詢。
7. 將類別拆成 `.h` 與 `.cpp`。

## 專題檔名

- `project_01_campus_food_basic.cpp`
- `project_02_campus_food_status.cpp`
- `project_03_campus_food_coupon.cpp`
- `project_04_campus_food_multi_order.cpp`
- `CampusOrder.h`
- `CampusOrder.cpp`
- `main.cpp`

---

# 15. 大量短練習題材與檔名

| 檔名                              | 題材             | 練習技術      |
| --------------------------------- | ---------------- | ------------- |
| `practice_10_instagram_post.cpp`  | 貼文按讚、取消讚 | private、規則 |
| `practice_11_youbike_rental.cpp`  | 租借分鐘與費用   | 成員函式      |
| `practice_12_gacha_character.cpp` | 角色稀有度與戰力 | enum class    |
| `practice_13_exam_countdown.cpp`  | 考試倒數         | 建構／解構    |
| `practice_14_subscription.cpp`    | 串流續訂         | 建構子多載    |
| `practice_15_concert_queue.cpp`   | 搶票排隊號       | static        |
| `practice_16_group_buy.cpp`       | 團購訂單         | 物件陣列      |
| `practice_17_shared_scooter.cpp`  | 騎乘扣款         | 參考傳遞      |
| `practice_18_dorm_washing.cpp`    | 洗衣機排程       | 類別狀態      |
| `practice_19_pet_hotel.cpp`       | 寵物入住／退房   | 生命週期      |
| `practice_20_playlist.cpp`        | 播放清單         | vector 物件   |
| `practice_21_chat_message.cpp`    | 聊天室訊息       | 巢狀類別      |
| `practice_22_split_bill.cpp`      | AA 制分帳        | friend 討論   |
| `practice_23_mobile_plan.cpp`     | 資費比較         | 物件參數      |
| `practice_24_delivery_order.cpp`  | 訂單狀態         | 封裝、enum    |

---

# 16. 常見錯誤診斷

## 1. 類別結尾漏分號

```cpp
class User { }
```

修正：`class User { };`

## 2. 建構子寫了 void

```cpp
void User() {}
```

這是名為 User 的普通成員函式，不是建構子。建構子沒有回傳型別。

## 3. const 函式修改成員

```cpp
void show() const { score++; }
```

違反唯讀承諾；應重新思考 show 是否真的需要修改。

## 4. 忘記類別範圍

```cpp
int total() const { ... }
```

類外定義應為 `int FoodOrder::total() const`。

## 5. 裸 new 忘記 delete

優先改用區域物件或 `make_unique`。

## 6. static 函式使用 this

static 不屬於某個物件，所以沒有 this。

## 7. 傳值卻期待原物件改變

若需求是修改原物件，考慮參考或指標。

## 8. friend 當成成員呼叫

朋友函式仍是非成員，通常直接以函式名稱呼叫。

---

# 17. 課堂口頭題庫

1. class 是物件還是物件藍圖？
2. 每個物件會共用普通資料成員嗎？
3. private 解決什麼問題？
4. public 是不是越多越方便？
5. 成員函式為何可直接讀 private？
6. 類外定義為何需要 `::`？
7. 物件與指標分別使用什麼存取符號？
8. 建構子何時執行？
9. 建構子能否有回傳型別？
10. 自訂有參數建構子後，預設建構子一定存在嗎？
11. 解構子能多載嗎？
12. 為何後建立物件通常先解構？
13. new 物件由誰負責釋放？
14. unique_ptr 解決什麼風險？
15. friend 是不是類別成員？
16. friend 關係是否雙向？
17. this 指向誰？
18. static 成員有幾份？
19. static 函式有沒有 this？
20. 傳值、傳指標、傳參考如何選擇？

---

# 18. 紙筆測驗與答案

## 選擇題

1. 哪個最能描述 class？  
   A. 單一整數　B. 物件藍圖　C. 迴圈　D. 標頭檔

2. 哪一項通常用來保護物件規則？  
   A. private　B. cout　C. include　D. return

3. 指標 p 呼叫成員函式應使用：  
   A. `p.show()`　B. `p->show()`　C. `p::show()`　D. `&p.show()`

4. 哪個函式在物件離開作用域時自動呼叫？  
   A. main　B. friend　C. 解構子　D. static

5. 所有物件共用一份的資料應宣告為：  
   A. const　B. static　C. friend　D. virtual

6. 唯讀且避免複製大型物件，適合：  
   A. `T`　B. `T*`　C. `const T&`　D. `int&`

答案：1-B、2-A、3-B、4-C、5-B、6-C。

## 讀程式題

```cpp
Cart a;
Cart b;
a.add(50);
b.add(30);
```

若 total 是普通成員，a 與 b 的 total 是否共用？答：不共用。

```cpp
Cart& add(int price) {
    total += price;
    return *this;
}
```

為何能連續 `.add()`？答：每次回傳目前物件的參考。
