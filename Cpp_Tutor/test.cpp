#include <iostream>
using namespace std;

template <typename T>
T findMax(T* arr, int size) {
    T max = arr[0];
    for (int i = 1; i < size; ++i)
        if (arr[i] > max)
            max = arr[i];
    return max;
}


int main(){
    float arr[] = {1.5, 3.2, 2.7};
    cout << findMax(arr, 3) << endl;   // 輸出：3.2
}