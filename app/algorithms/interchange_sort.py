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
        "sorted": []
    })

    for i in range(n - 1):
        for j in range(i + 1, n):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [i, j],
                "swapping": [],
                "pivot": None,
                "sorted": []
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
                    "sorted": []
                })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n))
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history