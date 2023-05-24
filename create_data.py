from connection import create_connection
from model import Customer

def insert_customer(conn, customer: model.Customer):
    cursor = conn.cursor()
    sql = "INSERT INTO User (first_name, last_name, address, username, email) VALUES (?, ?, ?, ?, ?)"
    data = (first_name, last_name, address, username, email)
    cursor.execute(sql, data)

    return cursor.lastrowid

# def insert_product(conn, product: dict):
#     sql = "INSERT INTO product (name) VALUES (?)"
#     cursor = conn.cursor()
#     cursor.execute(sql, [product["name"]])
#     conn.commit()
#     return cursor.lastrowid



    # product = qd.select_product(conn, product["product_name"], "name")
    # if product:
    #     author_id = product[0]
    # else:
    #     product_id = insert_product(conn, {"name": product["product_name"]})

    # category = qd.select_category(conn, book["category"], "name")
    # if category:
    #     category_id = category[0]
    # else:
    #     category_id = insert_category(conn, {"name":book["category"]})

    # cursor.execute(sql, [book["name"], book["published"], author_id, category_id])
    # conn.commit()
    # return cursor.lastrowid


def main():
    database = "product_retail.db"
    conn = create_connection(database)

    if conn:

        with conn:
            insert_customer(conn, {"first_name":"Sherwin",
                               "last_name":"Manchester",
                               "username":"sherman",
                               "email": "smanchester@gmail.com",
                               "address":"222 Plum Ln Pocatello, Id",
                               "hashed_password": "stheman"})

if __name__ == "__main__":
    main()
