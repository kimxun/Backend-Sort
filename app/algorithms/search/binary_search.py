def binary_search_logic(arr, target):
    steps = []
    comparisons = 0
    discarded = []

    left = 0
    right = len(arr) - 1

    steps.append({
        "array": arr.copy(),
        "low": left,
        "high": right,
        "mid": None,
        "comparing": [],
        "discarded": discarded.copy(),
        "found": False,
        "line": 2,
        "keys": ["left", "right", "mid", "target"],
        "vals": [left, right, "-", target],
        "action": (
            f"Bắt đầu tìm {target} trong mảng đã sắp xếp. "
            f"Phạm vi ban đầu từ vị trí {left} đến {right}"
        )
    })

    while left <= right:

        mid = (left + right) // 2
        comparisons += 1

        steps.append({
            "array": arr.copy(),
            "low": left,
            "high": right,
            "mid": mid,
            "comparing": [mid],
            "discarded": discarded.copy(),
            "found": False,
            "line": 4,
            "keys": ["left", "right", "mid", "a[mid]", "target"],
            "vals": [left, right, mid, arr[mid], target],
            "action": (
                f"Xét phạm vi từ vị trí {left} đến {right}. "
                f"Chọn vị trí giữa mid = {mid}, có giá trị {arr[mid]}"
            )
        })

        if arr[mid] == target:

            steps.append({
                "array": arr.copy(),
                "low": left,
                "high": right,
                "mid": mid,
                "comparing": [mid],
                "discarded": discarded.copy(),
                "found": True,
                "line": 6,
                "keys": ["left", "right", "mid", "a[mid]", "target", "found_index"],
                "vals": [left, right, mid, arr[mid], target, mid],
                "action": f"{target} bằng {arr[mid]}, tìm thấy tại vị trí {mid}"
            })

            return steps, comparisons, mid

        elif target < arr[mid]:
            discarded.extend(range(mid, right + 1))

            steps.append({
                "array": arr.copy(),
                "low": left,
                "high": right,
                "mid": mid,
                "comparing": [],
                "discarded": discarded.copy(),
                "found": False,
                "line": 8,
                "keys": ["left", "right", "mid", "a[mid]", "target"],
                "vals": [left, right, mid, arr[mid], target],
                "action": (
                    f"{target} nhỏ hơn {arr[mid]}, bỏ nửa bên phải và "
                    f"tiếp tục tìm từ vị trí {left} đến {mid - 1}"
                )
            })

            right = mid - 1

        else:
            discarded.extend(range(left, mid + 1))

            steps.append({
                "array": arr.copy(),
                "low": left,
                "high": right,
                "mid": mid,
                "comparing": [],
                "discarded": discarded.copy(),
                "found": False,
                "line": 10,
                "keys": ["left", "right", "mid", "a[mid]", "target"],
                "vals": [left, right, mid, arr[mid], target],
                "action": (
                    f"{target} lớn hơn {arr[mid]}, bỏ nửa bên trái và "
                    f"tiếp tục tìm từ vị trí {mid + 1} đến {right}"
                )
            })

            left = mid + 1

    steps.append({
        "array": arr.copy(),
        "low": left,
        "high": right,
        "mid": None,
        "comparing": [],
        "discarded": discarded.copy(),
        "found": False,
        "line": 12,
        "keys": ["left", "right", "mid", "target", "found_index"],
        "vals": [left, right, "-", target, -1],
        "action": (
            f"Phạm vi tìm kiếm đã rỗng vì vị trí trái {left} "
            f"lớn hơn vị trí phải {right}. Không tìm thấy {target}"
        )
    })

    return steps, comparisons, -1
