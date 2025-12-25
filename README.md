# Analisis empiris perbandingan performa implementasi **Recursive** vs **Iterative** dari algoritma Merge Sort menggunakan dataset real epidemiologi dari RSUD Sukoharjo (1,289 records).
---

## 🎯 Overview

Penelitian ini menganalisis perbedaan performa antara dua implementasi Merge Sort:

| Implementation | Approach | Recursion Depth | Stack Usage |
|---------------|----------|-----------------|-------------|
| **Recursive** | Top-Down | O(log n) ≈ 11 levels | ~700 bytes |
| **Iterative** | Bottom-Up | None | Minimal |

Meskipun secara teoritis keduanya memiliki kompleksitas waktu **O(n log n)**, penelitian ini membuktikan bahwa performa praktis kedua implementasi **virtually identical** dengan overhead hanya **1.39%** pada dataset penuh.

---

## 🔍 Key Findings

### 1. **Minimal Performance Gap** 
- **Recursive**: 3.136 ms
- **Iterative**: 3.093 ms  
- **Difference**: 0.043 ms (**1.39% overhead**)

### 2. **Amortization Effect Proven**
- Small data (n=50): **16% overhead**
- Large data (n=1289): **1.4% overhead**
- Overhead menurun seiring bertambahnya ukuran data

### 3. **Shallow Recursion Advantage**
- Recursion depth: **log₂(n) ≈ 11 levels**
- Stack overhead: **~700 bytes** (minimal!)
- Berbeda drastis dengan linear recursion (~30% overhead)

### 4. **Algorithmic Equivalence**
- Comparison count difference: **<7%**
- Both follow **O(n log n)** curve perfectly
- No fundamental algorithmic difference

---

## 📊 Dataset

**Source**: Data Penyakit Rawat Inap RSUD Sukoharjo  
**Period**: Januari 2014 - September 2024 (130 bulan)  
**Records**: 1,289 entries  
**Format**: CSV (semicolon-delimited)

### Data Structure
```
month, year, ranking, icd_code, disease_name, total_patients
```

### Sorting Criteria (multi-key)
1. `year` (ascending)
2. `month` (ascending)
3. `total_patients` (descending)
4. `ranking` (ascending)

---

## 💻 Implementation

### Recursive Merge Sort (Top-Down)
```cpp
void mergeSortRecursive(vector<Record> &arr, int left, int right, long long &compCount) {
    if (left >= right) return;
    
    int mid = left + (right - left) / 2;
    mergeSortRecursive(arr, left, mid, compCount);
    mergeSortRecursive(arr, mid + 1, right, compCount);
    merge(arr, left, mid, right, compCount);
}
```

**Characteristics:**
- Recursion depth: log₂(1289) ≈ 11 levels
- Function calls: ~2,577 calls
- Stack memory: ~700 bytes

### Iterative Merge Sort (Bottom-Up)
```cpp
void mergeSortIterative(vector<Record> &arr, long long &compCount) {
    int n = arr.size();
    for (int step = 1; step < n; step *= 2) {
        for (int left = 0; left < n - step; left += 2 * step) {
            int mid = left + step - 1;
            int right = min(left + 2 * step - 1, n - 1);
            merge(arr, left, mid, right, compCount);
        }
    }
}
```

**Characteristics:**
- Loop iterations: log₂(n) ≈ 11 iterations
- No recursion overhead
- Stack memory: O(1)

---

## 📈 Results

### Performance Comparison Table

| Size (n) | Recursive (ms) | Iterative (ms) | Overhead (%) | Winner    |
|----------|----------------|----------------|--------------|-----------|
| 1        | 0.0003         | 0.0001         | 0.0          | Iterative |
| 10       | 0.0            | 0.0            | 15.2         | Iterative |
| 50       | 0.1            | 0.1            | 16.2         | Iterative |
| 100      | 0.2            | 0.2            | -0.7         | Recursive |
| 250      | 0.5            | 0.5            | 1.9          | Iterative |
| 500      | 1.2            | 1.1            | 7.2          | Iterative |
| 1000     | 2.3            | 2.2            | 4.1          | Iterative |
| **1289** | **3.136**      | **3.093**      | **1.4**      | **Iterative** |

### Statistical Summary
- **Average overhead**: 6.04%
- **Full dataset overhead**: 1.39%
- **Iterative wins**: 7/8 cases (87.5%)
- **Comparison count difference**: <7%

---

## 📊 Graphs

### 1. Time Comparison
![Time Comparison](output/graphs/merge_time_comparison.png)
> Kedua garis hampir overlap - performa virtually identical

### 2. Overhead Analysis  
![Overhead Analysis](output/graphs/merge_overhead_analysis.png)
> Amortization effect: overhead menurun pada larger datasets

### 3. Comparison Count
![Comparison Count](output/graphs/merge_comparisons_count.png)
> Both implementations follow O(n log n) curve

### 4. Head-to-Head Comparison
![Final Comparison](output/graphs/merge_final_comparison.png)
> Visual comparison untuk full dataset (n=1289)

### 5. Growth Pattern Verification
![Growth Pattern](output/graphs/merge_growth_pattern.png)
> Log-log plot confirming O(n log n) complexity

---

## 📁 Project Structure

```
merge-sort-analysis/
├── src/
│   └── merge_sort_analysis.cpp      
├── data/
│   └── Data_Penyakit_Rawat_Inap_2014-2024.csv
├── output/
│   ├── merge_sort_results.csv       
│   └── graphs/
│       ├── merge_time_comparison.png
│       ├── merge_overhead_analysis.png
│       ├── merge_comparisons_count.png
│       ├── merge_final_comparison.png
│       └── merge_growth_pattern.png
├── scripts/
│   └── visualize_merge_sort.py      
├── README.md
```

---

## 🚀 How to Run

### Prerequisites
- C++ compiler with C++17 support (g++ 11.x or higher)
- Python 3.x (for graph generation)

### Compilation
```bash
g++ -std=c++17 -O2 -o merge_sort_analysis src/merge_sort_analysis.cpp
```

## 🔬 Mathematical Analysis

### Time Complexity
```
T(n) = 2·T(n/2) + Θ(n)

Using Master Theorem:
→ T(n) = Θ(n log n)  [Both implementations]
```

### Space Complexity
| Implementation | Auxiliary Space | Stack Space | Total    |
|---------------|-----------------|-------------|----------|
| Recursive     | O(n)            | O(log n)    | O(n)     |
| Iterative     | O(n)            | O(1)        | O(n)     |







