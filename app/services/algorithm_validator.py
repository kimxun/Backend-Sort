import ast
import re
import os
import importlib.util
import unicodedata
import multiprocessing

FORBIDDEN_MODULES = {
    "os", "sys", "subprocess", "socket", "requests", "shutil",
    "pickle", "ctypes", "importlib", "urllib", "http", "ftplib",
    "smtplib", "sqlite3", "multiprocessing", "threading", "asyncio",
    "eval", "exec", "compile", "__import__", "open", "input",
}

ALLOWED_MODULES = {"math", "random", "copy"}

REQUIRED_FUNCTION_NAME = "run_logic"
REQUIRED_STEP_KEYS = {
    "array", "comparing", "swapping", "pivot",
    "sorted", "line", "keys", "vals", "action"
}

MAX_STEPS = 5000
MAX_EXECUTION_SECONDS = 15
MAX_FILE_SIZE_BYTES = 200 * 1024

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'algorithms', 'uploaded')

COMPLEXITY_MAP = {
    'bubble-sort': ('O(n^2)', 'O(1)'),
    'selection-sort': ('O(n^2)', 'O(1)'),
    'insertion-sort': ('O(n^2)', 'O(1)'),
    'merge-sort': ('O(n log n)', 'O(n)'),
    'quick-sort': ('O(n log n)', 'O(log n)'),
    'heap-sort': ('O(n log n)', 'O(1)'),
    'counting-sort': ('O(n + k)', 'O(k)'),
    'radix-sort': ('O(d*(n+k))', 'O(n+k)'),
    'linear-search': ('O(n)', 'O(1)'),
    'binary-search': ('O(log n)', 'O(1)'),
    'interchange-sort': ('O(n^2)', 'O(1)'),
}


class AlgorithmValidationError(Exception):
    pass


class AlgorithmExecutionTimeout(Exception):
    pass


