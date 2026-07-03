def binary_search_logic(arr, target):
    steps = []
    comparisons = 0
    low, high = 0, len(arr) - 1
    found_index = -1

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        steps.append({
            'array': arr,
            'low': low,
            'high': high,
            'mid': mid,
            'comparing': [mid],
            'found': False,
            'message': f'So sánh arr[{mid}] = {arr[mid]} với {target}'
        })
        if arr[mid] == target:
            found_index = mid
            steps.append({
                'array': arr,
                'comparing': [],
                'found': True,
                'message': f'Tìm thấy {target} tại vị trí {mid}'
            })
            break
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    if found_index == -1:
        steps.append({
            'array': arr,
            'comparing': [],
            'found': False,
            'message': f'Không tìm thấy {target}'
        })

    return steps, comparisons, found_index