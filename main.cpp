#include <bits/stdc++.h>
using namespace std;

struct Record {
    string month;
    int    year{};
    int    ranking{};
    string icd;
    string disease;
    int    total{};
};


string trim(const string &s) {
    size_t start = s.find_first_not_of(" \t\r\n");
    if (start == string::npos) return "";
    size_t end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

int monthToIndex(const string &m) {
    string s = m;
    for (auto &c : s) c = tolower(c);

    if (s.find("januari")   != string::npos) return 1;
    if (s.find("februari")  != string::npos) return 2;
    if (s.find("maret")     != string::npos) return 3;
    if (s.find("april")     != string::npos) return 4;
    if (s.find("mei")       != string::npos) return 5;
    if (s.find("juni")      != string::npos) return 6;
    if (s.find("juli")      != string::npos) return 7;
    if (s.find("agustus")   != string::npos) return 8;
    if (s.find("september") != string::npos) return 9;
    if (s.find("oktober")   != string::npos) return 10;
    if (s.find("nopember")  != string::npos ||
        s.find("november")  != string::npos) return 11;
    if (s.find("desember")  != string::npos) return 12;
    return 0;
}

vector<string> splitCsvSemicolon(const string &line) {
    vector<string> fields;
    string cur;
    bool inQuotes = false;

    for (char ch : line) {
        if (ch == '"') {
            inQuotes = !inQuotes;
        } else if (ch == ';' && !inQuotes) {
            fields.push_back(cur);
            cur.clear();
        } else {
            cur.push_back(ch);
        }
    }
    fields.push_back(cur);
    return fields;
}

bool parseRecordLine(const string &line, Record &rec) {
    if (line.empty()) return false;

    auto fields = splitCsvSemicolon(line);

    if (fields.size() < 6) return false;

    string yearStr = trim(fields[1]);
    if (yearStr.empty() || !isdigit(yearStr[0]))
        return false;

    rec.month   = trim(fields[0]);
    rec.year    = stoi(yearStr);
    rec.ranking = stoi(trim(fields[2]));
    rec.icd     = trim(fields[3]);

    string desc;
    for (size_t i = 4; i + 1 < fields.size(); ++i) {
        if (!desc.empty()) desc += ";";
        desc += fields[i];
    }
    for (char &c : desc) if (c == '\t') c = ' ';
    rec.disease = trim(desc);

    rec.total = stoi(trim(fields.back()));
    return true;
}


bool recordLess(const Record &a, const Record &b) {
    if (a.year != b.year) return a.year < b.year;

    int ma = monthToIndex(a.month);
    int mb = monthToIndex(b.month);
    if (ma != mb) return ma < mb;

    if (a.total != b.total) return a.total > b.total;

    return a.ranking < b.ranking;
}


void mergeRange(vector<Record> &arr, int left, int mid, int right,
                long long &compCount) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<Record> L(n1), R(n2);
    for (int i = 0; i < n1; ++i) L[i] = arr[left + i];
    for (int j = 0; j < n2; ++j) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        compCount++;
        if (recordLess(L[i], R[j])) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSortRecursiveImpl(vector<Record> &arr, int left, int right,
                            long long &compCount) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSortRecursiveImpl(arr, left, mid, compCount);
    mergeSortRecursiveImpl(arr, mid + 1, right, compCount);
    mergeRange(arr, left, mid, right, compCount);
}

void mergeSortRecursive(vector<Record> &arr, long long &compCount) {
    compCount = 0;
    if (!arr.empty())
        mergeSortRecursiveImpl(arr, 0, (int)arr.size() - 1, compCount);
}

void mergeSortIterative(vector<Record> &arr, long long &compCount) {
    compCount = 0;
    int n = (int)arr.size();
    if (n <= 1) return;

    for (int step = 1; step < n; step *= 2) {
        for (int left = 0; left < n - step; left += 2 * step) {
            int mid   = left + step - 1;
            int right = min(left + 2 * step - 1, n - 1);
            mergeRange(arr, left, mid, right, compCount);
        }
    }
}

string autoDetectCsv() {
    vector<string> possibleNames = {
        "Data_Penyakit_Rawat Inap_2014-2024.csv",
        "Data_Penyakit_Rawat_Inap_2014-2024.csv",
        "data_penyakit.csv"
    };

    vector<string> searchPaths = {
        "./",
        "../",
        "../../",
        "bin/Debug/",
        "bin/Release/"
    };

    for (const auto &folder : searchPaths) {
        for (const auto &name : possibleNames) {
            string full = folder + name;
            ifstream test(full);
            if (test.good()) {
                return full;
            }
        }
    }
    return "";
}

vector<Record> loadData(const string &filename) {
    vector<Record> data;
    ifstream fin(filename);
    if (!fin) {
        cerr << "Gagal membuka file: " << filename << "\n";
        return data;
    }

    string line;
    while (getline(fin, line)) {
        Record r;
        if (parseRecordLine(line, r)) {
            data.push_back(r);
        }
    }
    return data;
}

struct ResultRow {
    int n;
    double recursiveMs;
    double iterativeMs;
    long long recursiveComp;
    long long iterativeComp;
    string winner;
    double overheadPercent;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << fixed << setprecision(4);
    string filename = autoDetectCsv();
    if (filename.empty()) {
        cerr << "ERROR: File CSV tidak ditemukan.\n"
             << "Pastikan file \"Data_Penyakit_Rawat Inap_2014-2024.csv\" "
             << "berada di folder project atau bin/Debug.\n";
        return 1;
    }

    cout << "File CSV ditemukan: " << filename << "\n";

    auto allData = loadData(filename);
    if (allData.empty()) {
        cerr << "Tidak ada data valid yang berhasil dibaca.\n";
        return 1;
    }

