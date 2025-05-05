def divide(a, b):
    # assert b != 1, "Divisor cannot be 1"
    assert a % b == 0, f"{a} isn't divisable by {b}"
    return a / b

print(divide(4,3))  