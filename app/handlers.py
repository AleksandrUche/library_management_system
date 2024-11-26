def add_book_handler(library):
    title = input('Введите название книги: ')
    author = input('Введите автора книги: ')
    year = int(input('Введите год издания книги: '))
    library.add_book(title, author, year)

def remove_book_handler(library):
    book_id = int(input('Введите ID книги для удаления: '))
    library.remove_book(book_id)

def search_books_handler(library):
    query = input('Введите название, автора или год для поиска: ')
    results = library.search_books(query)
    if results:
        for book in results:
            print(
                f'ID: {book.id}, Title: {book.title}, Author: {book.author}, '
                f'Year: {book.year}, Status: {book.status}'
            )
    else:
        print('Книги не найдены.')


def change_status_handler(library):
    book_id = int(input('Введите ID книги для изменения статуса: '))
    new_status = input('Введите новый статус ("в наличии" или "выдана"): ')
    library.change_status(book_id, new_status)

def exit_program_handler():
    print('Выход из программы.')

def invalid_choice_handler():
    print('Некорректный выбор. Пожалуйста, попробуйте снова.')
