from model import *
import datetime
import app

with app.app_context():
    db.create_all()

    customer1 = Customer(first_name="Sherwin",
                         last_name="Manchester",
                         username="sherman",
                         email= "smanchester@gmail.com",
                         address="222 Plum Ln Pocatello, Id",
                         hashed_password= "stheman")

    customer2 = Customer(first_name="Carlo",
                         last_name="Morrison",
                         username="cmorrison",
                         email= "cmorrison101@gmail.com",
                         address="367 Ranger Ct Ruidoso, Nm",
                         hashed_password= "pass12345")

    customer3 = Customer(first_name="Neve",
                        last_name="Reilly",
                        username="catluvr234",
                        email= "catluvr234@gmail.com",
                        address="473 Opal Ave Oxford, Mi",
                        hashed_password= "calicotabby4")

    customer4 = Customer(first_name="Zane",
                         last_name="Hester",
                         username="coppiceintoned",
                         email= "coppiceintoned@gmail.com",
                         address="777 Oracle Blvd Herkimer, Ny",
                         hashed_password= "uG7q9PL8")

    customer5 = Customer(first_name="Ellis",
                         last_name="Knoxx",
                         username="guitarrh3ro@gmail.com",
                         email= "gh3roknoxx@gmail.com",
                         address="894 Rayhan Rd Dayton, Tn",
                         hashed_password= "helloflask!")

    customer6 = Customer(first_name="Zane",
                         last_name="Hester",
                         username="cceintoned",
                         email= "cceintoned@gmail.com",
                         address="777 Herkimer, Ny",
                         hashed_password= "afjnwi")

    product1 = Product(product_name="Oversized Chicago Bulls 6 Rings T-Shirt",
                         product_desc="Images from the Chicago Bulls final championship during their dynamic run of winning 6 NBA championships in the 90s.",
                        in_stock=10,                         
                        product_price= 24.99,
                         product_category="Shirts",
                         )

    product2 =   Product(product_name = "T-Shirt",
                         product_desc = "A classic through and through, Gap mens long sleeve t shirts the ideal addition to his wardrobe. With a soft jersey knit, long sleeves, a crew neckline, and banded cuffs, Gap long sleeve shirts for men are a must for his lifestyle.",
                         in_stock = 12,
                         product_price = 14.99,
                         product_category = "CLOTHING",
                         product_brand = "GAP")

     #how can we get our order price to be calculated based on product and quantity
    order =     Order(price = 31.57,
                       date = datetime.datetime.today(),
                       customer_id = 1,
                       product_id = 1)

    review =    Review(customer_id = 1,
                       product_id = 1,
                        rating = 4.5,
                        comment = '''This is a wonderful product and the material is great.
                        Definitely Will be buying more products like this.''',
                       created_at = datetime.datetime.today())

    order_product_data = [
             {'order_id': 1, 'product_id': 1, 'quantity': 2}
         ]

    for data in order_product_data:
         db.session.execute(order_product.insert().values(data))


    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.add(customer4)
    db.session.add(customer5)

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(order)
    db.session.add(review)

    db.session.commit()
