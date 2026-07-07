def linear_search_logic(arr, target):
    steps = []
    comparisons = 0

    steps.append({
        "array": arr.copy(),
        "current_index": -1,
        "comparing": [],
        "found": False,
        "line": 2,
        "action": (
            f"Bắt đầu tìm {target}. Kiểm tra lần lượt từng phần tử "
            f"từ đầu đến cuối mảng"
        )
    })

    i = 0

    while i < len(arr) and arr[i] != target:
        comparisons += 1

        steps.append({
            "array": arr.copy(),
            "current_index": i,
            "comparing": [i],
            "found": False,
            "line": 3,
            "action": (
                f"Kiểm tra vị trí {i}: giá trị {arr[i]} không bằng {target}, "
                f"tiếp tục sang vị trí {i + 1}"
            )
        })

        i += 1

    if i < len(arr):
        comparisons += 1

        steps.append({
            "array": arr.copy(),
            "current_index": i,
            "comparing": [i],
            "found": True,
            "line": 7,
            "action": (
                f"Kiểm tra vị trí {i}: giá trị {arr[i]} bằng {target}. "
                f"Đã tìm thấy tại vị trí {i}"
            )
        })

        return steps, comparisons, i

    steps.append({
        "array": arr.copy(),
        "current_index": -1,
        "comparing": [],
        "found": False,
        "line": 6,
        "action": (
            f"Không có phần tử nào trong mảng bằng {target}. "
         
        )
    })

    return steps, comparisons, -1
