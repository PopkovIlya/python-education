"""This is the simple calculator.

It has a one class calculator with four methods.
"""


class Calculator:
    """This is a simple calculator.

    It can add, subtract, multiply and divide two numbers.
    """

    @staticmethod
    def add_numbers(first_number, second_number):
        """return the sum of two numbers"""
        return first_number + second_number

    @staticmethod
    def subtract_numbers(first_number, second_number):
        """return the result of subtraction of two numbers"""
        return first_number - second_number

    @staticmethod
    def multiply_numbers(first_number, second_number):
        """return the result of multiplication of two numbers"""
        return first_number * second_number

    @staticmethod
    def divide_numbers(first_number, second_number):
        """return the result of the numbers division.

        If b is equal to 0, an exception will be thrown
        """
        if second_number == 0:
            raise Exception("You cannot divide by 0")
        return first_number / second_number
