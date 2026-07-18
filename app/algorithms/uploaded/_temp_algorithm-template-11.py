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
            "action": f"Lượt {i+1}: đưa phần tử {'nhỏ nhất' if sort_order == 'asc' else 'lớn nhất'} về đầu dãy chưa sắp xếp."
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
                    "action": f"Hoán đổi a[{j}] và a[{j-1}] vì {sorted_arr[j]} {'<' if sort_order == 'asc' else '>'} {sorted_arr[j-1]}. Sau hoán đổi a[{j}] = {sorted_arr[j]}, a[{j-1}] = {sorted_arr[j-1]}"
                })

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(i + 1)),
            "line": 6,
            "keys": ["sorted_idx"],
            "vals": [i],
            "action": f"Đã đưa phần tử {'nhỏ nhất' if sort_order == 'asc' else 'lớn nhất'} về vị trí {i}. Giá trị {sorted_arr[i]} đã nằm đúng vị trí."
        })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 7,
        "keys": ["Tổng số phép so sánh", "Tổng số phép hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Mảng đã được sắp xếp"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history