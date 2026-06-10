from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from algorithms.interchange_sort import interchange_sort_logic
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)  

print("CONFIG DB =", app.config["SQLALCHEMY_DATABASE_URI"])
algorithms_db = {
    "interchange": {
        "title": "Interchange Sort",
        "pseudo_code": [
            "for i = 0 -> n-2",
            "   for j = i+1 -> n-1",
            "      if a[i] > a[j]",
            "         swap(a[i], a[j])"
        ],
        "complexity": {
            "best": "O(n²)",
            "avg": "O(n²)",
            "worst": "O(n²)",
            "space": "O(1)"
        }
    }
}


# @app.route('/api/algorithms', methods=['GET'])
# def get_algorithms():
#     return jsonify(algorithms_db)


# @app.route('/api/sort', methods=['POST'])
# def sort_array():
#     data = request.get_json()

#     array = data.get("array", [])
#     algorithm = data.get("algorithm", "interchange")

#     if algorithm == "interchange":
#         steps = interchange_sort_logic(array)
#         return jsonify({
#             "success": True,
#             "steps": steps
#         })

#     return jsonify({
#         "success": False,
#         "message": "Thuật toán chưa được hỗ trợ"
#     }), 400


if __name__ == '__main__':
      with app.app_context():
        try:
            db.session.execute(db.text("SELECT 1"))
            print("✅ Kết nối MySQL thành công!")
        except Exception as e:
            print("❌ Kết nối MySQL thất bại!")
            print(e)
    
app.run(debug=True, port=5000)