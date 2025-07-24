#include <iostream>
#include <cstdarg>
using namespace std;

int aaa = 5; // gloabal

void f(){
    int aaa = 6; // loacl
    cout << aaa;
}

int main() {
    f();
    cout << aaa;
}


