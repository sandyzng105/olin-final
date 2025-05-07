# SQL Injections: Command-Line User Portal for a Clothing Store

This is a **command-line-based e-commerce user portal** simulating a customer’s interaction with the fictional Olin Clothing Store. The application is built in Python and uses **SQLite** as a local database backend.

The application intentionally includes SQL injection vulnerabilities to showcase how insecure coding practices can be exploited.

> ⚠️ **Security Warning**:  
> This application is only for educational purposes.

---

## Features

### Core Functionality
- **User Authentication** via email and password (both safe and vulnerable versions included)
- **View Personal Information**: name, email, phone, addresses
- **View Past Orders**: including order date and shipping status
- **View Payment Methods**: shows hashed card info
- **List & Edit Product Reviews**

---

## Database Schema

The create_db.py script sets up the SQLite database with dummy data. Run it once to initialize the database.db file.

### Users
- Stores customer info: name, email, phone, addresses, password (SHA1-hashed)
- `user_id` is used to link orders, reviews, and payment methods

### Products
- Info: name, description, price, stock
- Linked to product categories via `category_id`

### Categories
- Classifies products (e.g., Dresses, Shirts, Shoes)

### Orders
- Tracks purchases (`order_date`, `status`)
- Linked to `Users`

### Payment Methods
- Stores card number, expiration, CVV
- Linked to `Users` via `user_id`

### Reviews
- Users rate and review products
- Linked via `product_id` and `user_id`

---

## Client Command-Line Interface

Written in Python (`client_sql.py`) with a text-based menu:

```bash
1. View my profile information
2. View my orders
3. View my payment methods
4. List all my reviews
5. Edit my reviews
6. Exit
```

---

## Getting Started

### Prerequisites

- Install Python
- Install SQLite

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sandyzng105/olin-final.git
   cd olin-final
   ```
2. **Create and populate the database**:

    Run the script to set up the SQLite database with sample data:
    ```bash
    python create_db.py
    sqlite3 database.db
    ```
3. **Run the client interface**:

    ```bash
    python client_sql.py
    ```
4. **Login Credentials (sample users)**:

| Email                                             | Password          |
| ------------------------------------------------- | ----------------- |
| alice@example.com    | password123       |
| bob@example.com       | securepass        |
| charlie@example.com | mypassword        |
| diana@example.com    | wonderwoman       |
| ethan@example.com     | missionimpossible |

---

## Interesting Challenges We Encountered

We originally wanted to make a full-stack application with React and Vite for the frontend, and using Flask to connect the frontend to the backend server. However, we realized that we would not have enough time to design and implement a full website for this project in the limited time we had, so we settled for making a command-line interface that could allow the user to access their account details.


