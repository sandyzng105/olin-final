import sqlite3
import hashlib

def sha1_hash(text):
    return hashlib.sha1(text.encode()).hexdigest()

def create_database():
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key enforcement
    c = conn.cursor()

    c.executescript("""
    DROP TABLE IF EXISTS Images;
    DROP TABLE IF EXISTS Reviews;
    DROP TABLE IF EXISTS Payment_Methods;
    DROP TABLE IF EXISTS Shopping_Cart;
    DROP TABLE IF EXISTS Orders;
    DROP TABLE IF EXISTS Users;
    DROP TABLE IF EXISTS Products;
    DROP TABLE IF EXISTS Categories;
    DROP TABLE IF EXISTS Deliveries;

    CREATE TABLE Categories (
        category_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    );

    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT,
        shipping_address TEXT,
        billing_address TEXT,
        password TEXT NOT NULL
    );

    CREATE TABLE Orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );

    CREATE TABLE Shopping_Carts (
        shopping_cart_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );

    CREATE TABLE Payment_Methods (
        payment_method_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        card_number TEXT NOT NULL,
        expiration_date TEXT NOT NULL,
        cvv TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );

    CREATE TABLE Reviews (
        review_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        user_id INTEGER,
        rating INTEGER NOT NULL,
        comment TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );

    CREATE TABLE Deliveries (
        delivery_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        address TEXT,
        ts TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    );

    CREATE TABLE Images (
        image_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        url TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    """)

    # Insert dummy data
    categories = [
        ("Dresses",),
        ("Pants",),
        ("Shirts",),
        ("Shoes",)
    ]
    c.executemany("INSERT INTO Categories (name) VALUES (?)", categories)

    products = [
        ("Summer Dress", "Light summer dress", 49.99, 20, 1),
        ("Jeans", "Blue denim jeans", 39.99, 30, 2),
        ("T-Shirt", "Cotton T-shirt", 19.99, 50, 3),
        ("Sneakers", "Running sneakers", 59.99, 25, 4)
    ]
    c.executemany("INSERT INTO Products (name, description, price, stock_quantity, category_id) VALUES (?, ?, ?, ?, ?)", products)

    users = [
        ("Alice", "Smith", "alice@example.com", "555-1234", "123 Maple St", "123 Maple St", sha1_hash("password123")),
        ("Bob", "Johnson", "bob@example.com", "555-5678", "456 Oak St", "456 Oak St", sha1_hash("securepass"))
    ]
    c.executemany(
    "INSERT INTO Users (first_name, last_name, email, phone_number, shipping_address, billing_address, password) VALUES (?, ?, ?, ?, ?, ?, ?)", users)

    #########################added more data
   orders = [( 1, "May 1, 2025", "success"),
    ( 1, "May 1, 2025", "failed"),
    ( 2, "Apr 30, 2025", "success"),
    ( 2, "May 2, 2025", "pending"),
    ( 2, "May 3, 2025", "success"),
    ( 2, "May 4, 2025", "success"),
    ]
    c.executemany(
    "INSERT INTO Orders (user_id, order_date, status) VALUES (?, ?, ?)", orders)
    

    shopping_cart_items =[  (1, 1, 2, 20.0),
                            (2, 2, 5, 33.0),
                            (3, 3, 1, 11.5),
                            (4, 3, 2, 23.0),
                            (5, 4, 1, 11.5),
                            (6, 4, 1, 11.5),
    ]
    c.executemany(
    "INSERT INTO Shopping_Carts (order_id, product_id, quantity, subtotal) VALUES (?, ?, ?, ?)", shopping_cart_items)

    user_reviews = [    (1, 1, 1, 4, "best product ever", "Apirl 10, 2025"),
                        (2, 2, 3, 3, "just so so", "Apirl 12, 2025"),
                        (3, 2, 5, 5, "perfect", "May 1, 2025"),
                        (3, 2, 6, 4, "Bought another one", "May 1, 2025")
    ]

    c.executemany(
    "INSERT INTO Reviews (product_id, user_id, order_id, rating, comment, ts) VALUES (?, ?, ?, ?, ?, ?)", user_reviews)


    deliveries = [  ("Amphithreater Parkway 4900, CA 94043", "May 01, 2025", 1),
                    ("106 Central St, Wellesley, MA 02481", "April 12, 2025", 3),
                    ("106 Central St, Wellesley, MA 02481", "May 4, 2025", 5),
                    ("106 Central St, Wellesley, MA 02481", "May , 2025", 6)
    ]

    c.executemany(
    "INSERT INTO Deliveries (address, ts, order_id) VALUES (?, ?, ?)", deliveries)

    #########################
    
    payment_methods = [
        (1, sha1_hash("4111111111111111"), "12/26", sha1_hash("123")),
        (2, sha1_hash("4222222222222222"), "11/25", sha1_hash("456"))
    ]
    c.executemany("INSERT INTO Payment_Methods (user_id, card_number, expiration_date, cvv) VALUES (?, ?, ?, ?)", payment_methods)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
