def quick_sort_logic(arr):
    steps_history = []
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    sorted_indices = set()

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": []
    })

    def _quick_sort(arr, low, high):
        if low < high:
            pi, steps_part = _partition(arr, low, high)
            sorted_indices.add(pi)
            steps_history.extend(steps_part)
            steps_history.append({
                "array": arr.copy(),
                "comparing": [],
                "swapping": [],
                "pivot": pi,
                "sorted": list(sorted_indices)
            })
            _quick_sort(arr, low, pi - 1)
            _quick_sort(arr, pi + 1, high)
        else:
            if low == high and low not in sorted_indices:
                sorted_indices.add(low)
                steps_history.append({
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [],
                    "pivot": low,
                    "sorted": list(sorted_indices)
                })

    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        partition_steps = []

        for j in range(low, high):
            partition_steps.append({
                "array": arr.copy(),
                "comparing": [j, high],
                "swapping": [],
                "pivot": high,
                "sorted": list(sorted_indices)
            })
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                partition_steps.append({
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [i, j],
                    "pivot": high,
                    "sorted": list(sorted_indices)
                })

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        partition_steps.append({
            "array": arr.copy(),
            "comparing": [],
            "swapping": [i + 1, high],
            "pivot": high,
            "sorted": list(sorted_indices)
        })
        return i + 1, partition_steps

    _quick_sort(sorted_arr, 0, n - 1)

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n))
    })

    steps = len(steps_history)
    comparisons = 0
    swaps = 0

    return sorted_arr, steps, comparisons, swaps, steps_history