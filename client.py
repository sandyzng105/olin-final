import sqlite3
import hashlib

def sha1_hash(text):
    return hashlib.sha1(text.encode()).hexdigest()

def connect_db():
    return sqlite3.connect('database.db')

def authenticate_user(conn, email, password):
    c = conn.cursor()
    c.execute("SELECT user_id, first_name, password FROM Users WHERE email = ?", (email,))
    user = c.fetchone()
    if user:
        user_id, first_name, stored_password = user
        if stored_password == sha1_hash(password):
            return (user_id, first_name)
    return None

def view_user_info(conn, user_id):
    c = conn.cursor()
    c.execute("""
        SELECT first_name, last_name, email, phone_number, shipping_address, billing_address
        FROM Users
        WHERE user_id = ?
    """, (user_id,))
    user_info = c.fetchone()
    if user_info:
        print("\n--- Your Information ---")
        print(f"Name: {user_info[0]} {user_info[1]}")
        print(f"Email: {user_info[2]}")
        print(f"Phone: {user_info[3]}")
        print(f"Shipping Address: {user_info[4]}")
        print(f"Billing Address: {user_info[5]}")
    else:
        print("User information not found.")

def view_orders(conn, user_id):
    c = conn.cursor()
    c.execute("""
        SELECT order_id, order_date, status
        FROM Orders
        WHERE user_id = ?
    """, (user_id,))
    orders = c.fetchall()
    if orders:
        print("\n--- Your Orders ---")
        for order in orders:
            print(f"Order ID: {order[0]}, Date: {order[1]}, Status: {order[2]}")
    else:
        print("No orders found.")

def view_payment_methods(conn, user_id):
    c = conn.cursor()
    c.execute("""
        SELECT payment_method_id, card_number, expiration_date
        FROM Payment_Methods
        WHERE user_id = ?
    """, (user_id,))
    methods = c.fetchall()
    if methods:
        print("\n--- Your Payment Methods ---")
        for method in methods:
            print(f"Payment ID: {method[0]}, Card Number (Hashed): {method[1]}, Expiry: {method[2]}")
    else:
        print("No payment methods found.")

def main():
    conn = connect_db()
    print("Welcome to the Clothing Store Client!")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    user = authenticate_user(conn, email, password)
    if not user:
        print("Authentication failed. Incorrect email or password.")
        conn.close()
        return

    user_id, first_name = user
    print(f"Welcome, {first_name}!")

    while True:
        print("\nWhat would you like to do?")
        print("1. View my information")
        print("2. View my orders")
        print("3. View my payment methods")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            view_user_info(conn, user_id)
        elif choice == '2':
            view_orders(conn, user_id)
        elif choice == '3':
            view_payment_methods(conn, user_id)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    conn.close()

if __name__ == "__main__":
    main()