    cout << "Total record terbaca: " << allData.size() << "\n\n";

    cout << "==============================================================\n";
    cout << "       ANALISIS MERGE SORT: RECURSIVE vs ITERATIVE\n";
    cout << "  Dataset: Penyakit Rawat Inap RSUD Sukoharjo\n";
    cout << "  Periode: Januari 2014 - September 2024\n";
    cout << "==============================================================\n\n";


    int totalN = (int)allData.size();
    vector<int> sizes = {1, 10, 50, 100, 250, 500, 1000};


    if (totalN > 1000) {
        sizes.push_back(totalN);
    }

    vector<ResultRow> results;

    using namespace std::chrono;

    cout << left;
    cout << "------------------------------------------------------------------------------------\n";
    cout << setw(8)  << "N"
         << setw(16) << "Recursive(ms)"
         << setw(16) << "Iterative(ms)"
         << setw(14) << "Rec_Cmp"
         << setw(14) << "Iter_Cmp"
         << setw(12) << "Winner"
         << "Overhead%\n";
    cout << "------------------------------------------------------------------------------------\n";

    for (int n : sizes) {
        if (n > totalN) continue;

        vector<Record> v1(allData.begin(), allData.begin() + n);
        vector<Record> v2 = v1;

        long long compRec = 0, compIter = 0;

        auto start1 = high_resolution_clock::now();
        mergeSortRecursive(v1, compRec);
        auto end1   = high_resolution_clock::now();
        double tRec = duration<double, std::milli>(end1 - start1).count();

        auto start2 = high_resolution_clock::now();
        mergeSortIterative(v2, compIter);
        auto end2   = high_resolution_clock::now();
        double tIter = duration<double, std::milli>(end2 - start2).count();

        double overheadPercent = 0.0;
        if (tIter > 0.0001) {
            overheadPercent = ((tRec - tIter) / tIter) * 100.0;
        }

        string win;
        if (fabs(tRec - tIter) < 1e-6) {
            win = "Tie";
        } else if (tRec < tIter) {
            win = "Recursive";
        } else {
            win = "Iterative";
        }

        results.push_back({n, tRec, tIter, compRec, compIter, win, overheadPercent});

        cout << setw(8)  << n
             << setw(16) << tRec
             << setw(16) << tIter
             << setw(14) << compRec
             << setw(14) << compIter
             << setw(12) << win
             << fixed << setprecision(1) << overheadPercent << "%\n";
    }

    cout << "------------------------------------------------------------------------------------\n\n";

    int winRec = 0, winIter = 0, tie = 0;
    double sumOverhead = 0.0;
    double sumAbsOverhead = 0.0;

    for (const auto &row : results) {
        if (row.winner == "Recursive") winRec++;
        else if (row.winner == "Iterative") winIter++;
        else tie++;

        sumOverhead += row.overheadPercent;
        sumAbsOverhead += fabs(row.overheadPercent);
    }

    int m = (int)results.size();
    double avgOverhead = sumOverhead / m;
    double avgAbsOverhead = sumAbsOverhead / m;

    cout << "==============================================================\n";
    cout << "                  HASIL ANALISIS\n";
    cout << "==============================================================\n\n";

    cout << "WINNER STATISTICS:\n";
    cout << "--------------------------------------------------------------\n";
    cout << "Recursive menang  : " << winRec  << " kali ("
         << fixed << setprecision(1) << (winRec*100.0/m) << "%)\n";
    cout << "Iterative menang  : " << winIter << " kali ("
         << fixed << setprecision(1) << (winIter*100.0/m) << "%)\n";
    cout << "Seri / seimbang   : " << tie     << " kali ("
         << fixed << setprecision(1) << (tie*100.0/m) << "%)\n\n";

    if (!results.empty()) {
        auto &lastRow = results.back();
        cout << "FULL DATASET ANALYSIS (n=" << lastRow.n << "):\n";
        cout << "--------------------------------------------------------------\n";
        cout << "Recursive time     : " << fixed << setprecision(4) << lastRow.recursiveMs << " ms\n";
        cout << "Iterative time     : " << fixed << setprecision(4) << lastRow.iterativeMs << " ms\n";
        cout << "Time difference    : " << fixed << setprecision(4)
             << fabs(lastRow.recursiveMs - lastRow.iterativeMs) << " ms\n";
        cout << "Overhead           : " << fixed << setprecision(2)
             << lastRow.overheadPercent << "%\n\n";

        cout << "Recursive comps    : " << lastRow.recursiveComp << " operations\n";
        cout << "Iterative comps    : " << lastRow.iterativeComp << " operations\n";

        long long compDiff = abs(lastRow.recursiveComp - lastRow.iterativeComp);
        double compDiffPercent = 0.0;
        if (lastRow.iterativeComp > 0) {
            compDiffPercent = (compDiff * 100.0) / lastRow.iterativeComp;
        }
        cout << "Comparison diff    : " << compDiff << " ("
             << fixed << setprecision(2) << compDiffPercent << "%)\n\n";
    }


    ofstream fout("merge_sort_results.csv");
    if (!fout) {
        cerr << "GAGAL membuat file merge_sort_results.csv\n";
        return 1;
    }

    fout << "N,Recursive_ms,Iterative_ms,Recursive_comparisons,Iterative_comparisons,"
         << "Winner,Overhead_Percent\n";

    for (const auto &row : results) {
        fout << row.n << ","
             << row.recursiveMs << ","
             << row.iterativeMs << ","
             << row.recursiveComp << ","
             << row.iterativeComp << ","
             << row.winner << ","
             << row.overheadPercent << "\n";
    }
    fout.close();
    return 0;
}
