from aiogram.fsm.state import State, StatesGroup

class UserThread(StatesGroup):
    thread_id = State()