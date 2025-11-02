from aiogram.fsm.state import State, StatesGroup

class Registry(StatesGroup):
    name = State()
    flag = State()
    leader = State()
    change_flag = State()