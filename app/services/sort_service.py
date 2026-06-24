from app.algorithms import interchange_sort_logic as interchange_sort
from app.algorithms import quick_sort_logic as quick_sort
from app.algorithms import selection_sort_logic as selection_sort
from app.repositories.algorithm_repository import AlgorithmRepository
from app.repositories.simulation_history_repository import SimulationHistoryRepository
from app.models.algorithm import Algorithm
from app.config.cache import cache


def sort_array_with_metrics(arr, algorithm, sort_order="asc"):
    if not isinstance(arr, list):
        raise ValueError("Input must be a list")

    # Đổi biến '_' thành 'steps_list' và trả 'steps_list' về cho controller
    if algorithm == 'interchange_sort':
        sorted_arr, step_count, comparisons, swaps, steps_list = interchange_sort(arr, sort_order)
        return sorted_arr, steps_list, comparisons, swaps
        
    elif algorithm == 'quick_sort':
        sorted_arr, step_count, comparisons, swaps, steps_list = quick_sort(arr, sort_order)
        return sorted_arr, steps_list, comparisons, swaps
        
    elif algorithm == 'selection_sort':
        sorted_arr, step_count, comparisons, swaps, steps_list = selection_sort(arr, sort_order)
        return sorted_arr, steps_list, comparisons, swaps
        
    else:
        raise ValueError(
            f"Unsupported algorithm: {algorithm}. Only support: interchange_sort, quick_sort, selection_sort")


class SortService:
    @staticmethod
    def get_all_algorithms(page=None, limit=None, is_admin=False):
        if page is None or limit is None:
            return AlgorithmRepository.get_all(is_admin=is_admin)
        else:
            if page < 1:
                page = 1
            if limit < 1:
                limit = 5
            offset = (page - 1) * limit

            query = Algorithm.query
            if is_admin:
                query = query.filter(Algorithm.status != -1)
            else:
                query = query.filter_by(status=1)

            total = query.count()
            filename = query.offset(offset).limit(limit).all()
            return {
                "data": [a.to_dict() for a in filename],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "totalPages": (total + limit - 1) // limit
                }
            }

    @staticmethod
    def get_algorithm_by_id(algorithm_id):
        return AlgorithmRepository.get_by_id(algorithm_id)

    @staticmethod
    def get_algorithm_by_slug(slug):
        return AlgorithmRepository.get_by_slug(slug)

    @staticmethod
    def create_algorithm(data):
        return AlgorithmRepository.create(data)

    @staticmethod
    def save_simulation(user_id, algorithm_id, input_data, sorted_result,
                        steps, comparisons, swaps, execution_time_ms):
        # Đảm bảo nếu truyền vào một list các bước, DB vẫn lưu số lượng bước (int)
        final_step_count = len(steps) if isinstance(steps, list) else steps

        data = {
            'user_id': user_id,
            'algorithm_id': algorithm_id,
            'input_data': input_data,
            'sorted_result': sorted_result,
            'steps': final_step_count, # Lưu con số vào Database để tránh lỗi cấu trúc bảng
            'comparisons': comparisons,
            'swaps': swaps,
            'execution_time_ms': execution_time_ms
        }
        return SimulationHistoryRepository.create(data)

    @staticmethod
    def get_user_history(user_id):
        return SimulationHistoryRepository.get_by_user(user_id)

    @staticmethod
    def update_algorithm(algorithm_id, data):
        return AlgorithmRepository.update(algorithm_id, data)

    @staticmethod
    def delete_algorithm(algorithm_id):
        return AlgorithmRepository.delete(algorithm_id)