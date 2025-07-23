#include <iostream>
using namespace std;


// Function Declaration（函式宣告）
int add(int a, int b);

int main() {
    int x = 10;
    int y = 20;
    int result = add(x, y); // Function Call（函式呼叫）
    cout << "x + y = " << result << endl; // x + y = 30
    return 0;
}

// Function Definition（函式定義）：定義函式本體：實際執行加法並回傳結果
int add(int a, int b) {
    return a + b;
}