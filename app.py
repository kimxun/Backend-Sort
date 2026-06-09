from flask import Flask, jsonify, request
from flask_cors import CORS

# Import từ algorithms package
from algorithms import (
    interchange_sort_logic,
    selection_sort_logic,
    quick_sort_logic
)

app = Flask(__name__)
CORS(app)

# Database thuật toán
algorithms_db = {
    "interchange": {
        "id": "interchange",
        "title": "Interchange Sort",
        "description": "Thuật toán hoán vị - so sánh từng cặp và hoán đổi.",
        "pseudo_code": ["for i = 0 to n-2", "    for j = i+1 to n-1", "        if a[i] > a[j] then swap"],
        "complexity": {"best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"}
    },
    "selection": {
        "id": "selection",
        "title": "Selection Sort",
        "description": "Chọn phần tử nhỏ nhất và hoán đổi vào vị trí đúng.",
        "pseudo_code": ["for i = 0 to n-2", "    min = i", "    for j = i+1 to n-1", "        if a[j] < a[min]"],
        "complexity": {"best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"}
    },
    "quick": {
        "id": "quick",
        "title": "Quick Sort",
        "description": "Thuật toán chia để trị nhanh nhất trên thực tế.",
        "pseudo_code": ["quickSort(low, high)", "    pi = partition()", "    quickSort(low, pi-1)"],
        "complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)", "space": "O(log n)"}
    }
}

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    return jsonify({
        "success": True,
        "data": list(algorithms_db.values()),
        "count": len(algorithms_db)
    })

@app.route('/api/sort', methods=['POST'])
def sort_array():
    try:
        data = request.get_json()
        array = data.get("array", [])
        algorithm = data.get("algorithm", "interchange")
        sort_order = data.get("sortOrder", "asc")

        if not array or len(array) == 0:
            return jsonify({"success": False, "message": "Mảng không được rỗng"}), 400

        if algorithm == "interchange":
            steps = interchange_sort_logic(array, sort_order)
        elif algorithm == "selection":
            steps = selection_sort_logic(array, sort_order)
        elif algorithm == "quick":
            steps = quick_sort_logic(array, sort_order)
        else:
            return jsonify({"success": False, "message": "Thuật toán chưa được hỗ trợ"}), 400

        return jsonify({
            "success": True,
            "algorithm": algorithm,
            "original": array,
            "result": steps[-1]["array"],
            "steps": steps,
            "totalSteps": len(steps)
        })

    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi server: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')