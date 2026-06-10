from app.algorithms import interchange_sort, quick_sort, selection_sort


def sort_array(arr, algorithm):

    if not isinstance(arr, list):
        raise ValueError("Input must be a list")

    if algorithm == 'interchange_sort':
        return interchange_sort(arr)
    elif algorithm == 'quick_sort':
        return quick_sort(arr)
    elif algorithm == 'selection_sort':
        return selection_sort(arr)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}. Supported: interchange_sort, quick_sort, selection_sort")