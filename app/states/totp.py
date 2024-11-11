from aiogram.fsm.state import State, StatesGroup

class TotpState(StatesGroup):
    name = State()
    key = State()