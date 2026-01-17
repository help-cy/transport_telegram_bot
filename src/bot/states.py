from aiogram.fsm.state import State, StatesGroup


class ReportStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_media = State()
    reviewing_report = State()
