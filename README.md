### README: Book Management API

---

#### **Overview**

This project is a Django-based RESTful API for managing a collection of books. It provides endpoints for basic CRUD operations and supports pagination and filtering based on `author` and `published_date`. 

---

### **Features**

- **CRUD Operations**: Create, Read, Update, Delete books.
- **Pagination**: Supports pagination for large datasets.
- **Filtering**: Allows filtering by `author` and `published_date`.
- **Built with**:
  - **Django** and **Django REST Framework**.
  - **SQLite** as the database.
  - Tested using Django's TestCase and Postman.

---

### **Setup Instructions**

#### **Step 1: Clone the Repository**
```bash
git clone <repository-link>
cd book_project
```

#### **Step 2: Set Up the Environment**
1. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### **Step 3: Apply Migrations**
```bash
python manage.py migrate
```

#### **Step 4: Run the Development Server**
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

---

### **API Endpoints**

#### **1. Books Endpoints**

| Method   | Endpoint             | Description                   | Body Example                                                                                       |
|----------|----------------------|-------------------------------|---------------------------------------------------------------------------------------------------|
| `GET`    | `/books/`            | List all books with pagination. | N/A                                                                                               |
| `POST`   | `/books/`            | Add a new book.               | `{ "title": "Book Three", "author": "Author Three", "published_date": "2021-01-01", "isbn": "1234567890125", "available_copies": 15 }` |
| `GET`    | `/books/{id}/`       | Retrieve a specific book.      | N/A                                                                                               |
| `POST`   | `/books/{id}/`       | Update book details.           | `{ "title": "Updated Book" }`                                                                     |
| `DELETE` | `/books/{id}/`       | Delete a book.                 | N/A                                                                                               |

---

### **Filters**

- **Filter by Author**:  
  `GET /books/?author=partial_author_name`  
  Example:  
  ```http
  http://127.0.0.1:8000/books/?author=Author One
  ```

- **Filter by Published Date**:  
  `GET /books/?published_date=YYYY-MM-DD`  
  Example:  
  ```http
  http://127.0.0.1:8000/books/?published_date=2023-01-01
  ```

- **Combine Filters**:  
  `GET /books/?author=Author%20One&published_date=2023-01-01`

---

### **Pagination**

- **Default Page Size**: 10 items per page.  
- **Query Parameters**:
  - `?page=<page_number>`  
    Example:  
    ```http
    http://127.0.0.1:8000/books/?page=2
    ```

---

### **Testing the API**

#### **Using Postman**
1. Import the API endpoints in Postman.
2. Test each endpoint by sending requests with the appropriate HTTP method and body.

#### **Using Django Test Suite**
Run the tests to verify functionality:
```bash
python manage.py test books
```

**Tested Features**:
- CRUD operations.
- Filtering by `author` and `published_date`.
- Pagination behavior.

---

### **Contributing**

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.

---

### **Contact**

For any issues or suggestions, please contact [payasvijainrj19@gmail.com].
