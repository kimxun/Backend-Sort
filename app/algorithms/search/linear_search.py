def linear_search_logic(arr, target):
    steps = []
    comparisons = 0
    found_index = -1

    for i, val in enumerate(arr):
        comparisons += 1
        steps.append({
            'array': arr,
            'current_index': i,
            'comparing': [i],
            'found': False,
            'message': f'So sánh arr[{i}] = {val} với {target}'
        })
        if val == target:
            found_index = i
            steps.append({
                'array': arr,
                'current_index': i,
                'comparing': [],
                'found': True,
                'message': f'Tìm thấy {target} tại vị trí {i}'
            })
            break

    if found_index == -1:
        steps.append({
            'array': arr,
            'current_index': -1,
            'comparing': [],
            'found': False,
            'message': f'Không tìm thấy {target} trong mảng'
        })

    return steps, comparisons, found_index