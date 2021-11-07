from model.restaurant import Restaurant
from model.customer import *

if __name__ == '__main__':
    restaurant = Restaurant("Y Varvary", "42 Backer Street, London", 3)

    customers = [
        Visitor(0, "Vasya", "Ivanov", 200),
        Visitor(1, "Petya", "Petrenko", 5000),
        OnlineCustomer(2, "Grigoriy", "Skovoroda", 20),
        OnlineCustomer(3, "Mr", "Nobody", 30000),
        Visitor(4, "Uncle", "Bob", 0)
    ]

    restaurant.open()

    for customer in customers:
        restaurant.add_customer(customer)
    restaurant.manage_customers()

    restaurant.close()
