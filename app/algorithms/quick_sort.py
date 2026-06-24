def quick_sort_logic(arr, sort_order="asc"):
    steps_history = []
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    sorted_indices = set()
    comparisons = 0
    swaps = 0

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": [],
        "line": 1,
        "keys": ["n"],
        "vals": [n],
        "action": "Bắt đầu thuật toán Quick Sort"
    })

    def _quick_sort(l, r):
        nonlocal comparisons, swaps

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": None,
            "sorted": list(sorted_indices),
            "line": 2,
            "keys": ["l", "r"],
            "vals": [l, r],
            "action": f"Gọi đệ quy phân đoạn từ chỉ số {l} đến {r}"
        })

        if l >= r:
            if l == r:
                sorted_indices.add(l)
            return

        mid = (l + r) // 2
        x = sorted_arr[mid]
        i = l
        j = r
        pivot_idx = mid

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": pivot_idx,
            "sorted": list(sorted_indices),
            "line": 3,
            "keys": ["l", "r", "pivot_idx", "chốt x"],
            "vals": [l, r, pivot_idx, x],
            "action": f"Chọn phần tử chốt x = {x} tại vị trí {pivot_idx}"
        })

        while i <= j:
            while i <= r:
                comparisons += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [i, pivot_idx],
                    "swapping": [],
                    "pivot": pivot_idx,
                    "sorted": list(sorted_indices),
                    "line": 5,
                    "keys": ["i", "j", "a[i]", "chốt x"],
                    "vals": [i, j, sorted_arr[i], x],
                    "action": f"Tìm phần tử bên trái >= chốt: Kiểm tra a[{i}] = {sorted_arr[i]}"
                })
                condition = sorted_arr[i] < x if sort_order == "asc" else sorted_arr[i] > x
                if condition:
                    i += 1
                else:
                    break

            while j >= l:
                comparisons += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [j, pivot_idx],
                    "swapping": [],
                    "pivot": pivot_idx,
                    "sorted": list(sorted_indices),
                    "line": 6,
                    "keys": ["i", "j", "a[j]", "chốt x"],
                    "vals": [i, j, sorted_arr[j], x],
                    "action": f"Tìm phần tử bên phải <= chốt: Kiểm tra a[{j}] = {sorted_arr[j]}"
                })
                condition = sorted_arr[j] > x if sort_order == "asc" else sorted_arr[j] < x
                if condition:
                    j -= 1
                else:
                    break

            if i <= j:
                if i < j:
                    swaps += 1
                    sorted_arr[i], sorted_arr[j] = sorted_arr[j], sorted_arr[i]

                    if pivot_idx == i:
                        pivot_idx = j
                    elif pivot_idx == j:
                        pivot_idx = i

                    steps_history.append({
                        "array": sorted_arr.copy(),
                        "comparing": [],
                        "swapping": [i, j],
                        "pivot": pivot_idx,
                        "sorted": list(sorted_indices),
                        "line": 8,
                        "keys": ["i", "j", "a[i]", "a[j]"],
                        "vals": [i, j, sorted_arr[i], sorted_arr[j]],
                        "action": f"Hoán đổi phần tử lỗi vị trí: a[{i}] và a[{j}]"
                    })
                i += 1
                j -= 1

        if l < j:
            _quick_sort(l, j)
        elif l == j:
            sorted_indices.add(l)

        if i < r:
            _quick_sort(i, r)
        elif i == r:
            sorted_indices.add(r)

    _quick_sort(0, n - 1)

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 10,
        "keys": ["Tổng so sánh", "Tổng hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Hoàn thành sắp xếp Quick Sort"
    })

    steps = len(steps_history)

    return sorted_arr, steps, comparisons, swaps, steps_history