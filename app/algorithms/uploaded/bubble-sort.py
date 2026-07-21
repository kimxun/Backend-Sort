DISPLAY_CODE = """void BubbleSort(int a[], int N) {
    int i, j;
    for (i = 0; i < N - 1; i++) {
        for (j = N - 1; j > i; j--) {
            if (a[j] < a[j - 1]) {
                swap(a[j], a[j - 1]);
            }
        }
    }
}"""

FEATURES = []
TIME_COMPLEXITY = "O(n^2)"
SPACE_COMPLEXITY = "O(1)"

DESCRIPTION = (
    "Bubble Sort là thuật toán sắp xếp đơn giản. "
    "Ý tưởng: Duyệt nhiều lần qua mảng, so sánh các cặp phần tử liền kề và hoán đổi nếu sai thứ tự. "
    "Mỗi lượt duyệt sẽ đưa phần tử lớn nhất (hoặc nhỏ nhất) về cuối (hoặc đầu) dãy."
)

STEPS = [
    "1. Bắt đầu từ phần tử đầu tiên, duyệt từ cuối mảng về đầu.",
    "2. So sánh cặp phần tử liền kề (a[j] và a[j-1]).",
    "3. Nếu a[j] < a[j-1] (với thứ tự tăng dần) hoặc a[j] > a[j-1] (với thứ tự giảm dần), hoán đổi chúng.",
    "4. Tiếp tục với j giảm dần đến i+1.",
    "5. Sau mỗi vòng lặp i, phần tử a[i] đã được đặt đúng vị trí.",
    "6. Tăng i và lặp lại bước 2–5 cho đến khi i đạt n-1.",
    "7. Kết thúc, mảng được sắp xếp."
]

def run_logic(arr, sort_order="asc"):
    steps_history = []
    comparisons = 0
    swaps = 0
    sorted_arr = arr.copy()
    n = len(sorted_arr)

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": [],
        "line": 1,
        "keys": ["n"],
        "vals": [n],
        "action": f"Bắt đầu Bubble Sort theo thứ tự {'tăng dần' if sort_order == 'asc' else 'giảm dần'}."
    })

    for i in range(n - 1):
        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(i)) if i > 0 else [],
            "line": 3,
            "keys": ["i"],
            "vals": [i],
            "action": f"Lượt {i+1}: đưa phần tử {'nhỏ nhất' if sort_order == 'asc' else 'lớn nhất'} về vị trí a[{i}]."
        })

        for j in range(n - 1, i, -1):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [j, j - 1],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(i)) if i > 0 else [],
                "line": 4,
                "keys": ["j", "a[j]", "a[j-1]"],
                "vals": [j, sorted_arr[j], sorted_arr[j - 1]],
                "action": f"So sánh a[{j}] = {sorted_arr[j]} với a[{j - 1}] = {sorted_arr[j - 1]}"
            })

            condition = (
                sorted_arr[j] < sorted_arr[j - 1]
                if sort_order == "asc"
                else sorted_arr[j] > sorted_arr[j - 1]
            )
            if condition:
                old_val_j = sorted_arr[j]
                old_val_j_minus_1 = sorted_arr[j - 1]
                sorted_arr[j], sorted_arr[j - 1] = sorted_arr[j - 1], sorted_arr[j]
                swaps += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [],
                    "swapping": [j, j - 1],
                    "pivot": None,
                    "sorted": list(range(i)) if i > 0 else [],
                    "line": 5,
                    "keys": ["j"],
                    "vals": [j],
                    "action": (
                        f"Hoán đổi a[{j}] và a[{j-1}] "
                        f"vì a[{j}] {'<' if sort_order == 'asc' else '>'} a[{j-1}] "
                        f"({old_val_j} {'<' if sort_order == 'asc' else '>'} {old_val_j_minus_1}). "
                        f"Sau hoán đổi a[{j}] = {sorted_arr[j]}, a[{j-1}] = {sorted_arr[j-1]}"
                    )
                })

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(i + 1)),
            "line": 6,
            "keys": ["i"],
            "vals": [i],
            "action": f"Kết thúc lượt {i+1}. Phần tử {sorted_arr[i]} đã về đúng vị trí a[{i}]."
        })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 7,
        "keys": ["Tổng so sánh", "Tổng hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Mảng đã được sắp xếp."
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history