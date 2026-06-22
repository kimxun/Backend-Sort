def selection_sort_logic(arr, sort_order="asc"):
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

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [i, j],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(i))
            })

            condition = sorted_arr[j] < sorted_arr[min_idx] if sort_order == "asc" else sorted_arr[j] > sorted_arr[
                min_idx]
            if condition:
                min_idx = j
        if min_idx != i:
            sorted_arr[i], sorted_arr[min_idx] = sorted_arr[min_idx], sorted_arr[i]
            swaps += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [],
                "swapping": [i, min_idx],
                "pivot": None,
                "sorted": list(range(i + 1))
            })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n))
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history