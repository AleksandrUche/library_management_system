import json
import os

from handlers import (
    add_book_handler,
    remove_book_handler,
    search_books_handler,
    change_status_handler,
    invalid_choice_handler,
    exit_program_handler,
)
from enums import Menu, BookStatus


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int,
                 status: str = BookStatus.AVAILABLE.value):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['id'], data['title'], data['author'], data['year'], data['status']
        )


class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data]

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False,
                      indent=4)

    def add_book(self, title: str, author: str, year: int):
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f'Книга: "{title}" добавлена с ID: {book_id}.')

    def remove_book(self, book_id: int):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f'Книга с ID: {book_id} удалена.')
                return
        print(f'Книга с ID: {book_id} не найдена.')

    def search_books(self, query: str):
        query = query.lower()
        return [book for book in self.books if self._matches_query(book, query)]

    @staticmethod
    def _matches_query(book: Book, query: str) -> bool:
        return (query in book.title.lower() or
                query in book.author.lower() or
                query == str(book.year))

    def display_books(self):
        if not self.books:
            print('Нет книг в библиотеке.')
            return
        for book in self.books:
            print(
                f'ID: {book.id}, Title: {book.title}, Author: {book.author}, '
                f'Year: {book.year}, Status: {book.status}'
            )

    def change_status(self, book_id: int, new_status: str):
        for book in self.books:
            if book.id == book_id:
                active_statuses = [status.value for status in BookStatus]
                if new_status in active_statuses:
                    book.status = new_status
                    self.save_books()
                    print(f'Статус книги с ID: {book_id} изменен на "{new_status}".')
                else:
                    print(f'Неверный статус. Доступные статусы: {active_statuses}.')
                return
        print(f'Книга с ID: {book_id} не найдена.')


def handler(library: Library):
    main_menu = [elem.text for elem in Menu]
    actions = {
        Menu.ADD_BOOK.program: lambda: add_book_handler(library),
        Menu.REMOVE_BOOK.program: lambda: remove_book_handler(library),
        Menu.SEARCH_BOOKS.program: lambda: search_books_handler(library),
        Menu.DISPLAY_BOOKS.program: library.display_books,
        Menu.CHANGE_STATUS.program: lambda: change_status_handler(library),
        Menu.PROGRAM_EXIT.program: exit_program_handler
    }

    while True:
        print('\nМеню:')
        print(*main_menu, sep='\n')

        choice = int(input(f'Выберите действие (1-{len(main_menu)}): '))

        action = actions.get(choice, lambda: invalid_choice_handler())
        action()
        if action is exit_program_handler:
            break


if __name__ == '__main__':
    library = Library('library.json')
    handler(library)
