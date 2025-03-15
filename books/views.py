from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size = 10  

# List all books or create a new book
class BookListCreateView(APIView):
    def get(self, request):
        """
        GET /books/ → List all books (with optional filtering by author or published_date).
        """
        author = request.query_params.get('author')
        published_date = request.query_params.get('published_date')
        books = Book.objects.all().order_by('published_date')

        # Filtering based on query parameters
        if author:
            books = books.filter(author__icontains=author)
        if published_date:
            books = books.filter(published_date=published_date)

        # Pagination
        paginator = Pagination()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        POST /books/ → Add a new book.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific book
class BookDetailView(APIView):
    def get(self, request, pk):
        """
        GET /books/{id}/ → Retrieve a single book by its ID.
        """
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        POST /books/{id}/ → Update book details.
        """
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE /books/{id}/ → Remove a book.
        """
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