def generate_slug_from_filename(filename):
    name = os.path.splitext(filename)[0]
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    name = re.sub(r"(?<!^)(?=[A-Z])", "-", name)
    name = name.replace("_", "-").replace(" ", "-")
    name = name.lower()
    name = re.sub(r"[^a-z0-9-]", "", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def remove_docstring(source):
    stripped = source.lstrip()
    if stripped.startswith('"""') or stripped.startswith("'''"):
        quote = stripped[:3]
        end = stripped.find(quote, 3)
        if end != -1:
            return stripped[end+3:].lstrip()
    return source


def extract_display_code(source_code):
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "DISPLAY_CODE":
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        return node.value.value
    return None


def extract_features(source_code):
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "FEATURES":
                    if isinstance(node.value, ast.List):
                        features = []
                        for item in node.value.elts:
                            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                                features.append(item.value)
                        return features
    return []


def extract_time_complexity(source_code: str):
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TIME_COMPLEXITY":
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        return node.value.value
    return None


def extract_space_complexity(source_code: str):
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "SPACE_COMPLEXITY":
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        return node.value.value
    return None


def validate_source_code(source_code: str):
    if len(source_code.encode("utf-8")) > MAX_FILE_SIZE_BYTES:
        raise AlgorithmValidationError(
            f"File vượt quá giới hạn {MAX_FILE_SIZE_BYTES // 1024}KB."
        )

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise AlgorithmValidationError(f"Lỗi cú pháp Python: {e}")

    found_function = False
    function_args = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split(".")[0]
                if root_module in FORBIDDEN_MODULES:
                    raise AlgorithmValidationError(
                        f"Không được phép import module '{root_module}'."
                    )
                if root_module not in ALLOWED_MODULES:
                    raise AlgorithmValidationError(
                        f"Module '{root_module}' không nằm trong danh sách cho phép "
                        f"({', '.join(ALLOWED_MODULES)})."
                    )
        if isinstance(node, ast.ImportFrom):
            root_module = (node.module or "").split(".")[0]
            if root_module in FORBIDDEN_MODULES:
                raise AlgorithmValidationError(
                    f"Không được phép import từ module '{root_module}'."
                )
            if root_module not in ALLOWED_MODULES:
                raise AlgorithmValidationError(
                    f"Module '{root_module}' không nằm trong danh sách cho phép."
                )

        if isinstance(node, ast.Call):
            func_name = None
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            if func_name in FORBIDDEN_MODULES:
                raise AlgorithmValidationError(
                    f"Không được phép gọi hàm '{func_name}'."
                )

        if isinstance(node, ast.FunctionDef) and node.name == REQUIRED_FUNCTION_NAME:
            found_function = True
            function_args = [arg.arg for arg in node.args.args]

    if not found_function:
        raise AlgorithmValidationError(
            f"File phải có hàm tên chính xác '{REQUIRED_FUNCTION_NAME}(arr, sort_order=\"asc\")'."
        )

    if function_args is None or function_args[:1] != ["arr"]:
        raise AlgorithmValidationError(
            f"Hàm '{REQUIRED_FUNCTION_NAME}' phải có tham số đầu tiên tên 'arr'."
        )

    return True


def _worker_run_algorithm(filepath, module_name, test_array, queue):
    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        func = getattr(module, REQUIRED_FUNCTION_NAME)
        result = func(test_array.copy(), "asc")
        queue.put(("ok", result))
    except Exception as e:
        queue.put(("error", str(e)))


def load_and_test_module(filepath: str, slug: str):
    module_name = f"uploaded_algo_{slug.replace('-', '_')}"
    test_array = [5, 3, 8, 1, 9, 2, 7]

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=_worker_run_algorithm,
        args=(filepath, module_name, test_array, queue)
    )
    process.start()

    status = None
    value = None
    try:
        status, value = queue.get(timeout=MAX_EXECUTION_SECONDS)
    except Exception:
        pass
    finally:
        process.join(timeout=2)
        if process.is_alive():
            process.terminate()
            process.join()

    if status is None:
        raise AlgorithmValidationError(
            f"Thuật toán chạy quá {MAX_EXECUTION_SECONDS} giây hoặc không trả về kết quả "
            "— có thể bị lặp vô hạn hoặc crash không rõ nguyên nhân."
        )

    if status == "error":
        raise AlgorithmValidationError(f"Lỗi khi chạy thử thuật toán: {value}")

    sorted_arr, steps_count, comparisons, swaps, steps_history = value

    if not isinstance(sorted_arr, list):
        raise AlgorithmValidationError("Giá trị trả về đầu tiên (sorted_arr) phải là list.")

    if not isinstance(steps_history, list) or len(steps_history) == 0:
        raise AlgorithmValidationError("steps_history phải là list và không được rỗng.")

    if len(steps_history) > MAX_STEPS:
        raise AlgorithmValidationError(
            f"steps_history có {len(steps_history)} bước, vượt quá giới hạn {MAX_STEPS}. "
            "Kiểm tra lại thuật toán có bị lặp vô hạn không."
        )

    for idx, step in enumerate(steps_history):
        if not isinstance(step, dict):
            raise AlgorithmValidationError(f"Bước thứ {idx} trong steps_history không phải dict.")
        missing_keys = REQUIRED_STEP_KEYS - set(step.keys())
        if missing_keys:
            raise AlgorithmValidationError(
                f"Bước thứ {idx} thiếu các key bắt buộc: {', '.join(missing_keys)}."
            )
        if not isinstance(step["keys"], list) or not isinstance(step["vals"], list):
            raise AlgorithmValidationError(
                f"Bước thứ {idx}: 'keys' và 'vals' phải là list."
            )
        if len(step["keys"]) != len(step["vals"]):
            raise AlgorithmValidationError(
                f"Bước thứ {idx}: 'keys' và 'vals' phải có cùng độ dài."
            )

    if sorted(test_array) != sorted_arr:
        raise AlgorithmValidationError(
            "Kết quả sắp xếp không chứa đúng các phần tử ban đầu."
        )

    return True


def validate_and_save_algorithm_file(file_storage, original_filename: str):
    if not original_filename.endswith(".py"):
        raise AlgorithmValidationError("Chỉ chấp nhận file .py")

    slug = generate_slug_from_filename(original_filename)
    if not slug:
        raise AlgorithmValidationError("Không thể tạo slug hợp lệ từ tên file.")

    source_code = file_storage.read().decode("utf-8")
    file_storage.seek(0)

    display_code = extract_display_code(source_code)
    features = extract_features(source_code)
    time_complexity = extract_time_complexity(source_code)
    space_complexity = extract_space_complexity(source_code)

    if not time_complexity and slug in COMPLEXITY_MAP:
        time_complexity, _ = COMPLEXITY_MAP[slug]
    if not space_complexity and slug in COMPLEXITY_MAP:
        _, space_complexity = COMPLEXITY_MAP[slug]

    source_code = remove_docstring(source_code)
    validate_source_code(source_code)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    temp_filepath = os.path.join(UPLOAD_DIR, f"_temp_{slug}.py")
    with open(temp_filepath, "w", encoding="utf-8") as f:
        f.write(source_code)

    try:
        load_and_test_module(temp_filepath, slug)
        final_filepath = os.path.join(UPLOAD_DIR, f"{slug}.py")
        os.replace(temp_filepath, final_filepath)
        return slug, final_filepath, display_code, features, time_complexity, space_complexity
    except AlgorithmValidationError:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        raise


def load_uploaded_algorithm_function(slug: str):
    filepath = os.path.join(UPLOAD_DIR, f"{slug}.py")
    if not os.path.exists(filepath):
        return None

    module_name = f"uploaded_algo_{slug.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, REQUIRED_FUNCTION_NAME, None)