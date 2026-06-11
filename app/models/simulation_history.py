class SimulationHistory:
    def __init__(self, id=None, user_id=None, algorithm_id=None, input_data=None,
                 sorted_result=None, steps=0, comparisons=0, swaps=0,
                 execution_time_ms=0, executed_at=None):
        self.id = id
        self.user_id = user_id
        self.algorithm_id = algorithm_id
        self.input_data = input_data
        self.sorted_result = sorted_result
        self.steps = steps
        self.comparisons = comparisons
        self.swaps = swaps
        self.execution_time_ms = execution_time_ms
        self.executed_at = executed_at

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}