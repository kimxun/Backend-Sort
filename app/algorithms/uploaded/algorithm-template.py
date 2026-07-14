DISPLAY_CODE = """void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}"""

FEATURES = ["pivot"] 

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
            "sorted": list(range(n - i, n)) if i > 0 else [],
            "line": 2,
            "keys": ["i"],
            "vals": [i],
            "action": f"Lượt {i+1}: đưa phần tử {'lớn nhất' if sort_order == 'asc' else 'nhỏ nhất'} về cuối dãy chưa sắp xếp."
        })

        for j in range(n - i - 1):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [j, j + 1],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(n - i, n)) if i > 0 else [],
                "line": 3,
                "keys": ["j", "a[j]", "a[j+1]"],
                "vals": [j, sorted_arr[j], sorted_arr[j + 1]],
                "action": f"So sánh a[{j}] = {sorted_arr[j]} với a[{j + 1}] = {sorted_arr[j + 1]}"
            })

            condition = (
                sorted_arr[j] > sorted_arr[j + 1]
                if sort_order == "asc"
                else sorted_arr[j] < sorted_arr[j + 1]
            )
            if condition:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swaps += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [],
                    "swapping": [j, j + 1],
                    "pivot": None,
                    "sorted": list(range(n - i, n)) if i > 0 else [],
                    "line": 4,
                    "keys": ["j"],
                    "vals": [j],
                    "action": f"Vì {sorted_arr[j+1]} {'>' if sort_order == 'asc' else '<'} {sorted_arr[j]} nên hoán đổi vị trí {j} và {j + 1}. Sau hoán đổi a[{j}] = {sorted_arr[j]}, a[{j+1}] = {sorted_arr[j+1]}"
                })

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(n - i - 1, n)),
            "line": 5,
            "keys": ["sorted_idx"],
            "vals": [n - i - 1],
            "action": f"Đã đưa phần tử {'lớn nhất' if sort_order == 'asc' else 'nhỏ nhất'} về vị trí {n - i - 1}. Giá trị {sorted_arr[n - i - 1]} đã nằm đúng vị trí."
        })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 6,
        "keys": ["Tổng số phép so sánh", "Tổng số phép hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Mảng đã được sắp xếp"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history