#include <iostream>
#include <thread>

using namespace std;

void some_function() {
    cout << "some_function is running in thread " << this_thread::get_id() << endl;
}

void some_other_function() {
    cout << "some_other_function is running in thread " << this_thread::get_id() << endl;
}


int main(){
    thread t1(some_function);  // 建立 t1，擁有一個執行緒
    thread t2 = move(t1); // 2. 將 t1 的所有權轉移給 t2。t1 現在不再擁有執行緒。

    t1 = thread(some_other_function); // 3. 重新為 t1 建立一個新的執行緒，t1 又重新擁有執行緒了。
    thread t3 = move(t1); // 5. 將 t2 的所有權轉移給 t3。t2 現在不再擁有執行緒。
    t2.join();
    t3.join();
    // some_function is running in thread some_other_function is running in thread 0xa0002af000xa0002b000 輸出交錯或混疊
}

