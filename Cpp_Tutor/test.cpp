#include <iostream> 
using namespace std; 

int main() { 
    int num[2][4] = { 
        {312, 16, 35, 65}, 
        {52, 111, 77, 80} 
    }; 

    // 二維陣列本體即為指標（指向第一列） 
    cout << "num         = " << num << endl; // 0x7ffffcbc0 
    cout << "num + 1     = " << (num + 1) << endl; // 0x7ffffcbd0 (從0x7ffffcbc0 後移16格byte) 
 
    // 解參考(一層)取得列地址 
    cout << "*(num)      = " << *(num) << endl; // 0x7ffffcbc0 
    cout << "*(num + 1)  = " << *(num + 1) << endl; // 0x7ffffcbd0 (從0x7ffffcbc0 後移16格byte) 
 
    // // 解參考(兩層)取得值 
    cout << "*(*(num)+0)     = " << *(*(num + 0)+0) << endl; // 312 = num[0][0] 
    cout << "*(*(num + 1)+0)  = " << *(*(num + 1)+0) << endl; // 52 = num[1][0] 
 
    // // 再示範一次解參考(兩層)取得值 
    cout << "*(num) + 2         = " << *(num) + 1 << endl; // 0x7ffffcbe4 
    cout << "*(num + 1) + 2     = " << *(num + 1) + 1 << endl; // 0x7ffffcbf4 
    cout << "*(*(num) + 2)      = " << *(*(num + 0) + 1)  << endl;       // 16  = num[0][2] 
    cout << "*(*(num + 1) + 2)  = " << *(*(num + 1) + 2) << endl;   // 77 = num[1][2] 
    return 0; 
}