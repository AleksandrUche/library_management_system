import enum


class Menu(enum.Enum):
    """Главное меню"""
    ADD_BOOK = 1, '1. Добавить книгу'
    REMOVE_BOOK = 2, '2. Удалить книгу'
    SEARCH_BOOKS = 3, '3. Искать книги'
    DISPLAY_BOOKS = 4, '4. Отобразить все книги'
    CHANGE_STATUS = 5, '5. Изменить статус книги'
    PROGRAM_EXIT  = 6, '6. Выход'

    def __init__(self, program: int, text: str):
        self.program = program
        self.text = text

class BookStatus(enum.Enum):
    """Статус книги"""
    AVAILABLE = "в наличии"
    ISSUED = "выдана"
