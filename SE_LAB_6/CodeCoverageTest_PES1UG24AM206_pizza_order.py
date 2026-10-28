"""Code (line) coverage tests for pizza_order.py.

Goal: execute every line of pizza_order.py at least once.
"""
import pytest
from pizza_order import pizza_price, order_discount, delivery_status


# ---------- pizza_price ----------

def test_plain_medium_pizza():
    assert pizza_price("medium", 0, False) == 350


def test_unknown_size_raises():
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("extra large", 1, False)


def test_negative_toppings_raises():
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("small", -1, False)


def test_more_than_three_toppings():
    # 500 + 3*40 + 2*30 = 680
    assert pizza_price("large", 5, False) == 680


def test_cheese_burst_medium():
    # 350 + 2*40 + 100 = 530
    assert pizza_price("medium", 2, True) == 530


def test_cheese_burst_small_raises():
    with pytest.raises(ValueError, match="cheese burst not available"):
        pizza_price("small", 1, True)


# ---------- order_discount ----------

def test_small_order_gets_no_discount():
    assert order_discount(250, "monday", True) == 0


def test_tuesday_half_price_student():
    # 600 // 2 + 50 = 350
    assert order_discount(600, "tuesday", True) == 350


def test_weekend_no_discount_student():
    assert order_discount(600, "saturday", True) == 50


def test_weekday_ten_percent_student():
    # 600 // 10 + 50 = 110
    assert order_discount(600, "wednesday", True) == 110


# ---------- delivery_status ----------

def test_on_time_delivery():
    assert delivery_status(20, 3) == "on time"


def test_too_far_not_deliverable():
    assert delivery_status(20, 15) == "not deliverable"


def test_late_delivery():
    assert delivery_status(40, 5) == "late"


def test_very_late_free_pizza():
    assert delivery_status(60, 5) == "free pizza"
