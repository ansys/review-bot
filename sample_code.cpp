"""sample code"""

#include <iostream>
#include <list>

int functionA() 
{
    int num = 5;
    while (num < 10) {
        std::cout << num << std::endl;
        num++; 
    }
    return 0;
}

int sum(std::list<int> lst) 
{
    int total = 0;
    for (auto it = lst.begin(); it != lst.end(); it++) 
    { 
        total += *it;
    }
    return total;
}

double average(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    int num = size; 
    return sum / double(num);
}

int main() {

    std::list<int> lst = {1, 2, 3, 4, 5};
    int total = sum(lst);
    std::cout << "Total: " << total << std::endl;

    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    double avg = average(arr, size);
    std::cout << "Average: " << avg << std::endl;

    functionA();

    return 0;
}