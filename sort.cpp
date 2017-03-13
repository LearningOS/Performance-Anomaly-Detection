#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <functional>
#include <random>
#include <limits>
#include <chrono>


void qsort(std::vector<int>& arr, int l, int r) {
    int i = l, j = r;
    int k = arr[(i + j) / 2];
    while (i <= j) {
        while (arr[i] < k) {
            i++;
        }
        while (arr[j] > k) {
            j--;
        }
        if (i <= j) {
            std::swap(arr[i], arr[j]);
            i++; j--;
        }
    }
    if (l < j) {
        qsort(arr, l, j);
    }
    if (i < r) {
        qsort(arr, i, r);
    }
}


int main() {
    std::minstd_rand gen;
    std::uniform_int_distribution<> dis(
        std::numeric_limits<int>::min(), std::numeric_limits<int>::max());
    const int n = 1000000;
    
    for (int i = 0; i < 10000; i++) {
        std::vector<int> arr;
        std::generate_n(std::back_inserter(arr), n, std::bind(dis, gen));
        auto start = std::chrono::steady_clock::now();
        std::sort(arr.begin(), arr.end());
        auto end = std::chrono::steady_clock::now();
        int sort_duration =
            std::chrono::duration_cast<std::chrono::milliseconds>
                (end - start).count();
        std::cout << sort_duration << std::endl;    
    }
    
    // for (int i = 0; i < 100; i++) {
    //     std::vector<int> arr;
    //     std::generate_n(std::back_inserter(arr), n, std::bind(dis, gen));
    //     auto start = std::chrono::steady_clock::now();
    //     qsort(arr, 0, n-1);
    //     auto end = std::chrono::steady_clock::now();
    //     int sort_duration =
    //         std::chrono::duration_cast<std::chrono::milliseconds>
    //             (end - start).count();
    //     std::cout << sort_duration << std::endl;    
    // }
    
    return 0;
}
