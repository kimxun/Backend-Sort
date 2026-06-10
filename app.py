from flask import Flask, jsonify
from flask_cors import CORS
from app.controllers.sort_controller import sort_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(sort_bp, url_prefix='/api/sort')

@app.route('/')
def home():
    return jsonify({
        "message": "Backend Sort API is running",
        "endpoints": {
            "POST /api/sort": "Sort an array. Body: { \"array\": [3,1,2], \"algorithm\": \"quick_sort\" }"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)