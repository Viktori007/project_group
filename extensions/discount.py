from datetime import datetime, timedelta


def calculate_discount(purchases: list[datetime, float]):
    now = datetime.now()

    total_last_week = 0
    total_last_month = 0
    total_last_three_months = 0

    for purchase in purchases:
        purchase_time = datetime.strptime(purchase[0], '%Y-%m-%d %H:%M:%S')

        time_difference = now - purchase_time

        if time_difference <= timedelta(days=7):
            total_last_week += purchase[1]

        if time_difference <= timedelta(days=30):
            total_last_month += purchase[1]

        if time_difference <= timedelta(days=90):
            total_last_three_months += purchase[1]

    if total_last_three_months > 200000:
        discount = 15
    elif total_last_month > 50000:
        discount = 10
    elif total_last_week > 10000:
        discount = 5
    else:
        discount = 0

    discount = min(discount, 15)

    return float(discount)


purchases = [
    ('2023-10-01 12:00:00', 5000),
    ('2023-10-10 14:00:00', 7000),
    ('2023-09-15 10:00:00', 30000),
    ('2023-08-20 09:00:00', 100000),
]

discount = calculate_discount(purchases)
print(f"Скидка: {discount}%")
