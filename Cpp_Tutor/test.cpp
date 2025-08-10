#include <iostream>
using namespace std;

class Box {
private:
    double length, width, height;

public:
    // 建構子
    Box(double l = 1, double w = 1, double h = 1) {
        length = l;
        width = w;
        height = h;
    }

    void set(double l, double w, double h) {
        length = l;
        width = w;
        height = h;
    }

    void show() {
        cout << "尺寸：" << length << " x " << width << " x " << height << endl;
    }
};

// 傳參考呼叫函式
void update(Box& b1, Box& b2) {
    cout << "🔧 將 boxB 的尺寸設定給 boxA...\n";
    b1 = b2;  // 或使用 b1.set(...) 也可以
}

int main() {
    Box boxA(3, 3, 3);
    Box boxB(5, 5, 5);

    cout << "🚩 更新前：" << endl;
    boxA.show();
    boxB.show();

    update(boxA, boxB);  // 傳參考呼叫

    cout << "\n✅ 更新後 boxA：" << endl;
    boxA.show();
    return 0;
}