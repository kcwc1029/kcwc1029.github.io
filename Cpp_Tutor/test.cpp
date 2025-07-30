#include <iostream>
using namespace std;

// 接收一個指向含有 5 個 int 的陣列指標
void printArray(int (*p)[5]) {
    for (int i = 0; i < 5; ++i) {
        cout << (*p)[i] << " "; // 取陣列的值
        // cout << *p[i] << " "; // 為定義行為
    }
    cout << endl;
}

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printArray(&arr);  // 傳整個陣列的位址
    return 0;
}