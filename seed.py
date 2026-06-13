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
        # Nếu muốn reset database (xoá sạch và tạo lại bảng), bỏ comment 2 dòng dưới
        db.drop_all()
        db.create_all()
        print("🌱 Seeding data...")

        cat_sort = AlgorithmCategoryRepository.create("Sorting")
        print("Created category: Sorting")

        selection = AlgorithmRepository.create({
            'name': 'Selection Sort',
            'code': 'def selection_sort(arr): ...',
            'description': 'Selection sort algorithm',
            'time_complexity': 'O(n^2)',
            'space_complexity': 'O(1)',
            'category_id': cat_sort.id,
            'slug': 'selection-sort'
        })
        print("Created algorithm: Selection Sort")

        quick = AlgorithmRepository.create({
            'name': 'Quick Sort',
            'code': 'def quick_sort(arr): ...',
            'description': 'Quick sort algorithm',
            'time_complexity': 'O(n log n)',
            'space_complexity': 'O(log n)',
            'category_id': cat_sort.id,
            'slug': 'quick-sort'
        })
        print("Created algorithm: Quick Sort")

        interchange = AlgorithmRepository.create({
            'name': 'Interchange Sort',
            'code': 'def interchange_sort(arr): ...',
            'description': 'Interchange sort algorithm',
            'time_complexity': 'O(n^2)',
            'space_complexity': 'O(1)',
            'category_id': cat_sort.id,
            'slug': 'interchange-sort'
        })
        print("Created algorithm: Interchange Sort")

        admin = UserRepository.create({
            'username': 'admin',
            'password': generate_password_hash('admin123'),
            'full_name': 'Administrator',
            'email': 'admin@example.com',
            'role': 1
        })
        print("Created admin user")

        user = UserRepository.create({
            'username': 'user1',
            'password': generate_password_hash('user123'),
            'full_name': 'Nguyen Van A',
            'email': 'user1@example.com',
            'role': 0
        })
        print("Created user1")

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