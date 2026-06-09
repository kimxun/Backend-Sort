def interchange_sort_logic(arr, order="asc"):
    """
    Interchange Sort với đầy đủ thông tin visualization
    """
    arr = arr.copy()          # Không thay đổi mảng gốc
    steps = []
    n = len(arr)
    
    # Bước khởi tạo
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "description": "Khởi tạo mảng ban đầu"
    })
    
    for i in range(n - 1):
        for j in range(i + 1, n):
            # Bước so sánh
            steps.append({
                "array": arr.copy(),
                "comparing": [i, j],
                "swapping": [],
                "description": f"So sánh a[{i}] = {arr[i]} và a[{j}] = {arr[j]}"
            })
            
            # Xác định điều kiện hoán đổi
            should_swap = (arr[i] > arr[j]) if order == "asc" else (arr[i] < arr[j])
            
            if should_swap:
                # Thực hiện hoán đổi
                arr[i], arr[j] = arr[j], arr[i]
                
                steps.append({
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [i, j],
                    "description": f"Hoán đổi a[{i}] ↔ a[{j}]"
                })
    
    # Bước kết thúc
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "description": "Hoàn thành sắp xếp!"
    })
    
    return steps