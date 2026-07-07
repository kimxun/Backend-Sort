def binary_search_logic(arr, target):
    steps = []
    comparisons = 0

    left = 0
    right = len(arr) - 1

    steps.append({
        "array": arr.copy(),
        "low": left,
        "high": right,
        "mid": None,
        "comparing": [],
        "found": False,
        "line": 2,
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
            "found": False,
            "line": 4,
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
                "found": True,
                "line": 6,
                "action": f"{target} bằng {arr[mid]}, tìm thấy tại vị trí {mid}"
            })

            return steps, comparisons, mid

        elif target < arr[mid]:

            steps.append({
                "array": arr.copy(),
                "low": left,
                "high": right,
                "mid": mid,
                "comparing": [],
                "found": False,
                "line": 8,
                "action": (
                    f"{target} nhỏ hơn {arr[mid]}, bỏ nửa bên phải và "
                    f"tiếp tục tìm từ vị trí {left} đến {mid - 1}"
                )
            })

            right = mid - 1

        else:

            steps.append({
                "array": arr.copy(),
                "low": left,
                "high": right,
                "mid": mid,
                "comparing": [],
                "found": False,
                "line": 10,
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
        "found": False,
        "line": 12,
        "action": (
            f"Phạm vi tìm kiếm đã rỗng vì vị trí trái {left} "
            f"lớn hơn vị trí phải {right}. Không tìm thấy {target}"
        )
    })

    return steps, comparisons, -1
