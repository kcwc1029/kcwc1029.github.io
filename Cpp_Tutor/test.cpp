#include <iostream>
using namespace std;
bool flag = true;

bool func(int n){ // n = 49
    if (n == 1){
        return false;
    } 


    for (int i=2 ; i<n; i++){
        if(n % i ==0){
            return true;
        }
    }
    return false;
}


int main(){
    int N = 13;
    // cin >>N;
    
    if (func(N) == true) {
        cout << "Yes" <<endl;
    }
    else{
        cout << "No" << endl;
    }
    return 0;
}