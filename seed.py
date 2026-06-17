import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.database.db import db
from app.repositories.algorithm_category_repository import AlgorithmCategoryRepository
from app.repositories.algorithm_repository import AlgorithmRepository
from app.repositories.user_repository import UserRepository
from app.repositories.simulation_history_repository import SimulationHistoryRepository
from werkzeug.security import generate_password_hash

def seed():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    with app.app_context():
        # Reset database (xóa và tạo lại)
        db.drop_all()
        db.create_all()
        print("🌱 Seeding data...")

        # Tạo loại thuật toán
        cat_sort = AlgorithmCategoryRepository.create("Sorting")
        print("Created category: Sorting")

        # Tạo thuật toán Selection Sort (code C++)
        selection = AlgorithmRepository.create({
            'name': 'Selection Sort',
            'code': 'void selection_sort(int arr[], int n) {\n\tfor (int i = 0; i < n-1; i++) {\n\t\tint min_idx = i;\n\t\tfor (int j = i+1; j < n; j++)\n\t\t\tif (arr[j] < arr[min_idx])\n\t\t\t\tmin_idx = j;\n\t\tswap(arr[i], arr[min_idx]);\n\t}\n}',
            'description': 'Selection sort algorithm',
            'time_complexity': 'O(n^2)',
            'space_complexity': 'O(1)',
            'category_id': cat_sort.id,
            'slug': 'selection-sort'
        })
        print("Created algorithm: Selection Sort")

        # Tạo thuật toán Quick Sort (code C++)
        quick = AlgorithmRepository.create({
            'name': 'Quick Sort',
            'code': 'int partition(int arr[], int low, int high) {\n\tint pivot = arr[high];\n\tint i = low - 1;\n\tfor (int j = low; j < high; j++) {\n\t\tif (arr[j] <= pivot) {\n\t\t\ti++;\n\t\t\tswap(arr[i], arr[j]);\n\t\t}\n\t}\n\tswap(arr[i+1], arr[high]);\n\treturn i+1;\n}\n\nvoid quick_sort(int arr[], int low, int high) {\n\tif (low < high) {\n\t\tint pi = partition(arr, low, high);\n\t\tquick_sort(arr, low, pi-1);\n\t\tquick_sort(arr, pi+1, high);\n\t}\n}',
            'description': 'Quick sort algorithm',
            'time_complexity': 'O(n log n)',
            'space_complexity': 'O(log n)',
            'category_id': cat_sort.id,
            'slug': 'quick-sort'
        })
        print("Created algorithm: Quick Sort")

        # Tạo thuật toán Interchange Sort (code C++)
        interchange = AlgorithmRepository.create({
            'name': 'Interchange Sort',
            'code': 'void interchange_sort(int arr[], int n) {\n\tfor (int i = 0; i < n-1; i++) {\n\t\tfor (int j = i+1; j < n; j++) {\n\t\t\tif (arr[i] > arr[j]) {\n\t\t\t\tswap(arr[i], arr[j]);\n\t\t\t}\n\t\t}\n\t}\n}',
            'description': 'Interchange sort algorithm',
            'time_complexity': 'O(n^2)',
            'space_complexity': 'O(1)',
            'category_id': cat_sort.id,
            'slug': 'interchange-sort'
        })
        print("Created algorithm: Interchange Sort")

        # Tạo admin user (có status = 1)
        admin = UserRepository.create({
            'username': 'admin',
            'password': generate_password_hash('admin123'),
            'full_name': 'Administrator',
            'email': 'admin@example.com',
            'role': 1,
            'status': 1   # thêm trạng thái kích hoạt
        })
        print("Created admin user")

        # Tạo user1 (có status = 1)
        user = UserRepository.create({
            'username': 'user1',
            'password': generate_password_hash('user123'),
            'full_name': 'Nguyen Van A',
            'email': 'user1@example.com',
            'role': 0,
            'status': 1   # thêm trạng thái kích hoạt
        })
        print("Created user1")

        # Tạo lịch sử mô phỏng (gắn với user1)
        SimulationHistoryRepository.create({
            'user_id': user.id,
            'algorithm_id': selection.id,
            'input_data': '[5, 3, 8, 1]',
            'sorted_result': '[1, 3, 5, 8]',
            'steps': 10,
            'comparisons': 6,
            'swaps': 3,
            'execution_time_ms': 2
        })
        SimulationHistoryRepository.create({
            'user_id': user.id,
            'algorithm_id': quick.id,
            'input_data': '[9, 2, 7, 4]',
            'sorted_result': '[2, 4, 7, 9]',
            'steps': 5,
            'comparisons': 8,
            'swaps': 3,
            'execution_time_ms': 1
        })
        SimulationHistoryRepository.create({
            'user_id': user.id,
            'algorithm_id': interchange.id,
            'input_data': '[4, 2, 7, 1]',
            'sorted_result': '[1, 2, 4, 7]',
            'steps': 8,
            'comparisons': 6,
            'swaps': 4,
            'execution_time_ms': 1
        })
        print("Created simulation history for all three algorithms")
        print("🎉 Seeding completed!")

if __name__ == "__main__":
    seed()