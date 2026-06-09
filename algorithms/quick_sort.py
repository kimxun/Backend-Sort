def quick_sort_logic(arr, order="asc"):
    """
    Quick Sort với visualization (sử dụng Lomuto partition)
    """
    arr = arr.copy()
    steps = []
    
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        
        steps.append({
            "array": arr.copy(),
            "comparing": [high],
            "swapping": [],
            "description": f"Chọn pivot = a[{high}] = {pivot}"
        })
        
        for j in range(low, high):
            steps.append({
                "array": arr.copy(),
                "comparing": [j, high],
                "swapping": [],
                "description": f"So sánh a[{j}] với pivot {pivot}"
            })
            
            should_swap = (arr[j] <= pivot) if order == "asc" else (arr[j] >= pivot)
            
            if should_swap:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    steps.append({
                        "array": arr.copy(),
                        "comparing": [],
                        "swapping": [i, j],
                        "description": f"Hoán đổi a[{i}] ↔ a[{j}]"
                    })
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append({
            "array": arr.copy(),
            "comparing": [],
            "swapping": [i + 1, high],
            "description": f"Đặt pivot vào vị trí đúng: {i+1}"
        })
        
        return i + 1
    
    def quicksort(low, high):
        if low < high:
            pi = partition(low, high)
            quicksort(low, pi - 1)
            quicksort(pi + 1, high)
    
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "description": "Bắt đầu Quick Sort"
    })
    
    quicksort(0, len(arr) - 1)
    
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "description": "Hoàn thành Quick Sort!"
    })
    
    return steps