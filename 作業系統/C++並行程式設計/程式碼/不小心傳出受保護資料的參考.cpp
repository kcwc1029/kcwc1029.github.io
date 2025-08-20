#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <stdexcept>
#include <chrono> // 處理時間和時間間隔的

// 1. 定義我們的資料結構
class some_data {
public:
    int a;
    std::string b;
    void do_something() {
        std::cout << "Data: a = " << a << ", b = " << b << std::endl;
    }
};

// 2. 定義一個全域指標，用來儲存受保護資料的參考
// 這個指標就是我們將要「偷」來的
some_data* unprotected_data_ptr = nullptr;

// 3. 模擬一個惡意的外部函數
// 它將受保護資料的參考偷偷傳遞給全域指標
void malicious_function(some_data& protected_data) {
    std::cout << "malicious_function: I am inside the lock, but I'm stealing the pointer!" << std::endl;
    
    // 將受保護資料的參考賦值給全域指標
    unprotected_data_ptr = &protected_data;

    // 我們也可以在鎖內進行操作
    protected_data.a = 999;
}

// 4. 定義保護資料的類別
class data_wrapper {
private:
    some_data data;
    std::mutex m;

public:
    data_wrapper() {
        data.a = 10;
        data.b = "original";
    }

    // 這是文件中的 process_data 函數
    // 它在鎖內呼叫使用者傳入的函數
    template<typename Function>
    void process_data(Function func) {
        std::lock_guard<std::mutex> lock(m);
        // 將受保護資料的參考傳遞給外部函數
        func(data);
    }
    
    // 提供一個安全的讀取函數，用於觀察資料狀態
    void print_data_safely() {
        std::lock_guard<std::mutex> lock(m);
        data.do_something();
    }
};

// 5. 主程式入口
int main() {
    std::cout << "--- 範例開始 ---" << std::endl;

    data_wrapper my_wrapper;
    
    // 在呼叫 process_data 前，先觀察資料狀態
    std::cout << "Before calling malicious_function:" << std::endl;
    my_wrapper.print_data_safely();

    // 啟動一個執行緒來執行 process_data，傳入惡意函數
    std::cout << "\nStarting a new thread to run process_data..." << std::endl;
    std::thread t([&my_wrapper](){
        my_wrapper.process_data(malicious_function);
    });

    t.join();

    // 在這個時間點，process_data 已經執行完畢，鎖已被釋放
    std::cout << "\nprocess_data thread finished. The lock has been released." << std::endl;

    // 現在，我們可以使用「偷來的參考」來存取資料了
    // 注意：這裡我們直接使用 unprotected_data_ptr，完全沒有上鎖！
    if (unprotected_data_ptr) {
        std::cout << "\nAttempting to access data via stolen pointer without a lock:" << std::endl;

        // 我們可以讀取資料
        std::cout << "Stolen pointer reads: a = " << unprotected_data_ptr->a << ", b = " << unprotected_data_ptr->b << std::endl;
        
        // 也可以在無保護的情況下修改它
        std::cout << "Modifying data via stolen pointer..." << std::endl;
        unprotected_data_ptr->b = "modified (unprotected)";

        // 模擬另一個執行緒同時讀取
        // 為了簡單起見，這裡不創建新執行緒，但你可以想像
        // 另一個執行緒此時呼叫 print_data_safely()，可能會讀到被修改一半的資料
        std::cout << "Unprotected access complete." << std::endl;
    }

    // 最終，我們再次透過安全的介面來觀察資料狀態
    std::cout << "\nFinal state of the protected data (accessed safely):" << std::endl;
    my_wrapper.print_data_safely();
    
    std::cout << "--- 範例結束 ---" << std::endl;

    return 0;
}

// malicious_function 的危險性：
//     在 process_data 內部，當 malicious_function 被呼叫時，data 是被 Mutex 鎖住的。這段時間內，其他執行緒無法修改它。
//     但 malicious_function 卻將 data 的位址 (&protected_data) 賦值給了全域的 unprotected_data_ptr。
//     這就是「資料洩漏」。 我們將一個受保護資源的訪問權限，傳遞到了鎖的保護範圍之外。
// 鎖釋放後的危險性：
//     當 process_data 執行完畢，std::lock_guard 會自動釋放 Mutex。
//     此時，unprotected_data_ptr 這個全域指標仍然指向我們的 some_data。
//     主程式現在可以隨時透過 unprotected_data_ptr 來讀取或修改 some_data，而完全不需要獲取鎖。
//     這意味著，如果此時有另一個執行緒也正在透過 data_wrapper::print_data_safely() 來讀取資料，就可能發生競爭條件：
//     一個執行緒正在鎖內讀取或修改資料。另一個執行緒在鎖外，透過 unprotected_data_ptr 同時修改資料。最終導致資料不一致或程式崩潰。




