# utils.py
def convert_currency(amount, source_currency, target_currency):
    """
    Convert an amount from the source currency to the target currency.

    Args:
        amount (float): The amount to be converted.
        source_currency (str): The currency code of the source currency (e.g., 'GBP', 'USD', 'EUR').
        target_currency (str): The currency code of the target currency (e.g., 'GBP', 'USD', 'EUR').

    Returns:
        float: The converted amount in the target currency.

    Raises:
        ValueError: If the source or target currency is not supported.
    """
    # Hard-coded exchange rates
    exchange_rates = {
        'GBP': {'GBP': 1.0, 'USD': 1.4, 'EUR': 1.2},
        'USD': {'GBP': 0.71, 'USD': 1.0, 'EUR': 0.86},
        'EUR': {'GBP': 0.83, 'USD': 1.16, 'EUR': 1.0},
    }

    # Check if the source and target currencies are valid
    if source_currency not in exchange_rates or target_currency not in exchange_rates:
        raise ValueError("Invalid source or target currency")

    # Get the conversion rate
    conversion_rate = exchange_rates[source_currency][target_currency]

    # Convert the amount
    converted_amount = amount * conversion_rate

    return converted_amount