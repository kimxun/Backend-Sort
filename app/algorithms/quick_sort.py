def quick_sort_logic(arr):
    steps_history = [arr.copy()]
    if len(arr) <= 1:
        return arr, 0, 0, 0, steps_history
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    sorted_left, s1, c1, sw1, hist1 = quick_sort_logic(left)
    sorted_right, s2, c2, sw2, hist2 = quick_sort_logic(right)
    sorted_arr = sorted_left + [pivot] + sorted_right
    steps = s1 + s2 + len(arr)
    comparisons = c1 + c2 + (len(arr)-1)
    swaps = sw1 + sw2
    combined_history = hist1 + hist2 + [sorted_arr]
    return sorted_arr, steps, comparisons, swaps, combined_history