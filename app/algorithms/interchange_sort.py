def interchange_sort_logic(arr, sort_order="asc"):
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
        "action": (
             f"Bắt đầu Interchange Sort theo thứ tự "
            f"{'tăng dần' if sort_order == 'asc' else 'giảm dần'}. "
        )
    })

    for i in range(n - 1):
        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(i)),
            "line": 3,
            "keys": ["i", "n"],
            "vals": [i, n],
            "action": (
                f"Lượt {i + 1}: kiểm tra giá trị tại vị trí {i} "
                f"với các phần tử từ vị trí {i + 1} đến {n - 1}"
            )
        })

        for j in range(i + 1, n):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [i, j],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(i)),
                "line": 5,
                "keys": ["i", "j", "a[i]", "a[j]"],
                "vals": [i, j, sorted_arr[i], sorted_arr[j]],
                "action": (
                    f"So sánh a[{i}] = {sorted_arr[i]} với "
                    f"a[{j}] = {sorted_arr[j]}"
                )
            })

            left_value = sorted_arr[i]
            right_value = sorted_arr[j]
            condition = left_value > right_value if sort_order == "asc" else left_value < right_value
            if condition:
                sorted_arr[i], sorted_arr[j] = sorted_arr[j], sorted_arr[i]
                swaps += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [],
                    "swapping": [i, j],
                    "pivot": None,
                    "sorted": list(range(i)),
                    "line": 6,
                    "keys": ["i", "j", "a[i]", "a[j]"],
                    "vals": [i, j, sorted_arr[i], sorted_arr[j]],
                    "action": (
                        f"Vì {left_value} "
                        f"{'lớn hơn' if sort_order == 'asc' else 'nhỏ hơn'} "
                        f"{right_value}, hoán đổi vị trí {i} và {j}. "
                        f"Sau hoán đổi a[{i}] = {sorted_arr[i]}, "
                        f"a[{j}] = {sorted_arr[j]}"
                    )
                })

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(range(i + 1)),
            "line": 3,
            "keys": ["i", "a[i]"],
            "vals": [i, sorted_arr[i]],
            "action": (
                f"Đã kiểm tra xong vị trí {i}. "
                f"Giá trị {sorted_arr[i]} đã nằm đúng vị trí"
            )
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
        "action": f"Mảng đẫ được sắp xếp"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history
