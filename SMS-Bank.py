import re
from datetime import datetime, timedelta

# آدرس فایل
file_path = "D:\\AVIDA\\CODE\\Bank\\SMS.txt"

# الگوهای جستجو
deposit_pattern = r"واریز: ([\d,]+) ریال"
withdrawal_pattern = r"برداشت: ([\d,]+) ریال"
date_pattern = r"(\d{4}/\d{2}/\d{2})"  # الگو برای تاریخ

# تابع تبدیل تاریخ شمسی به تعداد روزها از یک مبدا
def convert_jalali_to_days(date_str):
    # تبدیل تاریخ شمسی به میلادی (این تابع نیاز به کتابخانه‌ی jalali دارد)
    # برای سادگی، فرض می‌کنیم تاریخ‌ها به ترتیب هستند و نیازی به تبدیل دقیق نداریم.
    # در اینجا فقط سال، ماه و روز را استخراج می‌کنیم.
    year, month, day = map(int, date_str.split('/'))
    return year * 365 + month * 30 + day  # تقریب ساده برای محاسبه تعداد روزها

# خواندن محتوای فایل
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # ذخیره تراکنش‌ها به همراه تاریخ
    transactions = []
    current_date = None

    for line in content:
        # استخراج تاریخ
        date_match = re.search(date_pattern, line)
        if date_match:
            current_date = date_match.group(1)

        # استخراج واریز
        deposit_match = re.search(deposit_pattern, line)
        if deposit_match and current_date:
            amount = int(deposit_match.group(1).replace(',', ''))
            transactions.append(("deposit", amount, current_date))

        # استخراج برداشت
        withdrawal_match = re.search(withdrawal_pattern, line)
        if withdrawal_match and current_date:
            amount = int(withdrawal_match.group(1).replace(',', ''))
            transactions.append(("withdrawal", amount, current_date))

    # گروه‌بندی تراکنش‌ها در بازه‌های ۳۰ روزه
    if not transactions:
        print("No transactions found.")
    else:
        # پیدا کردن اولین تاریخ
        first_date = transactions[0][2]
        first_days = convert_jalali_to_days(first_date)

        # ذخیره جمع واریزها و برداشت‌ها در هر بازه
        period_deposits = 0
        period_withdrawals = 0
        current_period_start = first_days

        print("Transactions per 30-day periods:")
        for transaction in transactions:
            type_, amount, date = transaction
            transaction_days = convert_jalali_to_days(date)

            # اگر تراکنش در بازه‌ی ۳۰ روزه فعلی نباشد، نتایج را نمایش داده و بازه را به‌روزرسانی کنید
            if transaction_days >= current_period_start + 30:
                print(f"Period from day {current_period_start} to {current_period_start + 29}:")
                print(f"  Total Deposits: {period_deposits:,}")
                print(f"  Total Withdrawals: {period_withdrawals:,}")
                print("-" * 40)

                # بازنشانی جمع‌ها برای بازه‌ی جدید
                period_deposits = 0
                period_withdrawals = 0
                current_period_start += 30

            # اضافه کردن مقدار به جمع بازه‌ی فعلی
            if type_ == "deposit":
                period_deposits += amount
            elif type_ == "withdrawal":
                period_withdrawals += amount

        # نمایش نتایج برای آخرین بازه
        print(f"Period from day {current_period_start} to {current_period_start + 29}:")
        print(f"  Total Deposits: {period_deposits:,}")
        print(f"  Total Withdrawals: {period_withdrawals:,}")

except FileNotFoundError:
    print("Error: File not found.")
except Exception as e:
    print(f"An error occurred: {e}")