
#include <iostream>
using namespace std;

// 這邊都是用語法糖
void f1(int arr[]) {
    // 位移運算
    for (int i = 0; i < 5; ++i) {
        cout << arr+i << " "; // 取地址
    }
    cout << "\n";
    for (int i = 0; i < 5; ++i) {
        cout << *(arr+i) << " "; // 取值
    }
    cout << "\n";

    // 語法糖
    for (int i = 0; i < 5; ++i) {
        cout << arr[i] << " "; // 取值
    }
    cout << "\n";
    for (int i = 0; i < 5; ++i) {
        cout << &arr[i] << " "; // 取地址
    }
    cout << "\n";
}

void f2(int* arr) {
    // 位移運算
    for (int i = 0; i < 5; ++i) {
        cout << arr + i << " "; // 取地址
    }
    cout << "\n";
    for (int i = 0; i < 5; ++i) {
        cout << *(arr + i) << " "; // 取值
    }
    cout << "\n";

    // 語法糖
    for (int i = 0; i < 5; ++i) {
        cout << arr[i] << " "; // 取值
    }
    cout << "\n";
    for (int i = 0; i < 5; ++i) {
        cout << &arr[i] << " "; // 取地址
    }
    cout << "\n";
}

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    f1(arr);

    cout << "========================\n";
    f2(arr);
    return 0;
}
