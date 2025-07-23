// test.cpp
#include <iostream>
using namespace std;

extern int counter;  // 告訴編譯器：變數定義在別處

int main() {
    cout << "Counter = " << counter << endl; // Counter = 42
    return 0;
}