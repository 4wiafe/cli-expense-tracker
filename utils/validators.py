from decimal import Decimal


def to_cents(amount_str):
    return int(Decimal(amount_str) * 100)


def validate_amount(amount_str):
    try:
        Decimal(amount_str)
        return True
    except:
        return False
