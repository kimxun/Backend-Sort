def interchange_sort_logic(arr):
    arr = arr.copy()
    steps = []

    n = len(arr)

    steps.append({
        "array": arr.copy(),
        "description": "Mảng ban đầu"
    })

    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]

                steps.append({
                    "array": arr.copy(),
                    "description": f"Hoán đổi phần tử tại vị trí {i} và {j}"
                })

    steps.append({
        "array": arr.copy(),
        "description": "Hoàn thành sắp xếp"
    })

    return steps