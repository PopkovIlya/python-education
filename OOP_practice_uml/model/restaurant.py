from typing import List
from collections import deque

from model.customer import Customer
from model.order import OrderType
from model.worker import *


class Restaurant:
    """
    Represents the restaurant entity
    """

    def __init__(self, name, address=None, available_seats=0):
        self.__name = name
        self.__available_seats = available_seats
        self.__address = address
        self.__kitchen = Kitchen()
        self.__waiter = Waiter(self.__kitchen)
        self.__chief = Chief(self.__kitchen)
        self.__courier = Courier()
        self.__customers_queue = deque()
        self.__customers = {}

    def open(self):
        """
        Opens the restaurant
        """
        print("Welcome!\n")

    def manage_customers(self):
        """
        Doing some internal work to serve the customers
        """
        self.__receive_orders()
        self.__cook_dishes()
        self.__deliver_orders()

    def __receive_orders(self):
        while self.__customers_queue:
            customer = self.__customers_queue.popleft()
            self.__customers[customer.cid] = customer  # put customer to database
            self.__waiter.bring_menu()
            order = customer.make_order(self.__waiter.bring_menu())
            self.__waiter.receive_order(order)

    def __cook_dishes(self):
        while self.__kitchen.get_orders():
            order = self.__kitchen.get_next_order()
            self.__chief.cook(order)

    def __deliver_orders(self):
        while self.__kitchen.get_dishes():
            dish = self.__kitchen.get_dishes().popleft()
            customer = self.__customers[dish.order.get_customer_id()]
            if dish.order.get_order_type() is OrderType.local:
                self.__waiter.deliver_order(dish.order, customer)
            else:
                self.__courier.deliver_order(dish.order, customer)

    def add_customer(self, customer: Customer):
        """
        Add a new customer to the restaurant (no matter if it is online or offline order)

        :param customer: a new restaurant customer
        """
        if self.__available_seats == 0:
            print(f"There are no empty seats! {customer.first_name} {customer.last_name} please come later")
            return
        print(f"Hello {customer.first_name} {customer.last_name}. Please take a seat")
        self.__customers_queue.append(customer)
        self.__available_seats -= 1

    def close(self):
        """
        Closes the restaurant
        """
        print("\nThanks for your visit! We are closing now")
