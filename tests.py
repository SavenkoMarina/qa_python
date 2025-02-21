from main import BooksCollector
import pytest


@pytest.fixture
def collector():
    return BooksCollector()

class TestBooksCollector:
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_wrong_name(self, collector):
        assert len(collector.get_books_genre()) == 0
        collector.add_new_book('1'*42)
        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize('genre', ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre(self, collector, genre):
        book_name = 'How to stop drink vodka in the morning'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_books_genre()[book_name] == genre


    def test_set_book_genre_wrong(self, collector):
        book_name = 'How to stop drink vodka in the morning'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Нонфикшн')
        assert collector.get_books_genre()[book_name] == ''

        collector.set_book_genre(book_name + '!', 'Фантастика')
        assert collector.get_books_genre()[book_name] == ''


    def test_get_book_genre(self, collector):
        book_name = 'How to stop drink vodka in the morning'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')
        assert collector.get_book_genre(book_name) == 'Фантастика'

        assert collector.get_book_genre('book_name') is None

    def test_get_books_with_specific_genre(self, collector):
        books_name = [
            'How to stop drink vodka in the morning',
            'Гордость и предубеждение и зомби',
            'Что делать, если ваш кот хочет вас убить',
            'Как перестать писать тесты и начать жить',
        ]
        for book_name in books_name:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, 'Фантастика')

        assert collector.get_books_with_specific_genre('Детективы') == []

        collector.add_new_book('Му-му')
        collector.set_book_genre('Му-му', 'Детективы')

        assert collector.get_books_with_specific_genre('Детективы') == ['Му-му']

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert len(fantasy_books) == len(books_name)
        for name in fantasy_books:
            assert name in books_name

    @pytest.mark.parametrize('books', [
        {},
        {'Му-му': 'Детективы', 'Как перестать писать тесты и начать жить': 'Детективы'},
    ])
    def test_get_books_genre(self, books, collector):
        for name, genre in books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert books == collector.get_books_genre()

    def test_get_books_for_children(self, collector):
        books = {
            'Му-му': 'Ужасы',
            'Как перестать писать тесты и начать жить': 'Детективы',
            'Мои слезы - твоя радость': 'Фантастика',
        }
        for name, genre in books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        books_for_children = collector.get_books_for_children()
        assert len(books_for_children) == 1
        assert books_for_children == ['Мои слезы - твоя радость']


    def test_add_book_in_favorites(self, collector):
        books = ['Му-му', 'Мои слезы - твоя радость']
        for name in books:
            collector.add_new_book(name)

        assert collector.get_list_of_favorites_books() == []
        for name in books:
            collector.add_book_in_favorites(name)

        assert collector.get_list_of_favorites_books() == books

        collector.add_book_in_favorites('Затылок и радость')
        assert collector.get_list_of_favorites_books() == books

    def test_delete_book_from_favorites(self, collector):
        books = ['Му-му', 'Мои слезы - твоя радость']
        for name in books:
            collector.add_new_book(name)

        assert collector.get_list_of_favorites_books() == []
        for name in books:
            collector.add_book_in_favorites(name)

        collector.delete_book_from_favorites(books[0])
        assert collector.get_list_of_favorites_books() == books[1:]

    @pytest.mark.parametrize('books', [
        [],
        ['Затылок и радость', 'Светлое будущее', 'Теплые коты'],
    ])
    def test_get_list_of_favorites_books(self, books, collector):
        for name in books:
            collector.add_new_book(name)

        assert collector.get_list_of_favorites_books() == []
        for name in books:
            collector.add_book_in_favorites(name)

        assert collector.get_list_of_favorites_books() == books