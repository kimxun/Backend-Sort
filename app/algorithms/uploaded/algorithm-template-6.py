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

FEATURES = ["candidate"] 

def run_logic(arr, sort_order="asc"):
    steps_history = []
    comparisons = 0
    swaps = 0
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    target_label = "nhỏ nhất" if sort_order == "asc" else "lớn nhất"

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "candidate": None,
        "pivot": None,
        "sorted": [],
        "line": 1,
        "keys": ["N"],
        "vals": [n],
        "action": (
            f"Bắt đầu Selection Sort theo thứ tự "
            f"{'tăng dần' if sort_order == 'asc' else 'giảm dần'}. "
        )
    })

    for i in range(n - 1):
        min_idx = i
        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "candidate": min_idx,
            "pivot": None,
            "sorted": list(range(i)),
            "line": 4,
            "keys": ["i", "min" if sort_order == "asc" else "max"],
            "vals": [i, min_idx],
            "action": (
                f"Lượt {i + 1}: tạm xem a[{i}] = {sorted_arr[i]} "
                f"là phần tử {target_label}"
            )
        })

        for j in range(i + 1, n):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [j],
                "swapping": [],
                "candidate": min_idx,
                "pivot": None,
                "sorted": list(range(i)),
                "line": 6,
                "keys": ["i", "j", "min" if sort_order == "asc" else "max", "a[j]", "a[min]" if sort_order == "asc" else "a[max]"],
                "vals": [i, j, min_idx, sorted_arr[j], sorted_arr[min_idx]],
                "action": (
                    f"So sánh a[{j}] = {sorted_arr[j]} với phần tử "
                    f"{target_label} hiện tại a[{min_idx}] = {sorted_arr[min_idx]}"
                )
            })

            condition = sorted_arr[j] < sorted_arr[min_idx] if sort_order == "asc" else sorted_arr[j] > sorted_arr[
                min_idx]

            if condition:
                min_idx = j
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [],
                    "swapping": [],
                    "candidate": min_idx,
                    "pivot": None,
                    "sorted": list(range(i)),
                    "line": 7,
                    "keys": ["i", "j", "min" if sort_order == "asc" else "max", "a[min]" if sort_order == "asc" else "a[max]"],
                    "vals": [i, j, min_idx, sorted_arr[min_idx]],
                    "action": (
                        f"a[{j}] = {sorted_arr[j]} phù hợp hơn, cập nhật vị trí "
                        f"phần tử {target_label} thành {j}"
                    )
                })

        if min_idx != i:
            sorted_arr[i], sorted_arr[min_idx] = sorted_arr[min_idx], sorted_arr[i]
            swaps += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [],
                "swapping": [i, min_idx],
                "candidate": None,
                "pivot": None,
                "sorted": list(range(i + 1)),
                "line": 8,
                "keys": ["i", "min" if sort_order == "asc" else "max", "a[i]", "a[min]" if sort_order == "asc" else "a[max]"],
                "vals": [i, min_idx, sorted_arr[i], sorted_arr[min_idx]],
                "action": (
                    f"Hoán đổi vị trí {i} và {min_idx}. "
                    f"Đưa giá trị {sorted_arr[i]} vào đúng vị trí {i}"
                )
            })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "candidate": None,
        "pivot": None,
        "sorted": list(range(n)),
        "line": 9,
        "keys": ["Tổng so sánh", "Tổng hoán đổi"],
        "vals": [comparisons, swaps],
        "action":  f"Mảng đẫ được sắp xếp"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history
