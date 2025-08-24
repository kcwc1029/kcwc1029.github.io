#include <list> // 使用串列 (list) 資料結構的頭文件。
#include <mutex>
#include <thread>
#include <algorithm>
#include <iostream>

using namespace std;

// 定義共享資料和 Mutex
list<int> some_list;
mutex some_mutex; 

// 寫入資料的函數
void add_to_list(int new_value)
{
    lock_guard<mutex> guard(some_mutex); // 這行程式碼就是保護機制的核心。
    // lock_guard 是一個「鎖的守衛」。當它被建立時，它會自動鎖住你傳入的 Mutex (some_mutex)。
    // 要 guard 物件存在（也就是在這個函數的 {} 區塊內），some_mutex 就會一直被鎖住。
    // 其他任何想鎖 some_mutex 的執行緒都會被阻塞，直到這個函數執行完畢。

    some_list.push_back(new_value); // 對共享資料進行修改的地方
    // 因為它被寫在 lock_guard 的保護區內，所以你可以確保在執行這行程式碼時，
    // 不會有其他執行緒同時修改 some_list，從而避免了競爭條件。

    // 當函數執行完畢，guard 物件會被自動銷毀。
    // lock_guard 的解構函數會自動呼叫 some_mutex.unlock()，釋放鎖。
    // 這就是 RAII (Resource Acquisition Is Initialization) 的精髓。
}

// 讀取資料的函數
bool list_contains(int value_to_find)
{
    lock_guard<mutex> guard(some_mutex); // 讀取資料也要鎖定，保證資料的一致性
    return find(some_list.begin(), some_list.end(), value_to_find) != some_list.end();
}

int main(){
    // 建立兩個執行緒，分別加入資料
    thread t1(add_to_list, 42);
    thread t2(add_to_list, 99);

    t1.join();
    t2.join();

    // 主執行緒查詢資料
    cout << "Contains 42? " << (list_contains(42) ? "Yes" : "No") << endl;
    cout << "Contains 99? " << (list_contains(99) ? "Yes" : "No") << endl;
    cout << "Contains 7? "  << (list_contains(7)  ? "Yes" : "No") << endl;

    return 0;
}

