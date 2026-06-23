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
        "sorted": []
    })

    def _quick_sort(l, r):
        nonlocal comparisons, swaps
        if l >= r:
            if l == r:
                sorted_indices.add(l)
            return

        mid = (l + r) // 2
        x = sorted_arr[mid]
        i = l
        j = r
        pivot_idx = mid

        while i <= j:
            while i <= r:
                comparisons += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [i, pivot_idx],
                    "swapping": [],
                    "pivot": pivot_idx,
                    "sorted": list(sorted_indices)
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
                    "sorted": list(sorted_indices)
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
                        "sorted": list(sorted_indices)
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
        "sorted": list(range(n))
    })

    steps = len(steps_history)

    return sorted_arr, steps, comparisons, swaps, steps_history