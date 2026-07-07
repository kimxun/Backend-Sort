def quick_sort_logic(arr, sort_order="asc"):
    steps_history = []
    sorted_arr = arr.copy()
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
        "vals": [len(sorted_arr)],
        "action": (
            f"Bắt đầu thuật toán Quick Sort theo thứ tự "
            f"{'tăng dần' if sort_order == 'asc' else 'giảm dần'}. "
        )
    })

    def quick_sort(l, r):
        nonlocal comparisons, swaps

        if l >= r:
            return

        i = l
        j = r
        pivot_idx = (l + r) // 2
        x = sorted_arr[pivot_idx]

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": pivot_idx,
            "sorted": [],
            "line": 3,
            "keys": ["l", "r", "pivot"],
            "vals": [l, r, x],
            "action": (
                f"Đang sắp xếp đoạn mảng từ vị trí {l} đến {r}. "
                f"Chọn phần tử giữa đoạn có giá trị {x} "
                f"(vị trí {pivot_idx}) làm chốt (pivot). "
                f"Mục tiêu là đưa các phần tử "
                f"{'nhỏ hơn' if sort_order == 'asc' else 'lớn hơn'} pivot sang bên trái và "
                f"{'lớn hơn' if sort_order == 'asc' else 'nhỏ hơn'} pivot sang bên phải."
            )
        })

        while i <= j:

            while True:
                comparisons += 1

                move_i = (
                    sorted_arr[i] < x
                    if sort_order == "asc"
                    else sorted_arr[i] > x
                )

                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [i],
                    "swapping": [],
                    "pivot": pivot_idx,
                    "sorted": [],
                    "line": 6,
                    "keys": ["i", "a[i]", "pivot"],
                    "vals": [i, sorted_arr[i], x],
                    "action": (
                        (
                            f"Đang kiểm tra a[{i}] = {sorted_arr[i]}. "
                            f"Vì giá trị này "
                            f"{'nhỏ hơn' if sort_order == 'asc' else 'lớn hơn'} pivot ({x}) "
                            f"nên đã nằm đúng phía. "
                            f"Tăng i để kiểm tra phần tử tiếp theo."
                        )
                        if move_i
                        else (
                            f"Đang kiểm tra a[{i}] = {sorted_arr[i]}. "
                            f"Giá trị này chưa nằm đúng phía so với pivot ({x}), "
                            f"nên con trỏ i dừng tại vị trí {i}."
                        )
                    )
                })

                if move_i:
                    i += 1
                else:
                    break

            while True:
                comparisons += 1

                move_j = (
                    sorted_arr[j] > x
                    if sort_order == "asc"
                    else sorted_arr[j] < x
                )

                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [j],
                    "swapping": [],
                    "pivot": pivot_idx,
                    "sorted": [],
                    "line": 7,
                    "keys": ["j", "a[j]", "pivot"],
                    "vals": [j, sorted_arr[j], x],
                    "action": (
                        (
                            f"Đang kiểm tra a[{j}] = {sorted_arr[j]}. "
                            f"Vì giá trị này "
                            f"{'lớn hơn' if sort_order == 'asc' else 'nhỏ hơn'} pivot ({x}) "
                            f"nên đã nằm đúng phía. "
                            f"Giảm j để kiểm tra phần tử phía trước."
                        )
                        if move_j
                        else (
                            f"Đang kiểm tra a[{j}] = {sorted_arr[j]}. "
                            f"Giá trị này chưa nằm đúng phía so với pivot ({x}), "
                            f"nên con trỏ j dừng tại vị trí {j}."
                        )
                    )
                })

                if move_j:
                    j -= 1
                else:
                    break

            if i <= j:
                swaps += 1

                left_value = sorted_arr[i]
                right_value = sorted_arr[j]

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
                    "sorted": [],
                    "line": 9,
                    "keys": ["i", "j"],
                    "vals": [i, j],
                    "action": (
                        (
                            f"Con trỏ i = {i} chưa vượt con trỏ j = {j}. "
                            f"Giá trị {left_value} ở bên trái và {right_value} ở bên phải "
                            f"chưa nằm đúng phía của pivot {x}, nên hoán đổi hai giá trị. "
                            f"Sau đó tăng i lên {i + 1} và giảm j xuống {j - 1}."
                        )
                        if i != j
                        else (
                            f"Hai con trỏ gặp nhau tại vị trí {i}. "
                            f"Giá trị {left_value} được giữ nguyên, sau đó tăng i lên {i + 1} "
                            f"và giảm j xuống {j - 1} để kết thúc chia đoạn."
                        )
                    )
                })

                i += 1
                j -= 1

        steps_history.append({
            "array": sorted_arr.copy(),
            "comparing": [],
            "swapping": [],
            "pivot": pivot_idx,
            "sorted": [],
            "line": 13,
            "keys": ["i", "j", "l", "r"],
            "vals": [i, j, l, r],
            "action": (
                f"Con trỏ i = {i} đã vượt con trỏ j = {j}, "
                f"nên kết thúc chia đoạn từ {l} đến {r} và không hoán đổi thêm. "
                f"Đoạn bên trái là từ {l} đến {j}; "
                f"đoạn bên phải là từ {i} đến {r}."
            )
        })

        if l < j:
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [],
                "swapping": [],
                "pivot": None,
                "sorted": [],
                "line": 14,
                "keys": ["l", "j"],
                "vals": [l, j],
                "action": (
                    f"Đoạn bên trái từ {l} đến {j} còn ít nhất hai phần tử, "
                    f"tiếp tục Quick Sort đoạn này."
                )
            })

            quick_sort(l, j)

        if i < r:
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [],
                "swapping": [],
                "pivot": None,
                "sorted": [],
                "line": 15,
                "keys": ["i", "r"],
                "vals": [i, r],
                "action": (
                    f"Đoạn bên phải từ {i} đến {r} còn ít nhất hai phần tử, "
                    f"tiếp tục Quick Sort đoạn này."
                )
            })

            quick_sort(i, r)

    quick_sort(0, len(sorted_arr) - 1)

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(len(sorted_arr))),
        "line": 16,
        "keys": ["Tổng số phép so sánh", "Tổng số phép hoán đổi"],
        "vals": [comparisons, swaps],
        "action": (
            f"Toàn bộ mảng đã được sắp xếp theo thứ tự "
            f"{'tăng dần' if sort_order == 'asc' else 'giảm dần'}. "
            f"Thuật toán thực hiện tổng cộng {comparisons} phép so sánh "
            f"và {swaps} phép hoán đổi."
        )
    })

    return (
        sorted_arr,
        len(steps_history),
        comparisons,
        swaps,
        steps_history,
    )
