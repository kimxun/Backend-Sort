from flask import Flask, jsonify
from flask_cors import CORS
from app.controllers.sort_controller import sort_bp
from config import Config
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)  
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
      with app.app_context():
        try:
            db.session.execute(db.text("SELECT 1"))
            print("✅ Kết nối MySQL thành công!")
        except Exception as e:
            print("❌ Kết nối MySQL thất bại!")
            print(e)
if __name__ == '__main__':
    app.run(debug=True)