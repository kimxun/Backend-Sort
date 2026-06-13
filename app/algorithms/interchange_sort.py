def interchange_sort_logic(arr):
    steps = 0
    comparisons = 0
    swaps = 0
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    steps_history = [sorted_arr.copy()]
    for i in range(n-1):
        for j in range(i+1, n):
            comparisons += 1
            steps += 1
            if sorted_arr[i] > sorted_arr[j]:
                sorted_arr[i], sorted_arr[j] = sorted_arr[j], sorted_arr[i]
                swaps += 1
                steps_history.append(sorted_arr.copy())
        steps += 1
    return sorted_arr, steps, comparisons, swaps, steps_history