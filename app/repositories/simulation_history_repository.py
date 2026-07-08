from app.database.db import db
from app.models.simulation_history import SimulationHistory

class SimulationHistoryRepository:
    @staticmethod
    def get_all():
        return SimulationHistory.query.order_by(
            SimulationHistory.executed_at.desc(),
            SimulationHistory.id.desc()
        ).all()

    @staticmethod
    def get_by_id(history_id):
        return SimulationHistory.query.get(history_id)

    @staticmethod
    def get_by_user(user_id):
        return SimulationHistory.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(data):
        history = SimulationHistory(
            user_id=data['user_id'],
            algorithm_id=data['algorithm_id'],
            input_data=data['input_data'],
            sorted_result=data['sorted_result'],
            steps=data['steps'],
            comparisons=data['comparisons'],
            swaps=data['swaps'],
            execution_time_ms=data['execution_time_ms']
        )
        db.session.add(history)
        db.session.commit()
        return history

    @staticmethod
    def update(history_id, data):
        history = SimulationHistory.query.get(history_id)
        if history:
            history.user_id = data.get('user_id', history.user_id)
            history.algorithm_id = data.get('algorithm_id', history.algorithm_id)
            history.input_data = data.get('input_data', history.input_data)
            history.sorted_result = data.get('sorted_result', history.sorted_result)
            history.steps = data.get('steps', history.steps)
            history.comparisons = data.get('comparisons', history.comparisons)
            history.swaps = data.get('swaps', history.swaps)
            history.execution_time_ms = data.get('execution_time_ms', history.execution_time_ms)
            db.session.commit()
        return history

    @staticmethod
    def delete(history_id):
        history = SimulationHistory.query.get(history_id)
        if history:
            db.session.delete(history)
            db.session.commit()
            return True
        return False
