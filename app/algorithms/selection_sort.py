def selection_sort_logic(arr, sort_order="asc"):
    steps_history = []
    comparisons = 0
    swaps = 0
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    target_label = "nhỏ nhất" if sort_order == "asc" else "lớn nhất"
    compare_symbol = "<" if sort_order == "asc" else ">"

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": [],
        "line": 1,
        "keys": ["N"],
        "vals": [n],
        "action": "Bắt đầu thuật toán Selection Sort"
    })

    for i in range(n - 1):
        min_idx = i
        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(i)),
            "line": 4,
            "keys": ["i", "min" if sort_order == "asc" else "max"],
            "vals": [i, min_idx],
            "action": f"Thiết lập phần tử {target_label} tạm thời tại vị trí i = {i}"
        })

        for j in range(i + 1, n):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [j, min_idx],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(i)),
                "line": 6,
                "keys": ["i", "j", "min" if sort_order == "asc" else "max", "a[j]", "a[min]" if sort_order == "asc" else "a[max]"],
                "vals": [i, j, min_idx, sorted_arr[j], sorted_arr[min_idx]],
                "action": f"So sánh a[j] ({sorted_arr[j]}) {compare_symbol} a[{min_idx}] ({sorted_arr[min_idx]})"
            })

            condition = sorted_arr[j] < sorted_arr[min_idx] if sort_order == "asc" else sorted_arr[j] > sorted_arr[
                min_idx]

            if condition:
                min_idx = j
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [],
                    "swapping": [],
                    "pivot": None,
                    "sorted": list(range(i)),
                    "line": 7,
                    "keys": ["i", "j", "min" if sort_order == "asc" else "max", "a[min]" if sort_order == "asc" else "a[max]"],
                    "vals": [i, j, min_idx, sorted_arr[min_idx]],
                    "action": f"Tìm thấy phần tử {target_label}, cập nhật vị trí {'min' if sort_order == 'asc' else 'max'} = {min_idx}"
                })

        if min_idx != i:
            sorted_arr[i], sorted_arr[min_idx] = sorted_arr[min_idx], sorted_arr[i]
            swaps += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [],
                "swapping": [i, min_idx],
                "pivot": None,
                "sorted": list(range(i + 1)),
                "line": 8,
                "keys": ["i", "min" if sort_order == "asc" else "max", "a[i]", "a[min]" if sort_order == "asc" else "a[max]"],
                "vals": [i, min_idx, sorted_arr[i], sorted_arr[min_idx]],
                "action": f"Đổi chỗ phần tử {target_label} về đúng vị trí đầu đoạn: Hoán đổi a[{i}] và a[{min_idx}]"
            })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 9,
        "keys": ["Tổng so sánh", "Tổng hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Tất cả các phần tử đã được đưa về đúng vị trí. Hoàn thành!"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history
