import sqlite3
import hashlib
import datetime

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
        ("Sneakers", "Running sneakers", 59.99, 25, 4),
        ("Evening Gown", "Elegant evening gown", 99.99, 10, 1),
        ("Chinos", "Comfortable chinos", 44.99, 15, 2),
        ("Polo Shirt", "Classic polo shirt", 29.99, 40, 3),
        ("Boots", "Leather boots", 89.99, 5, 4),
        ("Casual Dress", "Everyday casual dress", 34.99, 12, 1),
        ("Cargo Pants", "Stylish cargo pants", 49.99, 18, 2)
    ]
    c.executemany("INSERT INTO Products (name, description, price, stock_quantity, category_id) VALUES (?, ?, ?, ?, ?)", products)

    users = [
        ("Alice", "Smith", "alice@example.com", "555-1234", "123 Maple St", "123 Maple St", sha1_hash("password123")),
        ("Bob", "Johnson", "bob@example.com", "555-5678", "456 Oak St", "456 Oak St", sha1_hash("securepass")),
        ('Charlie', 'Brown', 'charlie@example.com', '555-8765', '789 Pine St', '789 Pine St', sha1_hash("mypassword")),
        ('Diana', 'Prince', 'diana@example.com', '555-4321', '321 Elm St', '321 Elm St', sha1_hash("wonderwoman")),
        ('Ethan', 'Hunt', 'ethan@example.com', '555-6666', '655 Cedar St', '655 Cedar St', sha1_hash("missionimpossible")),
        ('Felicity', 'Smoak', 'felicity@example.com', '555-3456', '987 Birch St', '987 Birch St', sha1_hash("hackergirl")),
        ('Sandy', 'Zheng', 'sandy@example.com', '555-2345', '159 Spruce St', '159 Spruce St', sha1_hash("orange")),
        ('Khyatee', 'Atolia', 'khyatee@example.com', '555-6780', '753 Fir St', '753 Fir St', sha1_hash("strawberry")),
        ('Jiayi', 'Shao', 'jiayi@example.com', '555-7890', '951 Willow St', '951 Willow St', sha1_hash("blueberry")),
        ('Riccardo', 'Pucella', 'ricardo@example.com', '555-6789', '654 Cedar St', '654 Cedar St', sha1_hash("passionfruit"))

    ]
    c.executemany(
    "INSERT INTO Users (first_name, last_name, email, phone_number, shipping_address, billing_address, password) VALUES (?, ?, ?, ?, ?, ?, ?)", users)
    
    payment_methods = [
        (1, sha1_hash("4111111111111111"), "12/26", sha1_hash("123")),
        (2, sha1_hash("4222222222222222"), "11/25", sha1_hash("456")),
        (3, sha1_hash("4333333333333333"), "10/24", sha1_hash("789")),
        (4, sha1_hash("4444444444444444"), "09/23", sha1_hash("012")),
        (5, sha1_hash("5555555555554444"), "08/22", sha1_hash("345")),
        (6, sha1_hash("6666666666667777"), "07/21", sha1_hash("678")),
        (7, sha1_hash("7777777777778888"), "06/20", sha1_hash("901")),
        (8, sha1_hash("8888888888889999"), "05/19", sha1_hash("234")),
        (9, sha1_hash("9999999999990000"), "04/18", sha1_hash("567")),
        (10, sha1_hash("1010101010101010"), "03/17", sha1_hash("890"))
    ]
    c.executemany("INSERT INTO Payment_Methods (user_id, card_number, expiration_date, cvv) VALUES (?, ?, ?, ?)", payment_methods)

    now = datetime.datetime.now().isoformat()

    # (product_id, user_id, rating, comment, timestamp)
    reviews = [
        (1, 1, 5, "Absolutely love this dress! Fits perfectly and the material is great.", now),
        (2, 1, 4, "Comfortable jeans, though the length was a bit short for me.", now),
        (3, 2, 3, "The t-shirt is okay, but shrunk slightly after washing.", now),
        (4, 2, 5, "Great sneakers! Super comfy and good for running.", now),
        (1, 2, 2, "Sneakers didn't fit well, and the return process was slow.", now),
        (5, 3, 4, "The dress is beautiful, but the color is slightly different from the picture.", now),
        (2, 3, 5, "Best jeans I've ever owned! Highly recommend.", now),
        (3, 4, 1, "T-shirt arrived with a stain. Very disappointed.", now),
        (4, 4, 4, "Good quality sneakers for the price.", now),
        (1, 5, 3, "Dress is nice but not as expected.", now),
        (2, 6, 5, "Jeans are perfect!", now),
        (3, 7, 4, "T-shirt is comfortable and fits well.", now),
        (4, 8, 2, "Sneakers are okay but not very durable.", now),
        (1, 9, 5, "Dress is stunning! Got many compliments.", now),
        (2, 10, 3, "Jeans are good but a bit tight.", now)
    ]
    
    c.executemany("""
        INSERT INTO Reviews (product_id, user_id, rating, comment, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, reviews)

    # (order_id, user_id, order_date, status)
    orders = [
        (1, 1, "2025-05-01T10:30:00", "Shipped"),
        (2, 2, "2025-05-02T14:45:00", "Processing"),
        (3, 1, "2025-05-03T09:15:00", "Delivered"),
        (4, 2, "2025-05-04T16:20:00", "Cancelled"),
        (5, 3, "2025-05-05T11:00:00", "Shipped"),
        (6, 4, "2025-05-06T13:30:00", "Processing"),
        (7, 5, "2025-05-07T15:45:00", "Delivered"),
        (8, 6, "2025-05-08T17:00:00", "Cancelled"),
        (9, 7, "2025-05-09T12:00:00", "Shipped"),
        (10, 8, "2025-05-10T18:30:00", "Processing")
    ]

    c.executemany("""
        INSERT INTO Orders (order_id, user_id, order_date, status)
        VALUES (?, ?, ?, ?)
    """, orders)


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()