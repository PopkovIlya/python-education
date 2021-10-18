import pytest
from freezegun import freeze_time
from hw8_testing import *


def test_even_odd_to_return_even():
    assert even_odd(2) == "even", "Should be even"


def test_even_odd_to_return_odd():
    assert even_odd(1) == "odd", "Should be odd"


@pytest.mark.xfail(raises=TypeError)
def test_even_odd_to_return_negative_string():
    even_odd("2")


def test_sum_all_numbers():
    assert sum_all(1, 2, 3) == 6, "Should be 6"


def test_sum_all_to_return_zero_if_we_have_no_params():
    assert sum_all() == 0, "Should be zero"


@pytest.mark.xfail(raises=TypeError)
def test_sum_all_numbers_negative_string():
    sum_all("1, 2, 3")


@freeze_time("2021-10-18 01:00:00")
def test_time_of_day_night():
    assert time_of_day() == "night", "Should be night"


@freeze_time("2021-10-18 13:00:00")
def test_time_of_day_afternoon():
    assert time_of_day() == "afternoon", "Should be night"


@freeze_time("2021-10-18 07:00:00")
def test_time_of_day_morning():
    assert time_of_day() == "morning", "Should be night"


@pytest.mark.xfail(raises=TypeError)
def test_time_of_day_negative():
    assert time_of_day("2021-10-18 07:00:00") == "morning", "Should be night"


class TestProduct:
    @pytest.mark.parametrize("quantity, subtract, expected_result", [(32, 2, 30), (10, 5, 5), (3, 2, 1)])
    def test_subtract_quantity(self, quantity, subtract, expected_result):
        product = Product("stuff", 1, quantity)
        product.subtract_quantity(subtract)
        assert product.quantity == expected_result, f"Should be {expected_result}"

    @pytest.mark.xfail(raises=TypeError)
    def test_negative_init_without_param(self):
        product = Product()

    def test_subtract_quantity_default(self):
        product = Product("stuff", 1.0)
        product.subtract_quantity(1)
        assert product.quantity == 0, f"Should be 0"

    @pytest.mark.xfail(raises=TypeError)
    def test_negative_subtract_quantity(self):
        product = Product("stuff", 1.0)
        product.subtract_quantity("1")

    @pytest.mark.parametrize("quantity, add, expected_result", [(10, 2, 12), (10, 5, 15), (0, -1, -1)])
    def test_add_quantity(self, quantity, add, expected_result):
        product = Product("stuff", 1.2, quantity)
        product.add_quantity(add)
        assert product.quantity == expected_result, f"Should be {expected_result}"

    @pytest.mark.xfail(raises=TypeError)
    def test_negative_add_quantity(self):
        product = Product("stuff", 1.0)
        product.add_quantity("1")

    def test_change_price(self):
        product = Product("stuff", 10.0)
        expected = 12.0
        product.change_price(expected)
        assert product.price == expected, f"Should be {expected}"

    @pytest.mark.xfail(raises=ZeroDivisionError)
    def test_negative_change_price(self):
        product = Product("stuff", 1.0)
        product.change_price(1/0)


class TestShop:
    @pytest.fixture
    def computer(self):
        return Product("computer", 1000.0, 1)

    @pytest.fixture
    def phone(self):
        return Product("phone", 150, 20)

    @pytest.mark.xfail(raises=TypeError)
    def test_negative_init_shop(self):
        shop = Shop("stuff", 1.0)

    @pytest.mark.parametrize("shop", (Shop(), Shop(Product("phone", 150, 20))))
    def test_add_product(self, shop, computer):
        shop.add_product(computer)
        assert computer in shop.products, "Product was not added to shop"

    def test_sell_product_not_product(self):
        shop = Shop()
        assert shop.sell_product("phone") is None, "Should return None"

    @pytest.mark.xfail(raises=ZeroDivisionError)
    def test_negative_add_product(self):
        shop = Shop()
        shop.sell_product(1/0)

    def test_sell_product_not_enough_products(self, computer):
        shop = Shop(computer)
        with pytest.raises(ValueError):
            shop.sell_product(computer.title, 2)
        assert "Should be ValueError, not enough quantity product"

    def test_self_product_enough_products_del_product(self, computer):
        shop = Shop(computer)
        shop.sell_product(computer.title)
        assert computer not in shop.products, "Product was bot deleted"

    def test_self_product_subtract_quantity_product(self, phone):
        quantity_before_sell = phone.quantity
        shop = Shop(phone)
        shop.sell_product(phone.title)
        assert phone.quantity == quantity_before_sell-1, "Should be 19"

    def test_self_product_add_money(self, computer):
        shop = Shop(computer)
        shop.sell_product(computer.title)
        assert computer.price == shop.money, "Should be 0, product was not deleted"

