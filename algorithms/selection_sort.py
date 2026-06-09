def selection_sort_logic(arr, order="asc"):
    """
    Selection Sort với đầy đủ thông tin visualization
    """
    arr = arr.copy()
    steps = []
    n = len(arr)
    
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "description": "Khởi tạo mảng ban đầu"
    })
    
    for i in range(n - 1):
        min_idx = i  # hoặc max_idx tùy theo thứ tự
        
        for j in range(i + 1, n):
            # So sánh
            steps.append({
                "array": arr.copy(),
                "comparing": [min_idx, j],
                "swapping": [],
                "description": f"So sánh a[{min_idx}] và a[{j}]"
            })
            
            # Cập nhật min/max
            if order == "asc":
                if arr[j] < arr[min_idx]:
                    min_idx = j
            else:
                if arr[j] > arr[min_idx]:
                    min_idx = j
        
        # Hoán đổi nếu cần
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                "array": arr.copy(),
                "comparing": [],
                "swapping": [i, min_idx],
                "description": f"Hoán đổi a[{i}] ↔ a[{min_idx}] (phần tử nhỏ nhất/lớn nhất)"
            })
    
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "description": "Hoàn thành sắp xếp!"
    })
    
    return steps