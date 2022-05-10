from decimal import Decimal

def normalize(d):
    """
    Normalize a decimal number, and remove exponential formatting.
    """

    if type(d) is not Decimal:
        d = Decimal(d)

    d = d.normalize()

    # Ref: https://docs.python.org/3/library/decimal.html
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
