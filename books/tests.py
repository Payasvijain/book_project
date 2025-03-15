from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book


class BookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create initial data for testing
        cls.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            published_date="2023-01-01",
            isbn="1234567890123",
            available_copies=5,
        )
        cls.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            published_date="2022-01-01",
            isbn="1234567890124",
            available_copies=10,
        )

    def test_list_books(self):
        """Test GET /books/"""
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract titles from response and ensure they are in the expected order
        response_titles = [book['title'] for book in response.data['results']]
        expected_titles = [self.book2.title, self.book1.title]  # Ordered by published_date
        self.assertEqual(response_titles, expected_titles)

    def test_filter_books_by_author(self):
        """Test GET /books/?author=Author One"""
        response = self.client.get("/books/", {"author": "Author One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], "Author One")

    def test_filter_books_by_published_date(self):
        """Test GET /books/?published_date=2022-01-01"""
        response = self.client.get("/books/", {"published_date": "2022-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['published_date'], "2022-01-01")

    def test_create_book(self):
        """Test POST /books/"""
        new_book_data = {
            "title": "Book Three",
            "author": "Author Three",
            "published_date": "2021-01-01",
            "isbn": "1234567890125",
            "available_copies": 15,
        }
        response = self.client.post("/books/", new_book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the newly created book
        created_book = Book.objects.get(isbn="1234567890125")
        self.assertEqual(created_book.title, "Book Three")

    def test_retrieve_book(self):
        """Test GET /books/{id}/"""
        response = self.client.get(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_update_book(self):
        """Test POST /books/{id}/"""
        updated_data = {"available_copies": 20}
        response = self.client.post(f"/books/{self.book1.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.available_copies, 20)

    def test_delete_book(self):
        """Test DELETE /books/{id}/"""
        response = self.client.delete(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_invalid_create_book(self):
        """Test POST /books/ with invalid data"""
        invalid_data = {
            "title": "Book Four",
            "author": "Author Four",
            # Missing 'published_date' and 'isbn'
            "available_copies": 5,
        }
        response = self.client.post("/books/", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        response = self.client.get("/books/?author=Author One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that only books matching the author filter are returned
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], "Author One")

    def test_filter_books_by_published_date(self):
        """Test filtering books by published_date"""
        response = self.client.get("/books/?published_date=2023-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that only books matching the published_date filter are returned
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['published_date'], "2023-01-01")

    def test_filter_books_by_author_and_published_date(self):
        """Test filtering books by author and published_date"""
        response = self.client.get("/books/?author=Author One&published_date=2023-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that only books matching both filters are returned
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], "Author One")
        self.assertEqual(response.data['results'][0]['published_date'], "2023-01-01")
