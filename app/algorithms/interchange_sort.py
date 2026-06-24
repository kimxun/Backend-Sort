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
        "action": "Khởi tạo mảng và bắt đầu thuật toán"
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
            "action": f"Vòng lặp i: i = {i}"
        })

        for j in range(i + 1, n):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [i, j],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(i)),
                "line": 4,
                "keys": ["i", "j", "a[i]", "a[j]"],
                "vals": [i, j, sorted_arr[i], sorted_arr[j]],
                "action": f"So sánh a[{i}] ({sorted_arr[i]}) và a[{j}] ({sorted_arr[j]})"
            })

            condition = sorted_arr[i] > sorted_arr[j] if sort_order == "asc" else sorted_arr[i] < sorted_arr[j]

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
                    "action": f"Thỏa mãn điều kiện, hoán đổi a[{i}] và a[{j}]"
                })


    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 9,
        "keys": ["Tổng số phép so sánh", "Tổng số phép hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Mảng đã được sắp xếp hoàn toàn"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history