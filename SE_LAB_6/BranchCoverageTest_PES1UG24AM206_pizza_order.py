"""Branch coverage tests for pizza_order.py.

Goal: make every decision (if / elif / else) evaluate both True and False,
including the boundary values where each condition flips.
"""
import pytest
from pizza_order import pizza_price, order_discount, delivery_status


# ---------- pizza_price ----------

def test_unknown_size_raises():
    # size not in SIZE_PRICE -> True
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("extra large", 1, False)


def test_negative_toppings_raises():
    # toppings < 0 -> True
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("small", -1, False)


def test_plain_medium_pizza():
    # toppings > 3 -> False, is_cheese_burst -> False
    assert pizza_price("medium", 0, False) == 350


def test_exactly_three_toppings_boundary():
    # toppings > 3 -> False at the boundary: 200 + 3*40 = 320
    assert pizza_price("small", 3, False) == 320


def test_four_toppings_boundary():
    # toppings > 3 -> True just past the boundary: 200 + 120 + 30 = 350
    assert pizza_price("small", 4, False) == 350


def test_more_than_three_toppings():
    # 500 + 3*40 + 2*30 = 680
    assert pizza_price("large", 5, False) == 680


def test_cheese_burst_medium():
    # is_cheese_burst -> True, size == "small" -> False: 350 + 80 + 100 = 530
    assert pizza_price("medium", 2, True) == 530


def test_cheese_burst_large_with_many_toppings():
    # 500 + 120 + 30 + 100 = 750
    assert pizza_price("large", 4, True) == 750


def test_cheese_burst_small_raises():
    # is_cheese_burst -> True, size == "small" -> True
    with pytest.raises(ValueError, match="cheese burst not available"):
        pizza_price("small", 1, True)


# ---------- order_discount ----------

def test_small_order_gets_no_discount():
    # order_total < 300 -> True
    assert order_discount(250, "tuesday", True) == 0


def test_order_just_below_threshold():
    assert order_discount(299, "monday", False) == 0


def test_order_at_threshold():
    # order_total < 300 -> False at the boundary: 300 // 10 = 30
    assert order_discount(300, "monday", False) == 30


def test_tuesday_half_price_student():
    # day == "tuesday" -> True, is_student -> True: 600 // 2 + 50
    assert order_discount(600, "tuesday", True) == 350


def test_tuesday_half_price_non_student():
    # is_student -> False
    assert order_discount(600, "tuesday", False) == 300


def test_saturday_no_discount_non_student():
    # elif weekend -> True ("saturday")
    assert order_discount(600, "saturday", False) == 0


def test_sunday_student_only_discount():
    # elif weekend -> True ("sunday"), is_student -> True
    assert order_discount(600, "sunday", True) == 50


def test_weekday_ten_percent_student():
    # elif weekend -> False -> else: 600 // 10 + 50
    assert order_discount(600, "wednesday", True) == 110


def test_weekday_ten_percent_non_student():
    assert order_discount(600, "friday", False) == 60


# ---------- delivery_status ----------

def test_too_far_not_deliverable():
    # distance_km > 10 -> True
    assert delivery_status(20, 15) == "not deliverable"


def test_distance_at_limit_is_deliverable():
    # distance_km > 10 -> False at the boundary
    assert delivery_status(20, 10) == "on time"


def test_on_time_delivery():
    # minutes_taken <= 30 -> True
    assert delivery_status(20, 3) == "on time"


def test_on_time_at_thirty_minutes():
    assert delivery_status(30, 3) == "on time"


def test_late_just_after_thirty():
    # minutes_taken <= 30 -> False, <= 45 -> True
    assert delivery_status(31, 3) == "late"


def test_late_at_forty_five_minutes():
    assert delivery_status(45, 3) == "late"


def test_free_pizza_after_forty_five():
    # minutes_taken <= 45 -> False
    assert delivery_status(46, 3) == "free pizza"
