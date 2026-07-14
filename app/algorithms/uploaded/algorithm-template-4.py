DISPLAY_CODE = """void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}"""

FEATURES = ["pivot"]

DESCRIPTION = "So sánh lần lượt các cặp phần tử liền kề, đưa phần tử lớn nhất về cuối dãy."

TIME_COMPLEXITY = "O(n^2)"

SPACE_COMPLEXITY = "O(1)"

STEPS = [
    "Duyệt từ đầu dãy đến cuối dãy",
    "So sánh phần tử hiện tại với phần tử kế tiếp",
    "Nếu phần tử hiện tại > phần tử kế tiếp → hoán đổi",
    "Lặp lại cho đến khi không còn hoán đổi nào xảy ra"
]

def run_logic(arr, sort_order="asc"):
    steps_history = []
    comparisons = 0
    swaps = 0
    sorted_arr = arr.copy()
    n = len(sorted_arr)

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": [],
        "line": 1,
        "keys": ["n"],
        "vals": [n],
        "action": (
            f"Bắt đầu Bubble Sort theo thứ tự "
            f"{'tăng dần' if sort_order == 'asc' else 'giảm dần'}."
        )
    })

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparisons += 1
            steps_history.append({
                "array": sorted_arr.copy(),
                "comparing": [j, j + 1],
                "swapping": [],
                "pivot": None,
                "sorted": list(range(n - i, n)),
                "line": 3,
                "keys": ["j", "a[j]", "a[j+1]"],
                "vals": [j, sorted_arr[j], sorted_arr[j + 1]],
                "action": f"So sánh a[{j}] = {sorted_arr[j]} với a[{j + 1}] = {sorted_arr[j + 1]}"
            })

            condition = (
                sorted_arr[j] > sorted_arr[j + 1]
                if sort_order == "asc"
                else sorted_arr[j] < sorted_arr[j + 1]
            )
            if condition:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swaps += 1
                steps_history.append({
                    "array": sorted_arr.copy(),
                    "comparing": [],
                    "swapping": [j, j + 1],
                    "pivot": None,
                    "sorted": list(range(n - i, n)),
                    "line": 4,
                    "keys": ["j"],
                    "vals": [j],
                    "action": f"Hoán đổi vị trí {j} và {j + 1}"
                })

    steps_history.append({
        "array": sorted_arr.copy(),
        "comparing": [],
        "swapping": [],
        "pivot": None,
        "sorted": list(range(n)),
        "line": 5,
        "keys": ["Tổng số phép so sánh", "Tổng số phép hoán đổi"],
        "vals": [comparisons, swaps],
        "action": "Mảng đã được sắp xếp"
    })

    return sorted_arr, len(steps_history), comparisons, swaps, steps_history