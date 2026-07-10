"""
=====================================================================
TEMPLATE THUẬT TOÁN - BẮT BUỘC TUÂN THEO ĐỊNH DẠNG NÀY ĐỂ UPLOAD ĐƯỢC
=====================================================================

QUY TẮC BẮT BUỘC:
1. File PHẢI có đúng MỘT hàm tên chính xác là: run_logic
2. Chữ ký hàm PHẢI là: def run_logic(arr, sort_order="asc")
   - arr: list các số (list[int] hoặc list[float])
   - sort_order: string "asc" hoặc "desc"
3. Hàm PHẢI return đúng thứ tự 5 giá trị (tuple), không được thiếu/thừa:
   return sorted_arr, len(steps_history), comparisons, swaps, steps_history

4. steps_history PHẢI là list các dict, mỗi dict PHẢI có đủ các key sau
   (thiếu key nào, bước đó sẽ không hiển thị đúng trên giao diện mô phỏng):

   {
       "array": list,        # trạng thái mảng tại bước này (BẮT BUỘC copy(), không share reference)
       "comparing": list,    # index đang so sánh, vd [i, j] hoặc [] nếu không có
       "swapping": list,     # index đang hoán đổi, vd [i, j] hoặc [] nếu không có
       "pivot": int hoặc None,   # index pivot (dùng cho quick sort...), None nếu không áp dụng
       "sorted": list,       # các index đã được xác định đúng vị trí cuối cùng
       "line": int,          # số dòng code tương ứng (dùng để highlight code khi mô phỏng chạy)
       "keys": list[str],    # tên các biến muốn hiển thị (vd ["i", "j"])
       "vals": list,         # giá trị tương ứng với "keys" (PHẢI cùng độ dài với keys)
       "action": str         # mô tả bước này bằng tiếng Việt, hiển thị cho người xem
   }

5. KHÔNG được import các thư viện ngoài danh sách cho phép:
   Cho phép: (không cần import gì cả cho hầu hết thuật toán sắp xếp cơ bản)
   Nếu cần thêm, chỉ được: math, random, copy
   CẤM: os, sys, subprocess, socket, requests, open(), eval(), exec(), __import__,
        importlib, shutil, pickle, ctypes, hoặc bất kỳ thư viện I/O / network nào khác.
   (Backend sẽ tự động quét và từ chối file nếu phát hiện các từ khoá cấm ở trên)

6. KHÔNG được có vòng lặp vô hạn / không giới hạn số bước quá lớn.
   Backend sẽ tự động dừng và báo lỗi nếu steps_history vượt quá 5000 phần tử,
   hoặc nếu thời gian thực thi hàm vượt quá 15 giây.

7. Tên file khi upload sẽ tự động dùng làm slug (bỏ đuôi .py, chuẩn hoá về dạng
   chữ-thường-có-gạch-ngang). Ví dụ: file "Bubble_Sort.py" -> slug "bubble-sort".
   Slug này sẽ được dùng để tra cứu khi chạy mô phỏng, nên đặt tên file rõ ràng,
   không trùng với thuật toán đã có sẵn (selection-sort, quick-sort,
   interchange-sort, linear-search, binary-search) trừ khi bạn muốn GHI ĐÈ.

8. NÊN khai báo biến DISPLAY_CODE (chuỗi) chứa pseudocode / code mẫu hiển thị
   trên giao diện Code Editor. Nếu không có, hệ thống vẫn lưu được nhưng sẽ để
   trống ô Code và nhắc nhở admin tự nhập tay.

=====================================================================
VÍ DỤ MẪU: BUBBLE SORT (copy cấu trúc này để viết thuật toán của bạn)
=====================================================================
"""

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