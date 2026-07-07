import sys
import os
import json
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
from app.config.cache import cache
from app.models.algorithm import Algorithm
from app.models.algorithm_category import AlgorithmCategory
from app.models.simulation_history import SimulationHistory
from app.models.user import User
def seed():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    cache.init_app(app)
    CORS(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        print("🌱 Seeding data...")

        cat_sort = AlgorithmCategoryRepository.create("Sorting")
        print("Created category: Sorting")

        cat_search = AlgorithmCategoryRepository.create("Searching")
        print("Created category: Searching")

        selection = AlgorithmRepository.create({
            'name': 'Selection Sort',
            'code': 'void SelectionSort(int a[], int N) {\n\tint min;\n\tfor( int i = 0; i < N-1; i++ ) {\n\t\tmin = i;\n\t\tfor ( int j = i+1; j < N; j++ )\n\t\t\tif (a[j] < a[min])\n\t\t\t\tmin = j;\n\t\tswap( a[min], a[i] );\n\t}\n}',
            'description': 'Tìm phần tử nhỏ nhất trong phần chưa sắp xếp, đặt vào đầu danh sách. Lặp lại cho đến hết.',
            'time_complexity': 'O(n^2)',
            'space_complexity': 'O(1)',
            'steps': json.dumps([
            'Đặt i = 0, minIdx = i',
            'Duyệt j từ i+1 đến cuối',
            'Nếu a[j] < a[minIdx] → minIdx = j',
            'Hoán đổi a[i] ↔ a[minIdx]',
            'Tăng i, lặp lại'
        ]),
            'category_id': cat_sort.id,
            'slug': 'selection-sort',
            'status': 1
        })
        print("Created algorithm: Selection Sort")

        quick = AlgorithmRepository.create({
            'name': 'Quick Sort',
            'code': 'void QuickSort(int a[], int l, int r) {\n\tint i, j, x;\n\tx = a[(l+r)/2];\n\ti = l; j = r;\n\tdo {\n\t\twhile (a[i]<x) i++;\n\t\twhile (a[j]>x) j--;\n\t\tif (i<=j) {\n\t\t\tswap(a[i],a[j]);\n\t\t\ti++;\n\t\t\tj--;\n\t\t}\n\t} while (i<=j);\n\tif (l<j) QuickSort(a,l,j);\n\tif (i<r) QuickSort(a,i,r);\n}',
            'description': 'Chọn một phần tử làm mốc, sau đó chia mảng thành hai phần: phần tử nhỏ hơn mốc và phần tử lớn hơn mốc. Lặp lại quy trình cho từng phần.',
            'time_complexity': 'O(n log n)',
            'space_complexity': 'O(log n)',
            'steps': json.dumps([
            'Chọn mốc x = a[(l+r)/2], đặt i = l, j = r',
            'Tìm a[i] ≥ x và a[j] ≤ x nằm sai vị trí',
            'Nếu i ≤ j → Hoán vị a[i] ↔ a[j], tăng i, giảm j',
            'Lặp lại kiểm tra cho đến khi i > j',
            'Đệ quy với dãy con bên trái l đến j và bên phải i đến r'
        ]),
            'category_id': cat_sort.id,
            'slug': 'quick-sort',
            'status': 1
        })
        print("Created algorithm: Quick Sort")

        interchange = AlgorithmRepository.create({
            'name': 'Interchange Sort',
            'code': 'void InterchangeSort(int a[], int N) {\n\tint i,j;\n\tfor(i=0; i<N-1; i++)\n\t\tfor(j=i+1; j<N; j++)\n\t\t\tif(a[i]>a[j])\n\t\t\t\tswap(a[i],a[j]);\n}',
            'description': 'So sánh từng cặp phần tử theo thứ tự và hoán đổi ngay nếu chúng không đúng vị trí.',
            'time_complexity': 'O(n^2)',
            'space_complexity': 'O(1)',
            'category_id': cat_sort.id,
            'slug': 'interchange-sort',
            'steps': json.dumps([
            'Duyệt i từ 0 đến n-2',
            'Duyệt j từ i+1 đến n-1',
            'Nếu a[i] > a[j] → hoán đổi a[i] ↔ a[j]',
            'Tăng i, lặp lại'
        ]),
            'status': 1
        })
        print("Created algorithm: Interchange Sort")

        linear = AlgorithmRepository.create({
            'name': 'Linear Search',
            'code': 'int LinearSearch1(int a[], int N, int x) {\n\tint i = 0;\n\twhile ((i < N) && (a[i] != x))\n\t\ti++;\n\tif (i == N)\n\t\treturn -1;\n\treturn i;\n}',
            'description': 'Duyệt tuần tự từng phần tử cho đến khi tìm thấy giá trị cần tìm hoặc hết mảng.',
            'time_complexity': 'O(n)',
            'space_complexity': 'O(1)',
            'steps': json.dumps([
            'Bắt đầu từ i = 0',
            'So sánh arr[i] với giá trị cần tìm',
            'Nếu bằng → trả về i (tìm thấy)',
            'Nếu không → tăng i lên 1 và lặp lại',
            'Nếu i >= N mà chưa tìm thấy → trả về -1'
        ]),
            'category_id': cat_search.id,
            'slug': 'linear-search',
            'status': 1
        })
        print("Created algorithm: Linear Search")

        binary = AlgorithmRepository.create({
            'name': 'Binary Search',
            'code': 'int BinarySearch(int a[], int N, int x) {\n\tint left = 0, right = N - 1, mid;\n\tdo {\n\t\tmid = (left + right) / 2;\n\t\tif (x == a[mid])\n\t\t\treturn mid;\n\t\telse if (x < a[mid])\n\t\t\tright = mid - 1;\n\t\telse\n\t\t\tleft = mid + 1;\n\t} while (left <= right);\n\treturn -1;\n}',
            'description': 'Tìm kiếm trên mảng đã sắp xếp bằng cách liên tục chia đôi khoảng tìm kiếm.',
            'time_complexity': 'O(log n)',
            'space_complexity': 'O(1)',
            'steps': json.dumps([
            'Đặt left = 0, right = N-1',
            'Tính mid = (left + right) / 2',
            'So sánh arr[mid] với x',
            'Nếu bằng → trả về mid',
            'Nếu arr[mid] < x → left = mid + 1',
            'Nếu arr[mid] > x → right = mid - 1',
            'Lặp lại cho đến khi tìm thấy hoặc left > right'
        ]),
            'category_id': cat_search.id,
            'slug': 'binary-search',
            'status': 1
        })
        print("Created algorithm: Binary Search")

        admin = UserRepository.create({
            'username': 'admin',
            'password': generate_password_hash('admin123'),
            'full_name': 'Administrator',
            'email': 'admin@example.com',
            'role': 1,
            'status': 1
        })
        print("Created admin user")

        user = UserRepository.create({
            'username': 'user1',
            'password': generate_password_hash('user123'),
            'full_name': 'Nguyen Van A',
            'email': 'user1@example.com',
            'role': 0,
            'status': 1
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
